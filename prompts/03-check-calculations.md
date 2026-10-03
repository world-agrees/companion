# Check calculations

Supply raw values or tables with source identifiers, units, periods, and any conventions needed. Ask for executable calculations only where the assistant has an appropriate tool. Reproduce important totals outside the model's prose.

## Copy and adapt

```text
Question: [financial, statistical, scheduling, or other calculation]
Inputs: [sources and values]
Units and periods: [definitions]
Calculation tools permitted: [tools or none]

Identify the required inputs before calculating. Mark missing
values as missing; do not silently fill them in.

For each result, show the source identifier for every input,
the units, the formula, and any assumption. Separate one-time
and recurring values. Preserve uncertainty and relevant ranges.

Use an appropriate available calculation tool when permitted.
Report what was actually executed and its output. If no tool
was used, label the calculation unexecuted; do not invent a log.

Check unit consistency, totals, rounding, and omitted costs.
Explain which finding affects the recommendation and which
values I should independently verify.
```

## Check the result

Check that the executed code or spreadsheet used the supplied data. Verify the formula and assumptions before checking the arithmetic alone. A correct calculation of the wrong period can produce the wrong decision.

## Small example with known arithmetic

Inputs: current annual cost $48,000; proposed annual cost $36,000; proposed first-year implementation cost $15,000; no other changes assumed. Recurring saving: $12,000. First-year proposed total: $51,000, or $3,000 more than current spending. This is a fictional calculation specimen, not a measured model result.
