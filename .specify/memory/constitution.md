<!--
Sync Impact Report
- Version change: N/A -> 1.0.0
- Modified principles:
	- Principle 1 -> I. Arquitectura MVC y Monorepo (NO NEGOCIABLE)
	- Principle 2 -> II. Stack Tecnologico Obligatorio
	- Principle 3 -> III. Especificacion Antes de Tareas y Trazabilidad
	- Principle 4 -> IV. Calidad de Pruebas y Cobertura Minima
	- Principle 5 -> V. Despliegue Estandar en Heroku y Operabilidad
- Added sections:
	- Additional Constraints
	- Development Workflow
- Removed sections:
	- None
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md
	- ✅ .specify/templates/spec-template.md
	- ✅ .specify/templates/tasks-template.md
	- ✅ templates/spec-template.md
	- ⚠ pending .specify/templates/commands/*.md (directory does not exist in this repository)
	- ✅ .github/copilot-instructions.md (reviewed, no stale references found)
- Deferred TODOs:
	- TODO(RATIFICATION_DATE): Confirm original ratification date of the constitution.
-->

# MVC Finance App Constitution

## Core Principles

### I. Arquitectura MVC y Monorepo (NO NEGOCIABLE)
Todas las implementaciones MUST seguir arquitectura MVC de Django y vivir en un
monorepo unico. Cada cambio funcional MUST mapearse a capas de modelo, vista
y template segun corresponda, evitando logica de negocio embebida en templates.
Rationale: mantener separacion de responsabilidades, escalabilidad del dominio
y consistencia en colaboracion.

### II. Stack Tecnologico Obligatorio
El backend MUST usar Django; persistencia MUST usar PostgreSQL a traves de
Django ORM; frontend MUST usar Django Templates + HTMX. No se permite introducir
frameworks alternativos de backend, ORMs paralelos o SPAs desacopladas sin una
enmienda explicita de la constitucion. Rationale: reducir complejidad operativa
y maximizar productividad con un stack coherente.

### III. Especificacion Antes de Tareas y Trazabilidad
Ninguna tarea de implementacion MUST crearse sin una especificacion previa que
respete la plantilla oficial `spec-template.md`. Toda tarea MUST enlazar su
spec fuente y MUST registrar un estado de implementacion verificable
(draft/approved/implemented para specs; pending/in-progress/done para tareas).
Rationale: asegurar trazabilidad de decisiones, alcance controlado y auditoria.

### IV. Calidad de Pruebas y Cobertura Minima
Toda entrega MUST incluir pruebas unitarias e integracion suficientes para
alcanzar al menos 80% de cobertura total del codigo modificado y del modulo
impactado. Un cambio NO cumple Definition of Done si no demuestra cobertura en
CI o evidencia equivalente reproducible. Rationale: reducir regresiones en un
sistema financiero y sostener evolucion segura.

### V. Despliegue Estandar en Heroku y Operabilidad
El despliegue productivo MUST realizarse en Heroku Container con Dyno Basic y
Heroku Postgres Essential-0. Configuracion, migraciones y secretos MUST estar
externalizados por variables de entorno y procedimientos reproducibles.
Rationale: mantener un camino de despliegue unico, simple y operable.

## Additional Constraints

- Django apps MUST mantener responsabilidades claras: modelos en `models.py` o
	`models/`, casos de uso en servicios y vistas delgadas.
- Toda consulta compleja MUST implementarse con Django ORM de forma legible,
	testeada y sin SQL crudo salvo justificacion documentada en ADR.
- HTMX MUST usarse para interactividad incremental y degradacion progresiva; los
	templates MUST permanecer accesibles sin JavaScript critico.
- Cambios de infraestructura MUST documentarse en ADR antes de implementacion.

## Development Workflow

1. Especificar: crear `spec.md` usando exactamente la plantilla oficial.
2. Planificar: producir `plan.md` con chequeo de constitucion aprobado.
3. Generar el ADR (Architecture Decision Record) para decisiones de stack, arquitectura o
   despliegue según `adr-template.md`.
4. Tareas: generar `tasks.md` solo desde una spec aprobada.
5. Implementar: ejecutar tareas actualizando estado de cada una.
6. Validar: ejecutar pruebas y verificar cobertura >= 80% antes de merge.
7. Desplegar: aplicar migraciones y publicar en Heroku con checklist operativo.

Code review MUST verificar cumplimiento de los principios I-V, evidencia de
pruebas y trazabilidad entre spec, plan, tareas y commits.

## Governance
Esta constitucion prevalece sobre practicas informales del repositorio.
Enmiendas MUST incluir: propuesta escrita, impacto en plantillas y plan de
migracion si aplica. El versionado sigue SemVer de gobernanza:

- MAJOR: eliminacion o redefinicion incompatible de principios.
- MINOR: adicion de principios/secciones o expansion normativa material.
- PATCH: aclaraciones editoriales sin cambio de obligacion.

Toda PR MUST incluir una seccion de cumplimiento constitucional y evidencias
objetivas (tests, cobertura, enlaces a spec/plan/tasks). Revision de cumplimiento
MUST ocurrir al menos en cada merge a rama principal.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Confirm original adoption date. | **Last Amended**: 2026-08-15
