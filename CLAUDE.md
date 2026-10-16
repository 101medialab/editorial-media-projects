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

`202607-hypebeast-hypegolf`, `levis-digital-experience`.

No build step. A single prebuilt `index.html` (with inline CSS/JS) plus an `assets/` directory. The campaign path is hardcoded as `<base href="/<directory>/" />` inside the HTML. Deploy with:

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
- `202610-dr-martens` is an empty placeholder for an upcoming campaign.
- Campaigns are iframe-embedded, so pages include the `pym.js` `pym.Child` snippet (Vite campaigns) and use viewport-relative sizing; a shared fix used `vh`-driven iframe growth with a relative base href. Keep iframe-height communication intact when editing layouts.
