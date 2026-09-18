import ast
from pathlib import Path
import unittest


SWAT_SIMULATOR_ROOT = Path(__file__).resolve().parents[1]


class PlcControlBlockCallTest(unittest.TestCase):
    def test_mv_fbd_calls_supply_reset_argument(self):
        invalid_calls = []
        for source_path in sorted((SWAT_SIMULATOR_ROOT / "real_plc").glob("plc*.py")):
            tree = ast.parse(source_path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "MV_FBD"
                    and len(node.args) != 4
                ):
                    invalid_calls.append(
                        f"{source_path.name}:{node.lineno} has {len(node.args)} arguments"
                    )

        self.assertEqual(invalid_calls, [])


if __name__ == "__main__":
    unittest.main()
