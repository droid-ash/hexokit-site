#!/usr/bin/env python3
"""make-b.py — generate the "B" (minimal) variation of every iteration.

For each NN-name.html, writes NN-name-b.html: the same page, same copy, same
structure, with every real product screenshot (<img src="assets/hexokit-*.webp">)
replaced by a schematic drawn in HTML/CSS — the real layout and chrome, but only
3–6 elements, big type, everything else reduced. The schematic fills the exact box
the image occupied (aspect-ratio from the img's width/height), so nothing reflows.

Two pages get the "no product" treatment their references use: 09 (the tilted phone
becomes a single hexagon and one mono line) and 11 (the panel image becomes a thin
schematic strip). Re-run after editing any A file:  python3 make-b.py
"""
import re, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))

KIT_CSS = r"""
/* ── minimal schematic kit (variation B): real layout, ≤6 elements, no images ── */
.mk{--mk-bg:#0f1216;--mk-bg2:#141920;--mk-fg:#d8dce4;--mk-mut:#6f7987;--mk-line:rgba(255,255,255,.09);--mk-acc:#d4a73a;--mk-ok:#59d499;--mk-warn:#ffc533;--mk-bad:#ff6161;
 width:100%;aspect-ratio:var(--ar,16/10);background:var(--mk-bg);color:var(--mk-fg);font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:clamp(8px,1.45cqw,15px);line-height:1.55;display:grid;overflow:hidden;box-sizing:border-box;position:relative;container-type:inline-size;text-align:left;font-weight:400;letter-spacing:0;font-style:normal}
.mk *{box-sizing:border-box;margin:0;text-shadow:none}
.mk .mk-top{grid-area:top;display:flex;align-items:center;gap:1em;padding:.7em 1.1em;border-bottom:1px solid var(--mk-line);color:var(--mk-mut);font-size:.9em;white-space:nowrap;overflow:hidden}
.mk .mk-top b{color:var(--mk-fg);font-weight:500}
.mk .mk-top i{width:.9em;height:.9em;border-radius:50%;background:var(--mk-line);flex:none}
.mk .mk-top i.r{margin-left:auto}
.mk aside{grid-area:side;border-right:1px solid var(--mk-line);padding:.9em 0;overflow:hidden}
.mk aside small{display:block;padding:0 1.1em .5em;font-size:.75em;letter-spacing:.08em;color:var(--mk-mut)}
.mk aside div{display:flex;align-items:center;gap:.7em;padding:.45em 1.1em;white-space:nowrap;overflow:hidden}
.mk aside div em{font-style:normal;color:var(--mk-mut);margin-left:auto;font-size:.85em}
.mk aside div.cur{background:var(--mk-bg2)}
.mk s{width:.7em;height:.7em;border-radius:50%;border:2px solid var(--mk-mut);flex:none;text-decoration:none;display:inline-block;position:relative}
.mk s.on{background:var(--mk-acc);border-color:var(--mk-acc)}
.mk s.wait{border-color:var(--mk-warn);box-shadow:0 0 0 .25em rgba(255,197,51,.22)}
.mk s.ok{background:var(--mk-ok);border-color:var(--mk-ok)}
.mk s.bad{background:var(--mk-acc);border-color:var(--mk-acc)}
.mk s.bad::after{content:"";position:absolute;inset:.12em;border-radius:50%;background:var(--mk-bad)}
.mk main{grid-area:main;padding:1.1em 1.4em;overflow:hidden}
.mk main p{white-space:nowrap}
.mk main p.d{color:var(--mk-mut)}
.mk .ok{color:var(--mk-ok)}.mk .warn{color:var(--mk-warn)}.mk .bad{color:var(--mk-bad)}.mk .acc{color:var(--mk-acc)}
.mk footer{grid-area:foot;padding:.5em 1.1em;border-top:1px solid var(--mk-line);color:var(--mk-mut);font-size:.85em;white-space:nowrap;overflow:hidden}
.mk-dash{grid-template:"top top" auto "side main" 1fr "foot foot" auto / 30% 1fr}
.mk-phone{grid-template:"top" auto "side" auto "main" 1fr "keys" auto / 1fr;font-size:clamp(8px,3.8cqw,15px)}
.mk-phone aside{border-right:0;border-bottom:1px solid var(--mk-line)}
.mk-phone.term{grid-template:"top" auto "main" 1fr "keys" auto / 1fr}
.mk .mk-keys{grid-area:keys;display:flex;gap:.4em;padding:.7em .9em;border-top:1px solid var(--mk-line);background:var(--mk-bg2)}
.mk .mk-keys span{flex:1;text-align:center;padding:.5em 0;border-radius:.4em;background:var(--mk-bg);border:1px solid var(--mk-line);font-size:.85em}
.mk-op{grid-template:"top" auto "main" 1fr / 1fr}
.mk-op .mk-in{margin-top:.7em;padding-top:.7em;border-top:1px solid var(--mk-line)}
.mk-op .mk-in span{color:var(--mk-mut)}
.mk-board{grid-template:"top top top" auto "a b c" 1fr / 1fr 1fr 1fr}
.mk-board section{padding:.9em 1.1em;border-right:1px solid var(--mk-line);overflow:hidden}
.mk-board section:last-child{border-right:0}
.mk-board section header{display:flex;align-items:center;gap:.6em;color:var(--mk-mut);margin-bottom:.6em;white-space:nowrap}
.mk-board section p{white-space:nowrap}
.mk-state{grid-template:"top" auto "side" 1fr / 1fr}
.mk-state aside{border-right:0}
.mk-state aside div{padding:.6em 1.1em}
.mk-hexo{display:grid;place-items:center;gap:28px;color:var(--fg);padding:40px 0}
.mk-hexo svg{width:min(260px,60%);aspect-ratio:200/220;fill:none;stroke:currentColor;stroke-width:1.2;filter:drop-shadow(0 0 40px var(--glow,rgba(255,255,255,.12)))}
.mk-hexo p{font-size:14px;color:var(--muted)}
"""

TOP = '<div class="mk-top"><b>▤ HexoKit</b><span>⌘K</span><i class="r"></i><i></i><i></i></div>'
ROWS = ('<small>SESSIONS · runKit</small>'
        '<div class="cur"><s class="on"></s>swift-fox<em>building</em></div>'
        '<div><s class="wait"></s>calm-heron<em>waiting on you</em></div>'
        '<div><s class="on"></s>amber-tern<em>building</em></div>'
        '<div><s></s>dev<em>just dev</em></div>'
        '<div><s></s>htop</div>')

SNIPPETS = {
    'dash': lambda ar, st: (
        f'<div class="mk mk-dash" style="--ar:{ar};{st}">{TOP}'
        f'<aside>{ROWS}</aside>'
        '<main><p>$ rk riff -N 3</p><p class="d">→ swift-fox · calm-heron · amber-tern</p>'
        '<p><b class="ok">●</b> building &nbsp;<b class="ok">●</b> building &nbsp;<b class="warn">◌</b> waiting on you</p>'
        '<p class="d">$ rk operator</p><p class="acc">▌</p></main>'
        '<footer>agt waiting 12s · 3 tracked · cpu 9% · dev-ws</footer></div>'),
    'phone': lambda ar, st: (
        f'<div class="mk mk-phone" style="--ar:{ar};{st}">'
        '<div class="mk-top"><b>HexoKit</b><span>dev-ws</span><i class="r"></i></div>'
        f'<aside>{ROWS}</aside>'
        '<main><p class="d">tap a pane</p><p class="d">you are in the shell you left at your desk</p></main>'
        '<div class="mk-keys"><span>tab</span><span>ctrl</span><span>esc</span><span>↑</span><span>↓</span><span>⌘K</span></div></div>'),
    'phoneterm': lambda ar, st: (
        f'<div class="mk mk-phone term" style="--ar:{ar};{st}">'
        '<div class="mk-top"><b>calm-heron</b><span>agt waiting</span><i class="r"></i></div>'
        '<main><p>$ fab score --check-gate 7ajq</p><p>confidence 3.4 / 5.0</p><p>gate 3.0 · <b class="ok">pass</b></p><p class="d">&nbsp;</p>'
        '<p class="d">? proceed to apply</p><p class="acc">› y▌</p></main>'
        '<div class="mk-keys"><span>tab</span><span>ctrl</span><span>esc</span><span>↑</span><span>↓</span><span>⌘K</span></div></div>'),
    'op': lambda ar, st: (
        f'<div class="mk mk-op" style="--ar:{ar};{st}">'
        '<div class="mk-top"><b>⌁ OPERATOR</b><span>runKit · idle 56m</span><i class="r"></i></div>'
        '<main><p class="d">Ran 1 shell command</p><p>All green. Merging.</p><p>Merged. PR #865.</p>'
        '<p class="d">0 tracked · loop stopped</p><p>Start C8 and C9?</p>'
        '<p class="mk-in">› <span>start C8 and C9</span><b class="acc">▌</b></p></main></div>'),
    'board': lambda ar, st: (
        f'<div class="mk mk-board" style="--ar:{ar};{st}">'
        '<div class="mk-top"><b>▤ board · agents</b><span>3 pinned</span><i class="r"></i></div>'
        '<section style="grid-area:a"><header><s class="on"></s>swift-fox</header><p>Ran 3 tests</p><p class="ok">all green</p><p class="d">▌</p></section>'
        '<section style="grid-area:b"><header><s class="wait"></s>calm-heron</header><p>? auth provider</p><p class="d">waiting on you</p><p class="acc">▌</p></section>'
        '<section style="grid-area:c"><header><s></s>dev</header><p>$ just dev</p><p class="d">:4321 ready</p></section></div>'),
    'state': lambda ar, st: (
        f'<div class="mk mk-state" style="--ar:{ar};{st}">'
        '<div class="mk-top"><b>SESSIONS</b><span>one dot per window</span><i class="r"></i></div>'
        '<aside><div><s class="on"></s>swift-fox<em>working</em></div>'
        '<div><s class="wait"></s>calm-heron<em>waiting on you</em></div>'
        '<div><s></s>amber-tern<em>idle 43s</em></div>'
        '<div><s class="bad"></s>flaky-tz<em>review failed</em></div></aside></div>'),
}

ASSET_TO = {
    'hexokit-hero-desktop': 'dash', 'hexokit-desktop-app': 'dash',
    'hexokit-hero-phone': 'phone', 'hexokit-phone-terminal': 'phoneterm',
    'hexokit-operator-console': 'op', 'hexokit-operator': 'op',
    'hexokit-board': 'board', 'hexokit-agent-state': 'state', 'hexokit-fleet': 'state',
    'hexokit-web-tile': 'dash',
}

IMG = re.compile(r'<img\b[^>]*>')
ATTR = re.compile(r'(\w+)="([^"]*)"')

def replace_img(m, fname):
    attrs = dict(ATTR.findall(m.group(0)))
    src = attrs.get('src', '')
    mm = re.search(r'assets/(hexokit-[a-z-]+)\.webp', src)
    if not mm:
        return m.group(0)
    kind = ASSET_TO[mm.group(1)]
    ar = f"{attrs.get('width','16')}/{attrs.get('height','10')}"
    if fname.startswith('11-') and mm.group(1) == 'hexokit-hero-desktop':
        ar = '24/9'  # the editorial page gets a thin strip, not a full dashboard
    return SNIPPETS[kind](ar, attrs.get('style', ''))

HEX_SVG = ('<svg viewBox="0 0 200 220"><path d="M100 10l86 50v100l-86 50-86-50V60z"/>'
           '<path d="M100 210V110M14 60l86 50 86-50" opacity=".5"/></svg>')

for path in sorted(glob.glob(os.path.join(HERE, '[0-9][0-9]-*.html'))):
    fname = os.path.basename(path)
    if fname.endswith('-b.html'):
        continue
    s = open(path, encoding='utf-8').read()
    s = s.replace('</title>', ' · B (minimal)</title>', 1)
    s = s.replace('\n</style>', KIT_CSS + '</style>', 1)
    if fname.startswith('09-'):
        s = re.sub(r'<div class="obj">.*?</div>\s*</section>',
                   '<div class="obj"><div class="mk-hexo">' + HEX_SVG +
                   '<p class="mono">$ rk daemon start &nbsp;·&nbsp; http://localhost:3000</p></div></div>\n  </section>',
                   s, count=1, flags=re.S)
    s = IMG.sub(lambda m: replace_img(m, fname), s)
    out = path[:-5] + '-b.html'
    open(out, 'w', encoding='utf-8').write(s)
    print('wrote', os.path.basename(out), '· images left:', len(re.findall(r'assets/hexokit-', s)))
