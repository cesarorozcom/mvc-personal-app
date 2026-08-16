# Quickstart: Importar movimientos desde imagen o camara

## Objetivo

Levantar entorno local, ejecutar pruebas del modulo y validar el flujo funcional de importacion OCR con revision y confirmacion.

## Prerequisitos

- Python 3.12
- PostgreSQL disponible para desarrollo
- Credenciales AWS con permisos minimos para S3 y Textract
- Variables de entorno configuradas para Django y AWS

## Variables de entorno sugeridas

- `DJANGO_SETTINGS_MODULE=config.settings.local`
- `DATABASE_URL=postgres://...`
- `AWS_REGION=us-east-1`
- `AWS_ACCESS_KEY_ID=...`
- `AWS_SECRET_ACCESS_KEY=...`
- `IMPORT_IMAGE_BUCKET=finance-import-images-dev`

## Flujo local de ejecucion

1. Instalar dependencias del proyecto.
2. Ejecutar migraciones:
   - `python manage.py migrate`
3. Levantar servidor:
   - `python manage.py runserver`
4. Abrir modulo de movimientos y navegar a opcion de importacion por imagen/camara.
5. Cargar imagen de prueba (<= 10 MB).
6. Verificar que se cree una importacion en estado `queued`/`processing` y luego `review_required`.
7. Revisar propuestas:
   - corregir campos invalidos,
   - confirmar algunos movimientos,
   - descartar otros.
8. Confirmar guardado y verificar:
   - solo se persisten confirmados,
   - duplicados exactos quedan bloqueados,
   - propuestas descartadas no se guardan.

## Suite minima de pruebas

- Unitarias
  - normalizacion y validacion de `date`, `description`, `amount`, `currency`
  - deduplicacion exacta por usuario
  - transiciones de estado de `MovementImport`
- Integracion
  - create import -> OCR result -> review -> confirm
  - caso moneda no detectada con asignacion de moneda base y `requires_review=true`
  - caso importacion parcial con propuestas validas + propuestas para correccion

Comando recomendado:

- `pytest tests/unit/movements tests/integration/movements --cov=apps.movements --cov-report=term-missing`

## Criterios de validacion rapida

- Primera propuesta visible en <= 8 segundos para imagen legible <= 10 MB (entorno normal).
- Ningun movimiento guardado sin `date`, `description`, `amount != 0`, `currency` ISO 4217.
- Cobertura reportada >= 80% sobre el modulo impactado.
