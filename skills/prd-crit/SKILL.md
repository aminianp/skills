---
name: prd-crit
description: Reviewing a PRD draft, section, or rough notes with evidence-based critique. Classify claims, identify gaps, and surface inconsistencies without rewriting the document. Use this when user requests a review of the PRD, or they want to pressure test a section — a problem statement, a JTBD section, success metrics, or a full draft. Trigger even on rough notes or a single paragraph if the user wants structured feedback before writing it up. If the user shares anything that looks like product requirements, a problem statement, or user research and wants feedback, use this skill.
metadata:
  tags:
    - "product skills"
    - "prd"
    - "critique"
    - "review"
    - "product requirements"
    - "problem statement"
    - "JTBDs"
    - "success metrics"

---

# PRD Critique
There are a few aspects in an agentic PRD review:

1. **Co-Authoring:** Suggest writing that helps the user flesh out their ideas when they share rough notes and explicitly ask for help writing. This is a more collaborative process where you can propose specific language to help them get unstuck. Do not rewrite the document if they share a draft or ask for critique — instead, provide feedback on the content as-is, and only suggest specific language when they explicitly ask for help writing. If the context or intent is unclear, ask clarifying questions before suggesting language to ensure your suggestions are relevant and helpful.
2. **Claim Classification**: Identify major claims and assumptions, and classify them as `Data-backed`, `Anecdotal`, or `Hypothesis`. For non-data-backed claims, ask for evidence or propose experiments.
3. **Writing Clarity**: Flag language that is vague or overly verbose. Where possible, suggest ways to simplify the writing.
4. **Polish**: Identify any typos, grammatical errors, or formatting issues.
5. **Cross-Section Consistency**: Check for contradictions or disconnects between different sections of the PRD (e.g., problem statement vs. proposed solution, JTBDs vs. success metrics, etc.)

Keep findings specific to the content provided. Avoid generic PM advice that would apply to any PRD.

## Input
Accept any of the following in a Notion page, a Google Doc, or a markdown file:

- A full PRD
- A specific section (problem statement, JTBDs, success metrics, etc.)
- Rough notes to be pressure-tested before writing them up

If it's unclear what needs critiquing, ask: "Which section or claim do you most want challenged?"

## Claim Classification
Start by finding claims and assumptions in the content. A claim is any statement that asserts something to be true. For example, "Users are confused by the current onboarding flow" is a claim. "We should redesign the onboarding flow" is an assumption (that redesigning will solve the problem). Both need evidence to be validated. For every major claim or assumption, classify it as:
- `Data-backed` — supported by research, metrics, or cited evidence
- `Anecdotal` — based on qualitative signal without systematic validation
- `Hypothesis` — assumed true but untested

 Look for use of adjectives and adverbs, as they often signal claims (e.g., "severe problem", "frequent issue", "intuitive design"). Also look for statements that imply causality or correlation (e.g., "because of X, Y happens"). For `Anecdotal` or `Hypothesis` claims: ask for supporting evidence or propose a specific, measurable experiment to resolve the uncertainty.

## Section-Specific Checks

### Problem Statement
- Is vague language used where specificity is required? (e.g., "users struggle with X" with no indication of frequency or scope — flag it)
- Are claims classified per the Claim Classification section above?
- Is there a clear link between the problem and the persona who experiences it?

### Personas & JTBDs
- Are JTBDs worded as outcomes the user wants, not solutions or features? (Bad: "User wants to click a button to export" / Good: "User wants their data in a format their finance team can use")
- Are personas described specifically enough to be distinguishable from one another?
- Is JTBD prioritization stated? If multiple JTBDs are listed with no priority signal, flag it.

### Product Proposal & Goals
- Are non-goals explicitly stated? Flag their absence — unstated non-goals are a primary source of scope creep.
- Do stated goals use measurable language, or vague qualifiers like "improve", "enhance", "better"? Flag the latter.
- Is there a stated MVP or phasing? If not, flag it.

### Success Metrics
- Does each metric have a concrete measurement methodology, not just a label? ("Engagement" is not a metric; "7-day retention rate among activated users" is)
- Does each metric trace back to a specific JTBD or goal? Flag orphaned metrics.
- Are both leading indicators (early signals) and lagging indicators (outcome confirmation) present?

### Cross-Section Consistency
- Do the JTBDs attributed to each persona actually match how that persona is described?
- Do success metrics measure the stated goals, or just activity that's easy to track?
- Does the product proposal address the stated problem, or an adjacent one?
- Do non-goals contradict anything stated in the product proposal or user journeys?
- Are the same terms used consistently throughout? (e.g., if the persona is "recruiter" in one section and "hiring manager" in another, flag it)

## Final Checks
Every time you are invoked, read through the entire content at least once and catch any issues as described in the PRD Critique sections above. Comment on the doc if you see these issues.

## Output Format
Once you're done with the review, always return a verdict in chat + a summary of your findings:

1. **Verdict** — `Proceed` / `Proceed with Conditions` / `Needs Rework`
2. **Critical issues** — things that would cause the PRD to fail a review or produce the wrong product
3. **Gaps** — missing sections, unstated assumptions, or claims needing evidence
4. **Cross-section inconsistencies** — places where sections contradict or fail to connect
5. **Recommendations** — specific, actionable improvements (not rewrites)

If the file format supports commenting, leave your specific in-line comments with your findings and start it with **Agent Feedback**. If not, create an **Agent Feedback** section at the end of the document and list your feedback there.