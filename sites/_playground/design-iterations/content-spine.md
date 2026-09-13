# Content spine — what every iteration says

Every mockup in this folder renders the same facts in a different structure, so a
comparison judges **design**, not copy. This file is the single source for those
facts. Copy follows `fab/project/context.md` § Copy and the style sheet in
`docs/findings/landing-copy-study.md` § 5: short spoken sentences, one claim each,
outcome over mechanism, the reader's words bare, commands only if they exist
(`vn39`: the `rk` verbs are `agent board code code-server cron daemon desktop
doctor gui mcp mux notify operator present remote riff role serve skill status tab
tutorial update url`).

Sources: `content/hexokit/README.md`, `content/hexokit/site/{gui,boards}.md`,
`content/fab-kit/README.md`, `.agents/skills/_srad/SKILL.md`,
`sites/astro-starlight-terminal1/src/lib/landing-data.ts`, run-kit release notes
v3.19.38–.60 (2026-09-11 → 09-13).

---

## The arc

HexoKit is the base — the terminal, from anywhere. Everything else is one thing
you can do because the terminal is there. The page tells it in this order and
never all at once:

| # | Beat | One-line claim | Proof asset |
|---|------|----------------|-------------|
| 1 | **The terminal, from anywhere** | Your tmux, in the browser and on your phone. | `hexokit-hero-desktop.webp`, `hexokit-hero-phone.webp` |
| 2 | **A plan before any code** (fab-kit) | The agent scores its own assumptions. Under 3, it stops and asks. | Rendered `## Assumptions` table + `fab score` readout |
| 3 | **One agent runs the rest** (operator) | One agent watches the others and pings your phone. | `hexokit-operator-console.webp`, `hexokit-operator.webp`, `hexokit-board.webp`, `hexokit-fleet.webp`, `hexokit-agent-state.webp` |
| 4 | **From your phone, over your own network** | Serve it over Tailscale. Same panes on your phone. | `hexokit-phone-terminal.webp` |
| 5 | **The agent gets a screen** (GUI) | A desktop in a tile. The agent clicks, types, screenshots. | `hexokit-web-tile.webp` (tile concept), rendered GUI tile |
| 6 | **Six small tools, one job each** | HexoKit is the base. Each tool adds one thing. | Tool list |
| — | **What it refuses to be** | Not an agent wrapper. Plain files. Any agent. | It is / It isn't |
| — | **Install** | One line, then you are in. | Install block |

Each iteration leads with beat 1 and then chooses which of 2–6 to make its
second act. The rest follow at lower weight. No iteration gives every beat equal
weight — that is the failure mode of the current page.

---

## Brand strings (verbatim, never edited)

- Tagline: **Your tmux, in the browser and on your phone.**
- Sub-line: **Cockpit for the agent era.**
- Product: **HexoKit** (one word, capital H and K). Binary: `rk`.

---

## Beat 1 — The terminal, from anywhere

**H1** Your tmux, in the browser and on your phone.
**Sub** Cockpit for the agent era.
**Lead (30 words max)** A remote console for the machine you actually work on.
Every tmux session and pane is a live terminal, at your desk or on the couch.
Nothing to configure, no database.

Short variants for tight heroes:
- Every pane you left at your desk, live on your phone.
- State read straight from tmux. Nothing to sync.

**CTAs** Install · Read the docs · GitHub

**Supporting claims**
- One command per parallel agent. `rk riff` gives an agent its own git worktree
  and tmux window. `rk riff -N 3` starts three.
- A pane is just a pane. A build, a REPL, an ssh session, `htop`. The agent is
  one of the things you run, not the thing HexoKit is.
- `Cmd+K` finds everything. Sessions, panes, boards, settings.

---

## Beat 2 — A plan before any code (fab-kit)

**H** The agent plans before it builds.
Alternates: *No code until the plan clears.* · *Ten minutes of intake. Two hours
of rework saved.*

**Body (spoken, ≤ 4 sentences)** fab-kit puts an intake stage in front of every
change. The agent writes the plan and scores each assumption it made. Below the
gate, the pipeline refuses to run and tells you what to clarify. Above it, the
agent runs on its own.

**How the score works (for a deeper section)**
Four questions per decision: How clear was the signal? How reversible is it?
Can the agent actually know this? How many readings are there? Each is scored
0–100. Together they grade the decision:

| Grade | Composite | What happens |
|---|---|---|
| Certain | ≥ 80 | proceeds silently |
| Confident | ≥ 50 | proceeds, noted |
| Tentative | ≥ 20 | proceeds with a marker, `/fab-clarify` resolves it |
| Unresolved | < 20 | blocks and asks |

The change starts at **5.0** and every weak decision costs points. **Under 3.0
the gate closes.** A single risky decision stays visible; it is never averaged
away.

**Proof visual** a rendered intake `## Assumptions` table (4 rows, grades and
`S:nn R:nn A:nn D:nn`) and a terminal line:
```
$ fab score --check-gate 7ajq
confidence 3.4 / 5.0 · gate 3.0 · pass
```
and the failing twin:
```
confidence 2.6 / 5.0 · gate 3.0 · blocked — 1 unresolved: run /fab-clarify
```

**Also true (use sparingly)**
- Six stages that cannot be skipped: intake → apply → review → hydrate → ship
  → review-PR.
- A constitution of MUST / SHOULD / MUST NOT. Every plan and review checks
  against it.
- Review runs in a fresh sub-agent and loops back up to three times.
- What the change learned is written to `docs/memory/` in git. The next change
  starts smarter.

**Commands** `/fab-new`, `/fab-ff`, `/fab-clarify`, `fab score --check-gate`

---

## Beat 3 — One agent runs the rest (operator, boards, status)

**H** One agent watches the others.
Alternates: *Run a fleet, not a session.* · *Three agents, one dot each.*

**Body** `rk operator` opens a coordinator you talk to. It watches the fleet,
starts the next change, unblocks a stuck one, and pings your phone when it
needs you. One shortcut and its console slides down over whatever you are
looking at. Your pane never moves.

**Supporting claims**
- Pin panes from any machine into a board. Three agents and the dev server, side
  by side. The same board on your phone.
- Working, waiting, idle. One dot per window says which. Claude Code, Codex,
  Gemini CLI, Copilot CLI, Kimi Code and OpenCode report in after a one-time
  setup.
- `rk cron` wakes an agent on a schedule. `rk notify` pushes to your phone even
  with the tab closed.
- `rk riff -N 3` — three worktrees, three windows, three agents, one command.
  Failures roll back.

**Commands** `rk operator`, `rk riff -N 3`, `rk cron`, `rk notify`, `rk board`

---

## Beat 4 — From your phone, over your own network

**H** Steer it from your phone.
Alternates: *The agent waiting on you is one tap away.* · *Your network, your
machine, your phone.*

**Body** Serve the dashboard over Tailscale and open it on your phone. Same
sessions, same boards, same panes. A key bar for tab, ctrl and arrows. Nothing
leaves your tailnet.

**Steps (for a how-it-works block)**
1. `tailscale serve --bg http://localhost:3000`
2. Open `https://<machine>.<tailnet>.ts.net` on your phone.
3. Tap a pane. You are in the shell you left at your desk.

**Supporting** Touch targets tuned for a phone. Boards swipe as a carousel.
Push notifications arrive with the tab closed.

---

## Beat 5 — The agent gets a screen (GUI)

**H** Give the agent a screen.
Alternates: *A desktop in a tile.* · *Watch the agent use the computer.*

**Body** `rk gui on` starts a desktop on the host and puts it in a tile beside
your terminals. You watch from the browser or your phone. The agent opens apps,
clicks, types and takes screenshots. Off by default, and you can turn it off.

**Supporting**
- Four tiles per window: terminal, editor, web, desktop. `⌘1` to `⌘4`.
- On a phone: trackpad or touch pointer, a key bar, fullscreen.
- Pick the desktop: IceWM by default, or LXQt, XFCE, Plasma and others.
- Agents drive it through the CLI, gated on your switch. On a Mac it mirrors
  Screen Sharing, view only.

**Commands** `rk gui on`, `rk gui shot`, `rk gui exec`

---

## Beat 6 — Six small tools, one job each

**H** HexoKit is the base. Each tool adds one thing.
Alternate: *Six companions. Drop any one; the rest keep working.*

| Tool | Blurb (landing's own 6–7 words) | Command to show |
|---|---|---|
| fab-kit | a plan before any agent writes code. | `/fab-new` |
| wt | throwaway git worktrees, one per change. | `wt create flaky-tz` |
| idea | catch an idea without breaking flow. | `idea add "…"` |
| tu | what your AI coding sessions cost. | `tu --watch` |
| hop | jump to any of your repos. | `hop --all pull` |
| shll | installs and updates the whole set. | `shll setup agent` |

Plus **Desktop** — the Mac app around the dashboard. `rk desktop install`.

Each tool is its own CLI. No shared daemon, no SDK, no database. They compose
through files.

---

## What it refuses to be

**H** Use any agent, untouched.

**It is** A console for your tmux, built for the phone. Any agent, no database,
nothing to keep in sync.

**It isn't** An agent wrapper. It reads no agent's output and speaks no agent's
protocol. When the agent tools change again, this layer stays put.

**Plain files** Every plan, backlog and cost report is a file you can `cat`,
`grep` and `git diff`.

**Open source** MIT, all seven repos. (Star counts are small — never a headline.)

---

## Install

**H** One line, then you are in.
```
curl -fsSL hexokit.com/install | sh
brew install sahil87/tap/hexokit
```
Needs tmux 3.4 or newer. Run `rk doctor` if anything looks wrong.
Then: `rk daemon start` · open `localhost:3000` · `rk tutorial`.

---

## Nav and footer

Nav: Docs · Toolkit · GitHub · (Install button)
Footer: Docs · Toolkit · GitHub · Discord · versions.json · llms.txt
