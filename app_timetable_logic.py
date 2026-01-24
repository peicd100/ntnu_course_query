from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

import numpy as np
import pandas as pd
from PySide6.QtGui import QColor

from app_constants import DAY_LABEL, PERIODS, PERIOD_INDEX
from app_utils import format_cid4, strip_bracket_text_for_timetable


def darken(color: QColor, factor: float) -> QColor:
    r = max(0, min(255, int(color.red() * factor)))
    g = max(0, min(255, int(color.green() * factor)))
    b = max(0, min(255, int(color.blue() * factor)))
    return QColor(r, g, b)


def _subset_courses_by_ids(
    courses_df: pd.DataFrame, included_ids_sorted: np.ndarray, cols: List[str]
) -> pd.DataFrame:
    if courses_df is None or courses_df.empty:
        return pd.DataFrame(columns=cols)
    if included_ids_sorted is None or included_ids_sorted.size == 0:
        return courses_df.iloc[0:0][cols]

    ids = included_ids_sorted.astype(np.int64, copy=False)
    cid_arr = courses_df["_cid"].to_numpy(dtype=np.int64, copy=False)
    
    # D-03: Use searchsorted for O(k log n) lookup
    # We assume courses_df is sorted by _cid (ensured in app_excel.py)
    # Check if cid_arr is actually sorted (cheap check for first/last or just assume)
    # Since we control app_excel, we assume it is sorted.
    
    indices = np.searchsorted(cid_arr, ids)
    
    # Filter out indices that are out of bounds or don't match (id not found)
    valid_mask = (indices < len(cid_arr))
    if not valid_mask.all():
        indices = indices[valid_mask]
        ids = ids[valid_mask]
    
    # Double check matches
    if len(indices) > 0:
        matched_mask = (cid_arr[indices] == ids)
        indices = indices[matched_mask]
    
    if len(indices) == 0:
        return courses_df.iloc[0:0][cols]
        
    return courses_df.iloc[indices][cols]


def occupied_masks_sorted(courses_df: pd.DataFrame, included_ids_sorted: np.ndarray) -> Tuple[np.uint64, np.uint64]:
    if included_ids_sorted is None or included_ids_sorted.size == 0:
        return np.uint64(0), np.uint64(0)
    sub = _subset_courses_by_ids(courses_df, included_ids_sorted, ["_mask_lo", "_mask_hi"])
    if sub.empty:
        return np.uint64(0), np.uint64(0)

    arr_lo = sub["_mask_lo"].to_numpy(dtype="uint64", copy=False)
    arr_hi = sub["_mask_hi"].to_numpy(dtype="uint64", copy=False)
    occ_lo = np.bitwise_or.reduce(arr_lo) if arr_lo.size else np.uint64(0)
    occ_hi = np.bitwise_or.reduce(arr_hi) if arr_hi.size else np.uint64(0)
    return np.uint64(occ_lo), np.uint64(occ_hi)


def occupied_masks_from_arrays(
    mask_lo_arr: np.ndarray, mask_hi_arr: np.ndarray, cid_arr: np.ndarray, included_ids_sorted: np.ndarray
) -> Tuple[np.uint64, np.uint64]:
    # F-01: Use searchsorted on sorted arrays
    if included_ids_sorted.size == 0 or cid_arr.size == 0:
        return np.uint64(0), np.uint64(0)

    # F-01: Use searchsorted for O(k log n) lookup
    # cid_arr is sorted (ensured by MainWindow._build_course_binary_index)
    indices = np.searchsorted(cid_arr, included_ids_sorted)
    
    # Filter indices that are out of bounds
    valid_mask = (indices < len(cid_arr))
    if not valid_mask.all():
        indices = indices[valid_mask]
        included_ids_sorted = included_ids_sorted[valid_mask]
        
    if indices.size == 0:
        return np.uint64(0), np.uint64(0)

    # Check exact matches (searchsorted finds insertion point)
    matched_mask = (cid_arr[indices] == included_ids_sorted)
    final_indices = indices[matched_mask]
    
    if final_indices.size == 0:
        return np.uint64(0), np.uint64(0)

    occ_lo = np.bitwise_or.reduce(mask_lo_arr[final_indices])
    occ_hi = np.bitwise_or.reduce(mask_hi_arr[final_indices])
    return np.uint64(occ_lo), np.uint64(occ_hi)


def build_lane_assignment_sorted(courses_df: pd.DataFrame, included_ids_sorted: np.ndarray) -> Tuple[Dict[int, int], int]:
    if included_ids_sorted is None or included_ids_sorted.size == 0:
        return {}, 1
    sub = _subset_courses_by_ids(courses_df, included_ids_sorted, ["_cid", "_slots_set"])
    if sub.empty:
        return {}, 1

    used_by_slot: Dict[str, int] = {}
    lane_of: Dict[int, int] = {}
    max_lane = 1

    # D-04: Avoid itertuples for performance
    cids = sub["_cid"].to_numpy()
    slots_col = sub["_slots_set"].to_numpy()
    
    # Prepare data for sorting: (len_slots desc, cid asc)
    data = []
    for cid, slots in zip(cids, slots_col):
        l = len(slots) if isinstance(slots, set) else 0
        data.append((l, cid, slots))
    
    data.sort(key=lambda x: (-x[0], x[1]))

    for _, cid, slots in data:
        cid_i = int(cid)
        slots_set = slots if isinstance(slots, set) else set()
        if not slots_set:
            lane_of[cid_i] = 1
            continue

        used = 0
        for s in slots_set:
            used |= used_by_slot.get(s, 0)

        bitlen = used.bit_length() + 2
        inv = (~used) & ((1 << bitlen) - 1)
        lsb = inv & -inv
        lane = lsb.bit_length()

        lane_of[cid_i] = lane
        if lane > max_lane:
            max_lane = lane

        bit = 1 << (lane - 1)
        for s in slots_set:
            used_by_slot[s] = used_by_slot.get(s, 0) | bit

    return lane_of, max_lane


def build_timetable_matrix_per_day_lanes_sorted(
    courses_df: pd.DataFrame,
    included_ids_sorted: np.ndarray,
    locked_ids_set: Set[int],
    show_days: List[str],
) -> Tuple[
    List[List[str]],
    List[str],
    Dict[str, int],
    List[int],
    List[List[Optional[int]]],
    List[List[bool]],
]:
    lane_map, _ = build_lane_assignment_sorted(courses_df, included_ids_sorted)
    day_lanes: Dict[str, int] = {d: 1 for d in show_days}

    subset_meta = _subset_courses_by_ids(
        courses_df,
        included_ids_sorted,
        ["_cid", "中文課程名稱", "_slots_set", "_tt_label"],
    )

    # D-04: Pre-fetch columns to avoid DataFrame overhead in loops
    meta_cids = subset_meta["_cid"].to_numpy()
    meta_slots = subset_meta["_slots_set"].to_numpy()

    for cid, slots in zip(meta_cids, meta_slots):
        cid_i = int(cid)
        lane = lane_map.get(cid_i, 1)
        slots_set = slots if isinstance(slots, set) else set()
        for slot in slots_set:
            day, _per = slot.split("-", 1)
            if day in day_lanes and lane > day_lanes[day]:
                day_lanes[day] = lane

    day_offset: Dict[str, int] = {}
    col_day_idx: List[int] = []
    offset = 0
    for day_idx, d in enumerate(show_days):
        day_offset[d] = offset
        for _ in range(int(day_lanes[d])):
            col_day_idx.append(day_idx)
        offset += int(day_lanes[d])

    cols = offset
    matrix = [["" for _ in range(cols)] for _ in PERIODS]
    id_matrix: List[List[Optional[int]]] = [[None for _ in range(cols)] for _ in PERIODS]
    locked_matrix: List[List[bool]] = [[False for _ in range(cols)] for _ in PERIODS]
    conflict_slots: List[str] = []

    locked_ids_set = set(int(x) for x in locked_ids_set)

    # D-02: Use precomputed _tt_label if available
    has_tt_label = "_tt_label" in subset_meta.columns
    meta_labels = subset_meta["_tt_label"].to_numpy() if has_tt_label else None
    meta_cnames = subset_meta["中文課程名稱"].to_numpy() if not has_tt_label else None

    if has_tt_label:
        iterator = zip(meta_cids, meta_slots, meta_labels)
    else:
        iterator = zip(meta_cids, meta_slots, meta_cnames)

    for item in iterator:
        cid = item[0]
        slots = item[1]
        cid_i = int(cid)
        
        if has_tt_label:
            label = str(item[2])
        else:
            # Fallback
            cname = item[2]
            cname_show = strip_bracket_text_for_timetable(str(cname).strip())
            label = f"{cname_show}\n{format_cid4(cid_i)}".strip()

        slots_set = slots if isinstance(slots, set) else set()
        lane = lane_map.get(cid_i, 1)
        is_locked = (cid_i in locked_ids_set)

        for slot in slots_set:
            day, per = slot.split("-", 1)
            if day not in day_offset or per not in PERIOD_INDEX:
                continue

            # D-01: Use PERIOD_INDEX
            r = PERIOD_INDEX[per]
            c = day_offset[day] + (lane - 1)

            if matrix[r][c] and label not in matrix[r][c]:
                conflict_slots.append(f"{DAY_LABEL.get(day, day)} 第{per}節")
                matrix[r][c] = matrix[r][c] + "\n---\n" + label
                if is_locked:
                    locked_matrix[r][c] = True
            else:
                matrix[r][c] = label
                if id_matrix[r][c] is None:
                    id_matrix[r][c] = cid_i
                if is_locked:
                    locked_matrix[r][c] = True

    uniq: List[str] = []
    seen: Set[str] = set()
    for x in conflict_slots:
        if x not in seen:
            uniq.append(x)
            seen.add(x)

    return matrix, uniq, day_lanes, col_day_idx, id_matrix, locked_matrix
