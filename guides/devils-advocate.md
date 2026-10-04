# Devil's advocate: set up a second review

Documentation checked **October 3, 2026**. These are researched directions, not a live account test or a completed review. Availability depends on your client, plan, and administrator. Use the linked official instructions when controls differ.

Start with the [complete-document prompt](../prompts/13-devils-advocate.md) and [review report template](../templates/devils-advocate-review.md). The aim is a constructive, neutral assessment that can identify real problems and preserve sound work. No criticism quota is required.

## Prepare the same document and evidence

1. Save a complete version with a title, date, and revision identifier. Include the introduction, notes, appendices, and relevant figures. For an email, include the message and material needed to assess it.
2. State the intended audience, purpose, and requirements. Attach the original source records, not only another assistant's summaries.
3. Select a different capable model, preferably a different provider when your material is approved for that service. Changing the hosting provider for the same model does not create a different model family.
4. Inspect available context controls using the [ChatGPT](chatgpt.md) or [Claude](claude.md) guide. A fresh chat does not necessarily exclude memory, personal instructions, or retrieved files.
5. Keep the drafting model's verdict out of the initial review unless it is required evidence. Record the model and effort that actually answer, including any displayed model switch.

Another model may make the same mistakes. Check material findings against evidence rather than taking agreement as a vote.

## ChatGPT Work

ChatGPT Work is unavailable in a project using project-only memory. Start a separate task and inspect its environment, attached folders, plugins, sources, and standing context. These access controls do not establish the same memory boundary; a fresh Work task can still use applicable personal context. [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), [Work capabilities](https://learn.chatgpt.com/docs/use-chatgpt).

1. Open **Work** and start a new task.
2. Open the model and reasoning control beneath the composer. Use **Advanced** where shown, and select an available model such as **GPT 6.1 Sol** or **Astra**.
3. Select **Max** or **Ultra** when supported. In the desktop app, an available Ultra option can be shown with **Settings → Configuration → Ultra in model picker slider**. Account and workspace restrictions still apply.
4. Attach the complete version and sources. Paste the prompt, fill its fields, and explicitly request primary-source research where permitted.
5. If using Deep research, the documented web route is **+ → Deep research**. On desktop, open **Plugins → Deep research**, enable it if necessary, and use **Try now**. A research tool and a reasoning setting serve different purposes.

GPT 6.1 Sol is documented for **Work and Codex**, rather than ordinary Chat. Max devotes more time to one model's task; Ultra can use subagents. Require a reconciled assessment of the whole document after any delegated checks. The API's reasoning settings differ: `max` is supported for GPT 6.1 Sol, while the consumer UI's `Ultra` is not an API effort value.

Sources: [model controls and availability](https://learn.chatgpt.com/docs/models), [files and tasks](https://learn.chatgpt.com/docs/use-chatgpt), [web search and Deep research](https://learn.chatgpt.com/docs/web-search), [GPT 6.1 Sol API settings](https://developers.openai.com/api/docs/models/gpt-6.1-sol).

## Claude

1. Start a fresh chat or dedicated review project with the context controls selected deliberately.
2. Click the **model name beside the send button**. Select **Claude Fable 5.1** or **Claude Opus 5.5**, where available; use **More models** if necessary.
3. In the same menu, choose **Effort → Max** where available. Both models have thinking enabled. Max effort is distinct from a Max subscription. Opus 5.5 is offered on paid plans; Fable 5.1 can require usage credits on Pro or standard Team seats.
4. Use **+ → Add files or photos → select file → Open**, or drag the files into the composer.
5. Paste the prompt. Explicitly ask Claude to **search the web** for primary-source verification. The new experience searches automatically when appropriate; the older interface offers **+ → Web search**. Inspect original linked sources yourself.

Chat uploads currently allow 20 files, up to 500 MB each; project files have a 30 MB limit. PDFs can have up to 1,000 pages, subject to extraction and token limits. PDFs of 101–1,000 pages are processed as text rather than visually. Provide important figures separately and inspect the rendered original yourself.

An uploaded book or a one-million-token context does not establish that every page was read. Projects may retrieve selected portions of their files. Check the coverage report against identifiable locations and relevant sources. If a displayed fallback changes the model, record the model that actually answered.

Sources: [model and effort controls](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings), [Fable plan limits](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan), [Opus availability](https://www.anthropic.com/claude/opus), [file uploads](https://support.claude.com/en/articles/8241126-upload-files-to-claude), [paid context windows](https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans), [project retrieval](https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects), [web search](https://support.claude.com/en/articles/10684626-enable-and-use-web-search).

## GLM-5.3 through OpenRouter

OpenRouter lists **Z.ai: GLM 5.3**, API identifier `z-ai/glm-5.3`. It supports reasoning effort `low`, `high`, and `max`; reasoning is always enabled and `max` is the default. This documented API fragment is not a complete request:

```json
{
  "model": "z-ai/glm-5.3",
  "reasoning": { "effort": "max" }
}
```

Supply the document and review prompt in the request separately. OpenRouter Chat also accepts PDFs, but its authenticated model and parameter controls were not observed for this guide; no exact menu labels are asserted here.

GLM-5.3 is text-only. A PDF may be parsed into text, and images are not passed to this model as visual input. A reliable Markdown or text export can support prose review; inspect figures and PDF layout separately. Check the selected endpoint's limits. A larger output cap is not the same as greater reasoning effort, and reasoning can consume part of the output budget.

Sources: [OpenRouter model page](https://openrouter.ai/z-ai/glm-5.3), [Z.ai model documentation](https://docs.z.ai/guides/llm/glm-5.3), [OpenRouter reasoning](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens), [PDF handling](https://openrouter.ai/docs/guides/overview/multimodal/pdfs).

## Check the result before revising

- Require a coverage record before an overall verdict. Batches may be necessary; keep open issues and reconcile them after all sections are read. Check self-reported coverage rather than treating it as proof.
- Retain a claim ledger for factual assertions, a separate assessment of the argument, and actual calculation results. Distinguish unverified claims from demonstrated errors.
- Open consequential sources and reproduce important arithmetic. Assess a criticism by its evidence or specific reasoning, not its confidence.
- Record accepted corrections, rejected suggestions with reasons, and unresolved checks. Review changed passages and dependent summaries after revision.
- If no substantive fault was found, retain that finding with the version and coverage limits. Do not ask for more faults until the reviewer invents them.

This is an original workflow proposed for the book. It is not an experimentally validated cure for sycophancy. See the [source index](../SOURCES.md) for research on shared model errors and framing-dependent feedback.
