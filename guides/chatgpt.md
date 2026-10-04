# ChatGPT: choose the context before asking for advice

Documentation checked **October 3, 2026**. These are consumer ChatGPT web controls, not local Codex memory commands. Availability varies with your account, region, workspace, and version. This guide does not change your settings; choose the scope that fits the task.

## 1. Read and correct the visible memory

Open **Settings → Personalization → Memory**. Inspect the available summary or saved items; use the displayed correction controls. A response's **Sources** can identify relevant personal material, but neither view exposes all inputs. Remove a saved error and address its original chats or other surviving sources separately. [Official memory instructions](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)

Review **Memory** or the separate **Reference saved memories** and **Reference chat history** switches. Turning memory off leaves chats in place. **Delete and turn off memory**, where available, clears remembered information and disables it without deleting chats. Remaining chats can inform memory again if enabled later.

To delete a source chat, use its **••• → Delete** menu. For bulk deletion, open **Settings → Data controls → Delete all chats** and review the confirmation. Archived chats are retained and searchable. [History controls](https://help.openai.com/en/articles/8809935-deleting-and-archiving-chats-in-chatgpt).

In Healthcare and Regulated Workspaces, **improved memory** is disabled by default and is not covered by the BAA. Do not enter protected health information when using that feature. Project-only memory does not change its BAA coverage. Follow the approved feature-level configuration. [Official memory guidance](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)

Verification: write down one specific correction and inspect its stored wording. “The client accepted subject to a revised date” should retain that condition. The assistant saying “fixed” is not the verification.

## 2. Run a fresh comparison

Open a new chat. Select **Temporary**, then **Unpersonalized**, before sending anything. This excludes ordinary memory, custom instructions, and plugins. Both temporary modes avoid new memories; a personalized one can still read existing context. Saving converts it to a regular chat. Limited safety context and possible retention remain. [Official temporary-chat instructions](https://help.openai.com/en/articles/8914046-temporary-chat-in-chatgpt)

Verification: confirm the chosen mode before submitting the evidence. If the interface offers different choices, check its current instructions instead of assuming that “temporary” means no personalization.

## 3. Bound an ongoing project

1. Click **New project** in the sidebar and give it a purpose-specific name.
2. Open **••• → Project settings → Memory → Project-only memory → Save**, or select the mode during creation. Allow the documented delay of several hours.
3. Add only the relevant task records and source documents.
4. Add evidence and criteria instructions in **Project settings**; start a new project chat.

Project-only mode excludes saved personal memories and chats outside the project. Project chats can reference one another. Default mode differs by plan, and required account/workspace memory settings must be enabled. Reopen the settings to verify the selection. A project boundary does not make its contents accurate or prevent importing outside material. [Official project instructions](https://help.openai.com/en/articles/10169521-projects-in-chatgpt).

Project-only memory applies to Chat: ChatGPT Work is unavailable in that project. For a Work task, start a separate task and review its selected environment, attached folders, enabled plugins, and source permissions. These controls organize accessible material; they do not establish the same memory boundary. [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), [Work project sources](https://learn.chatgpt.com/docs/projects), [Work capabilities](https://learn.chatgpt.com/docs/use-chatgpt).

Separate hardware helps with local files and logins, but two devices using the same cloud account can share history. Separate work and personal accounts or providers, then use bounded projects within each. Inspect connected sources: an imported document or shared mailbox can bridge those contexts.

## 4. Review the other context sources

- **Standing instructions:** open **Settings → Personalization → Custom Instructions**. Edit the guidance or disable customization. A permanent instruction to defend your strategy can contaminate a request to assess it. [Custom instructions](https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions)
- **Files:** open Library, select an obsolete saved file, and use its deletion control. Chat removal alone does not remove Library files. [Library controls](https://help.openai.com/en/articles/20001052-using-library-to-manage-files-in-chatgpt)
- **Connected services:** open **Settings → Plugins**, select the app, and inspect its connected account or connection menu. Disconnect access you do not want. Other accounts or administrator-managed connections can remain; this does not erase material already copied into chats or memory. [App-account controls](https://help.openai.com/en/articles/20001494-connecting-and-managing-app-accounts-in-chatgpt)
- **Training choice:** open **Settings → Data controls** and turn off **Improve the model for everyone** if that is your preference. This does not remove history or disable memory. Voluntary feedback can have a separate training exception. [Data controls](https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt)

## 5. Ask for a check you can reproduce

Use the downloadable [scheduling example](../examples/scheduling/README.md), which includes the two input files and a calculation check. Supply the dated evidence, then use a request such as:

> Assess whether the Friday deadline is credible for one person doing the remaining tasks in sequence. Use task-list.csv and availability.txt. Show estimated work, available hours, and the difference. Cite the rows supporting the numbers. Separate estimates from measured facts. Identify missing dependencies. Do not treat my preference for Friday as evidence that the work fits. If additional sources are needed, identify them before using them.

For tasks estimated at 8, 7, and 5 hours, with 14 hours available, the arithmetic is **20 − 14 = 6 hours short**. Check that yourself. A recommendation that still promises Friday should explain a changed assumption rather than merely reassure you.

## 6. Check what changed after pushback

> Compare the previous recommendation with the revision. Name the new evidence supporting each changed factual claim. If no evidence changed, reassess against the original criteria and preserve supported warnings. Do not invent objections to appear critical.

Do not count changed tone as corrected reasoning. Follow the source, reproduce the relevant calculation, and check the condition that would change your decision. A prompt is an instruction; it is not a service-level access restriction or a guarantee against sycophancy.

## Keep a small context record

Save your own copy of the task, dated sources, selected mode, inspected memory corrections, output, and checks. Note what you could not inspect. A citation supports a claim only if its source actually establishes it; it is not a complete log of the model's input.

## 7. Tone and a weekly review

On the web, open **profile icon → Personalization → Base style and tone**. Under **Characteristics**, adjust warmth and enthusiasm if helpful. Style settings do not verify evidence or remove memory. [Personality](https://help.openai.com/en/articles/11899719-customizing-your-chatgpt-personality), [Characteristics](https://help.openai.com/en/articles/20001038-characteristics-in-chatgpt).

Use [prompt discipline](../prompts/11-prompt-discipline.md) for neutral questions and inspectable assessments. On Friday, use [weekly memory review](../prompts/12-weekly-memory-review.md) to propose corrections, inspect the actual controls, and prepare a dated Monday brief. The companion's weekly-context-review skill procedure can be copied into a ChatGPT request or project instructions; this reuses text rather than installing a Claude skill. Do not infer that a fluent “forgotten” message deleted a record.
