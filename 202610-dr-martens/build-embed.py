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
# Rename .post-body-content -> .post-body-content-none to drop the theme's
# rules on that wrapper. DRM_NO_RENAME=1 keeps the class as-is.
RENAME_POST_BODY = os.environ.get('DRM_NO_RENAME') != '1'
# Let the site header scroll off instead of staying pinned, so the campaign can
# use the whole viewport. DRM_KEEP_HEADER_STICKY=1 leaves it sticky.
SCROLL_OFF_HEADER = os.environ.get('DRM_KEEP_HEADER_STICKY') != '1'
# Reveal the first section as soon as it is on screen, rather than waiting for
# its top to reach the viewport top. DRM_NO_FIRST_REVEAL=1 disables this.
REVEAL_FIRST_WRAPPER = os.environ.get('DRM_NO_FIRST_REVEAL') != '1'
# Mobile: the sticky category strip under the masthead (.mobile-header-bottom,
# top:60px) pins over the campaign. Made static on narrow viewports only.
# DRM_KEEP_MOBILE_NAV=1 disables this.
UNSTICK_MOBILE_NAV = os.environ.get('DRM_KEEP_MOBILE_NAV') != '1'
# .post-body-article clips its own horizontal overflow.
CLIP_ARTICLE_X = os.environ.get('DRM_NO_ARTICLE_CLIP') != '1'
CLIP_MODE = os.environ.get('DRM_CLIP_MODE', 'clip')  # 'clip' or 'hidden'
# Branding: the campaign wrote "Dr Martens" without the period in image alts.
DR_PERIOD = os.environ.get('DRM_NO_DR_PERIOD') != '1'


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

    if DR_PERIOD:
        # The campaign shipped "Dr Martens" (no period) in the image `alt` attributes,
        # alongside correct "Dr. Martens" in the visible copy. Normalise to the brand's
        # own spelling. Applied to the markup; the alt strings live there, not in the JS.
        dr_before = len(re.findall(r'\bDr(?!\.)', markup))
        markup = re.sub(r'\bDr(?!\.)', 'Dr.', markup)
        print(f'  Dr -> Dr. in {dr_before} alt attribute(s)')

    if REVEAL_FIRST_WRAPPER:
        # The reveal fires once a wrapper's top reaches the viewport top:
        #     t <= (r ? s : 2) && n >= i        // r = already "in"
        # (t = wrapper rect.top, s = `buffer`, n = rect.bottom, i = innerHeight * exitAt).
        # So a section that starts on screen stays hidden until it is scrolled to the
        # very top. The first wrapper is already in view on arrival, so its threshold is
        # widened to the whole viewport — it reveals as soon as it is on screen at all,
        # while the rest of the sections keep the scroll-driven behaviour.
        old_cond = 'return t<=(r?s:2)&&n>=i'
        new_cond = (
            'if(e.wrapper===document.querySelector(".' + SCOPE + ' .dm__sticky-wrapper"))'
            'return n>0&&t<=innerHeight;'
            'return t<=(r?s:2)&&n>=i'
        )
        if old_cond in js:
            js = js.replace(old_cond, new_cond, 1)
        else:
            print('  ! reveal condition not found; first-wrapper reveal not widened')
    js = js.replace('document.documentElement.style.setProperty("--vh"',
                    'document.querySelector(".' + SCOPE + '").style.setProperty("--vh"')

    # gem-rain appends its layer to <body>. Detached from the scope it loses the
    # scoped `.dm-gem-rain{overflow:hidden}` rule, and its gems -- spawned at random x
    # and pushed side to side by the physics -- then extend the document's scrollWidth
    # past the viewport, producing a horizontal scrollbar that grows as gems appear.
    # Keeping the layer inside the scope restores the clip.
    js = js.replace('document.body.appendChild',
                    'document.querySelector(".' + SCOPE + '").appendChild')

    # --vh is the plain viewport. The site header is left to scroll off on its own
    # rather than being subtracted, so the campaign sizes itself to the full
    # viewport as the standalone build does.

    # sticky pins at top:0 by default, which is the viewport edge — under the site
    # header. Shift the pin point down by the header's occupied height. The notes
    # stage keeps its own 40px offset, measured from below the header.
    # Any --vh rule the themed page already carries is neutralised (see the appended
    # JS, which renames .post-body-content). Re-assert the var on :root so children
    # inherit the campaign's value by inheritance rather than by a nearer rule.
    header_css = f':root{{--vh:inherit}}'

    # The Hypebeast theme styles .post-body-content, and several of those rules reach
    # the campaign (the --vh override is the one that matters here). Renaming the class
    # only for our own ancestor subtree disables them without touching the rest of the
    # article. Done from JS rather than by hand so a re-paste keeps working even if the
    # wrapper's class changes upstream.
    # #page-header is sticky (156px tall at top:-99px, so only its bottom 57px shows).
    # Sticky pins it to the viewport for the whole page, so the campaign's full-viewport
    # wrappers always have it across their top. Setting it static lets it scroll away
    # with the article. This is deliberately unscoped: the header sits outside the
    # campaign's subtree. !important is needed because the theme's own rule sets it.
    header_rule = (
        '<style>#page-header{position:static!important}</style>'
    ) if SCROLL_OFF_HEADER else ''

    # Two more page-level rules, both deliberately unscoped because the elements they
    # target sit outside the campaign's subtree:
    #   .mobile-header-bottom  the sticky category strip under the masthead on narrow
    #                          viewports (top:60px, z-index 190). Static on mobile only,
    #                          so the desktop masthead is unaffected.
    #   .post-body-article     clips its own horizontal overflow, so anything in the
    #                          campaign that would widen the document is contained here.
    # The .site-main-nav selector the brief named does not exist in this theme; this is
    # the element that actually pins on mobile.
    # <site-main-nav> is a custom element that only exists in the beta layout
    # (https://hypebeast.com/_beta/enable sets hb_beta_layout, which adds
    # `beta-layout` to <body>). It ships static, but its own JS switches it to
    # `position:sticky; top:18px` on scroll, where it then sits over the campaign's
    # full-height wrappers. Forcing it static on mobile stops that.
    if UNSTICK_MOBILE_NAV:
        header_rule += (
            '@media (max-width:991px){'
            '.mobile-header-bottom{position:static!important}'
            'site-main-nav{position:static!important}'
            '}'
        ).join(['<style>', '</style>'])
    if CLIP_ARTICLE_X:
        header_rule += f'<style>.post-body-article{{overflow-x:{CLIP_MODE}}}</style>'

    rename = ''
    if RENAME_POST_BODY:
        rename = (
            '<script>(function(){var el=document.querySelector(".post-body-content");'
            'if(!el)return;'
            'el.classList.remove("post-body-content");'
            'el.classList.add("post-body-content-none")'
            '})();</script>'
        )

    doc = (
        '<!-- 202610-dr-martens — scoped inline embed.\n'
        '     Generated by build-embed.py; edit that, not this. -->\n'
        f'<div class="{SCOPE}">\n'
        f'{head_res}\n'
        f'<style>{rewrite_assets(scoped)}{header_css}</style>\n'
        f'{rewrite_assets(markup)}\n'
        f'{rewrite_assets(js)}\n'
        f'{rename}\n'
        '</div>\n'
        f'{header_rule}\n'
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
