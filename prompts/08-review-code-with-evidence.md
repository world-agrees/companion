# Review code with evidence

Use in a repository or environment the coding assistant is authorized to inspect. Supply requirements, affected paths, and commands the project actually uses. Do not supply secrets. A prompt cannot enforce sandbox, access, or memory boundaries.

## Copy and adapt

```text
Change or task: [description]
Requirements: [source or issue identifiers]
Affected paths: [paths]
Permitted checks: [commands and environment]

Review the code against the requirements. For each finding,
identify the file and location, the concrete failure condition,
and evidence of the impact. Distinguish observed defects
from speculative concerns. Do not invent issues to appear
critical and do not treat my confidence as a passing test.

Inspect relevant repository instructions and dependencies.
Use meaningful checks where permitted. Report exact commands,
exit status, and relevant results. Clearly mark checks that
were proposed, blocked, unavailable, or not run.

Check whether the tests exercise the requirement and a material
failure case; a test matching the implementation alone is not
sufficient. Summarize unresolved risks and evidence needed.
Do not claim the code passed checks that were not executed.
Do not deploy, publish, commit, or send messages unless
separately authorized for this task.
```

## Check the result

Read consequential code and test output. Confirm the checked version corresponds to the version you intend to use. A passing test does not establish correctness outside the cases it exercises. Stored repository guidance should never claim an unexecuted check has already passed.
