# Code Compass

Small, evidence-first comprehension skills for Codex and Claude Code. Start with a concrete worked example, not a request to explain a ticket you do not understand yet.

Each response aims for **Answer · Evidence · Next**, normally under 80 words. One uncertainty, one useful step, then stop. These are model instructions, not a guarantee of correct reasoning or a security boundary.

## Install into a project

Requires Python 3; no packages, network calls, hooks or services are installed. Review the files first. From this checkout:

```sh
python3 scripts/install.py --platform codex --target /path/to/project --dry-run
python3 scripts/install.py --platform codex --target /path/to/project
# Or, for Claude Code:
python3 scripts/install.py --platform claude --target /path/to/project
```

The installer copies complete skill folders to `.agents/skills/` (Codex) or `.claude/skills/` (Claude Code). It refuses existing skill folders and destination symlinks rather than overwriting them. Restart/reopen your agent session after installing if discovery has not refreshed. Inspect the skill picker to confirm availability; organization policy may restrict custom skills. This does not install anything into an employer repository unless you explicitly choose that project and have permission.

For personal use instead, manually copy the `skills/cc-*` folders into `~/.agents/skills/` for Codex or `~/.claude/skills/` for Claude Code. Do not install both project and personal copies with the same name unless you deliberately want overlapping discovery. Claude cloud/Cowork behavior differs from local Claude Code; consult its official documentation rather than assuming personal folders synchronize.

## Start here

In Codex:

```text
$cc-ground Use this issue/PR: <link or pasted text>. Repo: <root>.
Base/head if known: <refs>. I do not understand the problem yet.
Build one evidence-backed example, explain one blocking term, then stop.
```

In Claude Code, invoke `/cc-ground` with the same context. The installed skill names are the real invocation names: `$cc-term` in Codex, `/cc-term` in Claude Code. Bare `/term` or `/ground` are not aliases supplied by this package. Natural-language requests can also trigger skills by description.

| Skill | Use when | Small result |
| --- | --- | --- |
| `cc-ground` | The ticket itself is opaque | One state/action/actual/expected example |
| `cc-term` | One unfamiliar object blocks you | Its local meaning and one example |
| `cc-trace` | You need the old behavior | One meaningful transition for an input |
| `cc-why` | You need the reason for a change | Effect vs supported rationale vs unknown intent |
| `cc-probe` | Two explanations both seem possible | One discriminating lookup or test proposal |
| `cc-delta` | You can now approach the PR | One semantic before/after, mechanical churn separate |
| `cc-where` | You resume after an interruption | Current question, evidence, unknown and next check |

Do not run all skills as a checklist. Use whichever resolves the current barrier. A self-check or prediction question belongs *after* a worked example, not before it. Ask for a longer explanation only of the part that still blocks you.

## Fictional example

Use `examples/tiny-catalog/issue.md` and `catalog.py`, without installing dependencies or launching an IDE:

> Answer: The ordinary list excludes archived items; setting `include_archived=True` keeps them. For `[active A, archived B]`, static tracing predicts `[A]` by default.
>
> Evidence: `examples/tiny-catalog/catalog.py:1-5`; `test_catalog.py:5-7`. Tests have not been run in this example.
>
> Next: Inspect the caller to find which flag the page passes; that caller is not included here.

This is an authored demonstration, not a captured execution result. Missing caller evidence stays missing. Do not invent it to make the explanation satisfying.

## Guardrails

Skills use authorized read-only inspection first. They distinguish observations, static predictions, hypotheses and proposed tests. They do not grant access to private systems, authorize edits, upload code, install dependencies, or start production services. Keep sensitive code in an approved environment. The short-answer target never excuses hiding uncertainty.

State stays in the current conversation unless you ask to persist it. When context is lost, the assistant should reconstruct or ask for the missing artifact rather than claim memory.

## Validate locally

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s examples/tiny-catalog -v
```

The tests check installation behavior and the fictional fixture, not the quality of every possible model response. Skill behavior also needs evaluation on real, authorized tasks. No Claude Code runtime acceptance is claimed without a live test in that product.

## Sources and scope

Format and discovery references checked 2026-11-06:
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills)

Conceptual inspiration:
- Peter Naur, [Programming as Theory Building](https://pages.cs.wisc.edu/~remzi/Naur.pdf) (1985)
- Stanley Letovsky, [Cognitive Processes in Program Comprehension](https://iiif.library.cmu.edu/file/Newell_box00093_fld06587_doc0001/Newell_box00093_fld06587_doc0001.pdf)
- Michael Feathers, [Working Effectively with Legacy Code discussion](https://gotopia.tech/episodes/228/working-effectively-with-legacy-code)

The prompts are a practical synthesis, not quotations or a newly validated research method. No license grant is included; public visibility alone does not grant unrestricted reuse rights.
