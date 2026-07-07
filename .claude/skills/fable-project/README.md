# Fable Prompt Skill (`/fable-project`)

A Claude Code skill for unknowns-first prompting and implementation.

## Install in Claude Code

Project-only install:

```bash
mkdir -p .claude/skills
cp -R fable-project .claude/skills/fable-project
```

Personal install across projects:

```bash
mkdir -p ~/.claude/skills
cp -R fable-project ~/.claude/skills/fable-project
```

Then start Claude Code and run:

```text
/fable-project
```

or:

```text
/fable-project Build a new onboarding dashboard and help me discover the unknowns first
```

## Upload to claude.ai

Zip the outer `fable-project` folder and upload it as a custom Skill in Claude settings, if your plan supports custom Skills.

## Recommended use

Use `/fable-project` at the start of ambiguous work. The skill will interview you one question at a time, do a blind-spot pass, brainstorm/prototype where useful, create an implementation plan, implement only after approval, keep notes, and produce a final explainer plus quiz.
