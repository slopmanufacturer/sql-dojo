import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("dojo", ROOT / "dojo.py")
dojo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dojo)


class CompareTest(unittest.TestCase):
    def test_column_names_are_not_graded(self):
        ok, why = dojo.compare((["a"], [("1",)]), (["b"], [("1",)]), ordered=True)
        self.assertTrue(ok, why)

    def test_column_count_is_graded(self):
        ok, why = dojo.compare((["a"], [("1",)]), (["a", "b"], [("1", "2")]), ordered=True)
        self.assertFalse(ok)
        self.assertIn("columns", why)

    def test_ordered_reference_requires_the_same_order(self):
        ok, why = dojo.compare((["a"], [("1",), ("2",)]), (["a"], [("2",), ("1",)]), ordered=True)
        self.assertFalse(ok)
        self.assertIn("order", why)

    def test_unordered_reference_ignores_the_order(self):
        ok, why = dojo.compare((["a"], [("1",), ("2",)]), (["a"], [("2",), ("1",)]), ordered=False)
        self.assertTrue(ok, why)

    def test_unordered_reference_still_rejects_different_rows(self):
        ok, _ = dojo.compare((["a"], [("1",), ("2",)]), (["a"], [("1",), ("3",)]), ordered=False)
        self.assertFalse(ok)

    def test_null_is_not_the_empty_string(self):
        self.assertNotEqual(dojo.norm_row([None]), dojo.norm_row([""]))

    def test_floats_compare_at_six_decimals(self):
        self.assertEqual(dojo.norm_row([1.0000001]), dojo.norm_row([1.0]))


class ExercisesTest(unittest.TestCase):
    def test_the_readme_count_is_the_real_count(self):
        self.assertEqual(len(dojo.exercises()), 60)

    def test_every_exercise_has_its_five_files(self):
        for ex in dojo.exercises():
            for name in ("prompt.md", "starter.sql", "hints.md", "solution.sql", "expected.csv"):
                self.assertTrue((ex.path / name).is_file(), f"{ex.short}: missing {name}")

    def test_every_solution_matches_its_expected_csv(self):
        for ex in dojo.exercises():
            conn = dojo.connect()
            try:
                got = dojo.execute(conn, (ex.path / "solution.sql").read_text())
            finally:
                conn.close()
            expected = dojo.load_expected(ex)
            ok, why = dojo.compare(expected, got, dojo.solution_is_ordered(ex))
            self.assertTrue(ok, f"{ex.short}: {why}")


if __name__ == "__main__":
    unittest.main()
