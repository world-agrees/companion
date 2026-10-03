# Primary sources and documentation

Checked **October 2, 2026**. The product guides link the page supporting each instruction. This index is a route back to those sources and the research behind Part III, not a claim that a particular prompt or implementation eliminates sycophancy.

## Consumer products

**ChatGPT:** [Memory](https://help.openai.com/en/articles/8590148-memory-in-chatgpt), [Temporary chat](https://help.openai.com/en/articles/8914046-temporary-chat-in-chatgpt), [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), [Custom instructions](https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions), [App accounts](https://help.openai.com/en/articles/20001494-connecting-and-managing-app-accounts-in-chatgpt), [Library](https://help.openai.com/en/articles/20001052-using-library-to-manage-files-in-chatgpt), [Data controls](https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt).

**Claude:** [Search and memory](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context), [Incognito chats](https://support.claude.com/en/articles/12260368-use-incognito-chats), [Personalization](https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features), [Projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects).

**Microsoft Copilot:** [Current consumer controls](https://support.microsoft.com/en-us/privacy/microsoft-copilot/privacy-controls), [Legacy-version notice](https://support.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-privacy-controls), [Conversation history](https://support.microsoft.com/en-us/microsoft-copilot/conversation-history-in-microsoft-copilot). **Microsoft 365 Copilot:** [Saved memory](https://support.microsoft.com/en-us/microsoft-365-copilot/manage-copilot-memory-in-microsoft-365-copilot), [Personalization and temporary chat](https://support.microsoft.com/en-us/microsoft-365-copilot/personalize-what-microsoft-365-copilot-remembers), [History inferences](https://support.microsoft.com/en-us/microsoft-365-copilot/how-microsoft-365-copilot-chat-history-works), [Work-data grounding](https://support.microsoft.com/en-us/microsoft-365-copilot/what-information-does-copilot-use-to-answer-my-prompt).

## Coding assistants and agents

**Claude Code:** [Memory and CLAUDE.md](https://code.claude.com/docs/en/memory), [Permissions](https://code.claude.com/docs/en/permissions), [Interactive commands](https://code.claude.com/docs/en/interactive-mode), [Best practices](https://code.claude.com/docs/en/best-practices).

**Codex:** [Memories](https://learn.chatgpt.com/docs/customization/memories), [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Skills](https://learn.chatgpt.com/docs/build-skills), [MCP](https://learn.chatgpt.com/docs/extend/mcp).

**GitHub Copilot:** [Memory overview](https://docs.github.com/en/copilot/concepts/agents/copilot-memory), [Personal memory controls](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/copilot-memory/manage-for-yourself), [CLI context management](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/context-management), [Repository instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions).

**Hermes:** [Persistent memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/), [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles). **OpenClaw:** [Memory CLI](https://docs.openclaw.ai/cli/memory), [Dreaming](https://docs.openclaw.ai/concepts/dreaming), [Memory architecture](https://docs.openclaw.ai/concepts/memory).

**Anthropic developer documentation:** [Context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool), [Agent evaluations](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

**MCP teaching example:** June 18, 2025 specification for [stdio transport](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports), [lifecycle](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle), and [tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools). The example implements a tested subset, not a full SDK.

## Research and institutional practice

- Zana Buçinca, Maja Barbara Malaya, and Krzysztof Z. Gajos, [“To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-assisted Decision-making”](https://arxiv.org/abs/2102.09692) (2021).
- Michael Henry Tessler, Michiel A. Bakker, and colleagues, [“AI Can Help Humans Find Common Ground in Democratic Deliberation”](https://deepmind.google/research/publications/65220/) (2024).
- Di Wu and colleagues, [“LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory”](https://arxiv.org/abs/2410.10813) (ICLR 2025).
- Hakeem Hannoon and colleagues, [“Mitigating Over-Personalization in LLMs via Structured Memory”](https://arxiv.org/html/2608.08300v1) (August 2026 preprint).
- Zhishang Xiang and colleagues, [“MemSyco-Bench: Benchmarking Sycophancy in Agent Memory”](https://arxiv.org/abs/2607.01071) (July 2026 preprint).
- NIST, [*Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*](https://doi.org/10.6028/NIST.AI.600-1) (July 2024), voluntary guidance.
- Columbia Accident Investigation Board, [*Report*, Volume I](https://www.nasa.gov/wp-content/uploads/static/history/columbia/reports/CAIBreportv1.pdf) (August 2003), including the warning discussed on printed page 157.
- Center for Open Science, [Registered Reports](https://www.cos.io/initiatives/registered-reports).
- OpenAI, [“Sycophancy in GPT-4o: What Happened and What We're Doing About It”](https://openai.com/index/sycophancy-in-gpt-4o/) (April 29, 2025), and [“Expanding on What We Missed with Sycophancy”](https://openai.com/index/expanding-on-sycophancy/) (May 2, 2025).

These sources have different purposes: product instructions, proposed architectures, experiments, benchmarks, incident records, and institutional guidance. Read the corresponding chapter notes for limitations. The book's prompts, records, code, and supplier tests are proposed practices; they are not interventions validated by these papers.
