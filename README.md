# The World That Agrees With You: reader resources

Practical companion to Part III of Timothy O'Brien's *The World That Agrees With You: Understanding and Managing Sycophancy in the Age of AI*.

**Documentation checked October 2, 2026.** Start with one consequential task: inspect its context, supply the original evidence, check the result, and correct material that could influence later answers. These resources make that work concrete. They do not guarantee objective output or expose every hidden input in a hosted product.

## Choose a starting point

| Your task | Open this resource |
| --- | --- |
| Inspect ChatGPT memory and start a fresh assessment | [ChatGPT guide](guides/chatgpt.md) |
| Inspect Claude memory and distinguish conversation modes | [Claude guide](guides/claude.md) |
| Manage consumer or workplace Microsoft Copilot | [Microsoft Copilot guide](guides/microsoft-copilot.md) |
| Inspect coding-assistant instructions and history | [Claude Code](guides/claude-code.md), [GitHub Copilot](guides/github-copilot.md), [Codex](guides/codex.md) |
| Review agent memory writes and consolidation | [Hermes](guides/hermes.md), [OpenClaw](guides/openclaw.md) |
| Ask for an assessment grounded in evidence | [Ten reusable prompts](prompts/README.md) |
| Record the sources, decision, or correction | [Six templates](templates/README.md) |
| Try an example with a known arithmetic result | [Friday scheduling example](examples/scheduling/README.md) |
| Build inspectable memory and test preference pressure | [Developer walkthrough](developer/README.md) |
| Reuse a task-specific agent workflow | [Skills](#three-reusable-skills) |
| Expose one selected context manifest to an agent | [Read-only MCP example](plugins/context-inspector/README.md) |
| Check the primary documentation and research | [Source index](SOURCES.md) |

## A first exercise

1. Read the guide for your product. Select the context controls before submitting the question.
2. Open the [scheduling example](examples/scheduling/README.md). Supply its task list and availability record.
3. Ask for the calculation and the assumptions supporting the recommendation. The estimated work is twenty hours; availability is fourteen; the shortage is six.
4. Check the arithmetic independently. A desired deadline is not evidence of additional capacity.
5. If an answer changes after your objection, ask which new evidence caused the change. Record the difference rather than keep asking until you get reassurance.

For your own task, substitute the actual contract, test log, messages, or figures. A source identifier helps you locate evidence; it does not establish that the evidence is correct.

## Three reusable skills

- [Evidence review](skills/evidence-review/SKILL.md): distinguish supported findings, reports, assumptions, and unresolved claims.
- [Memory correction](skills/memory-correction/SKILL.md): identify a bad conclusion, its source, and dependent material that needs review.
- [Preference invariance](skills/preference-invariance/SKILL.md): compare matched requests while holding evidence fixed.

Read a skill before adding it to your agent. Installation depends on the product; the guides explain supported locations and controls. A Markdown instruction is not an access-control rule. The kit does not install itself or change account settings.

## Run the offline developer examples

Use Python 3.10 or later. From this directory:

```sh
python3 examples/scheduling/check.py
python3 developer/context_store.py
python3 developer/eval_runner.py
python3 -m unittest discover -s developer/tests -v
python3 -m unittest discover -s plugins/context-inspector -v
```

These use the standard library and require no network connection, API key, or model account. The evaluation fixtures deliberately include a failure. They are authored examples, not measurements of ChatGPT, Claude, or any other model. The [developer guide](developer/README.md) explains how to supply real outputs for checks you choose to run, and why a human still needs to examine the evidence and full response.

The memory store assumes trusted application code. Production identity, authorization, persistence, verification, and deletion need application enforcement. Its manifest records selected context, not the provider's complete internal input. The local MCP server reads one operator-selected manifest; it cannot discover hidden context.

## Use alongside the book

- **Chapter 8:** consumer controls, fresh assessments, evidence prompts, and corrections.
- **Chapter 9:** source manifests, calculations, commitments, and workplace handoffs.
- **Chapter 10:** developer memory design, correction of dependent records, skills, and tests.
- **Chapter 11:** supplier demonstrations, review authority, correction, and appeal.

The ZIP includes `SHA256SUMS` for its payload. On macOS or Linux, you can check an extracted copy from its root with `shasum -a 256 -c SHA256SUMS`. Checksums detect changed files; they do not certify factual correctness.

This companion accompanies the review draft as a local repository and ZIP. Product directions are documentation-checked, not live-account-tested. Settings vary by version, plan, region, and organizational policy. Follow the linked primary instructions when the interface differs, and record what you could not inspect. Rights remain as stated in [LICENSE.md](LICENSE.md).
