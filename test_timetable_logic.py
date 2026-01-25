import sys
import os
import unittest
import numpy as np
import pandas as pd

# Ensure we can import from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_timetable_logic import occupied_masks_from_arrays, build_lane_assignment_sorted

class TestTimetableLogic(unittest.TestCase):
    def setUp(self):
        # Setup a dummy dataframe for testing
        # CIDs: 10, 20, 30, 40
        # 10: Mask 1 (Low), 0 (High) -> e.g., Mon-1
        # 20: Mask 2 (Low), 0 (High) -> e.g., Mon-2
        # 30: Mask 1 (Low), 0 (High) -> e.g., Mon-1 (Conflict with 10)
        # 40: Mask 4 (Low), 0 (High) -> e.g., Mon-3
        
        self.cids = np.array([10, 20, 30, 40], dtype=np.int64)
        self.mask_lo = np.array([1, 2, 1, 4], dtype=np.uint64)
        self.mask_hi = np.array([0, 0, 0, 0], dtype=np.uint64)
        
        self.df = pd.DataFrame({
            "_cid": self.cids,
            "_mask_lo": self.mask_lo,
            "_mask_hi": self.mask_hi,
            "_slots_set": [
                {"一-1"},           # 10
                {"一-2"},           # 20
                {"一-1"},           # 30 (Conflict with 10)
                {"一-3"}            # 40
            ],
            "中文課程名稱": ["C1", "C2", "C3", "C4"],
            "_tt_label": ["C1\n0010", "C2\n0020", "C3\n0030", "C4\n0040"]
        })

    def test_occupied_masks_from_arrays(self):
        # Test subset: 10 and 20
        # Expected mask: 1 | 2 = 3
        included = np.array([10, 20], dtype=np.int64)
        lo, hi = occupied_masks_from_arrays(self.mask_lo, self.mask_hi, self.cids, included)
        self.assertEqual(lo, 3)
        self.assertEqual(hi, 0)

        # Test empty
        included = np.array([], dtype=np.int64)
        lo, hi = occupied_masks_from_arrays(self.mask_lo, self.mask_hi, self.cids, included)
        self.assertEqual(lo, 0)

        # Test non-existent ID (should be ignored)
        included = np.array([99], dtype=np.int64)
        lo, hi = occupied_masks_from_arrays(self.mask_lo, self.mask_hi, self.cids, included)
        self.assertEqual(lo, 0)

    def test_build_lane_assignment_sorted(self):
        # Test 10 and 30 (Conflict on Mon-1)
        # Should result in 2 lanes
        included = np.array([10, 30], dtype=np.int64)
        lane_map, max_lane = build_lane_assignment_sorted(self.df, included, None)
        self.assertEqual(max_lane, 2)
        self.assertEqual(len(lane_map), 2)
        self.assertNotEqual(lane_map[10], lane_map[30])

        # Test 10 and 20 (No conflict)
        # Should result in 1 lane
        included = np.array([10, 20], dtype=np.int64)
        lane_map, max_lane = build_lane_assignment_sorted(self.df, included, None)
        self.assertEqual(max_lane, 1)
        self.assertEqual(lane_map[10], 1)
        self.assertEqual(lane_map[20], 1)

if __name__ == '__main__':
    unittest.main()