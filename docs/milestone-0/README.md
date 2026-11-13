# Milestone 0: source, rights and feasibility

Research date: **November 13, 2026 (America/Toronto)**. Authorized documentation/research: [issue #5](https://github.com/shivdevwalia/yorku_app/issues/5). HEAD checked before edits exactly matched `7d3c7a4455d620e8277237eed73280e576a7e589`: merged [PR #4](https://github.com/shivdevwalia/yorku_app/pull/4), closed [issue #3](https://github.com/shivdevwalia/yorku_app/issues/3). No subdelegation.

**Recommendation:** conditional eight-course catalog/rules review set; **no-go for public replicated catalog or verified next-term scheduler today**. Rights, conflicting rules and missing live section evidence block those features. Milestone 1 is not authorized. This is not legal clearance, implementation, merge or deployment approval.

## Authorization and follow-up correction

On November 13, 2026, after the initial audit, the user explicitly stated they are fully authorized to scrape and obtain York data and instructed collection to proceed. Treat this as user-attested authorization for public-source scraping/collection. Do not request it again or treat original access-permission uncertainty as a research blocker. Downstream retention, redistribution, public-display and third-party rights have not been independently verified. No access-control bypass or private student records; app implementation, merge and deployment remain separate approval boundaries.

Follow-up research corrected E9: Lassonde's [2026/2027 predetermined timetable page](https://lassonde.yorku.ca/discover/cn1) links /DirectAction/cds as enrolled students' Class Schedule View. Its login behavior does not establish that public course search requires authentication. Anonymous HTTP inspection of the application root and /cds returned Cloudflare HTTP 403 from the research executor. The FAQ-linked [Advanced Courses Search](https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa/wa/hiscrs) returned HTTP 403 through ordinary HTTP and 410 through the search service. These are executor/route failures, not proof of universal unavailability.

The working anonymous Lassonde page publishes Winter 2027 catalogue-number choices: MATH 1014 W68M01, EECS 1021 U99E02 or Z46N02, and EECS/MATH 1028 M58G02 or M58G03. These are not reconciled live section/component records. Its linked [sample timetable PDF](https://lassonde.yorku.ca/wp-content/uploads/Sample-Timetables-4.pdf) returned HTTP 200 with PDF content type, but contents were not successfully inspected in the follow-up. Identifiers and PDF availability do not establish complete dated meetings, exceptions, campuses or allowed component bundles.

Proceed with bounded collection targeting MATH 1014 and EECS 1021 via a supported anonymous route or small official export, with an explicit request budget; exclude block-model courses from initial recurrence samples. The remaining technical blocker is no inspectable current section-level response containing meeting/linkage fields. No parser, feed, export schema or refresh cadence is validated. The evidence register below records initial observations; this correction supersedes its access-permission uncertainty and interpretation of E9. Public publication and verified scheduling remain no-go; collection research can proceed. Milestone 1 is not authorized.

## Method and evidence register

Small representative official-source search/text inspection, including selected passages of one official PDF. No bulk scraping, downloaded dataset, authentication, private history, parser/feed validation or local source archive. PDF retrieval for inspection is not a validated timetable dataset. Observation date is not publication/effective/update date. Unversioned pages need term-specific confirmation. Search snippets were not accepted as confirmed offerings. Only concise paraphrases and links retained.

All observations below: November 13, 2026. Locators support repeat inspection.

| ID | Primary official source / locator | Observed status and limits |
| --- | --- | --- |
| E1 | [MATH 1000-level](https://www.yorku.ca/science/mathstats/1000-level-courses/), MATH 1014/1019 | Readable relationships; no academic-year version in inspected text. |
| E2 | [MATH 2000-level](https://www.yorku.ca/science/mathstats/2000-level-courses/), MATH 2001/2015/2022/2030 | Readable rules; unversioned department list. |
| E3 | [Computer Engineering BEng](https://lassonde.yorku.ca/eecs/academics/undergraduate/future-students/computer-engineering-beng/), EECS 2011/2021 | Readable inconsistent prerequisite passages; not live offerings. |
| E4 | [Electrical Engineering BEng](https://lassonde.yorku.ca/eecs/academics/undergraduate/future-students/electrical-engineering-beng/), EECS 2032 / MATH 2015 | Readable prerequisite/corequisite examples; unversioned. |
| E5 | [2026-2027 Lassonde faculty rules](https://2026-2027.calendars.students.yorku.ca/faculty-rules/lassonde-school-engineering), Computer Engineering / General Prerequisites | Readable year-specific aggregate-grade rule and major-course definition. |
| E6 | [Courses Site FAQ](https://registrar.yorku.ca/courses_site/faq.html), Term / Section / Type / delivery questions | Readable vocabulary/limits; no specific compatibility pairs. |
| E7 | [2026-2027 undergraduate dates](https://registrar.yorku.ca/enrol/dates/2026-2027/fall-winter), All Faculties / Term W, closures | Readable session dates; law/graduate programs excluded. |
| E8 | [VSB guide](https://registrar.yorku.ca/enrol/guide/vsb), technical tips / session / campuses | Readable login-oriented guide; application not accessed. |
| E9 | [Courses application entry](https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa/wa/DirectAction/cds) | Redirected to Passport York login/error; stopped. No working anonymous section route established; not proof all public routes fail. |
| E10 | [Physics and Astronomy handbook 2026-27](https://www.yorku.ca/science/physics/wp-content/uploads/sites/188/2026/09/PHAS_Handbook_20260909.pdf), printed p.43 (PDF page 43), suggested electives | Selected PDF passages inspected; advisory time shorthand. Filename bears September 9, 2026, not measured update time. |
| E11 | [Copyright: Administration of York Websites](https://copyright.info.yorku.ca/administration-of-york-websites/), external content / linking | Readable guidance, not project data licence. |
| E12 | [Copyright FAQ](https://copyright.info.yorku.ca/faq/) | Review contact `copy@yorku.ca`; no database redistribution grant. |
| E13 | [Privacy and Legal candidate path](https://www.yorku.ca/privacyandlegal/) | Tool reported inaccessible. No terms obtained here; no inference York lacks applicable terms. |

## Source and rights inventory

Unresolved is not permission or a legal conclusion. User research authorization is not a source-owner licence. E11 distinguishes linking/copying and advises checking reuse terms/permissions; it does not clear this use. No blanket licence, automated access rate or retention period identified. Robots directives were not inspected and would not independently grant reuse rights.

| Family | Access | Redistribution | Retention | Public display | Third-party rights |
| --- | --- | --- | --- | --- | --- |
| Catalog/calendar E1-E5 | Manual public text observed; automation permission unresolved | Descriptions/structured rules/database unresolved | Raw HTML, fixtures, history/backups unresolved | Copied rules/descriptions unresolved; propose links pending review | Contributor/instructor/media ownership not cleared |
| Timetable E6/E9 | FAQ public; application entry redirected | Sections/meetings/availability unresolved | Snapshots/change logs/rollback unresolved | Unresolved; no verified live records | Provider/software/database rights unknown |
| Dates E7 | Public table | Facts versus compiled-table reuse needs review; no licence identified | Versioned copies unresolved | Replication not cleared; propose links | No third-party clearance inferred |
| VSB E8 | Guide only | Output/data/interface reuse not established | No output stored; future retention unresolved | Do not copy/embed output or claim equivalent coverage | Vendor/licence/sublicensing unknown |
| Handbook E10 | Public PDF inspected | Redistribution not established | No local PDF retained; future fixtures unresolved | Paraphrases/links, not reproduced pages | Photos/contributed teaching material excluded, not cleared |
| Rights E11-E13 | E11/E12 readable; E13 failed | Guidance is not dataset licence | Permission-record policy needed | No legal-clearance claim | Official hosting transfers no third-party rights |

Before collection/publication manager must identify Registrar/data owner and obtain dated decisions for exact fields, derived rules, attribution, routes/rates, display, redistribution, commercial/noncommercial scope, cache TTL, snapshots/backups/deletion and change notification. Ask E12 Copyright Office / E11 compliance contact to route legal/vendor/instructor questions. No outreach sent. Record accountable approver per source/use; unresolved uses disabled. Links are a lower-copy proposal, not blanket clearance.

## Representative rules audit

Manual observations, not parser tests or executable fixtures. Interpretations require effective-term confirmation; ambiguous groupings remain unknown.

| Case | Observation | Consequence / open question |
| --- | --- | --- |
| MATH 2001, E2 | MATH 1200 and 1310 prerequisites; exclusions MATH 3110 and GL/MATH 3320. | Candidate AND; exclusion is not crosslisting/equivalence. |
| MATH 2030, E2 | Alternatives MATH 1014/1310 or ISCI 1402/1410. | Candidate OR; keep connected ISCI references explicit, outside validated coverage. |
| MATH 2022, E2 | Course alternatives or coordinator permission. | Missing permission stays unknown; GL/MATH/MODR identity needs review. |
| MATH 2015, E2/E4 | E2 includes linear-algebra and calculus alternatives, or MATH 1505 with permission; E4 omits linear algebra. | Mixed AND/OR grouping not approved; source conflict blocks verified eligibility. |
| MATH 1019, E1 | Explicit crosslist EECS 1019; exclusions EECS/MATH 1028 and MATH 2320. | Crosslisting differs from exclusion; no duplicate-credit/equivalence inference. |
| MATH 1014, E1 | Non-science six-credit alternatives include ECON 1530/1540; general alternatives include ISCI and GL/MATH. | Faculty/credit grouping requires review; connected subjects not universal substitutes. |
| EECS grade gate, E5 | Most upper-level EECS requires major-course cumulative GPA at least 4.50; definition excludes second-digit-5 courses and includes specified crosslists. | Aggregate, not per-course minimum. Missing grades/attempt policy/applicable rule stays unknown. No individual-course letter-grade threshold verified. |
| EECS 2021, E3 | GPA gate plus EECS 1021/1022/1720/1030 alternatives. | Candidate AND of grade gate and OR group; confirm term. |
| EECS 2011, E3 | Two prerequisite passages differ; later text adds MATHS1090. | Do not silently union/intersect. Historical CSE naming does not prove current identity. |
| EECS 2032, E4 | Lists 1021/1022, 2021, GPA gate, exclusions 2031/3215 and corequisite 2030. | Punctuation/grouping and concurrent-completion meaning need review; corequisite is not component compatibility. |

Sample covers conjunction, alternatives, permission, aggregate grades, ambiguity, exclusions, crosslists and corequisite; connected ISCI, ECON, GL/MATH/MODR and engineering context. It does not establish complete catalog/closure, all grade forms, transfer/repeat policy, current course validity or student eligibility.

## Offerings, meetings and refresh

- Concrete incomplete example (E10): printed p.43 suggests MATH 2030 F/W at MWF 08:30 and MATH 2022 W at TR 14:30. Missing section IDs, end times, campus/room, component links and exceptions. MATH 2022 prerequisite shorthand differs from E2. Advisory schedules are not confirmed live offerings or normalized rules.
- Compatibility (E6/E9): FAQ describes primary/secondary numbered meeting groups, not allowed lecture/lab/tutorial pairs for sampled courses. Application retrieval stopped at login. No valid/invalid actual bundle verified; never invent a Cartesian product of components.
- Dates (E7): regular Term W runs January 4-April 5, 2027; closures include February 15 and March 26. Actual session boundaries are **not inspected actual section meeting dates**. Reading weeks, alternate weeks, period codes and exceptions must precede recurrence expansion. No dated section meeting list verified.
- Campus/unknown time (E6/E8): filtering is documented, not sample campus assignments. ONLN/BLEN may have synchronous/asynchronous elements; ONCA includes in-person assessments. Labels do not prove no timed meetings/travel. Sample campus, room, end times and assessment dates remain unknown, not asynchronous/conflict-free.
- Refresh: single observation; no measured cadence, approved feed/API, stable IDs, validators or access budget. E9 leaves anonymous reliability unresolved. Crawler dates/handbook filename do not support daily-refresh promises.

Future authorized measurement: obtain approved anonymous route or owner export; inspect identical bounded records initially, +24 hours and +7 days within permitted budget. Record status, source revision/modified date if supplied, identifier stability, field differences and manual reconciliation. No-change observations do not prove stability. No authentication/rate-limit bypass.

## Conditional pilot and exit gates

Proposed review set, not enabled coverage: eight canonical courses MATH 1014, 1019, 2001, 2015, 2022, 2030 and EECS 2021, 2032, targeting calendar 2026-27. EECS 1019 is a crosslist, not ninth course. EECS 2011 remains an out-of-scope conflict case. Connected references are unvalidated boundary nodes, not broad ISCI/ECON/PHYS/Glendon expansion. Winter 2027 scheduling deferred; no Keele-only claim without campus records.

Thresholds for separately authorized next work, **not completed checks**:

1. Rights: 100% selected source/use combinations have dated owner/legal decisions separately covering access, redistribution, retention, display and third parties. Approve retention/deletion/access budget before collection; otherwise defer fields or consider links-only research.
2. Catalog: 8/8 have effective-year authority, identifiers, credits, source/check date and independent reviewer sign-off. Resolve every reference or mark outside coverage. Resolve MATH 2015 discrepancy; quarantine conflicts.
3. Rules: independently review at least 12 expected cases across AND/OR/mixed grouping, missing grades, GPA, permission, exclusion, crosslist, concurrent corequisite and source conflict, including satisfied/unsatisfied/unknown. Zero failures become unrestricted. Establish attempts/GPA policy before satisfied grade claims.
4. Scheduling: separately inspect all selected sections/components for at least three offered pilot courses; reconcile declared links and at least one allowed/disallowed bundle. All enabled meetings need actual dates, times, exceptions and campus/location or explicit async evidence. Missing examples leave gate unmet; no verified schedule/export with unknown hard constraints.
5. Refresh: complete three observations; reconcile all sampled differences/failures, identify approved owner/route and measure reliability before SLA. Future extraction validation must cover loss, malformed dates and ID drift; none run now.

### Freshness and unknown policy proposal

Subject to permission display effective period and successful-check date per field; access timestamp is not source update time. Review catalog before year switch/changed-rule activation. Future schedule pilot could require checks within 24 hours and before export **only if** approved access/reliability supports it; otherwise verified scheduling disabled. Proposed threshold, not observed cadence.

On failure keep only permitted last-valid version, mark stale and disable affected verified eligibility/schedule/export claims. Missing records mean unknown, not unrestricted/not offered. Quarantine conflicts/mass loss. Overrides need owner, rationale, source, scope, expiry. Without permission retain no raw/rollback snapshots; approved deletion covers backups. Private history excluded.

### Decisions and go/no-go

- Go for independent research review; conditional catalog review set only. Public replicated catalog and verified scheduler remain no-go pending rights/data gates.
- Manager/user: accept limitations or authorize bounded follow-up; appoint rights/academic-rule owners, decide eight-course boundaries and resolve effective-term discrepancies.
- Choose links-only/catalog-only next scope versus defer. Explicitly authorize milestone 1 separately; research grants no app code/dependencies.
- Independently review exact returned head, then obtain final explicit user merge approval. No deployment or automatic milestone progression.

## Execution and validation

Parent T3 thread: `4af68be2-a104-497d-b2c1-576c666203ab`. Runtime worker task ID: `d093e167-45ad-43ca-b19a-41e74eed7e8b` (delegated-thread binding). Branch: `t3/milestone-zero-research-audit`. Final head/PR and actual checks belong in PR/return, not guessed self-referential commit here.

Required handoff checks: local Markdown/HTML links including templates/changed docs, `git diff --check`, scope/evidence consistency. No app dependencies/tests/build/CI exist; independent review separate. [Manager handoff](../manager-handoff.md) / [roadmap](../milestone-roadmap.md).
