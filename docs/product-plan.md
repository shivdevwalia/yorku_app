# Product plan

## Status and product

Approved baseline for [issue #3](https://github.com/shivdevwalia/yorku_app/issues/3), with Python mandatory for the backend. Documentation is awaiting merge/review. Milestone-0 execution is not authorized. See [roadmap](milestone-roadmap.md) and [handoff](manager-handoff.md).

Long-term: all-in-one academic planning across York faculties. First release: trustworthy next-term planning, not enrolment or official advice. All faculties supported by design; features enabled only for validated coverage. EECS/MATH plus connected subjects are candidates, not fixed pilot scope until data feasibility. Advanced professional/graduate programs come later.

## First release

- Explorer: codes, descriptions, credits, prerequisites, corequisites, exclusions, crosslistings, offerings, official links, provenance/freshness and coverage limits.
- Requirement navigator: AND/OR and satisfied/unsatisfied/unknown explanations; manual completed/in-progress history with attempts and grades.
- Valid section/component bundles, date-aware conflicts, blocked time, pinned sections, explainable ranked alternatives.
- Saved plans record inputs, dataset/algorithm/scoring versions; flag stale data and revalidate. Calendar export uses dated meetings; not enrolment or guaranteed continuing synchronization.
- Correction reporting routes errors to review, never directly overwrites published data. Phone/keyboard accessibility, accessible labels, and equivalent text graph navigation are required.

Public exploration requires no account; accounts optional for persistence/personalization. Define privacy, deletion, access controls before private history storage. No Passport York credentials/sessions, automatic enrolment, student-facing chatbot, or paid LLM API dependencies. All planning deterministic.

Later: licensed ratings (not a dependency), reviewed degree roadmaps, opt-in friends/freebusy, group optimization, graduation what-if. Sharing requires minimized data, consent/revocation; raw history is not a default social payload.

## Architecture

Python owns API, domain algorithms, ingestion, validation, jobs: modular monolith plus worker. Proposed concrete choices to validate during technical foundation: FastAPI, Pydantic, SQLAlchemy/Alembic. PostgreSQL stores structured/versioned data; object storage holds permitted source evidence. No installation now.

Next.js/TypeScript frontend communicates via versioned API/contracts generated or validated from OpenAPI. It renders explanations/provisional feedback, not a duplicated authoritative eligibility engine. Contract compatibility and integration checks enforce boundaries. Proposed React Flow graph has an equivalent navigable text alternative.

Start bounded Python constraint search, separate from HTTP/storage/adapters. Consider OR-Tools for complex later allocation only if warranted; do not install now.

## Deterministic semantics

Typed AST: AND, OR, course/credit conditions, grade thresholds, permission conditions. Preserve source text/pointers. Unsupported/ambiguous rules remain unknown; parse failure never becomes no prerequisites. Manual history is evidence, not official equivalence. In-progress work is not completed without explicit rule-specific assumptions. Missing grades, unresolved transfers, and unverified permissions remain unknown.

AND: unsatisfied if any child unsatisfied, satisfied only if all satisfied, otherwise unknown. OR: satisfied if any child satisfied, unsatisfied only if all unsatisfied, otherwise unknown. Grade/permission nodes require corresponding evidence. Evaluate exclusions and concurrent corequisites within proposed selections.

AND/OR goal search expands conjunctions/alternatives, deduplicates goals, detects cycles, explains blocked/uncertain branches. Requirement graph is not a verified degree audit. Search limits yield incomplete-search status, not false no-solution claims.

Hard rules: valid offering/section/component bundles, lecture/lab/tutorial compatibility, pins, blocked time, conflicts. Check actual date ranges, recurrence, exceptions, campuses/travel buffers, not weekday overlap alone. Explicit async differs from unknown time/date/location; unknown evidence prevents verified-feasible claims. Distinguish verified feasibility, provisional results, infeasibility.

Soft preferences: times, gaps, travel, compact days. Document weights/stable tie-breaks; version scoring and explain contributions. Never trade hard constraints for score. Record candidate/time/expansion limits and assumptions. Say best found within limits, not globally optimal without completeness evidence. Explain no solution through constraints/missing evidence; suggest user-controlled relaxations without silently weakening mandatory rules.

## Entities

| Area | Entities |
| --- | --- |
| Organization | Faculty, department, subject, campus, session, term, academic calendar |
| Catalog | Stable course, course version, historical/alternate identifiers, typed relationships, requirement trees |
| Delivery | Offering, section, component, meeting, compatibility; instructor and instructor assignment |
| Degree | Program, program version/calendar, program requirements |
| Personal | User, profile, attempt/status/grade, plan, blocked time, selection/pin, assumptions and versions |
| Operations | Source, snapshot/evidence, ingestion run, validation result, review override, published dataset/publication pointer |
| Later sharing | Consent, sharing relationship, freebusy projection, revocation |

Calendar version differs from teaching term; instructor assignment differs from course identity. Preserve historical interpretation for reproducibility. Source identifiers are not the sole identity key. Crosslisting requires explicit equivalence/double-counting semantics, not assumed interchangeable degree credit.

## Data trust and rights

Candidate sources: official York calendars, course timetables, faculty rules. No production feed, parser, or live extraction verified. User authorized access/scraping, but redistribution, retention, display, and third-party rights remain separately unverified. This documentation performs no scraping or rights research.

Pipeline: fetch -> permitted evidence -> parse -> normalize -> validate -> review -> publish versioned snapshots. Record source URL, retrieval time, effective calendar/term, parser version, findings, field-level provenance where feasible. Display freshness/coverage. Daily offering refresh is provisional until permissions, change frequency, reliability, and cost are measured, not a service promise.

Quarantine failures; retain last valid publication with stale warnings. Detect mass course/section/rule loss, identifier drift, malformed dates, invalid references, unexpected changes. Failed extraction never means no prerequisites or not offered. Resolve source conflicts via documented precedence/review, retaining evidence. Overrides require rationale, author, provenance, scope, expiry/recheck. Publish atomically, retain permitted rollback snapshots, revalidate affected plans after publication/rollback.

Official references supplied for context, not proof of feeds or rights:

- [Visual Schedule Builder](https://registrar.yorku.ca/enrol/guide/vsb)
- [Degree Progress Report](https://myacademicrecord.students.yorku.ca/degree-progress-report)
- [Course timetable FAQ](https://registrar.yorku.ca/courses_site/faq.html)
- [Applying to graduate](https://registrar.yorku.ca/graduation/apply)

## Quality

Require traceable sources, visible unknowns, feasible schedules, no-solution explanations, student usability, phone/keyboard access, text/graph parity, reproducible/versioned results. Never imply unvalidated coverage.

When app exists: frontend type/lint/build; Python lint/type/domain tests; ingestion fixture regression; generated contract compatibility; integration. Add stable required checks later, once reliable checks exist. Today: no application dependencies, build command, tests, or configured CI validation. Documentation checks are not application tests.
