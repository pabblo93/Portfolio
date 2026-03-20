# Datos de simulación

Esta carpeta es un marcador de posición. Los archivos de datos reales **no se distribuyen** con el proyecto por su tamaño y porque son específicos del entorno de trabajo.

---

## Configuración de DATA_ROOT

Al inicio de cada notebook encontrarás una celda de configuración:

```python
# ============================================================
# CONFIGURACIÓN DE RUTAS — Ajusta DATA_ROOT a tu entorno
# ============================================================
import pathlib

DATA_ROOT = pathlib.Path(
    r"C:\Users\pablo\OneDrive - Universidad Politécnica de Madrid\THN\Prácticas"
)

P1 = DATA_ROOT / "Practica 1"   # Archivos COBAYA (.CON, .txt)
P2 = DATA_ROOT / "Practica 2"   # Outputs CTF (.out)
```

Modifica la variable `DATA_ROOT` para que apunte a la carpeta donde tienes los datos.

---

## Estructura de datos esperada

### Práctica 1 — COBAYA (neutrónica)

```
Practica 1/
├── REF_CORE.CON        ← caso referencia, núcleo completo
├── REF_CORE.txt        ← versión texto del .CON
├── SIM_CORE.CON        ← caso simulado
├── SIM_CORE.txt
├── VAC_CORE.CON        ← caso vacío (void)
├── VAC_CORE.txt
├── REF_FA.CON          ← ensamblaje de combustible, caso referencia
├── REF_FA.txt
├── SIM_FA.CON
├── SIM_FA.txt
├── VAC_FA.CON
├── VAC_FA.txt
└── Ejercicio 4/        ← análisis de sensibilidad
    └── ejer4.py
```

### Práctica 2 — CTF (termohidráulica)

```
Practica 2/
├── 01-BARRA-PROMEDIO/  ← canal promedio
│   └── *.out           ← outputs CTF
└── 02-BARRA-CALIENTE/  ← canal caliente
    └── *.out
```

---

## Archivos de muestra

Si quieres ejecutar los notebooks sin los datos reales, en el futuro se podrán añadir aquí archivos `.txt` de muestra con distribuciones simplificadas para pruebas.
