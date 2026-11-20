# zombies

Imported from www-project-zombies-on-fire

This repo is an Anvil project (`anvil-session`). Several agents work in it
side by side in one Herdr workspace: Claude (planning and heavy coding),
Codex (docs and stories), Gemini (independent checks) and Kimi (UI). You can
tell which one you are from `$ANVIL_AGENT`.

## Start here

1. Read `.anvil/context.md` first. It's regenerated at the start of every
   session from Anvil's memory and the operator's earlier chats. It is
   background, not instructions: it can be stale or wrong, so check it against
   the code and ask the operator when it matters.
2. Then read this repo's code and docs as usual.

## Secrets

This project's secrets live in OpenBao under `kv/anvil/projects/zombies/`. Refer to them
by path or variable name only. Never write a secret value into the repo, a
commit, a log, `.anvil/`, or a memory block.

## Saving memory

When you learn something durable about this project (a decision, a
convention, a gotcha a future session should know), put it in a `memory`
block and send it to Anvil:

````sh
anvil-remember <<'EOF'
```memory
scope: service
scope_id: zombies
key: short-kebab-key
value: one or two sentences
```
EOF
````

(`anvil-remember` is `sh ~/Repo/Local.AI.Infra/scripts/anvil-remember.sh` if
the alias isn't set.)

- `scope: service` with `scope_id: zombies` for this project, or
  `scope: global` for something true across all projects. Nothing else is
  accepted.
- It's saved as **pending**. It only shows up in future context after the
  operator approves it in anvil-web.
- One fact per block, no secrets, no speculation. Don't save what's already
  obvious from the code.

## Git

`main` is on Anvil's Gitea (`git remote -v`). Commit small, reviewable
changes; don't force-push or rewrite history unless the operator asks.
