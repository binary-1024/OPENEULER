#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import tempfile
import unittest
from pathlib import Path

from check_eo import (
    check_lines_without_eo,
    check_rows_without_oe_release,
    release_has_oe_marker,
)


class CheckOeReleaseTests(unittest.TestCase):
    def test_release_marker_detection(self):
        self.assertTrue(release_has_oe_marker("2.oe2409"))
        self.assertTrue(release_has_oe_marker("oe1"))
        self.assertFalse(release_has_oe_marker("1"))
        self.assertFalse(release_has_oe_marker("noetic"))

    def test_only_release_field_is_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "packages.csv"
            with path.open("w", encoding="utf-8", newline="") as target:
                writer = csv.writer(target)
                writer.writerow(["comp_name", "version", "url"])
                writer.writerow(
                    [
                        "ros-noetic-ros-nodelet_core",
                        "1.10.1-1.x86_64",
                        "https://example.invalid/Packages/"
                        "ros-noetic-ros-nodelet_core-1.10.1-1.x86_64.rpm",
                    ]
                )
                writer.writerow(
                    [
                        "example",
                        "1.0-2.oe2409.x86_64",
                        "https://example.invalid/Packages/"
                        "example-1.0-2.oe2409.x86_64.rpm",
                    ]
                )
            rows = check_rows_without_oe_release(path)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0][1]["comp_name"], "ros-noetic-ros-nodelet_core")
            self.assertEqual(check_lines_without_eo(path), [(2, rows[0][1]["url"])])

    def test_bad_header_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.csv"
            path.write_text("name,url\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid CSV header"):
                check_rows_without_oe_release(path)


if __name__ == "__main__":
    unittest.main()
