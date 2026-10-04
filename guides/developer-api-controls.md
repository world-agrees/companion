# Developer API controls: build, inspect, check

Checked **October 3, 2026**. This guide supplements Chapter 11. The companion programs run offline with synthetic records. The SDK and memory-library examples below are optional integration recipes: they were checked against the linked primary documentation and syntax checked, but **were not installed or executed against a service**. Match them to your chosen SDK and model versions before use. These proposed controls make errors inspectable; they are not a measured cure for sycophancy.

## Run the offline examples first

From the `reader-resources` directory, use Python 3.10 or later:

```sh
python3 developer/context_store.py
python3 developer/compaction_demo.py
python3 developer/durable_memory.py
python3 developer/openai_requests.py
python3 developer/anthropic_requests.py
python3 developer/request_pipeline.py
python3 -m unittest discover -s developer/tests -v
```

These commands need no API key, SDK, model, or network. The payload builders print JSON. The store demonstrations use authored fixtures, and the durable demonstration uses its own temporary database. Their results establish what the local code does, not how accurately a deployed model behaves. See the [developer README](../developer/README.md) for the individual examples and deliberate evaluation failures.

Start with a request manifest rather than an entire transcript. Authenticate the caller in your application, select the authorized user and purpose, then select current record IDs. `Store.context()` returns the selected records and a checksum. `checked_context()` checks their declared scope, status, IDs, and checksum. Neither function authenticates a user or establishes that a source is true. Those checks belong to your application.

## Know where additional context enters

| Surface | Context to inspect | Correction to make |
| --- | --- | --- |
| Ordinary Claude Messages request | Top-level `system` and the messages your application sends. The ordinary endpoint is stateless. | Rebuild the request from the correct authorized records. |
| OpenAI Responses request | Explicit input, instructions, optional `previous_response_id` or Conversation state, files and tools. | Inspect every state mechanism you enabled; a fresh prompt alone may still reference stored state. |
| Your memory service or database | Records, indexes, extraction instructions, retrieval filters and writers. | Correct the stored record and review summaries or decisions derived from it. |
| Compaction | Replacement state, a summary where exposed, and which original material is no longer active. OpenAI encrypted compaction items are opaque. | Keep a separate source/correction ledger; check an exposed summary before continuing. Retain originals when policy permits. |
| Prompt cache | Reuse of submitted prompt prefixes. | Stop including obsolete material in newly assembled input; cache expiry is not an application correction plan. |

Sources: [Claude Messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages), [OpenAI conversation state](https://developers.openai.com/api/docs/guides/conversation-state), [OpenAI compaction](https://developers.openai.com/api/docs/guides/compaction), [Claude compaction](https://platform.claude.com/docs/en/build-with-claude/compaction), [Claude prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching).

The companion builders attach no stored conversation, memory tool, retrieved file, or arbitrary extra parameter. OpenAI's builder also uses `store=False`; that controls response application state, not every retention mechanism. Recheck the applicable endpoint, tool and organization settings against [OpenAI data controls](https://developers.openai.com/api/docs/guides/your-data).

## Keep model settings explicit

The examples use a small documented model set, not a compatibility table for every model. Record the exact model ID and request settings with an evaluation result. A provider update is a reason to rerun the representative evaluation cases.

| Example model IDs | Supported controls used here | Settings omitted here |
| --- | --- | --- |
| `gpt-6.1-sol`, `gpt-6-astra` | `reasoning.effort`: `low`, `medium`, `high`, `xhigh`, `max`; `max_output_tokens`. | Sampling arguments and `none` reasoning. |
| `gpt-6-sol`, `gpt-6-luna` | The same efforts plus `none`; the builder allows either `temperature` or `top_p` only with `none`. | Sampling arguments while reasoning is enabled; changing both sampling controls together. |
| `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-fable-5-1` | Explicit `thinking: {"type": "adaptive"}`; `output_config.effort`: `low`, `medium`, `high`, `xhigh`, `max`; `max_tokens`. | Manual `budget_tokens`, disabled thinking, and `temperature`, `top_p`, `top_k`. |

Sources: [GPT 6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol), [GPT 6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [GPT 6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol), [GPT 6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna), [GPT 6 parameter compatibility](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.1-sol); [Claude thinking](https://platform.claude.com/docs/en/build-with-claude/thinking), [Claude effort](https://platform.claude.com/docs/en/build-with-claude/effort), [Opus 5.5 migration](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide).

Temperature controls sampling variation when a model supports it. A lower setting is not a factuality check. More reasoning effort is also not verification: compare error rates, omissions, latency and cost on your own cases. Claude's effort setting is not a hard token budget; thinking and final text share the total output allowance. The builders' character caps are demonstration limits, not token counters. For a live integration, use the provider's current token-counting mechanism and leave room for output. [OpenAI token counting](https://developers.openai.com/api/docs/guides/token-counting), [Claude token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting).

## Optional SDK integration: separate generation from approval

The following code is a complete integration example for the companion builders. Save it beside them in `developer/` only if you choose to adapt it. It requires the optional `openai` and/or `anthropic` Python SDK in your own environment. Configure `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` through your deployment's secret mechanism, outside the source, prompts, fixtures and logs. No key discovery is needed to run the offline examples.

The functions below make network requests **only when called**. They have no top-level invocation. Both send synthetic corrected evidence that two release tests failed. The application gate therefore holds the release even if a model returns `proceed`.

```python
import json

from context_store import demo
from openai_requests import build_request as openai_payload
from anthropic_requests import build_request as claude_payload
from request_context import checked_context


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def validate_review(raw_text, manifest):
    context = checked_context(manifest)
    review = json.loads(
        raw_text, object_pairs_hook=reject_duplicate_keys
    )
    fields = {
        "verdict", "evidence_ids", "qualifications",
        "explanation",
    }
    if type(review) is not dict or set(review) != fields:
        raise ValueError("unexpected result fields")
    if review["verdict"] not in {
        "proceed", "hold", "insufficient_evidence",
    }:
        raise ValueError("unknown verdict")
    for field in ("evidence_ids", "qualifications"):
        values = review[field]
        if type(values) is not list or any(
            not isinstance(v, str) or not v.strip()
            for v in values
        ):
            raise ValueError("non-text or empty array item")
    if not isinstance(review["explanation"], str) or not (
        review["explanation"].strip()
    ):
        raise ValueError("missing explanation")
    ids = review["evidence_ids"]
    known = {r["id"] for r in context["records"]}
    if len(ids) != len(set(ids)) or not set(ids) <= known:
        raise ValueError("duplicate or unsubmitted source ID")
    if review["verdict"] == "proceed" and not ids:
        raise ValueError("approval without source IDs")
    return review


def release_gate(review, trusted_results, required_tests):
    # Inputs come from the application's recorded CI output,
    # never from model prose or the user's desired conclusion.
    if not required_tests or any(
        trusted_results.get(test) != "passed"
        for test in required_tests
    ):
        return "hold"
    # This remains a proposal. A separate actor authorizes action.
    return review["verdict"]


def fixture_context():
    store, _ = demo()
    manifest = store.context("alice", "release", ["m2"])
    return manifest


def finish(raw_text, manifest):
    review = validate_review(raw_text, manifest)
    # Authored fixture, not an observed CI run.
    fixture_results = {"smoke": "failed", "load": "failed"}
    decision = release_gate(
        review, fixture_results, ("smoke", "load")
    )
    return {
        "model_review": review,
        "application_decision": decision,
    }


def review_with_openai():
    from openai import OpenAI

    manifest = fixture_context()
    payload = openai_payload(
        "Do the release tests support proceeding?",
        manifest, model="gpt-6.1-sol", effort="high",
    )
    response = OpenAI().responses.create(**payload)
    if response.status != "completed":
        raise ValueError("response did not complete")
    for item in response.output:
        # No tools were requested. Unexpected calls are not results.
        if item.type not in {"message", "reasoning"}:
            raise ValueError("unexpected output item")
        if item.type == "message":
            for part in item.content:
                if part.type == "refusal":
                    raise ValueError("model refused the request")
                if part.type != "output_text":
                    raise ValueError("unexpected message content")
    if not response.output_text.strip():
        raise ValueError("no result text")
    return finish(response.output_text, manifest)


def review_with_claude():
    from anthropic import Anthropic

    manifest = fixture_context()
    payload = claude_payload(
        "Do the release tests support proceeding?",
        manifest, model="claude-opus-5-5", effort="high",
    )
    response = Anthropic().messages.create(**payload)
    if response.stop_reason != "end_turn":
        raise ValueError("response did not finish normally")
    parts = []
    for block in response.content:
        if block.type == "text":
            parts.append(block.text)
        elif block.type not in {"thinking", "redacted_thinking"}:
            raise ValueError("unexpected content or tool request")
    text = "".join(parts)
    if not text.strip():
        raise ValueError("no result text")
    return finish(text, manifest)
```

OpenAI structured responses can contain refusals, and incomplete responses need separate handling. A completed response with a tool call does not mean the tool ran. This no-tool recipe rejects unexpected output items. [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

Claude can return a refusal with HTTP 200, and output exhaustion can leave incomplete JSON. This recipe accepts only `end_turn`, so it also stops on `refusal`, `max_tokens`, `model_context_window_exceeded`, `tool_use`, or `compaction`. It deliberately rejects an enum spelling that differs from the requested values. Native document citations cannot share a request with `output_config.format`; these builders instead use application record IDs. [Claude structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs).

After parsing, inspect whether each cited source actually supports the conclusion. An ID can be valid while its use is misleading. Check source ownership, dates, missing records, factual conflicts and executed calculations. A valid citation location also does not establish source reliability. [Claude citations](https://platform.claude.com/docs/en/build-with-claude/citations).

The small release gate checks one application policy. It does not verify every assertion in the explanation. In production, replace the fixture with recorded test outcomes, verify their origin, define the required tests outside the model, and keep deployment permission in a separate authenticated action. Exceptions should stop the action; retrying transient failures is different from repeatedly asking until the model approves.

## Claude memory tools: you implement the storage boundary

Enabling `{"type": "memory_20250818", "name": "memory"}` gives Claude a client-side tool interface; your handler performs the requested operations. Allocate the store from trusted tenant/user/purpose identities. Canonicalize every requested path and enforce containment under that store, including traversal and encoded variants. Cap file sizes and returned content, define expiration and review consequential writes. A model-supplied `/memories` path is not authorization. The provider's local filesystem helper and tool runner are optional beta SDK surfaces, distinct from the tool itself. [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool).

The chapter's request builders omit this tool. If you add it, also add an inspectable record of actual tool operations and outcomes. A tool proposal is not execution, and a model's description of what happened is not your execution log. Use the same principle for browser and computer tools. [Computer use limitations](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool).

## Compaction: review the replacement before continuing

Current Claude threshold compaction uses beta header `compact-2026-01-12` and a `context_management.edits` entry with `type: "compact_20260112"`. Set `pause_after_compaction: true` to receive a `compaction` stop reason before normal continuation. Custom summary instructions replace the default instructions completely. Treat a missing or null summary as a failed checkpoint. [Threshold compaction](https://platform.claude.com/docs/en/build-with-claude/compaction-threshold).

On-demand compaction is a different protocol: beta `compact-2026-09-04`, with `compaction: {"type": "summarize"}`. It cannot be combined with `context_management`. Carry its signed block unchanged as the first message on later calls, with the beta header; remove the turns it replaced. Reintroduce original documents or images if later work needs them. Check the exact model's current capability before enabling this beta. [On-demand compaction](https://platform.claude.com/docs/en/build-with-claude/compaction-on-demand).

At a checkpoint, compare the replacement with the original sources. Preserve speaker, date, source IDs, uncertainty, corrected versions, failed tests and unresolved questions. If the summary is misleading, reject it and construct a fresh authorized request or a sourced correction; editing a signed block is not a supported repair. Keep a record of the accepted summary version when retention policy permits. [Offline compaction example](../developer/compaction_demo.py).

## LangGraph: thread state and long-term stores are separate

This optional recipe requires the `langgraph` package. It uses `InMemoryStore` and `InMemorySaver`, so the selected example has no embedding/model call or persistent database. Production database adapters have their own dependencies and retention behavior. Thread checkpoints and a separate store are different layers. [LangGraph memory](https://docs.langchain.com/oss/python/langgraph/add-memory).

```python
def langgraph_example():
    from langgraph.store.memory import InMemoryStore
    from langgraph.checkpoint.memory import InMemorySaver

    store = InMemoryStore()
    checkpointer = InMemorySaver()
    # In a real application, these values come from authentication.
    namespace = ("demo-tenant", "alice", "release")
    key = "build-42"
    store.put(namespace, key, {
        "text": "Load test failed.",
        "source": "test-log:build-42",
        "status": "current",
    })
    candidates = store.search(
        namespace, filter={"status": "current"}, limit=20
    )
    # search takes a namespace prefix, not an exact namespace.
    exact = [i for i in candidates if i.namespace == namespace]
    store.put(namespace, key, {
        "text": "Corrected log: smoke and load tests failed.",
        "source": "test-log:build-42-correction",
        "status": "current",
    })
    corrected = store.get(namespace, key)
    store.delete(namespace, key)
    # Only thread checkpoints; not the long-term store above.
    checkpointer.delete_thread("demo-thread")
    return exact, corrected
```

`put` writes or replaces a key; `get` reads it; `search` accepts a namespace prefix and filters; `delete` removes the named key. Exact-scope checks matter when sub-namespaces exist. Semantic querying requires an explicitly configured index/embedder; the example instead uses a metadata filter. `index=False` disables indexing of a value, not authorization or ordinary access. [Current BaseStore implementation](https://github.com/langchain-ai/langgraph/blob/main/libs/checkpoint/langgraph/store/base/__init__.py).

Before accepting a correction, find other summaries and decisions derived from the old value. Store replacement does not automatically identify those dependencies in your application. Deleting a thread's checkpoints does not remove long-term store records, traces or backups. Record which layer a “clear memory” control actually clears.

## Mem0: choose OSS or the hosted Platform deliberately

The Python package is `mem0ai`. OSS uses `Memory`; the hosted Platform uses `MemoryClient`. A default OSS `Memory()` uses remote OpenAI extraction and embedding models, local Qdrant storage under `/tmp/qdrant`, and SQLite history at `~/.mem0/history.db`. Local storage therefore does not establish local processing. The examples below receive an already configured instance and never instantiate these defaults. [OSS quickstart](https://docs.mem0.ai/open-source/python-quickstart).

Choose the extraction model, embedder, vector store, optional reranker, history location and outbound providers before constructing `Memory.from_config(config)`. Select dedicated storage paths/collections rather than reusing an agent's live store for experiments. The configuration documentation distinguishes self-managed and managed components. [OSS configuration](https://docs.mem0.ai/open-source/configuration).

### Add and retrieve a scoped record

Current OSS and Platform search calls put entity IDs inside `filters`; current OSS v3 rejects a top-level `user_id` search argument. The example uses one application-generated identifier for tenant, person and purpose. It is a retrieval scope, not proof of authorization. [Search operations](https://docs.mem0.ai/core-concepts/memory-operations/search).

```python
def add_and_search_oss(memory, authorized_scope):
    # memory is an already configured mem0.Memory instance.
    # authorized_scope comes from the application, not the model.
    messages = [{
        "role": "user",
        "content": (
            "Alice reported a failed load test on 2026-10-03; "
            "this report has not been independently verified."
        ),
    }]
    added = memory.add(
        messages, user_id=authorized_scope,
        metadata={"source": "meeting:2026-10-03"},
        infer=False,
    )
    found = memory.search(
        "release test results",
        filters={"user_id": authorized_scope},
    )
    return added, found


def add_platform(client, authorized_scope):
    # client is an externally configured mem0.MemoryClient.
    return client.add(
        messages=[{
            "role": "user",
            "content": "Alice reported a failed load test.",
        }],
        user_id=authorized_scope,
    )


def search_platform(client, authorized_scope):
    return client.search(
        "release test results",
        filters={"user_id": authorized_scope},
    )
```

With `infer=False`, OSS stores raw messages rather than extracting claims; embedding and storage operations still follow the configured providers. With inference enabled, inspect the extracted result. Current additions accumulate records rather than retiring contradictions automatically. Hosted additions return a pending event; confirm completion through the documented `GET /v1/event/{event_id}/` endpoint before relying on a search. The Platform also uses earlier messages sharing the identifiers during extraction, so a hosted extraction may see more than the new turn you submit. [Add operations](https://docs.mem0.ai/core-concepts/memory-operations/add).

### Correct or delete an inspected ID

Locate the exact memory ID and original source first. Build the allowlist below from an authenticated application query or reviewed record ownership, not from model text. Search ranking alone is not an ownership check.

```python
def correct_mem0(memory_or_client, memory_id, allowed_ids):
    if memory_id not in allowed_ids:
        raise PermissionError("record outside authorized scope")
    return memory_or_client.update(
        memory_id=memory_id,
        text="Corrected test log: smoke and load tests failed.",
        metadata={"source": "test-log:build-42-correction"},
    )


def delete_mem0(memory_or_client, memory_id, allowed_ids):
    if memory_id not in allowed_ids:
        raise PermissionError("record outside authorized scope")
    return memory_or_client.delete(memory_id=memory_id)
```

The current Python examples for OSS and Platform accept `update(memory_id=..., text=..., metadata=...)`. Prefer `text`; OSS documents `data` as a deprecated alias. Immutable records require deletion and re-addition. Inspect the operation response and search again to verify the corrected value. [Update operations](https://docs.mem0.ai/core-concepts/memory-operations/update).

Both deployments also expose `delete_all(user_id=...)`. Reserve it for an explicit scope-level erasure action after resolving the scope in your application. A single-record deletion does not roll back an old summary or recommendation elsewhere. Check the service result and your own retained transcripts, derived summaries, indexes and backups. [Delete operations](https://docs.mem0.ai/core-concepts/memory-operations/delete).

A similarity score measures retrieval relevance, not the truth of the retrieved claim. Preserve source/date/uncertainty in your application, review returned records before using them, and test isolation with harmless synthetic records in each scope. A library can supply retrieval and mutation functions; you still define who may use them and what a correction invalidates.

## Test the whole request path

For a consequential decision, vary the desired answer while keeping the source evidence fixed. Try neutral wording, user praise, user displeasure and a request to proceed despite a failed test. Measure whether factual findings, qualifications and the application gate stay consistent. Then correct a stored source, restart the process, retrieve again and check which summaries survive. Add cross-scope and expired-record cases.

Keep the evaluation artifacts separate: request manifest, prompt version, exact model settings, returned completion state, parsed response, source-check result and final action decision. Retain only what your policy permits. A second model can find a problem, but it is another model output; verify its objections against the same sources. Use [the evidence-constrained prompt](../prompts/15-evidence-constrained-api.md) and the [offline evaluation examples](../developer/README.md) as starting points.

For the long-running agent controls introduced in Chapter 10, see [Hermes](hermes.md), [OpenClaw](openclaw.md) and [memory services](memory-services.md). The companion remains subject to the author's [current rights notice](../LICENSE.md); this guide does not change its publication or distribution terms.
