# Fable Question Bank

Use these questions selectively. Ask one question at a time. Prioritize questions where the answer changes the plan.

## First question options

- What are we trying to create or change, and what would make the result feel successful?
- What is your current starting point: what do you already know, what are you unsure about, and how familiar are you with this codebase/domain?
- Where should I look first: files, folders, docs, tickets, designs, or examples?

## Blind spot prompts

- Do you want me to do a blind-spot pass before planning?
- What historical work, existing pattern, or prior attempt should I know about?
- What hidden constraint would make a normal best-practice answer wrong here?
- What would be expensive to discover only after implementation?

## Brainstorm prompts

- Should I brainstorm several approaches before choosing one?
- Do you want the cheapest viable solution, the highest-polish solution, or a spectrum?
- What tradeoff are you most willing to make: speed, polish, maintainability, cost, performance, or scope?

## Prototype prompts

- Is this a “you’ll know it when you see it” problem?
- Would you rather react to mockups before I touch the real app?
- Should I create 3–4 distinct directions using fake data?
- What reference should the prototype borrow from?

## Plan approval prompts

- Which of these decisions should I change before implementation?
- Are there user-facing behaviors here that need your approval?
- What must not change?
- What verification would make you confident this is done?

## Implementation prompts

- Should I proceed with conservative decisions and log deviations, or stop whenever I encounter uncertainty?
- Do you want me to keep an implementation-notes file?
- Should I run tests, create a demo, or generate screenshots after implementation?

## Analytics / data blind-spot prompts

Use when the task involves a metrics export, dashboard, or performance report (e.g. YouTube, LinkedIn, podcast, product analytics).

- What's the exact definition behind each headline metric (e.g. views vs. unique viewers, watch time vs. average view duration), and could that definition be misleading here?
- Is the time window a rolling window or a calendar period, and does that framing distort any comparison being made?
- Is one outlier item (a single video, post, or day) skewing the aggregate numbers?
- What's the traffic-source or channel-source mix, and does the story change if you exclude the largest source?
- Is there a new vs. returning audience split, and what does it imply that isn't visible in the top-line number?
- Were there any external pushes (cross-posts, paid promotion, algorithm changes, seasonality) that could explain a spike or dip independent of content quality?
- What's the comparison baseline — the account's own trailing average, a stated goal, or a niche benchmark — and is that baseline actually valid?
- What decision is this data meant to inform, and does the current cut of the data actually support that decision?

## Review prompts

- Do you want a reviewer-facing explainer?
- Do you want a quiz before merging so you understand what changed?
- Who is the audience for the final explanation: you, a teammate, reviewers, customers, or viewers?
