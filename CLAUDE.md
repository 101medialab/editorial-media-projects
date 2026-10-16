# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A monorepo of standalone editorial campaign microsites ("mini sites"), one top-level directory per campaign, built for Hypebeast/Hypebae/Popbee brands. It supersedes the older `resources` repo. Most are client-branded landing pages intended to be embedded in an article via iframe.

Campaigns are deployed to S3 (`campaigns-hypebeast` bucket) served from `https://campaigns.hypb.st/<directory>/`, fronted by CloudFront. There is no monorepo-level build, package.json, linter, or CI — each campaign is self-contained with its own dependencies and scripts.

## Three project archetypes

Identify which archetype a directory belongs to before working in it; the commands and layout differ substantially.

### 1. Vite + Vue (dated campaigns)

`202507-oakley`, `202511-yuki`, and `popbee/2025-most-hearted-awards` / `popbee/2026-most-hearted-awards`.

```
npm install
npm run dev          # vite dev server
npm run build        # vite build --base=<campaign-path>/
npm run deploy       # build, then ../deploy.sh $(pwd) dist <campaign-path>
```

- Vue 3 SFCs, Tailwind v4 via `@tailwindcss/vite` (`@import 'tailwindcss';` + `@theme {}` in `style.css`, **no** tailwind.config / postcss config).
- `~` is aliased to `src/`.
- `--base` **must** equal the S3 directory name, which is **not always the folder name** — `popbee/2026-most-hearted-awards` builds with `--base=/202603-most-hearted-awards/` and deploys to `202603-most-hearted-awards`. When creating or copying a campaign, keep the folder name, the `--base` value, and the third arg to `deploy.sh` consistent with each other, or assets 404 under the campaign path.
- Two structural styles:
  - **Single page** (oakley, yuki): one `index.html` → `src/main.js` → one monolithic `App.vue`. No component directory.
  - **Multi-page** (popbee): `build.rollupOptions.input` lists `index.html` + `result.html` as separate entries, each with its own root component (`Main.vue`, `Result.vue`, `Preview.vue`) and a page-scoped `src/components/<Page>/` directory. Also uses `vite-imagetools`, `vite-plugin-webfont-dl`, `swiper`, and `ofetch`; keeps static files in `public/`.

### 2. Hand-authored static HTML

`202607-hypebeast-hypegolf`, `levis-digital-experience`, `202610-dr-martens`.

No build step. A single prebuilt `index.html` (with inline CSS/JS) plus an asset directory (usually `assets/`; `202610-dr-martens` uses `images/` + `fonts/` instead). The campaign path is hardcoded as `<base href="/<directory>/" />` inside the HTML. Deploy with:

```
npm run deploy       # ../deploy.sh $(pwd) . <directory>
```

Note the second arg is `.` (there is no `dist/`).

### 3. Eleventy + Netlify CMS

`hypebeast-gift-guide`, `hypebae-gift-guide`, `hennessy-xo-kim-jones-hypebeast-com`, `hennessy-xo-kim-jones-hypebeast-cn`, `hypebae-diving-into-digital`, `hypebeast-audemars-piguet-x-marvel`.

These share a common skeleton, originally exported from Webflow:

```
npm install
npm run serve        # eleventy --serve (runs asset download first)
npm run build        # eleventy -> public/
npm run deploy       # s3-deploy via .env (NOT the shared deploy.sh)
npm run local-backend  # local Netlify CMS proxy server
```

Layout and data flow:

- **Input `cms/`**, **layouts `theme/`**, **output `public/`** (set in `.eleventy.js`; `theme` is wired in as Eleventy's `includes` dir). Content is `cms/pages/*.md` plus per-section folders; each markdown file's `layout:` frontmatter names a same-named template in `theme/`.
- **Mixed template engines**: `.html` templates are Liquid, `.njk` templates are Nunjucks. `_utils/filters.js` registers filters for both.
- `cms/_data/*.json` are Eleventy global data files, keyed by **content hashes** (`"337cfb41"`), not names — a Webflow artifact. Don't hand-edit `images.json` / `links.json` / `texts.json`; templates reference them by hash.
- `_utils/` is the shared plugin bundle, entered through `_utils/index.js`: collections, filters, transforms, shortcodes, plus `scripts/optimize-assets.js`.
- **`npm run optimize` runs automatically before every `serve`/`build`** (via `preserve`/`prebuild`). Despite the name it does **not** optimize images — it downloads the remote Webflow/CloudFront assets listed in `_utils/config/external-files.json` into `theme/assets/external/`, skipping any that already exist locally. A new remote image must be added to that JSON as well as to the CMS content.
- The client-side search index (`fuse.js`, `_utils/search.js`) is written to `public/_data/search-index.json` as a **side effect of a collection** rather than an explicit build step.
- Netlify is used for CMS git-gateway auth and function config only; **hosting is S3 + CloudFront**. The `functions/` directory the zip step and `netlify.toml` reference does not exist in most campaigns, so that step is a no-op.
- Deploys use `s3-deploy` driven by a per-campaign `.env` (`AWS_BUCKET_NAME`, `CF_DIST_ID`, credentials), not the root `deploy.sh`. `.env` files are gitignored; `.env.dist` holds the empty template.

## Shared deploy script

`deploy.sh` at the repo root is used by archetypes 1 and 2 (and is the only thing the `deploy` npm script wraps):

```
deploy.sh <project_path> <build_output_dir> <bucket_directory>
```

It confirms the destination exists via `aws s3api list-objects-v2`, prompts interactively for `y`/`n`, runs `aws s3 sync --delete` to `s3://campaigns-hypebeast/<bucket_directory>`, then invalidates `/<bucket_directory>/*` on CloudFront. Because of `--delete` and the interactive prompt, it needs the AWS CLI configured and an answer on stdin; it is not suitable for non-interactive CI as written.

## Tests

The only automated tests cover `deploy.sh`:

```
python3 -m unittest discover -s tests            # all (6 tests)
python3 -m unittest discover -s tests -k <name>  # single test
```

`tests/test_deploy.py` fakes the `aws` binary on `PATH` and asserts the script never uploads without confirmation and never invalidates the cache when an earlier step fails. Update it when changing `deploy.sh`.

## Conventions and gotchas

- `dist/` and `node_modules/` are gitignored and never committed — build output lives on disk only. `.DS_Store` is also ignored.
- Campaign directories are named `<YYYYMM>-<client>`; the deployed S3 directory sometimes differs from the folder name (see above).
- **Never commit credentials.** `.env`, `.env.*`, `node_modules`, and `dist` are gitignored; keep secrets in the per-campaign `.env` (copy from `.env.dist`) only. If you find a live key in a tracked file, treat it as a leak to report rather than something to quietly move.
- Campaigns are iframe-embedded — see **Embedding (pym)** below for the parent snippet and the `--vh` sizing contract. Keep iframe-height communication intact when editing layouts.
- `202610-dr-martens` is a hand-authored static campaign (archetype 2); its client build hardcoded root-absolute asset paths that were rewritten to `/202610-dr-martens/…` so they resolve under the campaign path.

## Embedding (pym)

Campaigns are embedded by this snippet, which lives in the article/CMS template — **not** in this repo, so it cannot be changed from here:

```html
<div id="hb-embed"></div>
<script src="https://pym.nprapps.org/pym.v1.min.js"></script>
<script>var pymParent = new pym.Parent('hb-embed', 'https://campaigns.hypb.st/<directory>/', {});</script>
```

- **pym v1 carries only `height`/`width` messages.** There is no `viewport-height`/`viewport-width`, and the parent sends only `initialWidth`/`childId` as iframe URL params. The parent resizes the iframe to the child's full content height, so inside an embedded campaign `window.innerHeight` is the *whole document* and raw CSS `vh`/`svh` is meaningless.
- **Iframe-safe sizing:** use `calc(var(--vh, 1vh) * N)` instead of raw `vh`/`svh`, with `--vh` set to 1% of the *visible* height — seed from `screen.height` when `window.self !== window.top`, and from `window.innerHeight` (plus a `resize` listener) when top-level. Seeding from `window.innerHeight` while embedded collapses the layout. Reference implementation: `202607-hypebeast-hypegolf`.
- **Parent half of the handshake (optional).** The campaign child already sends `viewport-height-request` and listens for `viewport-height`; only the parent side is missing, and pym's Parent does expose `onMessage`/`sendMessage`. Adding it makes embedded layout match standalone to ~0.1%:

```js
function sendViewportHeight() { pymParent.sendMessage('viewport-height', String(window.innerHeight)); }
pymParent.onMessage('viewport-height-request', sendViewportHeight);
window.addEventListener('resize', sendViewportHeight);
sendViewportHeight();
```


- **Scroll-driven campaigns need a second message: `scroll-offset`.** pym grows the iframe to the campaign's full content height so the article page scrolls, which leaves the iframe's own document permanently unscrolled. Any campaign built on document scroll — `position:sticky`, `position:fixed`, `document`/`window` scroll listeners, `IntersectionObserver`, or `innerHeight`-relative reveal tests — is dead in the embed until the parent relays where the reader is. `202610-dr-martens` is the reference: it ships an in-page shim that restores the reader's window as the viewport, and its embed must also send the reader's offset:

  ```js
  function sendState() {
    var f = pymParent.iframe, top = f.getBoundingClientRect().top + window.scrollY;
    pymParent.sendMessage('viewport-height', String(window.innerHeight));
    pymParent.sendMessage('scroll-offset', String(Math.round(window.scrollY - top)));
  }
  pymParent.onMessage('viewport-height-request', sendState);
  pymParent.onMessage('height', sendState);        // the campaign grew; re-measure
  window.addEventListener('scroll', sendState, { passive: true });
  window.addEventListener('resize', sendState);
  ```

  The 202507-oakley / 202511-yuki / 202607-hypebeast-hypegolf campaigns use no scroll-driven CSS or listeners at all, so they need only the snippet above them.

Without it `--vh` falls back to `screen.height`, so on a 1080p screen with a 900px window the embedded page renders ~19% taller than standalone. The addition is backward compatible — campaigns that ignore the message are unaffected, including those (like `202507-oakley`) that use no `--vh` at all.
