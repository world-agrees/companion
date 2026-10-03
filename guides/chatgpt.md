# ChatGPT: choose the context before asking for advice

Documentation checked **October 2, 2026**. These are consumer ChatGPT web controls, not local Codex memory commands. Availability varies with your account, region, workspace, and version. This guide does not change your settings; choose the scope that fits the task.

## 1. Read and correct the visible memory

Open **Settings → Personalization → Memory**. Inspect the available summary or saved items; use the displayed correction controls. A response's **Sources** can identify relevant personal material, but neither view exposes all inputs. Remove a saved error and address its original chats or other surviving sources separately. [Official memory instructions](https://help.openai.com/en/articles/8590148-memory-in-chatgpt)

Verification: write down one specific correction and inspect its stored wording. “The client accepted subject to a revised date” should retain that condition. The assistant saying “fixed” is not the verification.

## 2. Run a fresh comparison

Open a new chat. Select **Temporary**, then **Unpersonalized**, before sending anything. This excludes ordinary memory, custom instructions, and plugins. Both temporary modes avoid new memories; a personalized one can still read existing context. Saving converts it to a regular chat. Limited safety context and possible retention remain. [Official temporary-chat instructions](https://help.openai.com/en/articles/8914046-temporary-chat-in-chatgpt)

Verification: confirm the chosen mode before submitting the evidence. If the interface offers different choices, check its current instructions instead of assuming that “temporary” means no personalization.

## 3. Bound an ongoing project

Open the project, choose **••• → Project settings**, select **Project-only memory**, and save. Allow for the documented delay of several hours. Project chats and files remain usable within the project; a list of individual project memories is not exposed. [Official project instructions](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)

Verification: reopen the settings. Review the project's actual evidence and instructions, including old summaries that repeat a conclusion you corrected. A project boundary does not make its contents accurate.

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
