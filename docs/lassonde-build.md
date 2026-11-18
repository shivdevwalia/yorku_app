# Lassonde Atlas: local implementation

User authorized the Lassonde prerequisite map, exact-degree filtering, course search and public-source research on November 13, 2026. Scope is local implementation, not merge or deployment. Tracked in [issue #7](https://github.com/shivdevwalia/yorku_app/issues/7). Existing fictional `prototype/index.html` is preserved separately and is not used by this application.

## Run locally

Requires Python 3.10+ and Node.js 20.9+.

From the repository root:

```powershell
python -m backend.ingest --budget 900 --delay 0.2
python -m backend.server
```

In a second terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Open `http://127.0.0.1:3000`. Python binds only `127.0.0.1:8000`; Next.js binds only loopback and proxies `/api/v1` to Python. The Python standard-library server is for local development, not production hosting. No database, account, credentials or paid service is required.

`data/catalog.json` is a generated, gitignored local research snapshot. Do not publish or commit it as a cleared dataset. Subsequent imports reuse detail records with the same PID, reparse their source text, and keep the original retrieval timestamp. Use `--refresh` to retrieve fresh detail records. A request budget is per import, at most two concurrent requests with a globally serialized start delay. No automatic retries or background refresh are scheduled.

## Official sources and extraction

- [York calendar](https://2026-2027.calendars.students.yorku.ca/academic-calendar) embeds the official Kuali backend.
- [Catalogue metadata](https://york.kuali.co/api/v1/catalog/public/catalogs/691dc968c6306e23358308fc).
- [Course index](https://york.kuali.co/api/v1/catalog/courses/691dc968c6306e23358308fc) and [searched index](https://york.kuali.co/api/v1/catalog/courses/691dc968c6306e23358308fc?q=LE%2F). Both are normalized and compared. The catalog ID is pinned rather than silently switching academic years.
- Course detail route: `/api/v1/catalog/course/{catalogId}/{pid}` on `york.kuali.co`. Descriptions contain the original requirement text.
- [Lassonde 2026–2027 checklists](https://lassonde.yorku.ca/student-life/2026-2027-program-checklists). All downloadable XLSX/PDF links are discovered from this page, not maintained as guessed filenames.
- [Academic support](https://lassonde.yorku.ca/student-life/academic-support) explains that students must match the academic calendar for their program-entry year. Only 2026–2027 is imported here.

Observed catalogue scope is 428 source records / 426 canonical LE course codes across CCCC, CIVL, COOP, CSSD, DIGT, EATS, EECS, ENG, ESSE, MECH, TECL and TRON. An earlier conversational tally of 528 was an arithmetic error, not evidence of 100 missing records. `LE/ENG ` contains trailing whitespace; identifiers also sometimes contain credit/language suffixes. Normalization handles these explicitly. Duplicate PIDs/language/credit variants are not equivalent: primary details prefer English, and alternate source records remain linked with a review warning.

The current checklist hub exposes 35 files, not the 32 observed by the initial researcher. The application follows the current page and does not claim that file count equals degree count. Thirty-three XLSX files are structurally parsed, including two first-year planning aids. Two BASc CSSD PDF formats remain linked but unsupported; selecting one returns a visible unsupported-scope message, never a substituted degree map. Direct PDF inspection found layout/heading ambiguity; no curriculum is inferred from the filename alone.

XLSX extraction reads ZIP/XML in memory. It preserves sheet, cell, original text and context. Standard `Course Code` columns and Space Engineering's paired `Code` columns supply curriculum candidates. General Science templates have explicit course pools rather than populated code columns; these remain pools. Prerequisite-note columns are retained as context but are not degree-map seeds. Original curriculum groups, alternatives, optional entries and unresolved elective slots are inspectable in the degree filter. Year headings represent suggested sequencing, not enforced enrolment years. Unversioned workbook contents linked from the current-year index still need applicability review.

## What the map means

Python owns identity normalization, relationship extraction, degree scoping, graph closure and filtering. Next.js/TypeScript renders the API responses; it does not calculate eligibility.

- Prerequisite, corequisite and combined prerequisite/corequisite references are separate edge kinds.
- Exclusions, crosslistings, historical offerings and notes are separate sections and never prerequisite edges.
- `Prior to ...:` blocks remain historical, not current prerequisite branches.
- Label variants such as `Prerequisite(s)`, Unicode hyphens, `Prerequisites include`, and the observed source typo `Prerequiste(s)` are recognized.
- Observed source spellings `Pre-requites` and `Co-requsities`, plus colonless exclusion headings, are recognized as section boundaries before reference extraction. Unrecognized requirement-like headings generate visible warnings and terminate the preceding dependency section rather than silently adding their references to it.
- A connection is a course reference, **not an assertion that every connected course is mandatory**. AND/OR, grades, GPA, permissions, credit thresholds and other non-course conditions remain in source text. There is no eligibility engine in this build.
- A missing or unrecognized rule is unknown, not “no prerequisites.” Missing details and unresolved references remain explicit nodes. Historical/ambiguous identity references are not silently reassigned to current courses.
- The degree scope includes candidate alternatives/elective pools, not a verified mandatory-course list. General-education categories and free electives cannot all be represented as specific course nodes.
- Supporting prerequisite connections can extend outside the degree's named entries. Turning connections off shows only curriculum candidates. Map and text/list views use the same node set, with textual incoming-edge navigation.
- Course levels form visual columns; they are not recommended degree years or a topological ordering. Same-level prerequisites and cycles can exist.

## Local API contract

All responses are JSON with `Cache-Control: no-store`; metadata carries `schemaVersion: "1"`. OpenAPI 3.1 schemas live in `backend/contracts.py`, and generated frontend types are in `frontend/lib/types.ts`. `python -m backend.contracts --check-types` detects contract drift. Imports validate records against these schemas. Queries are processed by Python, never by a duplicated client rule engine.

| Endpoint | Purpose |
| --- | --- |
| `/api/v1/openapi.json` | OpenAPI 3.1 document and response schemas |
| `/api/v1/meta` | Calendar, coverage, provenance, extraction limits, failures and schema version |
| `/api/v1/programs` | Exact source labels, statuses, curriculum groups and source cell context |
| `/api/v1/courses?q=&subject=&program=&supporting=false` | Search within chosen scope; without program, the current LE catalogue |
| `/api/v1/courses/{URL-encoded canonical ID}` | Detailed single course, original rules and source links |
| `/api/v1/graph?program=&subject=&q=&supporting=true&focus=` | Degree/reference graph; optional prerequisite closure and course isolation |

Invalid scopes are HTTP 400; missing courses/endpoints are HTTP 404. Unsupported checklists fail visibly rather than widening silently to all courses. Data refreshes are offline CLI operations, not web endpoints.

Publication is atomic after validation. Empty indexes, duplicate final IDs, mixed calendar years, invalid provenance, major course/detail losses, empty curriculum-column extraction and major checklist extraction loss prevent replacement of the prior snapshot. Requests are restricted to the two official source hosts, with bounded response and workbook-decompression sizes.

## Validation and remaining gates

No pre-existing application test suite existed. Validation uses explicit parser fixtures and API assertions, Python compilation, frontend TypeScript/lint/build, and dependency audit; exact executed results belong in the handoff, not assumed from this description. Browser interaction, phone layout and assistive-technology behaviour are not claimed tested without a browser session.

Executed on November 13, 2026:

- 87 ad hoc assertions passed: observed prerequisite-label variants, exclusions versus prerequisite edges, combined/historical boundaries, false date-node prevention, unknown rules, compact/spaced/title search, all 33 extracted curriculum scopes, both unsupported checklists, all 12 subject graph closures, focus, empty search, invalid degree, cyclic fixture traversal, real loopback HTTP responses and 400/404 handling.
- All local dataset records and sampled actual API responses passed the OpenAPI schema validator.
- `python -m backend.contracts --check-types` and `python -m compileall -q backend` passed.
- `npm run typecheck`, `npm run lint` and `npm run build` passed from `frontend`.
- `npm audit --omit=dev --audit-level=moderate` found zero production vulnerabilities. Full audit reported seven moderate transitive lint-tool findings associated with minimatch; `npm audit fix` did not resolve them within the supported dependency ranges. No forced major-version override was applied.
- `git diff --check` passed. No existing persistent test suite or CI result is claimed.
- After review fixes, the final parser 1.3.1 snapshot was re-imported with 37 bounded requests and zero retrieval failures. It contains 426 current Lassonde details, 347 supporting-course records and 260 unresolved references; these categories are not all disjoint by faculty, and total stored records are 894. All 33 curriculum scopes and 12 subject closures were rechecked.
- Regression assertions verify that EECS 3622 does not require excluded EECS 4622, EECS 2032 does not acquire its exclusions as prerequisites, its misspelled corequisite heading correctly links EECS 2030, and CSSD 2101 links CSSD 1201. Unknown-heading boundaries are exercised explicitly.
- The final production frontend was started on `127.0.0.1:3000` with Python on `127.0.0.1:8000`. Actual HTTP requests verified home-page delivery, metadata, encoded single-course lookup, course search, degree graph scope, generated OpenAPI schemas and unsupported-PDF HTTP 400 through the Next.js proxy. This is HTTP integration evidence, not browser-interaction evidence.

Before public use: independent academic review of rule extraction, degree/elective semantics and variants; two CSSD PDF adapters; complete historical-entry-year coverage; reviewed AND/OR/non-course semantics if eligibility is added; approved public display/retention/redistribution scope; production server/storage/security; independent exact-commit review; explicit final merge/deployment approval. Catalogue completeness is bounded to the retrieved current official index, not every historical or graduate Lassonde course.

## Coordination

Parent thread: `486c9903-f13c-43ba-bd84-40b783b2b7b0`; baseline HEAD `44515845576cc84ebec8988fb2bc7e138705eef5`. Parent implements and integrates locally, preserving the existing untracked prototype and without switching branches or creating commits.

Research tasks, each isolated/read-only and completed without repository changes:

- `6d066fa3-53c4-4c96-ae49-0926c7c28c46`: official Kuali course routes and source discovery.
- `af5f7fd7-6f91-466e-ae14-93ca739e2c7d`: exact checklist labels, degree variants, representative workbook structures and applicability limits.

Both research reports are source findings, not independent implementation reviews. A working-tree review cannot replace the repository's eventual exact-commit review gate. No PR, merge or deployment has been performed.

Independent read-only working-tree review task `91303224-9f62-47fb-85be-f19c4a4b7969` verified baseline HEAD and implementation snapshot SHA256 `813ed32606e9d7f74b8021164b7b4880e7761de95fd801d1165e4c6e853adef1`. It found two parser defects (colonless exclusions absorbed into prerequisites; omitted CSSD prerequisite due to source spelling) and an isolation action offered outside the active map. The parent fixed these directly, added visible unknown-heading warnings, disabled out-of-map isolation with an explanation, and ran the regression/integration checks above. No second delegate was started for these small fixes.

Final backend/frontend snapshot SHA256: `9fd00ecf2d1389c1141f2f5a1c0749b8802aa4567a7bdf4110ec0e2bee432439`, computed over sorted nonignored backend/frontend paths, each UTF-8 path + NUL + raw bytes + NUL. This final snapshot is parent-validated, not independently re-reviewed or committed. User approval is still required before merge/deployment; eventual exact-commit review remains outstanding.

## Issue #7 completion checks (November 17, 2026)

The existing local implementation was checked against the only open issue, #7.
Repeatable offline regression checks now live in `backend/test_catalog.py`:

```powershell
python -m unittest backend.test_catalog -v
```

All eight tests passed, covering observed prerequisite spelling variants,
exclusion and historical boundaries, unknown-heading warnings, cyclic degree
closure, unsupported scopes, compact course search, encoded identifiers, and
real loopback HTTP 200/400/404 responses. Python compilation, generated contract
type checks, frontend typecheck, lint and production build, and `git diff --check`
also passed. These are current checks; the larger ad hoc assertion counts above
are historical evidence. The earlier statements that no persistent suite exists
describe the November 13 baseline; the offline regression suite is now included.
No new import, browser interaction, phone layout, or assistive-technology testing
was performed in this pass. Generated catalogue data and the separate prototype
remain outside the application commit. Merge and deployment require approval.

Parent T3 thread for this completion pass: `5965e064-562b-43f5-8596-32e586bd6a1b`.
Base: `44515845576cc84ebec8988fb2bc7e138705eef5`; no prerequisite PRs.

Independent review of `ca0222133daadaab2501b9affd5b0005643fb003` found
one P2 omission: abbreviated alternatives lost their inherited subject. Parser
1.4.0 now retains comma, and/or and slash-separated numeric alternatives.
Explicit multiple-faculty references remain unresolved with a visible warning;
faculty-free ambiguous identifiers remain unresolved rather than guessed.
Numeric ranges remain unsupported and now produce a visible warning.
Eleven offline regressions, Python compilation and generated type checks passed
after the fix. The original review does not cover this subsequent fix; these
small review changes were validated by the parent per the repository workflow.
Review task: `1c520fb2-0f43-48ba-972f-a0cd1946198c`.
