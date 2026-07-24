#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import io
import stat
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import run

TARGET_URL = (
    "https://dl-cdn.openeuler.openatom.cn/openEuler-24.09/everything/"
    "riscv64/Packages/"
    "texlive-nolbreaks-doc-svn26786.1.2-2.oe2409.noarch.rpm"
)


class UrlOnlyWorkflowTests(unittest.TestCase):
    def test_parsed_url_record_marks_epoch_unknown(self):
        record = run.parsed_url_record(TARGET_URL)
        self.assertEqual(record["comp_name"], "texlive-nolbreaks-doc")
        self.assertEqual(record["rpm_version"], "svn26786.1.2")
        self.assertEqual(record["release"], "2.oe2409")
        self.assertEqual(record["arch"], "noarch")
        self.assertIsNone(record["epoch"])
        self.assertFalse(record["epoch_known"])
        self.assertEqual(record["version"], "svn26786.1.2-2.oe2409.noarch")

    def test_parse_cli_outputs_machine_readable_csv(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = run.main(["parse", TARGET_URL])
        self.assertEqual(exit_code, 0)

        rows = list(csv.DictReader(io.StringIO(stdout.getvalue())))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["comp_name"], "texlive-nolbreaks-doc")
        self.assertEqual(rows[0]["epoch"], "")
        self.assertEqual(rows[0]["epoch_known"], "False")

    def test_parse_cli_reports_invalid_url(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = run.main(["parse", "not-an-rpm"])
        self.assertEqual(exit_code, 1)
        self.assertIn("not an RPM filename", stderr.getvalue())
        self.assertEqual(list(csv.DictReader(io.StringIO(stdout.getvalue()))), [])

    def test_generate_csv_from_urls_is_sorted_and_deduplicated(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output.csv"
            url_a = "https://example.invalid/Packages/a-1-1.x86_64.rpm"
            url_b = "https://example.invalid/Packages/b-v2-3.noarch.rpm"
            run.generate_csv_from_urls([url_b, url_a, url_b, ""], output)

            with output.open(encoding="utf-8", newline="") as source:
                rows = list(csv.DictReader(source))
            self.assertEqual([row["url"] for row in rows], [url_a, url_b])

    def test_generate_csv_from_url_lists_reports_source_line(self):
        with tempfile.TemporaryDirectory() as directory:
            input_dir = Path(directory) / "urls"
            input_dir.mkdir()
            (input_dir / "packages.txt").write_text(
                "https://example.invalid/a-1-1.noarch.rpm\nnot-an-rpm\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, r"packages\.txt:2"):
                run.generate_csv_from_url_lists(
                    input_dir, Path(directory) / "output.csv"
                )

    def test_normalize_repairs_boundary_without_reordering(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "packages.csv"
            first_url = (
                "https://example.invalid/Packages/"
                "ros-noetic-ros-nodelet_core-1.10.1-1.x86_64.rpm"
            )
            second_url = "https://example.invalid/Packages/example-1.0-2.noarch.rpm"
            with output.open("w", encoding="utf-8", newline="") as target:
                writer = csv.writer(target)
                writer.writerow(["comp_name", "version", "url"])
                writer.writerow(
                    ["ros-noetic-ros", "nodelet_core-1.10.1-1.x86_64", first_url]
                )
                writer.writerow(["example", "1.0-2.noarch", second_url])

            self.assertEqual(run.normalize_csv(output), 1)
            self.assertEqual(run.validate_csv(output), [])
            with output.open(encoding="utf-8", newline="") as source:
                rows = list(csv.DictReader(source))
            self.assertEqual([row["url"] for row in rows], [first_url, second_url])

    def test_atomic_writes_preserve_permissions_and_noop_skips_replace(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "packages.csv"
            output.touch(mode=0o640)
            run.generate_csv_from_urls([TARGET_URL], output)
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o640)

            with mock.patch("run.os.replace") as replace:
                self.assertEqual(run.normalize_csv(output), 0)
            replace.assert_not_called()

            new_output = Path(directory) / "new.csv"
            run.generate_csv_from_urls([TARGET_URL], new_output)
            self.assertEqual(stat.S_IMODE(new_output.stat().st_mode), 0o644)

    def test_validate_detects_boundary_duplicate_and_malformed_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            bad = Path(directory) / "bad.csv"
            url = (
                "https://example.invalid/Packages/"
                "ros-noetic-ros-nodelet_core-1.10.1-1.x86_64.rpm"
            )
            with bad.open("w", encoding="utf-8", newline="") as target:
                writer = csv.writer(target)
                writer.writerow(["comp_name", "version", "url"])
                writer.writerow(["ros-noetic-ros", "nodelet_core-1.10.1-1.x86_64", url])
                writer.writerow(["ros-noetic-ros-nodelet_core", "1.10.1-1.x86_64", url])
            errors = run.validate_csv(bad)
            self.assertTrue(any("expected" in error for error in errors))
            self.assertTrue(any("duplicate URL" in error for error in errors))

            malformed = Path(directory) / "malformed.csv"
            malformed.write_text(
                "comp_name,version,url\n"
                "a,1-1.noarch,https://example.invalid/a-1-1.noarch.rpm,extra\n",
                encoding="utf-8",
            )
            self.assertTrue(
                any(
                    "unexpected extra CSV fields" in error
                    for error in run.validate_csv(malformed)
                )
            )

    def test_validate_rejects_bad_header_empty_and_parse_error(self):
        with tempfile.TemporaryDirectory() as directory:
            bad_header = Path(directory) / "header.csv"
            bad_header.write_text("name,url\n", encoding="utf-8")
            self.assertIn("invalid CSV header", run.validate_csv(bad_header)[0])

            bad_rows = Path(directory) / "rows.csv"
            with bad_rows.open("w", encoding="utf-8", newline="") as target:
                writer = csv.writer(target)
                writer.writerow(["comp_name", "version", "url"])
                writer.writerow(["", "1.0-1.x86_64", "https://example.invalid/a.rpm"])
                writer.writerow(["a", "1.0-1.x86_64", "not-an-rpm"])
            errors = run.validate_csv(bad_rows)
            self.assertTrue(any("empty required field" in error for error in errors))
            self.assertTrue(any("parse error" in error for error in errors))

    def test_help_lists_only_url_based_commands(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout), self.assertRaises(SystemExit) as raised:
            run.main(["--help"])
        self.assertEqual(raised.exception.code, 0)
        help_text = stdout.getvalue()
        self.assertIn("parse", help_text)
        self.assertIn("validate", help_text)
        self.assertIn("normalize", help_text)
        self.assertIn("rebuild-local", help_text)
        self.assertNotIn("refresh", help_text)
        self.assertNotIn("repodata", help_text)


if __name__ == "__main__":
    unittest.main()
