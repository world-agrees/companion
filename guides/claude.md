# Claude: manage memory, history, projects, and repeatable reviews

Official documentation checked **October 3, 2026**. These are researched directions for Claude's consumer web interface, not a live account test. Plans, organization policies, and app versions affect availability. Claude Code has additional local files and settings.

## 1. Inspect and pause memory

1. Open **Settings → Memory → Topics**.
2. Select a topic. Use its edit icon to correct it, or **Delete** to remove it.
3. Review **Search and reference chats** separately; turn it off to stop past-chat search.
4. To stop reading and creating memory, turn off **Generate memory from chats** and choose **Pause memory**. Pause preserves existing entries. **Reset memory** permanently deletes the memory collection, including project memories.

Deleting a chat leaves its saved topic memories, so review both. Accounts still using **Settings → Capabilities → View and edit memory** have the legacy summary experience and different deletion behavior. Follow the matching section of the [official memory guide](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context).

Verification: inspect the edited entry. A request to forget something is less useful than checking what was actually changed.

Memory is unavailable to organizations with HIPAA, public-sector, or custom data-retention agreements. Check your organization’s approved configuration before following these consumer directions. [Official memory availability](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context)

## 2. Choose between incognito and a retained chat with memory off

For an assessment without existing memory or a future history entry:

1. Start a new chat **outside a project**.
2. Click the ghost icon at the upper right.
3. Confirm the **Incognito chat** label and black border before writing.
4. Save any output you need before closing the chat; it cannot be reopened.

Incognito does not use existing memory, contribute new memory, or enter searchable chat history. Profile instructions and custom styles can still apply. Retention is normally 30 days; Team and Enterprise exports and organizational policies still apply. The new Claude experience opens incognito in the previous chat interface, which cannot create files or run code. [Incognito instructions](https://support.claude.com/en/articles/12260368-use-incognito-chats).

To keep a chat while limiting prior context, start a new chat, click **+** in the message box, and turn **Memory** off **before the first message**. This skips memory and past-chat search for that chat. It also works within a project. The retained conversation can still be found by other chats later. [Per-chat memory controls](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context).

These modes limit particular context sources; they do not remove material you paste into the conversation or establish that an answer is objective.

## 3. Remove an unwanted chat from history

On the web, open **Chats and tasks**, find the chat, hover over it, click **⋮ → Delete**, and confirm. For several chats, use **⋮ → Select**, check the intended conversations, then **Delete** and confirm. Keep an authoritative record elsewhere if it needs to survive. [Delete or rename a conversation](https://support.claude.com/en/articles/8230524-delete-or-rename-a-conversation).

In the current Topics memory experience, deleting history does not remove related saved memories. Inspect Topics separately after deleting the source chat.

## 4. Create separate projects for separate purposes

1. Open **Projects** in the left sidebar, or visit [claude.ai/projects](https://claude.ai/projects).
2. Click **+ New Project**. Give it a name and description.
3. On Team or Enterprise, choose the appropriate visibility; keep it private if it should be limited to you and invited members.
4. In the project's knowledge area on the right, click **+** and upload the relevant documents.
5. Click **Set project instructions**, add the task's criteria and source requirements, and click **Save instructions**.
6. Start the conversation inside that project.

Projects are available on free accounts, with a five-project limit. A project name and description do not themselves become Claude's working evidence. [Create and manage projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects).

The memory guide documents a separate memory space and summary for each project; past-chat searches inside a project are limited to that project. Conversations within the same project can therefore influence later work. Account-wide instructions, enabled skills, and deliberately supplied sources remain additional layers. A project is useful separation, not a replacement for separate work and personal accounts or an organization's access rules. [Memory boundaries](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context).

## 5. Review tone and standing instructions

Click your initials at the lower left, open **Settings**, and review **Instructions for Claude**. These instructions apply across conversations. Project instructions apply within their project. Current documentation also directs tone and format customization to **Skills**. [Personalization features](https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features).

Try an instruction such as:

> Use direct language. Do not congratulate me for an idea unless the evidence supports a specific reason. Judge proposals against the stated criteria. Distinguish facts, interpretations, and missing evidence. Do not invent objections to sound independent.

Tone is a presentation choice. A blunt answer can still repeat an unsupported conclusion; a courteous answer can disagree for good reasons. Evaluate the evidence and calculations rather than the warmth of the response.

## 6. Install a review skill

Claude's consumer chat supports uploaded skills; a simple skill can be Markdown instructions without executable scripts.

1. For an individual account, open **Settings → Capabilities** and enable **Code execution and file creation**. Organization policies may control this at work.
2. Open **Customize → Skills**.
3. Click **+ → + Create skill → Upload a skill**.
4. Upload the ZIP containing the skill folder and its Markdown instructions, then enable the skill.
5. Ask explicitly to use it for the intended review, and inspect the resulting work.

Use the companion skills for evidence review, memory correction, and preference checks. Skills describe a procedure; they do not gain automatic access to settings or guarantee that a memory was deleted. [Use skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude), [create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).

Claude Code can instead load a project skill at `.claude/skills/<name>/SKILL.md`. Personal skills under `~/.claude/skills/` apply across local projects. These are distinct installation scopes. [Claude Code skills](https://code.claude.com/docs/en/skills).

## 7. Make Friday's review concrete

Bring the available memory entries, relevant source documents, and a list of this week's corrected conclusions. Ask the review procedure to propose what to retain, correct, date, or delete. If you vented on Wednesday, identify which statements described that day and which still describe your view on Friday.

Inspect the affected topics, originating chats, and project documents yourself. Start a new assessment using the checked evidence and selected memory mode. A corrected answer does not establish that every stored source has been corrected.

For ChatGPT, the same procedure can be copied into a prompt or an appropriate project's instructions. Attach any reference template used by the skill, or use the self-contained weekly review prompt. That uses the text as instructions; it does not install a Claude skill or confer access to ChatGPT's memory controls.
