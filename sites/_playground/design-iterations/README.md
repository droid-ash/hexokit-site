# design-iterations

Twelve standalone landing-page mockups for hexokit.com, each copying the
**measured structure** of one well-marketed tool site unrelated to terminals and
pairing it with the beat of the HexoKit story it is structurally best at telling.
Static HTML, no build step, no dependencies. Light and dark, down to 400px.

Open `index.html` for the gallery (rationale, thumbnails, links), or any
`NN-name.html` directly. From a HexoKit pane: `rk present index.html`.

| # | File | Reference | Structure borrowed | Second act |
|---|------|-----------|--------------------|------------|
| 01 | `01-cursor.html` | cursor.com | tiny H1, giant textured product panel, alternating bleed panels | operator |
| 02 | `02-linear.html` | linear.app | 64px/510 H1, 128px rhythm, two-column heads, r12 frames, changelog | fab gate |
| 03 | `03-langfuse.html` | langfuse.com | 840px column + rails, highlight marks, r2 key-hint buttons, tables, FAQ | operator |
| 04 | `04-supabase.html` | supabase.com | base + modules bento, "use one or all", code tabs, pixel display | toolkit |
| 05 | `05-posthog.html` | posthog.com | the site is a desktop: OS bar, icons, floating window, chunky buttons | GUI |
| 06 | `06-tailscale.html` | tailscale.com | 64px centred H1, five cards, laptop panel, stat cards, gradient panel | phone |
| 07 | `07-raycast.html` | raycast.com | tall streaked hero, floating glass nav, palette window, glass tiles | ⌘K / tiles |
| 08 | `08-vercel.html` | vercel.com | black, Geist −6% tracking, hairline grid, Plan·Build·Ship triptych | fab gate |
| 09 | `09-resend.html` | resend.com | serif display H1, outline r16 buttons, r24 cards, 96px rhythm | (restraint) |
| 10 | `10-replit.html` | replit.com | prompt box hero, icon row, colour bento r24 | operator |
| 11 | `11-cognition.html` | cognition.ai | serif body, 605px measure, exposed grid, gutter numbers, manifesto | what it isn't |
| 12 | `12-n8n.html` | n8n.io | floating nav card, glowing object, node canvas, glass info cards | operator |

## What is copied, what is not

Copied: layout, type scale, line heights, tracking, spacing rhythm, container
widths, button geometry, card radii/borders/shadows, section order — read off
each site's live DOM with Playwright on 2026-09-13 and stored in
`references/measurements.json`. Every mockup's head comment lists exactly what
it borrowed.

Not copied: any brand — logos, proprietary typefaces, illustrations, photos,
colours-as-identity, copy, customer logos, testimonials. Free faces stand in
(Geist, Instrument Serif, Space Grotesk, Nunito, DM Sans, Outfit, Manrope,
Newsreader). All twelve use HexoKit's own amber/teal accents and the product
screenshots in `assets/` (copies of the live site's `public/screenshots/`).

## Content

All copy comes from `content-spine.md` — one set of facts, sourced from
`content/hexokit/**`, `content/fab-kit/**`, the SRAD skill and the run-kit
release notes, written to the rules in `fab/project/context.md` § Copy and the
`vn39` verb list. The two brand strings are verbatim and never edited.

## Regenerating screenshots

```sh
just setup                                   # once per worktree — brings Playwright
node sites/_playground/design-iterations/shoot.mjs        # all
node sites/_playground/design-iterations/shoot.mjs 04 07  # some
```

Writes `shots/NN-name-{1440,400}-{dark,light}.png` (full page) and
`shots/NN-name-1440-{dark,light}-hero.png` (above the fold). Uses the installed
Chrome via Playwright's `channel: 'chrome'`, so nothing is downloaded.

Reference screenshots of the twelve sites were kept out of the repo (they are
other companies' pages); only the measurement JSON is committed.
