# Tasks: Importar movimientos desde imagen o camara

**Input**: Design documents from /specs/001-importar-movimientos-imagen/

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/import-movements-api.yaml, quickstart.md

**Tests**: REQUIRED. This task list includes tasks to reach and verify >=80% coverage on affected module(s).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

**Traceability**:
- Source spec: /specs/001-importar-movimientos-imagen/spec.md
- Task status tracking: markdown checkbox state is authoritative (`- [ ]` pending, `- [x]` done)

## Phase 0: Specification Gate (Blocking)

**Purpose**: Ensure implementation starts from a valid approved specification.

- [x] T000 Validate spec exists in specs/001-importar-movimientos-imagen/spec.md
- [X] T001 Confirm spec status is approved in specs/001-importar-movimientos-imagen/spec.md
- [X] T002 Link spec and plan references in specs/001-importar-movimientos-imagen/tasks.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize dependencies and project-level configuration for the feature.

- [x] T003 Add OCR and test dependencies in requirements.txt
- [x] T004 [P] Add import image bucket and retention settings in config/settings/base.py
- [x] T005 [P] Add environment variable documentation for AWS and import pipeline in .env.example
- [x] T006 Create movement import URL namespace and routes in apps/movements/urls.py
- [x] T007 [P] Register movement import URLs in config/urls.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the core foundation that all user stories depend on.

**Critical**: No user-story implementation starts before this phase is complete.

- [ ] T008 Create MovementImport and ImportedMovementProposal models in apps/movements/models.py
- [ ] T009 Generate schema migration for import entities in apps/movements/migrations/0001_movement_import_models.py
- [ ] T010 [P] Implement model constraints and state transition helpers in apps/movements/models.py
- [ ] T011 [P] Implement S3 image storage client with private object upload in apps/movements/services/image_storage.py
- [ ] T012 [P] Implement AWS Textract adapter with safe error mapping in apps/movements/services/textract_client.py
- [ ] T013 Implement proposal normalization and schema validation service in apps/movements/services/proposal_validation.py
- [ ] T014 Implement duplicate signature helper for canonical comparison in apps/movements/services/duplicate_guard.py
- [ ] T015 Implement async import orchestration service and status progression in apps/movements/services/image_import_pipeline.py

**Checkpoint**: Foundation ready for independent user story delivery.

---

## Phase 3: User Story 1 - Importar imagen/camara y revisar propuestas (Priority: P1) 🎯 MVP

**Goal**: Permit authenticated users to upload/capture an image, obtain OCR movement proposals, and review before save.

**Independent Test**: Starting from import screen, user submits image <=10 MB and sees import with proposals in review state, with valid schema errors highlighted before confirmation.

### Tests for User Story 1 (REQUIRED)

- [ ] T016 [P] [US1] Add API contract test for POST /api/movement-imports in tests/contract/test_import_movements_api.py
- [ ] T017 [P] [US1] Add API contract test for GET /api/movement-imports/{import_id} in tests/contract/test_import_movements_api.py
- [ ] T018 [P] [US1] Add integration test for camera/gallery upload to review flow in tests/integration/movements/test_import_review_flow.py
- [ ] T019 [P] [US1] Add unit tests for proposal parsing and schema validation in tests/unit/movements/test_proposal_validation.py
- [ ] T020 [US1] Add performance-oriented integration assertion for first proposal <=8s using mocked OCR in tests/integration/movements/test_import_review_flow.py

### Implementation for User Story 1

- [ ] T021 [P] [US1] Implement start import view (multipart upload, auth checks) in apps/movements/views/import_views.py
- [ ] T022 [P] [US1] Implement import detail view (status + proposal payload) in apps/movements/views/import_views.py
- [ ] T023 [US1] Implement service call from view to create queued import and store image in apps/movements/services/image_import_pipeline.py
- [ ] T024 [US1] Implement OCR post-processing to proposal objects in apps/movements/services/image_import_pipeline.py
- [ ] T025 [US1] Add HTML import start page with camera/gallery controls in apps/movements/templates/movements/import/start.html
- [ ] T026 [US1] Add review page template with proposal table and validation markers in apps/movements/templates/movements/import/review.html
- [ ] T027 [P] [US1] Add HTMX proposal row partial in apps/movements/templates/movements/import/_proposal_row.html
- [ ] T028 [US1] Add serializer/response mapping for MovementImport detail in apps/movements/serializers/import_serializers.py
- [ ] T029 [US1] Add structured safe logging for import lifecycle in apps/movements/services/image_import_pipeline.py

**Checkpoint**: User Story 1 is independently functional and testable.

---

## Phase 4: User Story 2 - Importacion parcial y correccion asistida (Priority: P2)

**Goal**: Allow partial imports when OCR confidence is low and require explicit review, including fallback currency assignment.

**Independent Test**: Given low-confidence OCR output or missing currency, user can edit proposals, fallback currency is applied, and only valid reviewed proposals can be confirmed.

### Tests for User Story 2 (REQUIRED)

- [ ] T030 [P] [US2] Add API contract test for PATCH /api/movement-imports/{import_id}/proposals/{proposal_id} in tests/contract/test_import_movements_api.py
- [ ] T031 [P] [US2] Add integration test for missing currency fallback and requires_review=true in tests/integration/movements/test_partial_import_review.py
- [ ] T032 [P] [US2] Add integration test for mixed confidence partial import workflow in tests/integration/movements/test_partial_import_review.py
- [ ] T033 [P] [US2] Add unit tests for confidence bucketing and review flags in tests/unit/movements/test_import_flags.py

### Implementation for User Story 2

- [ ] T034 [US2] Implement proposal patch endpoint for user edits/discard flag in apps/movements/views/import_views.py
- [ ] T035 [US2] Implement proposal update service with field-level validation in apps/movements/services/proposal_validation.py
- [ ] T036 [US2] Implement base account currency fallback and review flag rules in apps/movements/services/image_import_pipeline.py
- [ ] T037 [US2] Implement low-confidence classification thresholds in apps/movements/services/image_import_pipeline.py
- [ ] T038 [US2] Add HTMX interactions for inline proposal edit and discard in apps/movements/templates/movements/import/review.html
- [ ] T039 [P] [US2] Add view helper for manual-assisted capture fallback messaging in apps/movements/views/import_views.py
- [ ] T040 [US2] Add user-facing validation/error messages without PII leakage in apps/movements/forms/import_forms.py

**Checkpoint**: User Story 2 works independently with partial import behavior.

---

## Phase 5: User Story 3 - Bloqueo de duplicados y confirmacion selectiva (Priority: P3)

**Goal**: Prevent exact duplicate persistence and persist only explicitly confirmed proposals.

**Independent Test**: With pre-existing movement duplicates, confirm action persists only valid non-duplicate confirmed proposals and reports blocked/discarded counts.

### Tests for User Story 3 (REQUIRED)

- [ ] T041 [P] [US3] Add API contract test for POST /api/movement-imports/{import_id}/confirm in tests/contract/test_import_movements_api.py
- [ ] T042 [P] [US3] Add integration test for duplicate block enforcement on confirm in tests/integration/movements/test_confirm_duplicate_blocking.py
- [ ] T043 [P] [US3] Add integration test verifying confirmed-only persistence and discard exclusion in tests/integration/movements/test_confirm_duplicate_blocking.py
- [ ] T044 [P] [US3] Add unit tests for canonical duplicate signature normalization in tests/unit/movements/test_duplicate_guard.py

### Implementation for User Story 3

- [ ] T045 [US3] Implement confirm endpoint and summary response payload in apps/movements/views/import_views.py
- [ ] T046 [US3] Implement confirm service to persist only confirmed proposals in apps/movements/services/image_import_pipeline.py
- [ ] T047 [US3] Implement exact duplicate query against full user movement history in apps/movements/services/duplicate_guard.py
- [ ] T048 [US3] Add duplicate block reason propagation to proposal model fields in apps/movements/models.py
- [ ] T049 [US3] Add import completion state transition and counters in apps/movements/services/image_import_pipeline.py
- [ ] T050 [P] [US3] Add DB index for duplicate lookup performance in apps/movements/migrations/0002_duplicate_lookup_index.py
- [ ] T051 [US3] Add review UI indicators for blocked duplicates and confirm summary in apps/movements/templates/movements/import/review.html

**Checkpoint**: User Story 3 is independently functional and testable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Complete hardening, documentation, and coverage verification.

- [ ] T052 [P] Add end-to-end happy/edge path walkthrough doc in specs/001-importar-movimientos-imagen/quickstart.md
- [ ] T053 [P] Add operational runbook for OCR/S3 failures in docs/operations/import-movements.md
- [ ] T054 Refine secure error handling and logging redaction in apps/movements/services/image_import_pipeline.py
- [ ] T055 [P] Add lifecycle retention configuration validation test for S3 365-day policy in tests/integration/movements/test_image_retention_policy.py
- [ ] T056 Run full feature test suite with coverage threshold >=80% in tests/pytest.ini
- [ ] T057 Generate and archive coverage report artifact for review in reports/coverage/import-movements.txt
- [ ] T058 Final cleanup and consistency pass across movements import module in apps/movements/

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 0 -> Phase 1 -> Phase 2 -> User Story phases (3, 4, 5) -> Phase 6
- User stories depend on completion of Phase 2 only.
- Phase 6 depends on completion of all implemented user stories.

### User Story Dependencies

- US1 (P1): Starts after Phase 2, no dependency on US2/US3.
- US2 (P2): Starts after Phase 2, independent from US1 but reuses foundational services.
- US3 (P3): Starts after Phase 2, independent validation path but integrates confirm behavior with foundational models.

### Within-Story Order

- Tests first and failing expectation before implementation.
- View/API contracts before service integration in each story.
- Service implementation before final UI polish for that story.

---

## Parallel Opportunities

- Setup: T004, T005, T007 can run in parallel.
- Foundational: T011, T012, T013, T014 can run in parallel after T008/T009 baseline.
- US1 tests: T016, T017, T018, T019 can run in parallel.
- US1 UI/API split: T021, T022, T027 can run in parallel.
- US2 tests: T030, T031, T032, T033 can run in parallel.
- US3 tests: T041, T042, T043, T044 can run in parallel.
- Cross-story: US2 and US3 can be staffed in parallel after Phase 2.

---

## Parallel Example: User Story 1

- Run together: T016, T017, T018, T019
- Run together: T021, T022, T027

## Parallel Example: User Story 2

- Run together: T030, T031, T032, T033
- Run together: T036, T037, T039

## Parallel Example: User Story 3

- Run together: T041, T042, T043, T044
- Run together: T047, T050

---

## Implementation Strategy

### MVP First (US1)

1. Complete Phase 0, 1, and 2.
2. Complete US1 end-to-end (Phase 3).
3. Validate US1 independent test criteria.
4. Run coverage checks and ensure >=80% in affected module(s).

### Incremental Delivery

1. Deliver US1 (core import + review) as first production increment.
2. Deliver US2 (partial import and manual correction) as second increment.
3. Deliver US3 (duplicate blocking and selective confirmation) as third increment.
4. Execute Phase 6 hardening and final coverage reporting.

### Team Parallelization

1. Team aligns on Phase 0-2 together.
2. After Phase 2:
   - Engineer A: US1 completion/hardening.
   - Engineer B: US2 implementation.
   - Engineer C: US3 implementation.
3. Merge with contract/integration tests as gate.

---

## Notes

- All tasks follow strict checklist format: checkbox + TaskID + optional [P] + optional [USx] + file path.
- Testing tasks are explicitly included per story and coverage enforcement is included in T056/T057.
- Suggested first scope for executable MVP is US1 only.
