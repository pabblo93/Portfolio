# Regresión Lineal Simple

Introducción práctica a la regresión lineal con scikit-learn sobre datos sintéticos.

## Descripción

Implementación paso a paso de una regresión lineal simple:
- Generación de datos con relación lineal y ruido aleatorio
- Ajuste del modelo con scikit-learn
- Lectura e interpretación de coeficientes
- Predicción sobre nuevos datos
- Visualización de la recta de regresión

## Estructura del Proyecto

```
regression_project/
├── README.md
└── notebooks/
    └── linear_regression_intro.ipynb
```

## Conceptos Clave

- **X debe ser 2D** para sklearn → `reshape(-1, 1)`
- **`coef_`** → pendiente de la recta
- **`intercept_`** → punto de corte con el eje Y
- **R²** → proporción de varianza explicada por el modelo (1.0 = ajuste perfecto)

## Dependencias

```bash
pip install numpy scikit-learn matplotlib
```

## Uso

```bash
jupyter notebook notebooks/linear_regression_intro.ipynb
```

## Autor

Pablo - estudiante de Data Science
