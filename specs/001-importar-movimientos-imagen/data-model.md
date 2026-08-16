# Data Model: Importar movimientos desde imagen o camara

## Entity: MovementImport

Descripcion: sesion de importacion iniciada por un usuario a partir de una imagen.

Fields:
- id: UUID (PK)
- user_id: UUID/FK -> User (owner)
- account_id: UUID/FK -> Account (cuenta destino)
- source_type: enum(`camera`, `gallery`, `upload`)
- status: enum(`queued`, `processing`, `review_required`, `failed`, `completed`)
- image_storage_key: string(512)
- image_content_type: string(100)
- image_size_bytes: integer (max 10 * 1024 * 1024)
- extraction_engine: string (default `aws_textract`)
- extraction_started_at: datetime nullable
- extraction_finished_at: datetime nullable
- error_code: string(64) nullable
- error_message_safe: string(512) nullable
- created_at: datetime
- updated_at: datetime

Validation Rules:
- `status` debe seguir transiciones validas.
- `image_size_bytes` <= 10485760.
- `image_storage_key` obligatorio luego de carga exitosa.
- `error_message_safe` nunca debe contener PII.

State Transitions:
- `queued` -> `processing`
- `processing` -> `review_required`
- `processing` -> `failed`
- `review_required` -> `completed`
- `review_required` -> `failed` (si ocurre error de persistencia final)

## Entity: ImportedMovementProposal

Descripcion: movimiento propuesto por OCR y/o editado por usuario antes del guardado.

Fields:
- id: UUID (PK)
- import_id: UUID/FK -> MovementImport
- proposal_index: integer
- date: date nullable
- description: string(255) nullable
- amount: decimal(14,2) nullable
- currency: char(3) nullable
- confidence_score: decimal(5,4) nullable
- requires_review: boolean default true
- is_duplicate_blocked: boolean default false
- duplicate_reason: string(255) nullable
- is_discarded: boolean default false
- is_confirmed: boolean default false
- source_raw_text: text nullable
- created_at: datetime
- updated_at: datetime

Validation Rules:
- `currency` debe ser ISO 4217 (3 letras mayusculas) antes de confirmar.
- `amount` debe tener signo (`>0` ingreso, `<0` egreso, `0` invalido).
- `description` no vacia y longitud 3..255 antes de confirmar.
- `date` obligatoria en formato ISO (persistida como tipo date).
- Si `currency` fue inferida por moneda base, `requires_review` debe permanecer true hasta confirmacion explicita del usuario.

Business Rules:
- Duplicado exacto por usuario (`date`,`description_normalized`,`amount`,`currency`) bloquea confirmacion individual.
- Proposal descartada (`is_discarded=true`) no se persiste como movimiento final.

## Entity: Movement (existente en dominio)

Descripcion: registro financiero definitivo en historial del usuario.

Campos minimos relevantes para esta feature:
- id
- user_id
- account_id
- date
- description
- amount
- currency
- created_at

Integridad:
- Recomendado indice compuesto para busqueda de duplicados por usuario:
  - `(user_id, date, description_normalized, amount, currency)`

## Relationship Summary

- Un `MovementImport` pertenece a un `User` y a una `Account`.
- Un `MovementImport` tiene muchos `ImportedMovementProposal`.
- Un `ImportedMovementProposal` confirmado genera exactamente un `Movement`.
- Un `MovementImport` puede terminar sin `Movement` guardados (fallo o descarte total).

## Derived/Computed Fields

- description_normalized (en validacion/deduplicacion): trim + lowercase + colapso de espacios.
- confidence_bucket:
  - `high` si `confidence_score >= 0.85`
  - `medium` si `0.60 <= confidence_score < 0.85`
  - `low` si `< 0.60`

Regla de revision:
- `medium` y `low` siempre `requires_review=true`.
- `high` puede iniciar en `requires_review=false` excepto moneda inferida o duplicado bloqueado.
