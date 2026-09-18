import importlib.util
from pathlib import Path
import shlex
import sys
import types
import unittest
from unittest import mock


SWAT_SIMULATOR_ROOT = Path(__file__).resolve().parents[1]
PROTOCOLS_PATH = SWAT_SIMULATOR_ROOT / "protocols.py"


def load_protocols_module():
    spec = importlib.util.spec_from_file_location("testbed_protocols", PROTOCOLS_PATH)
    module = importlib.util.module_from_spec(spec)
    dependencies = {
        "cpppo": types.ModuleType("cpppo"),
        "pymodbus": types.ModuleType("pymodbus"),
    }
    with mock.patch.dict(sys.modules, dependencies):
        spec.loader.exec_module(module)
    return module


class ProtocolHelperPathTest(unittest.TestCase):
    def test_modbus_client_uses_repository_helper(self):
        protocols = load_protocols_module()
        with mock.patch.object(protocols.sys, "platform", "linux"):
            protocol = protocols.ModbusProtocol({"name": "modbus", "mode": 0})

        self.assertEqual(
            shlex.split(protocol._client_cmd),
            [
                sys.executable,
                str(SWAT_SIMULATOR_ROOT / "modbus_helpers" / "synch_client.py"),
            ],
        )

    def test_modbus_server_uses_repository_helper(self):
        protocols = load_protocols_module()
        config = {
            "name": "modbus",
            "mode": 1,
            "server": {
                "address": "127.0.0.1:502",
                "tags": (10, 10, 10, 10),
            },
        }
        with mock.patch.object(protocols.sys, "platform", "linux"), mock.patch.object(
            protocols.ModbusProtocol, "_start_server", return_value=object()
        ) as start_server:
            protocols.ModbusProtocol(config)

        command = shlex.split(start_server.call_args.kwargs["cmd_path"])
        self.assertEqual(
            command,
            [
                sys.executable,
                str(SWAT_SIMULATOR_ROOT / "modbus_helpers" / "servers.py"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
