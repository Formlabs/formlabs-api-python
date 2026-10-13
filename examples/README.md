# Examples

Runnable programs for `formlabs-sdk`, grouped by what they are for. The worked examples are
type-checked against the SDK and run against a stand-in PreForm Server on every change to the SDK.
The smoke tests are not: each talks to a real PreFormServer or the production Formlabs API, and most
read credentials from `FL_TEST_USER` / `FL_TEST_PASS`. Read the docstring at the top of a file before
running it.

| | |
|---|---|
| The six below | Worked examples, one uv project per folder. Each has a guide on the developer portal. Run one from its folder with `uv run <script>.py`. |
| [`smoke_tests/`](smoke_tests/) | One short program per API surface, each exercising it end to end against live services. Run these to check that a change still works against the real thing. |

## smoke_tests

| | |
|---|---|
| [`live_auth_smoke.py`](smoke_tests/live_auth_smoke.py) | `client.auth` against production: token mint, refresh, developer tokens, revocation. |
| [`live_preform_api_smoke.py`](smoke_tests/live_preform_api_smoke.py) | `client.preform`: launch or connect to a PreFormServer, create a scene, run an async operation. |

## Worked examples

Each folder is a uv project: its `pyproject.toml` lists what it needs, and `uv run` installs that into the
folder's own environment. In this repository the SDK comes from the checkout; the released copy of each
example, and its zip on the GitHub Release, installs the SDK release it was published with.

| | |
|---|---|
| [`printability-report/`](printability-report/) | Check STL files before a job is confirmed: PASS, WARN or FAIL for each part. |
| [`instant-quote/`](instant-quote/) | Quote parts in every material on a price list: resin, print time and price. |
| [`dental-presets/`](dental-presets/) | Apply a print preset to a set of scans and save a print-ready `.form` file. |
| [`print-setting-rollout/`](print-setting-rollout/) | Move every queued job from one print setting to another. |
| [`part-labels/`](part-labels/) | Turn a `.form` file into a billing summary and a bag label for each part. |
| [`web-sls-packer/`](web-sls-packer/) | A web app that packs STL parts into Fuse 1+ and Fuse X1 builds and sends them to printers. |
