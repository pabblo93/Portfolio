# 🛍️ Customer Purchase Model

Análisis y modelado predictivo de comportamientos de compra de clientes utilizando técnicas de Machine Learning.

## 📋 Descripción

Este proyecto implementa un pipeline completo de ML para predecir si un cliente será un comprador frecuente basándose en:
- Edad
- Ingresos anuales
- Monto de compra
- Score de lealtad
- Región geográfica

## 🎯 Objetivos

1. **Exploración de datos** - Análisis descriptivo del comportamiento de compra
2. **Preparación de datos** - Normalización, codificación de variables categóricas
3. **Modelado** - Regresión logística para clasificación binaria (compradores frecuentes vs ocasionales)
4. **Evaluación** - Métricas de precisión, recall, F1-score

## 📁 Estructura del Proyecto

```
customer_purchase_model/
├── README.md                          # Este archivo
├── data/
│   └── Customer Purchasing Behaviors.csv    # Dataset con 238 clientes
├── notebooks/
│   └── Ejercicios.ipynb              # Notebook con análisis completo
└── src/
    └── (modelos y utilidades)
```

## 📊 Dataset

**Fuente:** Kaggle - Customer Purchasing Behaviors  
**Muestras:** 238 clientes  
**Features:** 7 columnas (user_id, age, annual_income, purchase_amount, loyalty_score, region, purchase_frequency)

## 🔧 Instalación

### Requisitos previos
- Python 3.11+
- pip

### Setup

```bash
# Navegar a la carpeta del proyecto
cd machine_learning/customer_purchase_model

# Instalar dependencias
pip install -r ../requirements.txt

# O instalar localmente
pip install pandas numpy scikit-learn matplotlib kagglehub
```

## 🚀 Uso

### Ejecutar el análisis completo

```bash
# Opción 1: Jupyter Notebook
jupyter notebook notebooks/Ejercicios.ipynb

# Opción 2: VSCode
# Abrir en VS Code y ejecutar las celdas
```

## 📈 Resultados Esperados

- **R² Score (Regresión):** ~0.991
- **Accuracy (Clasificación):** ~80-85%
- **Visualización:** Gráficos de regresión lineal y métricas de clasificación

## 💡 Procesos Clave

1. **Limpieza de datos** - Manejo de valores faltantes
2. **Train-Test Split** - 80% entrenamiento, 20% prueba
3. **Encoding categórico** - OneHotEncoding para variable "region"
4. **Escalado** - StandardScaler para normalizar variables numéricas
5. **Evaluación** - Classification Report con precisión y recall por clase

## 🛠️ Dependencias Principales

| Librería | Versión | Uso |
|----------|---------|-----|
| `pandas` | 3.0.1 | Manipulación de datos |
| `numpy` | 2.4.2 | Operaciones numéricas |
| `scikit-learn` | 1.8.0 | Modelos ML y preprocesamiento |
| `matplotlib` | 3.10.8 | Visualización |
| `kagglehub` | 1.0.0 | Descarga de datasets |

## 📝 Notas Importantes

- El dataset está **moderadamente balanceado** (137 compradores activos, 101 ocasionales)
- Se implementó un **pipeline estándar de ML** con consideración de fuga de datos
- La variable `purchase_frequency` se usa para crear la etiqueta binaria

## 👤 Autor

Pablo - estudiante de Data Science

## 📚 Conceptos Aprendidos

- Regresión lineal simple
- Regresión logística (clasificación binaria)
- Preprocesamiento de datos en ML
- Métricas de evaluación (accuracy, precision, recall, F1)
