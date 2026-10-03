import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from server import Server


class InspectorTests(unittest.TestCase):
    def setUp(self):
        self.path = Path(__file__).with_name("manifest.example.json")
        self.server = Server(self.path)

    def request(self, method, params=None):
        return self.server.handle({"jsonrpc":"2.0", "id":1, "method":method, "params":params or {}})

    def start(self):
        self.request("initialize", {"protocolVersion":"2025-06-18"})
        self.server.handle({"jsonrpc":"2.0", "method":"notifications/initialized"})

    def test_lifecycle_and_read_only_tool(self):
        self.assertIn("error", self.request("tools/list"))
        self.start()
        tool = self.request("tools/list")["result"]["tools"][0]
        self.assertTrue(tool["annotations"]["readOnlyHint"])
        result = self.request("tools/call", {"name":"inspect_context"})["result"]
        self.assertFalse(result["isError"])
        self.assertEqual(result["structuredContent"]["domain"], "release")

    def test_caller_cannot_choose_a_different_file(self):
        self.start()
        result = self.request("tools/call", {"name":"inspect_context", "arguments":{"path":"/etc/passwd"}})
        self.assertEqual(result["error"]["code"], -32602)

    def test_stdio_parse_error_then_recovery(self):
        messages = ["not json", json.dumps({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18"}}), json.dumps({"jsonrpc":"2.0","method":"notifications/initialized"}), json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"inspect_context"}})]
        process = subprocess.run([sys.executable, str(Path(__file__).with_name("server.py")), "--manifest", str(self.path)], input="\n".join(messages)+"\n", text=True, capture_output=True, timeout=5, check=True)
        responses = [json.loads(x) for x in process.stdout.splitlines()]
        self.assertEqual(len(responses), 3)
        self.assertEqual(responses[0]["error"]["code"], -32700)
        self.assertEqual(responses[2]["result"]["structuredContent"]["owner"], "example-reader")
        self.assertEqual(process.stderr, "")

    def test_changed_invalid_manifest_returns_tool_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"manifest.json"
            path.write_text('{"records":[]}')
            server = Server(path)
            server.initialized = server.ready = True
            path.write_text('{"records":"broken"}')
            result = server.handle({"jsonrpc":"2.0", "id":2, "method":"tools/call", "params":{"name":"inspect_context"}})
            self.assertTrue(result["result"]["isError"])


if __name__ == "__main__":
    unittest.main()
