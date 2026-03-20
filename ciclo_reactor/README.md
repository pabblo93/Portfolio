# Ciclo de Operación de un Reactor Nuclear — Simulación con COBAYA y CTF

Proyecto de notebooks Jupyter que narran la simulación completa del ciclo de operación de un reactor nuclear de pequeña potencia (SMR) del tipo NuScale, usando los códigos de cálculo COBAYA (neutrónica) y CTF (termohidráulica).

El proyecto está organizado como un **libro técnico interactivo** en español, desarrollado en el contexto del Máster de Tecnología de Reactores Nucleares y desarrollado en la UPM.

---

## Estructura

```
ciclo_reactor/
├── README.md                        ← este archivo
├── requirements.txt                 ← dependencias Python
├── data/
│   └── README.md                    ← instrucciones de configuración de rutas
├── 00_introduccion.ipynb            ← El reactor NuScale y el ciclo de operación
├── 01_neutronics_cobaya.ipynb       ← Distribuciones de potencia con COBAYA
├── 02_termohidraulica_ctf.ipynb     ← Perfiles termohidráulicos con CTF
├── 03_acoplamiento.ipynb            ← Retroalimentación neutrónica-TH
└── 04_deplecion_ciclo.ipynb         ← Quemado y gestión del ciclo
```

---

## Notebooks

| Notebook | Contenido |
|---|---|
| `00_introduccion.ipynb` | Descripción física del NuScale SMR, esquema del ciclo de operación, herramientas de simulación |
| `01_neutronics_cobaya.ipynb` | Lectura de archivos COBAYA, distribuciones radial y axial de potencia, comparación REF/SIM/VAC, análisis de sensibilidad |
| `02_termohidraulica_ctf.ipynb` | Lectura de outputs CTF, canal promedio vs canal caliente, perfiles de temperatura, análisis DNB, validación Watts Bar |
| `03_acoplamiento.ipynb` | Retroalimentación neutrónica-TH, coeficientes de temperatura, acoplamiento COBAYA-CTF |
| `04_deplecion_ciclo.ipynb` | Quemado, evolución de k_eff, venenos neutrónico (Xe-135, Sm-149), gestión del ciclo |

---

## Configuración de datos

Los datos de simulación (archivos COBAYA `.CON`/`.txt` y outputs CTF `.out`) **no se incluyen** en este repositorio. Se referencian mediante una variable `DATA_ROOT` en cada notebook.

Ver `data/README.md` para instrucciones detalladas.

---

## Cómo ejecutar

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Configurar `DATA_ROOT` al inicio de cada notebook apuntando a la carpeta de prácticas.

3. Ejecutar desde Jupyter Lab o Jupyter Notebook:
   ```bash
   jupyter lab
   ```

---

## Herramientas de simulación

- **COBAYA**: Código de cálculo neutrónico del CIEMAT para reactores de agua ligera. Resuelve la ecuación de difusión de neutrones en 3D y genera distribuciones de flujo y potencia.
- **CTF**: Código termohidráulico basado en subchannel analysis, derivado de COBRA-TF. Calcula perfiles de temperatura, fracción de vapor y parámetros de seguridad como el DNBR.
- **NuScale SMR**: Reactor de agua a presión de pequeña potencia modular (77 MWe por módulo), diseño integral con circulación natural.

---

## Referencias

- NuScale Power Module Design and Operations, NuScale Power LLC
- COBAYA Code Manual, CIEMAT
- CTF Users Manual, NC State University / Westinghouse
- Prácticas de Neutrónica y Termohidráulica, Máster THN — UPM
