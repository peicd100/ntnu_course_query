from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

import numpy as np
from PySide6.QtCore import QObject, QRunnable, Signal

from app_constants import GENED_DEPT_NAME
from app_user_data import best_schedule_dir_path, save_best_schedule_cache, save_user_file
from app_utils import sorted_array_from_set_int


class SaveWorker(QObject, QRunnable):
    finished = Signal(int, bool, str)

    def __init__(
        self,
        token: int,
        path: str,
        username: str,
        favorites: Set[int],
        included_sorted: np.ndarray,
        locked_sorted: np.ndarray,
        fav_seq: Dict[int, int],
        courses_df,
    ):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.setAutoDelete(True)

        self.token = int(token)
        self.path = path
        self.username = username
        self.favorites = set(favorites)
        self.included_sorted = included_sorted.copy() if included_sorted is not None else np.empty((0,), dtype=np.int64)
        self.locked_sorted = locked_sorted.copy() if locked_sorted is not None else np.empty((0,), dtype=np.int64)
        self.fav_seq = dict(fav_seq)
        self.courses_df = courses_df

    def run(self):
        try:
            save_user_file(
                self.path,
                self.username,
                self.favorites,
                self.included_sorted,
                self.locked_sorted,
                self.fav_seq,
                self.courses_df,
            )
            self.finished.emit(self.token, True, "")
        except Exception as e:
            self.finished.emit(self.token, False, str(e))


@dataclass(frozen=True)
class _BestCandidate:
    cid: int
    credit: float
    gened: int
    mask_lo: np.uint64
    mask_hi: np.uint64


class BestScheduleWorker(QObject, QRunnable):
    finished = Signal(int, bool, bool, list, str)

    def __init__(
        self,
        token: int,
        user_dir_path: str,
        username: str,
        favorites: Set[int],
        locked_ids: Set[int],
        included_ids: Set[int],
        fav_seq: Dict[int, int],
        courses_df,
    ):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.setAutoDelete(True)

        self.token = int(token)
        self.user_dir_path = user_dir_path
        self.username = username
        self.favorites = set(int(x) for x in favorites)
        self.locked_ids = set(int(x) for x in locked_ids)
        self.included_ids = set(int(x) for x in included_ids)
        self.fav_seq = dict(fav_seq)
        self.courses_df = courses_df
        self.best_schedule_dir = best_schedule_dir_path(user_dir_path)

        self._cancel_requested = False

    def cancel(self) -> None:
        self._cancel_requested = True

    def _format_credit_text(self, value: float) -> str:
        if abs(value - round(value)) < 1e-9:
            return str(int(round(value)))
        return f"{value:.1f}".rstrip("0").rstrip(".")

    def _safe_credit(self, value) -> float:
        try:
            v = float(value)
            return 0.0 if np.isnan(v) else v
        except Exception:
            return 0.0

    def _build_candidates(self) -> Tuple[List[_BestCandidate], float, int, List[int], np.uint64, np.uint64]:
        if self.courses_df is None or self.courses_df.empty or not self.favorites:
            return [], 0.0, 0, [], np.uint64(0), np.uint64(0)

        cols = ["_cid", "學分", "系所", "_mask_lo", "_mask_hi"]
        target_ids = set(self.favorites) & self.included_ids
        if not target_ids:
            return [], 0.0, 0, [], np.uint64(0), np.uint64(0)
        sub = self.courses_df[self.courses_df["_cid"].isin(list(target_ids))][cols]
        if sub.empty:
            return [], 0.0, 0, [], np.uint64(0), np.uint64(0)

        candidates: List[_BestCandidate] = []
        base_credit = 0.0
        base_gened = 0
        locked_ids: List[int] = []
        base_lo = np.uint64(0)
        base_hi = np.uint64(0)

        for cid, credit, dept, mlo, mhi in sub.itertuples(index=False, name=None):
            cid_i = int(cid)
            cr = self._safe_credit(credit)
            gened = 1 if str(dept).strip() == GENED_DEPT_NAME else 0
            lo = np.uint64(mlo) if mlo is not None else np.uint64(0)
            hi = np.uint64(mhi) if mhi is not None else np.uint64(0)

            if cid_i in self.locked_ids:
                base_credit += cr
                base_gened += gened
                base_lo |= lo
                base_hi |= hi
                locked_ids.append(cid_i)
            else:
                candidates.append(_BestCandidate(cid_i, cr, gened, lo, hi))

        candidates.sort(key=lambda x: (-x.credit, x.cid))
        locked_ids.sort()

        return candidates, base_credit, base_gened, locked_ids, base_lo, base_hi

    def _build_order_map(self) -> Dict[int, int]:
        items = []
        for cid in self.favorites:
            cid_i = int(cid)
            locked = 1 if cid_i in self.locked_ids else 0
            seq = int(self.fav_seq.get(cid_i, 10**12))
            items.append((-locked, seq, cid_i))
        items.sort()
        out: Dict[int, int] = {}
        k = 1
        for _neg_lock, _seq, cid in items:
            out[int(cid)] = k
            k += 1
        return out

    def _compute_best_combinations(self) -> List[dict]:
        cand, base_credit, base_gened, locked_ids, base_lo, base_hi = self._build_candidates()
        if not cand and not locked_ids:
            return []

        order_map = self._build_order_map()

        best: List[dict] = []
        n = len(cand)

        suffix_max = [0.0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix_max[i] = suffix_max[i + 1] + max(0.0, cand[i].credit)

        selected: List[int] = []

        def consider_result(cur_credit: float, cur_gened: int) -> None:
            total_credit = base_credit + cur_credit
            total_gened = base_gened + cur_gened
            ids_all = sorted(locked_ids + selected)
            order_key = sorted(order_map.get(cid, 10**12) for cid in ids_all)
            priority_sum = sum(order_key)
            entry = {
                "credits": total_credit,
                "gened": total_gened,
                "ids": ids_all,
                "order_key": order_key,
                "priority_sum": priority_sum,
            }
            best.append(entry)
            best.sort(
                key=lambda x: (-x["credits"], x["priority_sum"], x["order_key"])
            )
            if len(best) > 5:
                del best[5:]

        def dfs(idx: int, mask_lo: np.uint64, mask_hi: np.uint64, cur_credit: float, cur_gened: int) -> None:
            if self._cancel_requested:
                return
            if idx >= n:
                consider_result(cur_credit, cur_gened)
                return

            if len(best) == 5:
                worst_credit = best[-1]["credits"]
                max_possible = base_credit + cur_credit + suffix_max[idx]
                if max_possible + 1e-9 < worst_credit:
                    return

            item = cand[idx]
            if (mask_lo & item.mask_lo) == 0 and (mask_hi & item.mask_hi) == 0:
                selected.append(item.cid)
                dfs(
                    idx + 1,
                    mask_lo | item.mask_lo,
                    mask_hi | item.mask_hi,
                    cur_credit + item.credit,
                    cur_gened + item.gened,
                )
                selected.pop()

            dfs(idx + 1, mask_lo, mask_hi, cur_credit, cur_gened)

        dfs(0, base_lo, base_hi, 0.0, 0)

        if not best:
            return []
        return best

    def _write_results(self, results: List[dict]) -> List[str]:
        if not results:
            return []

        files: List[str] = []
        used_names: Set[str] = set()
        locked_sorted = sorted_array_from_set_int(self.locked_ids)
        target_dir = self.best_schedule_dir or self.user_dir_path
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)

        for entry in results:
            if self._cancel_requested:
                return []
            credits_txt = self._format_credit_text(float(entry["credits"]))
            gened_cnt = int(entry["gened"])
            priority_sum = int(entry.get("priority_sum", 0))
            base_name = f"學分_{credits_txt}，優先度和_{priority_sum}"

            filename = f"{base_name}.xlsx"
            if filename in used_names:
                k = 2
                while True:
                    filename = f"{base_name}_{k}.xlsx"
                    if filename not in used_names:
                        break
                    k += 1

            used_names.add(filename)
            path = os.path.join(target_dir or self.user_dir_path, filename)

            included_ids = set(entry["ids"])
            included_sorted = sorted_array_from_set_int(included_ids)

            save_user_file(
                path,
                self.username,
                self.favorites,
                included_sorted,
                locked_sorted,
                self.fav_seq,
                self.courses_df,
            )
            files.append(path)

        save_best_schedule_cache(
            self.user_dir_path,
            sorted(self.favorites),
            sorted(self.locked_ids),
            [os.path.basename(p) for p in files],
        )

        return files

    def run(self):
        try:
            results = self._compute_best_combinations()
            if self._cancel_requested:
                self.finished.emit(self.token, False, True, [], "")
                return

            files = self._write_results(results)
            if self._cancel_requested:
                self.finished.emit(self.token, False, True, [], "")
                return

            if not files and results:
                self.finished.emit(self.token, False, False, [], "無法寫入最佳選課檔案。")
                return

            self.finished.emit(self.token, True, False, files, "")
        except Exception as e:
            if self._cancel_requested:
                self.finished.emit(self.token, False, True, [], "")
            else:
                self.finished.emit(self.token, False, False, [], str(e))
