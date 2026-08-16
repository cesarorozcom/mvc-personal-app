# ADR-001: Pipeline de importacion de movimientos desde imagen/camara

## Status
accepted

## Date

2026-08-15

---

## Context

El modulo de movimientos requiere importar datos financieros desde imagenes
(camara o galeria movil) con alta trazabilidad y bajo error operativo. El
proceso OCR puede tener latencia variable, por lo que una respuesta sincrona en
la misma solicitud HTTP degrada UX y aumenta riesgo de timeout. Ademas, se
necesita control de privacidad y auditoria sobre los archivos cargados.

Se decide estandarizar el pipeline de extraccion y confirmacion para cumplir
reglas de negocio del dominio financiero en el stack definido del proyecto.

## Decisiones

1. Se usa AWS Textract (integrado por `boto3`) como servicio OCR principal.
2. Las imagenes de importacion se almacenan en AWS S3 con retencion de 365 dias
   y eliminacion automatica al vencimiento.
3. El procesamiento OCR se ejecuta de forma asincrona mediante una entidad de
   importacion con estados (`queued`, `processing`, `review_required`, `failed`,
   `completed`) y flujo de revision en UI.
4. Se permite importacion parcial: movimientos confiables y movimientos marcados
   como requiere revision manual antes de confirmar.
5. Cuando no se detecta moneda (`currency`), se asigna la moneda base de la
   cuenta y se obliga revision explicita del usuario.
6. Se bloquean duplicados exactos contra todo el historial del usuario usando la
   firma (`date`, `description`, `amount`, `currency`).

## Alternative options

| Alternatives | Pros | Cons |
|--------|------|------|
| OCR local (Tesseract) | Menor dependencia de proveedor cloud | Menor precisión en documentos financieros heterogeneos y mayor costo operativo de ajuste |
| OCR sincrono en request web | Implementacion inicial simple | Riesgo alto de timeout, mala experiencia movil y baja resiliencia ante picos |
| No guardar imagen | Menor riesgo de retencion de datos | Menor capacidad de auditoria y depuracion de extracciones conflictivas |

## Consecuencias

### Positive

- Mayor precision de extraccion y consistencia operativa del pipeline OCR.
- Mejor UX al desacoplar tiempos de procesamiento del flujo interactivo.
- Trazabilidad clara de importaciones y decisiones de usuario en revision.
- Menor riesgo de duplicidad contable por bloqueo contra historial completo.

## Negativas o trade-offs

- Dependencia de servicios AWS (Textract + S3) y costo por uso.
- Mayor complejidad de orquestacion por naturaleza asincrona del flujo.
- Necesidad de monitoreo de estados y reintentos para importaciones fallidas.

## Referencias

- [Spec de la feature](../spec.md)
- [Constitucion del proyecto](../../../.specify/memory/constitution.md)
- Requisito funcional del usuario para importacion desde imagen/camara
