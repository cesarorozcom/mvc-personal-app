# Spec: Importar movimientos desde imagen o camara

## Metadata

| Campo | Valor |
|------|-------|
| Author| GitHub Copilot|
| Date | 2026-08-15|
| Status| draft|

### Alineacion Constitucional (obligatoria)

- **Arquitectura**: MVC en monorepo
- **Stack backend**: Django
- **Base de datos y ORM**: PostgreSQL + Django ORM
- **Frontend**: Django Templates + HTMX
- **Despliegue objetivo**: Heroku Container + Dyno Basic + Essential-0 Heroku Postgres
- **Cobertura minima de pruebas**: >= 80%

---

## Contexto y motivacion

Los usuarios de un gestor financiero suelen registrar movimientos manualmente, lo
que incrementa tiempo operativo y errores de digitacion. Este modulo permite
importar movimientos desde una imagen (recibo, comprobante, captura de estado de
cuenta) o desde la camara del dispositivo movil para acelerar la carga de datos.

Sin esta capacidad, la friccion de captura reduce la frecuencia de uso y limita
la calidad del historial financiero, impactando reportes, presupuestos y
seguimiento de flujo de caja.

## Clarifications

### Session 2026-08-15

- Q: Como se manejan duplicados frente al historial existente? -> A: Bloquear duplicados exactos contra todo el historial del usuario (`date`, `description`, `amount`, `currency`).
- Q: Donde y por cuanto tiempo se conservan las imagenes de importacion? -> A: Guardar la imagen en un bucket AWS S3 con retencion de 365 dias.
- Q: Que hacer cuando no se detecta `currency`? -> A: Asignar moneda base de la cuenta y marcar para revision antes de guardar.
- Q: Como manejar extraccion parcial en una imagen? -> A: Aceptar importacion parcial con movimientos marcados para revision manual.
- Q: Que libreria/servicio usar para extraer informacion de imagen? -> A: AWS Textract usando boto3.

---

## Requerimientos Funcionales

1. El sistema debe permitir al usuario cargar una imagen existente o capturar
   una foto desde un dispositivo movil para iniciar la importacion de
   movimientos.
2. El sistema debe extraer y proponer uno o mas movimientos a partir del
   contenido detectado en la imagen.
3. Cada movimiento propuesto debe contener el siguiente esquema:
   - `date`: fecha en formato ISO 8601 `YYYY-MM-DD`.
   - `description`: texto del movimiento tal como fue ingresado o detectado.
   - `amount`: numero con signo donde positivo representa ingreso
     (credit-money-in) y negativo representa egreso (debit-money-out).
   - `currency`: codigo ISO 4217 (por ejemplo: ARS, USD, COP).
4. El sistema debe mostrar una vista de revision previa al guardado para que el
   usuario confirme, edite o descarte cada movimiento propuesto.
5. El sistema debe validar formato y completitud de los campos antes de guardar
   movimientos confirmados.
6. El sistema debe registrar solamente los movimientos confirmados por el
   usuario.
7. El sistema debe bloquear duplicados exactos contra todo el historial del
  usuario (mismo `date`, `description`, `amount`, `currency`) e informar el
  motivo del bloqueo en la vista de revision.
8. El sistema debe informar de manera clara cuando una imagen no permite extraer
   movimientos confiables y ofrecer captura manual asistida.
9. El sistema debe almacenar cada imagen de importacion en un bucket AWS S3
  con retencion de 365 dias y eliminarla automaticamente al vencimiento.
10. Cuando no se detecte `currency`, el sistema debe asignar la moneda base de
  la cuenta y marcar el movimiento para revision explicita del usuario antes
  de confirmar el guardado.
11. El sistema debe permitir importacion parcial: movimientos con alta
   confiabilidad y movimientos marcados como "requiere revision" para
   correccion manual antes de confirmar.

---

## Requerimientos No Funcionales

- **Performance** La primera propuesta de movimientos debe mostrarse en menos de
  8 segundos para imagenes de hasta 10 MB en condiciones normales de red.
- **Seguridad** Las imagenes y datos extraidos deben procesarse bajo acceso
  autenticado, con proteccion de datos en transito y sin exponer informacion
  sensible en mensajes de error. Las imagenes almacenadas en S3 deben tener
  acceso restringido por usuario y ciclo de vida de eliminacion automatica a
  los 365 dias.
- **Mantenibilidad** Las reglas de validacion del esquema de movimiento deben
  centralizarse para reutilizacion y pruebas consistentes.

---

## Casos de uso / escenarios

### Escenario 1: Importar desde camara y confirmar movimientos

- **Actor:** Usuario autenticado
- **Precondiciones:** El usuario tiene acceso al modulo de movimientos y
  permisos para usar camara del dispositivo.
- **Flujo principal:**
  1. El usuario abre la opcion de importar movimientos.
  2. Captura una imagen desde la camara.
  3. El sistema procesa la imagen y propone movimientos con el esquema definido.
  4. El usuario revisa y corrige campos si es necesario.
  5. El usuario confirma el guardado.
- **Flujo alternativo:** Si algun campo requerido es invalido, el sistema marca
  el error y solicita correccion antes de permitir confirmar.
- **Postcondiciones:** Los movimientos confirmados quedan almacenados en el
  historial financiero del usuario.

---

### Escenario 2: Importar desde galeria con baja calidad de lectura

- **Actor:** Usuario autenticado
- **Precondiciones:** El usuario dispone de una imagen en galeria.
- **Flujo principal:**
  1. El usuario selecciona una imagen desde galeria.
  2. El sistema intenta extraer movimientos.
  3. El sistema detecta baja confiabilidad en la extraccion.
  4. El sistema muestra propuesta parcial y habilita edicion manual asistida.
  5. El usuario completa/corrige datos y confirma.
- **Flujo alternativo:** Si no se puede proponer ningun movimiento, el sistema
  ofrece crear movimientos manualmente con campos prellenados cuando sea
  posible.
- **Postcondiciones:** Se guardan solo los movimientos confirmados por el
  usuario; los no confirmados se descartan.

---

## Entidades clave

- **Movimiento**: registro financiero individual con `date`, `description`,
  `amount`, `currency`.
- **Importacion de movimientos**: sesion de carga desde imagen/camara que agrupa
  movimientos propuestos, corregidos, confirmados y descartados.

---

## Supuestos

- El modulo aplica a usuarios autenticados con acceso a su propio historial.
- El usuario puede editar cualquier campo propuesto antes de confirmar.
- La moneda por defecto de sugerencia puede inferirse por contexto, pero siempre
  debe quedar explicitada en el campo `currency` antes de guardar.

---

## Criterios de aceptacion
- [ ] El 95% de las importaciones con imagen legible generan al menos un
      movimiento propuesto sin reintento manual de carga.
- [ ] El 100% de los movimientos guardados cumplen formato valido en `date`
      (ISO 8601), `amount` (numero con signo) y `currency` (ISO 4217).
- [ ] Al menos el 90% de usuarios piloto completa una importacion y confirmacion
      en menos de 90 segundos.
- [ ] El 100% de movimientos descartados no aparece en el historial final.

---

## Alternativas consideradas

| Alternativa | Pros | Contras |
|--------|------|------|
| Carga manual exclusiva | Control total del usuario y menor ambiguedad | Mayor tiempo de registro y menor adopcion por friccion |
| Importacion automatica sin revision previa | Flujo rapido con menos pasos | Mayor riesgo de errores y menor confianza de usuario |
| Importacion con revision previa (elegida) | Balance entre velocidad y exactitud, con control de usuario | Requiere una etapa adicional de confirmacion |

---

## Decisiones Tomadas

Se adopta un flujo de importacion asistida con confirmacion humana antes del
persistido final. Esto prioriza calidad de datos financieros y reduce el riesgo
operativo frente a importaciones completamente automaticas.

Tambien se normaliza el esquema de movimiento con formatos estandar (ISO 8601 e
ISO 4217) para facilitar interoperabilidad, reporte y validacion consistente.

Para la extraccion de informacion desde imagen/camara se define AWS Textract,
integrado desde backend con boto3, para estandarizar el pipeline OCR del modulo.

Las decisiones arquitectonicas y trade-offs del pipeline quedan formalizadas en
el ADR de esta feature.

---

## Referencias

- Plantilla oficial de especificacion del repositorio.
- Constitucion del proyecto vigente.
- Requisito de feature: importacion de movimientos desde imagen o camara.
- ADR: [ADR-001 Pipeline importacion movimientos](adr/ADR-001-pipeline-importacion-movimientos.md)
