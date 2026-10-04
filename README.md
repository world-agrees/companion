# The World That Agrees With You: reader resources

Practical companion to Part III of Timothy O'Brien's *The World That Agrees With You: Understanding and Managing Sycophancy in the Age of AI*.

Book website: [worldagrees.com](https://worldagrees.com). Public companion repository: [world-agrees/companion](https://github.com/world-agrees/companion).

## Get the companion

Download the [current ZIP](https://github.com/world-agrees/companion/archive/refs/heads/main.zip) and extract it, or clone the repository:

```sh
git clone https://github.com/world-agrees/companion.git
cd companion
```

The guides, prompts, templates, skills, and examples are in this repository's root directory. Start with the table below. The repository contains the companion resources; the book is available separately through its website.

**Chapters 8–11 resources updated October 3, 2026; other guides retain their individual check dates.** Start with one consequential task: inspect its context, supply the original evidence, check the result, and correct material that could influence later answers. These resources make that work concrete. They do not guarantee objective output or expose every hidden input in a hosted product.

## Choose a starting point

| Your task | Open this resource |
| --- | --- |
| Inspect ChatGPT memory and start a fresh assessment | [ChatGPT guide](guides/chatgpt.md) |
| Inspect Claude memory and distinguish conversation modes | [Claude guide](guides/claude.md) |
| Manage consumer or workplace Microsoft Copilot | [Microsoft Copilot guide](guides/microsoft-copilot.md) |
| Inspect coding-assistant instructions and history | [Claude Code](guides/claude-code.md), [GitHub Copilot](guides/github-copilot.md), [Codex](guides/codex.md) |
| Review agent memory writes and consolidation | [Hermes](guides/hermes.md), [OpenClaw](guides/openclaw.md) |
| Inspect external memory providers and their integration scopes | [Mem0, Honcho, Hindsight, and Letta](guides/memory-services.md) |
| Ask for an assessment grounded in evidence | [Fifteen reusable prompts](prompts/README.md) |
| Review a complete document with a second model | [Devil's advocate setup](guides/devils-advocate.md), [copyable prompt](prompts/13-devils-advocate.md) |
| Organize evidence and check analysis before drafting | [Evidence workspace](guides/evidence-workspace.md), [staged prompts](prompts/14-evidence-workflow.md) |
| Run calculations and collect real data before recommending | [Calculation and research guide](guides/calculation-and-research.md), [calculation prompt](prompts/03-check-calculations.md) |
| Coordinate people and assistants on one document project | [Shared project instructions](templates/document-project-instructions.md) |
| Record the sources, decision, or correction | [Nine templates](templates/README.md) |
| Try an example with a known arithmetic result | [Friday scheduling example](examples/scheduling/README.md) |
| Inspect an executed cost comparison and Excel formulas | [Project cost example](examples/project-costs/README.md), [ready-to-open workbook](examples/project-costs/project-costs.xlsx) |
| Build inspectable memory and test preference pressure | [Developer walkthrough](developer/README.md) |
| Construct explicit API requests and validate proposals | [Developer API guide](guides/developer-api-controls.md), [API prompt](prompts/15-evidence-constrained-api.md) |
| Reuse a task-specific agent workflow | [Skills](#four-reusable-skills) |
| Expose one selected context manifest to an agent | [Read-only MCP example](plugins/context-inspector/README.md) |
| Check the primary documentation and research | [Source index](SOURCES.md) |

## A first exercise

1. Read the guide for your product. Select the context controls before submitting the question.
2. Open the [scheduling example](examples/scheduling/README.md). Supply its task list and availability record.
3. Ask for the calculation and the assumptions supporting the recommendation. The estimated work is twenty hours; availability is fourteen; the shortage is six.
4. Check the arithmetic independently. A desired deadline is not evidence of additional capacity.
5. If an answer changes after your objection, ask which new evidence caused the change. Record the difference rather than keep asking until you get reassurance.

For your own task, substitute the actual contract, test log, messages, or figures. A source identifier helps you locate evidence; it does not establish that the evidence is correct.

For substantial documents, keep a project directory with `evidence/`, `analysis/`, `output/`, and `prompts/`, plus explicit project instructions and a separate desired-outcome file. The document is the output of those smaller tasks. Consumer chats need the selected files supplied through supported uploads or connections; folder names and shared prompts do not themselves grant access or enforce context boundaries.

## Four reusable skills

- [Weekly context review](skills/weekly-context-review/SKILL.md): inspect visible context, propose corrections, and prepare a dated brief for next week.
- [Evidence review](skills/evidence-review/SKILL.md): distinguish supported findings, reports, assumptions, and unresolved claims.
- [Memory correction](skills/memory-correction/SKILL.md): identify a bad conclusion, its source, and dependent material that needs review.
- [Preference invariance](skills/preference-invariance/SKILL.md): compare matched requests while holding evidence fixed.

The **evidence-review** and **weekly-context-review** folders are self-contained; their [upload ZIPs](skill-uploads/) are ready for the documented consumer Claude workflow. For ChatGPT, copy the procedure into a prompt or suitable project instructions.

Read a skill before adding it to your agent. Installation depends on the product; the guides explain supported locations and controls. A Markdown instruction is not an access-control rule. The kit does not install itself or change account settings.

## Run the offline developer examples

Use Python 3.10 or later. From this directory:

```sh
python3 examples/scheduling/check.py
python3 developer/context_store.py
python3 developer/eval_runner.py
python3 developer/compaction_demo.py
python3 developer/durable_memory.py
python3 developer/openai_requests.py
python3 developer/anthropic_requests.py
python3 developer/request_pipeline.py
python3 -m unittest discover -s developer/tests -v
python3 -m unittest discover -s plugins/context-inspector -v
```

These use the standard library and require no network connection, API key, or model account. The evaluation fixtures deliberately include a failure. They are authored examples, not measurements of ChatGPT, Claude, or any other model. The agent-memory scripts demonstrate summary qualification loss and correction across processes. The API builders print explicit-context payloads without sending them; the request pipeline holds a well-formed approval when required test evidence fails. The [developer guide](developer/README.md) explains integration boundaries and why source IDs and valid JSON do not establish truth.

The separate [project cost example](examples/project-costs/README.md) uses XlsxWriter and openpyxl to create and inspect a formula-bearing workbook. Its instructions list those dependencies and distinguish Python-computed caches from recalculation in Excel. Readers can use the consumer calculation prompt without running the example locally.

The memory store assumes trusted application code. Production identity, authorization, persistence, verification, and deletion need application enforcement. Its manifest records selected context, not the provider's complete internal input. The local MCP server reads one operator-selected manifest; it cannot discover hidden context.

## Use alongside the book

- **Chapter 8:** consumer controls, local chat history, project boundaries, prompt discipline, tone, weekly reviews, corrections, and supporting files kept outside the chat.
- **Chapter 9:** evidence, analysis, output, and prompt folders; staged work and human checkpoints; a constructive Devil's advocate review; executed calculations, formula workbooks, source-backed research, preserved commitments, and explicit team responsibilities.
- **Chapter 10 and Appendix C:** Hermes and OpenClaw notes, history, write gates, consolidation, and correction; external memory services; offline summary and restart demonstrations; developer memory design, skills, and tests.
- **Chapter 11 and Appendix D:** API request construction, scoped and correctable memory, model-specific settings, evidence prompts, runtime validation, deterministic action gates, prompt libraries, and repeatable evaluations. Appendix D collects the primary developer references and explains where to begin with this companion.

The ZIP includes `SHA256SUMS` for its payload. On macOS or Linux, you can check an extracted copy from its root with `shasum -a 256 -c SHA256SUMS`. Checksums detect changed files; they do not certify factual correctness.

This companion is distributed through the public repository and the book's resource ZIP. Product directions are documentation-checked, not live-account-tested. Settings vary by version, plan, region, and organizational policy. Follow the linked primary instructions when the interface differs, and record what you could not inspect. Rights remain as stated in [LICENSE.md](LICENSE.md).
