#!/usr/bin/env python3
"""Generate embed.html — a paste-into-WordPress version of this campaign.

The article body cannot take the campaign as-is, for one overriding reason: the
campaign opens with a CSS reset whose selectors are bare elements
(`a,abbr,...,div,...,h1..h6,p,ul,table,button` plus `body{line-height:1}`). Dropped
raw into a post it strips the margins, fonts and list markers from the *whole
article*. So the reset is scoped, not removed.

This script turns index.html into a single self-contained block:

  * every selector is scoped under `.dm-embed-scope`, so the reset applies to the
    campaign and nothing else. `html`/`body`/`:root` collapse onto the scope
    element itself.
  * asset URLs become absolute (https://campaigns.hypb.st/202610-dr-martens/...),
    so no <base> is needed and the block is position-independent.
  * html/head/body wrappers are dropped; <main> becomes a <div> so the article
    does not end up with two <main> elements.
  * the stray `</div>` the client export carries immediately after `<body>` is
    removed — left in, it closes the scope wrapper at once and every campaign
    element lands outside it, unstyled. (Also fixes the campaign's own markup,
    which is one </div> over.)
  * --vh is written to the scope element rather than documentElement, so the
    campaign does not set a custom property on the host page's root.
  * gem-rain appends its layers to the scope element instead of <body>.

The campaign's JS is otherwise untouched: every DOM query it makes is
class-scoped or element-scoped, and the markup carries no ids, so it cannot
collide with the surrounding page.

Usage:  python3 build-embed.py          # reads index.html, writes embed.html
"""
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / 'index.html'
OUT = Path(os.environ.get('DRM_OUT', HERE / 'embed.html'))
ORIGIN = 'https://campaigns.hypb.st/202610-dr-martens/'
SCOPE = 'dm-embed-scope'
# The article supplies the reset, so the campaign's own element reset is dropped.
# DRM_KEEP_RESET=1 builds the scoped-but-reset-included variant, for comparison.
DROP_RESET = os.environ.get('DRM_KEEP_RESET') != '1'


def split_rules(css):
    """Split a stylesheet into top-level rules, respecting nesting."""
    rules, depth, start = [], 0, 0
    for i, ch in enumerate(css):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                rules.append(css[start:i + 1])
                start = i + 1
    if css[start:].strip():
        rules.append(css[start:])
    return rules


def scope_selector(sel):
    """Prefix one comma-separated selector list with the scope class."""
    out = []
    for part in sel.split(','):
        p = part.strip()
        if not p:
            continue
        root = re.match(r'^(html|body)(?=[.\[]|$)', p)
        if p == ':root' or root:
            suffix = p[len(root.group(0)):] if root else ''
            out.append('.' + SCOPE + suffix)
        else:
            out.append('.' + SCOPE + ' ' + p)
    return ','.join(out)


BARE_ELEMENT = re.compile(r'^[a-z][a-z0-9]*$')


# Element rules the campaign's own layout depends on. The article's reset differs
# from these (it sets p{margin-bottom:16px}, the campaign uses 10px), so dropping
# them grows the campaign's text panels by up to 96px each / ~115px overall.
# Everything here is scoped, so keeping them cannot leak.
KEEP_ELEMENT_RULES = {'body', 'ol,ul', 'p'}


def is_reset(head):
    """True for a pure element reset — every selector a bare element (or html/body).

    The article already supplies a reset, so the campaign's normalize block
    (the 81-selector zeroing, the HTML5 display:block list, blockquote/q, table,
    button) is dropped rather than scoped. Anything with a class, id, attribute
    or pseudo-class — including :root, which carries the campaign's colour
    tokens — is kept, as are the few element rules in KEEP_ELEMENT_RULES.
    """
    parts = [x.strip() for x in head.split(',')]
    if not parts:
        return False
    if all(x in ('html', 'body') or BARE_ELEMENT.match(x) for x in parts):
        return head not in KEEP_ELEMENT_RULES
    return False


def scope_css(css, drop_reset=True):
    out = []
    for rule in split_rules(css):
        rule = rule.strip()
        if not rule:
            continue
        head = rule.split('{', 1)[0].strip()
        if drop_reset and is_reset(head):
            continue
        if head.startswith('@'):
            at = head.split()[0].lower()
            if at in ('@font-face', '@keyframes', '@-webkit-keyframes', '@charset', '@import'):
                out.append(rule)                      # no selectors inside
            else:                                     # @media / @supports
                inner = rule[rule.index('{') + 1:rule.rindex('}')]
                out.append(f'{head}{{{scope_css(inner, drop_reset)}}}')
            continue
        out.append(scope_selector(head) + rule[rule.index('{'):])
    return ''.join(out)


def rewrite_assets(text):
    """Point campaign-relative asset URLs at the deployed origin."""
    return re.sub(r'/202610-dr-martens/((?:images|fonts)/)', ORIGIN + r'\1', text)


def main():
    src = SRC.read_text(encoding='utf-8')

    css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', src, re.S))
    scoped = scope_css(css, drop_reset=DROP_RESET)

    # External resources the campaign loads from <head>: Matter.js (gem-rain
    # physics — its absence is swallowed by a `if (!window.Matter) return` guard,
    # so gem-rain silently does nothing) and the Google Fonts links. These carry
    # over; the inline <head> script is handled with the body scripts below.
    head = src.split('</head>', 1)[0]
    head_res = '\n'.join(
        m.group(0) for m in re.finditer(r'<(?:link|script)\b[^>]*>(?:</script>)?', head)
        if re.search(r'(?:href|src)=', m.group(0))
    )

    body = src.split('</head>', 1)[1].split('</body>', 1)[0]
    scripts = re.findall(r'<script[^>]*>.*?</script>', body, re.S)
    for sc in scripts:
        body = body.replace(sc, '')
    # the --vh seeding script sits in <head>, before <base> — pull it in first so
    # it still runs before the campaign code
    inline_head = re.findall(r'<script(?![^>]*src)[^>]*>.*?</script>', head, re.S)
    scripts = inline_head + scripts
    markup = body.strip()

    # the export opens <body></div>; drop both, and demote <main>
    markup = re.sub(r'^<body[^>]*>\s*', '', markup)
    markup = re.sub(r'^</div>\s*', '', markup)
    markup = markup.replace('<main class="dm__wrapper">', '<div class="dm__wrapper">')
    markup = markup.replace('</main>', '</div>')

    js = '\n'.join(scripts)
    js = js.replace('document.documentElement.style.setProperty("--vh"',
                    'document.querySelector(".' + SCOPE + '").style.setProperty("--vh"')
    js = js.replace('document.body.appendChild',
                    'document.querySelector(".' + SCOPE + '").appendChild')

    doc = (
        '<!-- 202610-dr-martens — scoped inline embed.\n'
        '     Generated by build-embed.py; edit that, not this. -->\n'
        f'<div class="{SCOPE}">\n'
        f'{head_res}\n'
        f'<style>{rewrite_assets(scoped)}</style>\n'
        f'{rewrite_assets(markup)}\n'
        f'{rewrite_assets(js)}\n'
        '</div>\n'
    )
    OUT.write_text(doc, encoding='utf-8')

    leak = sum(
        1 for r in split_rules(rewrite_assets(scoped))
        for part in r.split('{', 1)[0].split(',')
        if part.strip() and not part.strip().startswith(('@', '.' + SCOPE))
    )
    print(f'wrote {OUT.name}: {len(doc)} bytes '
          f'({len(scoped)} css / {len(markup)} markup / {len(js)} js)')
    print(f'  selectors escaping the scope: {leak}')
    print(f'  remaining relative asset refs: {doc.count(chr(34) + "/202610-dr-martens/")}')


if __name__ == '__main__':
    main()
