from contextlib import redirect_stderr
import io
import runpy
from pathlib import Path
import sys
import types
import unittest
from unittest import mock


SWAT_SIMULATOR_ROOT = Path(__file__).resolve().parents[1]
CLIENT_PATH = SWAT_SIMULATOR_ROOT / "modbus_helpers" / "synch_client.py"


class SynchClientTimeoutTest(unittest.TestCase):
    def pymodbus_modules(self, client_class):
        pymodbus = types.ModuleType("pymodbus")
        client = types.ModuleType("pymodbus.client")
        sync = types.ModuleType("pymodbus.client.sync")
        sync.ModbusTcpClient = client_class
        client.sync = sync
        pymodbus.client = client
        return {
            "pymodbus": pymodbus,
            "pymodbus.client": client,
            "pymodbus.client.sync": sync,
        }

    def run_client(self, extra_args=None, response=None):
        args = [
            str(CLIENT_PATH),
            "-i",
            "127.0.0.1",
            "-p",
            "502",
            "-m",
            "w",
            "-t",
            "HR",
            "-o",
            "0",
            "-r",
            "1",
        ]
        args.extend(extra_args or [])

        if response is None:
            response = mock.Mock(function_code=0)
        client = mock.Mock()
        client.write_register.return_value = response
        client_class = mock.Mock(return_value=client)
        with mock.patch.dict(
            sys.modules,
            self.pymodbus_modules(client_class),
        ), mock.patch.object(sys, "argv", args):
            runpy.run_path(str(CLIENT_PATH), run_name="__main__")
        return client_class

    def test_default_timeout_is_ten_seconds(self):
        client_class = self.run_client()

        client_class.assert_called_once_with(
            "127.0.0.1",
            port=502,
            timeout=10.0,
        )

    def test_timeout_can_be_overridden(self):
        client_class = self.run_client(["--timeout-seconds", "12.5"])

        client_class.assert_called_once_with(
            "127.0.0.1",
            port=502,
            timeout=12.5,
        )

    def test_timeout_must_be_positive(self):
        client_class = mock.Mock()
        with self.assertRaises(SystemExit), redirect_stderr(
            io.StringIO()
        ), mock.patch.dict(
            sys.modules,
            self.pymodbus_modules(client_class),
        ), mock.patch.object(
            sys,
            "argv",
            [str(CLIENT_PATH), "--timeout-seconds", "0"],
        ):
            runpy.run_path(str(CLIENT_PATH), run_name="__main__")
        client_class.assert_not_called()

    def test_modbus_io_error_has_clear_message(self):
        response = object()

        with self.assertRaisesRegex(SystemExit, "Modbus request failed"):
            self.run_client(response=response)

    def test_modbus_exception_function_code_is_rejected(self):
        response = mock.Mock(function_code=0x83)

        with self.assertRaisesRegex(
            SystemExit,
            "Modbus request returned exception function code",
        ):
            self.run_client(response=response)


if __name__ == "__main__":
    unittest.main()
