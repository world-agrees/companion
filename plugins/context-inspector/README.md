# Local context inspector

An executable, read-only MCP server example, **not an installed or published marketplace plugin**. Python 3.10+; standard library only. Tested against its documented JSON-RPC subset using the MCP **2025-06-18** protocol. This is a teaching implementation, not a full SDK or production service.

It reports one manifest explicitly supplied at startup. It cannot reveal a provider's hidden instructions, private reasoning, selected memories, or undeclared retrieval. A manifest reports what the application put in that file; an honest, complete request logger still has to produce it.

From the resource directory, run the tests:

```sh
python3 -m unittest discover -s plugins/context-inspector -v
```

For a terminal smoke test:

```sh
python3 plugins/context-inspector/server.py \
  --manifest plugins/context-inspector/manifest.example.json
```

Paste these three lines, one at a time. The middle notification has no response:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"reader","version":"1"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"inspect_context","arguments":{}}}
```

For an MCP client supporting local stdio servers, set its launch command to your Python executable, and pass absolute paths to `server.py` and `--manifest`. Its available tool should be `inspect_context`; supply `{}` as arguments. No API key is needed. Do not expose a private manifest to a remote client merely because this example reads locally: the client receives its contents and may send them to its model provider.

Codex CLI has a documented registration command. If you choose to install this local example, substitute your own absolute paths:

```sh
codex mcp add context-inspector -- python3 \
  /absolute/path/plugins/context-inspector/server.py \
  --manifest /absolute/path/your-context-manifest.json
```

Registration changes the client's configuration; nothing in this resource kit registers it automatically. Check `codex mcp --help` in your version. Other clients have different configuration formats. Distribution through a plugin catalog is a separate packaging and review process.

The server accepts no path argument from tool callers, makes no writes or network requests, enforces a 1 MiB input-file limit, and prints only protocol messages on standard output. Manifest text is untrusted data, not a new instruction source. Production use needs stronger schema validation, access control, request-size limits, compatibility testing, and retention controls suited to the deployment.

Sources, checked October 2, 2026: [MCP stdio transport](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports), [lifecycle](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle), [tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools), and [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp).
