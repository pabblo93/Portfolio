# Mercado Eléctrico — Herramientas de Facturación e Indexación

Scripts desarrollados para la automatización de procesos de facturación de contratos indexados a mercado en el sector eléctrico español.

---

## Programas

### `Descarga_Matriz_OMIE_SQ.py`
Descarga automáticamente los precios cuartohorarios del mercado diario español desde la web pública de OMIE y construye la matriz mensual completa (96 cuartohoras × días del mes). El fichero de salida replica el formato oficial de OMIE, incluyendo medias por tramo y gestión automática de versiones de fichero.

**Resuelve:** la descarga y estructuración manual de precios de mercado para su uso en facturación de contratos indexados.

---

### `expansion_precios_horario_cuartohorario.py`
Transforma precios horarios exportados desde sistemas de liquidación a granularidad cuartohoraria, generando un Excel con los 96 cuartohoras diarios y todos los componentes de precio desagregados. Desarrollado tras el cambio regulatorio de octubre 2024 que introdujo la facturación cuartohoraria.

**Resuelve:** la adaptación de datos horarios al nuevo marco regulatorio cuartohorario sin pérdida de información por componente.

---

### `calculo_prdemcad_liquidacion_c2.ipynb`
Calcula el precio de demanda por servicios de ajuste (PRDEMCAD) a partir de los ficheros de Liquidación Común (C2) de REE. Parsea el ZIP de liquidación, clasifica las variables horarias y cuartohorarias, aplica las fórmulas oficiales de cada componente (RT3, RT6, CT3, CFP, BALX, SECX, BS3, RAD3, EXD, IN3, IN7) e incluye un control de coherencia contra el PRDEMCAD oficial. El resultado se exporta a Excel listo para incorporar a la factura.

**Resuelve:** el cálculo y auditoría de los servicios de ajuste en contratos indexados Passthrough, proceso anteriormente manual y propenso a errores.
