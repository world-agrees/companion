# Build an evidence workspace before asking for a proposal

Use this recipe for a project proposal, a consequential email, or another document that someone will use to make a decision. It separates the records, the investigation, and the writing. It also gives you places to check the work before an assistant turns a tentative finding into a confident recommendation.

The [staged prompts](../prompts/14-evidence-workflow.md) follow the same arrangement. Run one stage at a time. These instructions organize the work; they do not guarantee that the model will find every error or resist every preference.

## 1. Create an actual project folder

Choose a location your organization permits you to use. Create the empty folders first:

```text
project-proposal/
  project-instructions.md
  desired-outcome.md
  prompts/
    [selected, versioned stage procedures]
  evidence/
    source-manifest.md
    Exhibit-A-boss-email.eml
    Exhibit-B-project-budget.xlsx
    Exhibit-C-supplier-estimate.docx
  analysis/
    01-input-inventory.md
    02-cost-and-risk-analysis.md
    03-funder-questions.md
    04-checked-findings.md
  output/
    proposal-draft.md
```

The exhibits are examples of recognizable filenames. Supply your actual records; do not create documents claiming to contain evidence you do not have. The analysis and draft filenames show where results will go when those steps are performed. A Markdown file is a plain-text document; another editable format can serve the same purpose.

For shared work, adapt the [document-project instructions template](../templates/document-project-instructions.md) as **project-instructions.md**. Keep approved stage procedures in **prompts/**, recording each selected procedure's version, owner, inputs, and required outputs. Supply the current procedure explicitly in attachments, a paste, or supported project instructions. This folder does not make Markdown files load automatically or enforce access permissions.

Save original emails, their attachments, spreadsheets, requirements, estimates, test results, and relevant correspondence in **evidence/**. Include records that could challenge the proposal. Preserve the email's sender, date, and attachments. Preserve the spreadsheet's formulas and sheets. If you need an export, cleaned copy, transcript, or summary, put that derivative in **analysis/** and identify the original it came from.

If an original email format is unsupported, supply a readable TXT or PDF derivative with the original exhibit ID, sender, and source date. Keep its attachments separately identified. For a spreadsheet, use tooling capable of inspecting the relevant sheets and formulas where available. If you must supply exports, check them against the original and record which sheets, values, formulas, or formatting they omit. A readable export does not establish that the whole workbook was inspected.

Use the [source manifest template](../templates/source-manifest.md) to record each exhibit's identifier, filename, sender or author, source date, version, relevant pages or rows, and limitations. Record when you obtained the file if its source date is unknown. Connect attachments to their parent email. Mark superseded records and identify the version governing the task. An email approving one purchase is not approval of every item in a project budget, even if its subject says “Approved.”

Keep the originals intact. Retain a new dated version when a source changes rather than silently replacing the evidence behind an earlier analysis. Treat a model's summary as a generated result, not a replacement for the source. Prepare the manifest before the analysis, then retain the version used for that run.

## 2. Give the tool a real route to the records

Typing a folder path into a consumer chat does not grant access to your computer. In an attachments-based workflow, upload the selected exhibits and manifest. Check which items were attached and readable. If the assistant cannot write files, save its returned inventory and analysis yourself. Upload revised sources deliberately; do not assume a chat attachment updates when your local file changes.

If your tool supports explicitly connected local folders, inspect the access it actually grants. Connect the approved evidence and working folders needed for the current stage, rather than granting access to the entire parent directory. Where supported, enforce read-only access to **evidence/** and allow writes only to **analysis/** and **output/**. A prompt saying “do not modify the evidence” is useful, but it is not a filesystem permission or sandbox. Folder names are not access controls either.

Anthropic has announced that new Pro and Max Cowork tasks run in the cloud from **October 6, 2026**. Connected local folders still require the desktop app to be open; existing local tasks remain local. Local-file access and local execution are different properties. [Current Cowork documentation](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile).

Check the account, project instructions, memory, and connected sources before supplying workplace records. Chapter 8's context controls still matter. This folder arrangement does not establish isolation from unrelated conversations or services. The [context manifest](../templates/context-manifest.md) provides a place to record the settings and inputs you could inspect, the actual access controls, and what remains unknown. An assistant cannot promise a complete inventory of hidden inputs it cannot inspect.

## 3. Write the goal and the criteria separately from the findings

Create **desired-outcome.md** with a short setup such as:

```text
Prepared: [date and version]
Audience: [recipient or role]
Decision: [what the recipient needs to decide]
Decision authority: [known authority, or not established]
Hoped-for outcome: [my preference, explicitly labeled]

Requirements: [requirements with their source IDs and locations]
Evaluation criteria: [cost, capacity, timing, compatibility, etc.]
Priorities and trade-offs: [who set them and when]
Unknowns: [missing requirements, figures, authority, or constraints]
Additional research permitted: [scope, or none]
```

“I want the director to approve this project” is a preference. “The project meets the approved budget” is a factual claim that needs evidence and arithmetic. Preferences can legitimately determine priorities: a buyer may choose reliability over the lowest price. They cannot establish a product's reliability or change its price.

During the inventory, assessment, and funder-question stages, withhold **desired-outcome.md**. Supply the audience, decision question, requirements, and evaluation criteria separately, without your preferred verdict. Saying “My preference for approval is not evidence” still tells the reviewer you want approval. Let the first assessment begin without that cue.

For a local tool, exclude the goal file from the permitted reads where controls support that restriction. Read-only access still allows its contents to influence the assessment. If the tool cannot restrict access to that file, connect only the approved subfolders or use a separate review workspace containing the selected exhibits and neutral setup. An instruction not to read the goal file is not proof that it is inaccessible.

Ask which questions would help the recipient decide, including questions that might lead to a smaller project, a delay, or a refusal. Do not instruct the model to make approval look inevitable. If a requirement or criterion is missing, identify who needs to supply it rather than letting the assistant invent one.

## 4. Inventory the inputs before drawing conclusions

Run **Stage 1** in the prompt file. Ask for the files actually inspected, their dates and versions, and the coverage of pages, sheets, formulas, attachments, or other relevant material. List unreadable sections, missing attachments, conflicting figures, and requirements found only in a summary. Save the result as **analysis/01-input-inventory.md**.

Compare that result with your directory and source manifest. Open important locations yourself. A file appearing in the inventory does not prove that every sheet or attachment was read. A tool reporting access is not proof of full extraction. Resolve gaps that block a material finding; keep unresolved gaps visible in any analysis that proceeds.

## 5. Ask for analysis and questions, then inspect both

Run **Stage 2** for the assessment. Each material finding should identify the exhibit and precise location supporting it. Separate source statements, calculations, estimates, assumptions, and interpretations. Include contrary evidence and feasible alternatives under the same criteria. Do not require a criticism quota: a sound finding should remain sound.

For calculations, require source values, units, periods, exclusions, formulas, and rounding. Ask the assistant to distinguish calculations it actually executed from arithmetic it merely proposed. Save code or calculation work in **analysis/** where supported. Independently reproduce arithmetic that could change the decision.

Run **Stage 3** to produce **analysis/03-funder-questions.md**. This is a list for your review, not permission to contact the funder. Questions should explain what must be resolved, which exhibit or missing record is involved, and why the answer matters. They should cover cost, timing, dependencies, risks, obligations, and decision authority where relevant. The model should not impersonate the funder or guess that person's preferences. Add a new dated exhibit for any revised original or new answer rather than changing the earlier record.

Now open the intermediate results. Follow consequential claims back to the original exhibits. Check omitted costs, conflicting versions, unsupported approvals, and assumptions that could change the recommendation. Ask a responsible person to resolve requirements or authority questions the evidence cannot settle.

Use **Stage 4** to prepare a record of your checks. Save **analysis/04-checked-findings.md** only after you have reviewed it. Record what was verified, corrected, rejected, or left unresolved, with dates and source versions. A filename containing “checked” is not proof of verification. Your acceptance of this analysis is also not approval to fund the project, bind a colleague, or send a document.

## 6. Draft from the findings you have checked

Run **Stage 5** after the human checkpoint. Supply the checked findings and the source versions they cite. Now supply **desired-outcome.md** to explain the writing's purpose and intended audience, with any preferred outcome still labeled as a preference. It must not override the checked findings. Ask for a draft that preserves material conditions, uncertainties, contrary evidence, and unresolved questions. An estimate must remain an estimate; a request for approval must not become an approval already granted.

If drafting reveals a new material claim or issue, return it to **analysis/** for checking. Do not let the assistant fill the gap just to finish the document. For attachments-based chats, supply the checked analysis explicitly rather than assuming a new chat can see it.

Run **Stage 6** to compare the draft with the checked findings and exhibits. Use the [commitment comparison prompt](../prompts/04-preserve-commitments.md) for a rewrite of an existing message. Check who would be committed to what, by when, under which conditions, and with whose authority. Read the final draft yourself.

Keep the result in **output/** as a draft until the appropriate person approves its use. This workflow does not send, publish, approve expenditure, or authorize work. Retain the source manifest, analysis versions, and review record with the draft so a later correction can be traced to the findings it affects.
