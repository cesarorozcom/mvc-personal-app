# Implementation Plan: Importar movimientos desde imagen o camara

**Branch**: `001-before-specify-hook` | **Date**: 2026-08-15 | **Spec**: `specs/001-importar-movimientos-imagen/spec.md`

**Input**: Feature specification from `/specs/001-importar-movimientos-imagen/spec.md`

## Setup Output

Resultado aplicado segun `.specify/scripts/bash/setup-plan.sh --json` para esta feature activa:

```json
{
  "FEATURE_SPEC": "/Users/czarorozco/Documents/mvc-finance-app/specs/001-importar-movimientos-imagen/spec.md",
  "IMPL_PLAN": "/Users/czarorozco/Documents/mvc-finance-app/specs/001-importar-movimientos-imagen/plan.md",
  "SPECS_DIR": "/Users/czarorozco/Documents/mvc-finance-app/specs/001-importar-movimientos-imagen",
  "BRANCH": "001-before-specify-hook",
  "HAS_GIT": "true"
}
```

## Summary

Se implementara un pipeline de importacion de movimientos financieros desde imagen/camara con OCR en AWS Textract, almacenamiento de imagen en S3 con retencion de 365 dias, revision previa con HTMX y persistencia selectiva de movimientos confirmados. El flujo sera asincrono para cumplir objetivo de UX (<8s para primera propuesta) y mantendra controles de dominio: validacion de esquema, bloqueo de duplicados exactos contra historial completo y marcado explicito de movimientos que requieran revision.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: Django 5.x, django-htmx, boto3 (Textract + S3), psycopg[binary], gunicorn

**Storage**: PostgreSQL (Django ORM) para entidades de dominio + AWS S3 para imagenes de importacion

**Testing**: Django TestCase + pytest + pytest-django + coverage.py (objetivo minimo 80%)

**Target Platform**: Web server Linux en Heroku Container (Dyno Basic), clientes web y mobile web

**Project Type**: Aplicacion web monolitica Django MVC en monorepo

**Performance Goals**: Primera propuesta visible en <= 8 segundos para imagenes <= 10 MB; confirmacion de guardado p95 <= 2 segundos sin OCR

**Constraints**: Acceso autenticado; cifrado TLS en transito; S3 privado por usuario; retencion automatica 365 dias; sin exponer PII en errores; bloqueo estricto de duplicado exacto (`date`,`description`,`amount`,`currency`)

**Scale/Scope**: Feature para usuarios autenticados del modulo de movimientos; hasta 1 imagen por importacion y hasta 100 movimientos propuestos por imagen

## Constitution Check (Pre-Research Gate)

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Spec source exists and follows official `spec-template.md` structure.
- [x] Architecture decision is Django MVC in a monorepo layout.
- [x] Technical stack is Django + PostgreSQL (Django ORM) + Django Templates + HTMX.
- [x] Task generation is blocked until spec status is `approved` (estado actual: `draft`; no se generan `tasks.md` en este comando).
- [x] Test strategy defines evidence for minimum 80% coverage before merge.
- [x] Deployment path is Heroku Container with Dyno Basic and Essential-0 Postgres.

Resultado del gate: PASS.

## Project Structure

### Documentation (this feature)

```text
specs/001-importar-movimientos-imagen/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── import-movements-api.yaml
└── tasks.md            # Fase 2 (/speckit.tasks), no creado en este comando
```

### Source Code (repository root)

```text
apps/
└── movements/
    ├── models.py
    ├── services/
    │   ├── image_import_pipeline.py
    │   ├── textract_client.py
    │   └── duplicate_guard.py
    ├── views/
    │   └── import_views.py
    ├── templates/
    │   └── movements/import/
    │       ├── start.html
    │       ├── review.html
    │       └── _proposal_row.html
    └── urls.py

config/
├── settings/
└── urls.py

tests/
├── unit/movements/
└── integration/movements/
```

**Structure Decision**: Se implementa en una app Django de dominio (`apps/movements`) con vistas delgadas, servicios para OCR/orquestacion/reglas de duplicado y templates HTMX para revision incremental. Esto mantiene separacion MVC y trazabilidad de negocio.

## Phase 0 Research Scope

Preguntas resueltas en `research.md`:

1. Version de Python y librerias base para stack Heroku.
2. Patron asincrono para OCR con estados de importacion.
3. Estrategia de deduplicacion exacta y normalizacion minima de descripcion.
4. Politica de seguridad y ciclo de vida para imagenes en S3.
5. Criterios de confianza para importacion parcial y revision obligatoria.
6. Estrategia de pruebas y evidencia de cobertura >= 80%.

## Phase 1 Design Outputs

- `data-model.md` con entidades, relaciones, reglas de validacion y transiciones.
- `contracts/import-movements-api.yaml` con endpoints de importacion/revision/confirmacion.
- `quickstart.md` con flujo local y validacion funcional.

## Constitution Check (Post-Design Recheck)

- [x] Diseno mantiene MVC Django con logica de negocio en servicios, no en templates.
- [x] Persistencia definida sobre PostgreSQL via Django ORM.
- [x] Interaccion UI definida con Django Templates + HTMX (sin SPA desacoplada).
- [x] Trazabilidad preservada entre spec -> plan -> research/data-model/contracts/quickstart.
- [x] Estrategia de pruebas incluye unidad + integracion y umbral >= 80%.
- [x] Operacion objetivo mantiene Heroku Container + Dyno Basic + Essential-0 Postgres.

Resultado del re-check: PASS.

## Complexity Tracking

No se registran violaciones constitucionales ni excepciones de complejidad para esta fase de planificacion.
