# Research: Importar movimientos desde imagen o camara

## Decision 1: Runtime y version base

- Decision: Usar Python 3.12 con Django 5.x en contenedor Heroku.
- Rationale: Python 3.12 ofrece soporte vigente, buen rendimiento y compatibilidad estable con Django 5.x, boto3 y toolchain de pruebas.
- Alternatives considered:
  - Python 3.11: estable, pero menor horizonte de soporte.
  - Python 3.13: mas reciente, con mayor riesgo de incompatibilidades tempranas en dependencias.

## Decision 2: Orquestacion de OCR

- Decision: Pipeline asincrono con entidad de importacion y estados (`queued`, `processing`, `review_required`, `failed`, `completed`).
- Rationale: Evita timeouts HTTP y permite mostrar progreso while Textract procesa, manteniendo UX bajo objetivo de 8s para primera propuesta.
- Alternatives considered:
  - OCR sincrono en request web: implementacion simple, pero peor resiliencia y UX.
  - Cola externa dedicada desde dia 1: mayor robustez, pero sobrecosto de complejidad para primera version.

## Decision 3: Extraccion de datos financieros

- Decision: Usar AWS Textract via boto3 con post-procesado de reglas de dominio (fecha, monto con signo, moneda, descripcion).
- Rationale: Mejor precision general en documentos de tickets/comprobantes y alineacion con decisiones del ADR.
- Alternatives considered:
  - Tesseract local: menor costo variable cloud, pero menor precision y mayor costo operativo de ajuste.
  - Servicios OCR alternativos: sin decision previa en el proyecto y menor alineacion con stack AWS ya adoptado.

## Decision 4: Deteccion de duplicados

- Decision: Bloquear duplicados exactos por usuario usando firma canonica (`date`, `description`, `amount`, `currency`) con comparacion case-insensitive y trim de descripcion.
- Rationale: Cumple requerimiento funcional de bloqueo estricto y reduce falsos negativos triviales por diferencias cosmeticas.
- Alternatives considered:
  - Duplicado difuso con similitud textual: mayor complejidad y riesgo de falsos positivos.
  - No normalizar descripcion: mas simple, pero deja pasar duplicados por variaciones menores.

## Decision 5: Moneda no detectada

- Decision: Asignar `currency` con moneda base de la cuenta y marcar el movimiento como `requires_review=true`.
- Rationale: Permite importacion parcial sin perder trazabilidad ni introducir guardado automatico ambiguo.
- Alternatives considered:
  - Rechazar movimiento sin moneda: reduce errores, pero incrementa friccion y baja tasa de importacion.
  - Inferencia por heuristicas de texto/pais: util, pero propensa a errores silenciosos.

## Decision 6: Retencion y seguridad de imagenes

- Decision: Guardar imagen original en S3 privado (prefijo por usuario/importacion), cifrado en reposo SSE-S3 y lifecycle de 365 dias.
- Rationale: Cumple auditoria y requisito de retencion, minimizando riesgo de exposicion mediante acceso privado y URLs firmadas de corta vida.
- Alternatives considered:
  - No conservar imagen: menor riesgo de retencion, pero sin trazabilidad para soporte.
  - Retencion indefinida: mas capacidad de auditoria historica, pero costo y riesgo de privacidad mayores.

## Decision 7: Contrato de interfaz

- Decision: Exponer endpoints HTTP para crear importacion, editar propuestas, consultar estado y confirmar guardado; renderizar revision via templates/fragmentos HTMX.
- Rationale: Mantiene arquitectura Django MVC, UX incremental y desacopla cliente de pipeline OCR.
- Alternatives considered:
  - API JSON completa + SPA: fuera de la constitucion actual.
  - Form POST unico con flujo completo: poca observabilidad y mala experiencia en escenarios parciales.

## Decision 8: Estrategia de pruebas

- Decision: Combinar pruebas unitarias (parseo, validacion, deduplicacion, transiciones) e integracion (flujo crear->revisar->confirmar), con cobertura minima de 80%.
- Rationale: Las reglas de dominio y el flujo de estados requieren evidencia tanto aislada como end-to-end del modulo.
- Alternatives considered:
  - Solo integracion: alta confianza funcional, pero debugging mas costoso.
  - Solo unitarias: rapido, pero insuficiente para validar interaccion completa.

## Resolved Uncertainties

Todas las incertidumbres de contexto tecnico quedaron resueltas en decisiones concretas y alineadas con constitucion + ADR.
