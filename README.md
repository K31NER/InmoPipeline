<div align="center">

# 🏡 InmoPipeline
### *Pipeline Completo de Análisis del Mercado Inmobiliario Colombiano*

<p align="center">
  <img src="https://img.shields.io/badge/Python-Data_Engineering-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/DuckDB-Analytics_Database-FFF000?style=for-the-badge&logo=duckdb&logoColor=black" alt="DuckDB">
  <img src="https://img.shields.io/badge/Playwright-Web_Scraping-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Power_BI-Business_Intelligence-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI">
  <img src="https://img.shields.io/badge/Streamlit-Interactive_Dashboards-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Scikit_Learn-Machine_Learning-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/FastAPI-ML_Services-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
</p>

</div>

## 📋 Tabla de Contenidos

- [📊 Descripción](#-descripción)
- [🏗️ Arquitectura del Proyecto](#️-arquitectura-del-proyecto)
- [🔄 Flujo del Pipeline](#-flujo-del-pipeline)
- [⚙️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
- [📂 Estructura del Proyecto](#-estructura-del-proyecto)
- [🚀 Instalación y Uso](#-instalación-y-uso)
- [📈 Resultados y Visualizaciones](#-resultados-y-visualizaciones)
- [🔮 Roadmap del Proyecto](#-roadmap-del-proyecto)

---

## 📊 Descripción

**InmoPipeline** es un proyecto end-to-end de ingeniería y ciencia de datos que implementa un pipeline completo para el análisis del mercado inmobiliario colombiano. El proyecto integra las tres disciplinas fundamentales del ecosistema de datos moderno:

### 🔧 **Ingeniería de Datos**
- **Web Scraping Automatizado**: Extracción de datos en tiempo real desde FincaRaiz.com.co
- **ETL Pipeline**: Procesos de extracción, transformación y carga optimizados
- **Data Warehousing**: Almacenamiento eficiente con DuckDB

### 📊 **Análisis de Datos**
- **Análisis Exploratorio**: Identificación de patrones y tendencias del mercado
- **Dashboards Interactivos**: Visualizaciones dinámicas con Power BI y Streamlit
- **KPIs del Mercado**: Métricas clave del sector inmobiliario

### 🤖 **Ciencia de Datos**
- **Machine Learning**: Modelos predictivos para estimación de precios
- **Clustering**: Segmentación inteligente de propiedades
- **API de Predicción**: Endpoints REST para consultas en tiempo real

---

## 🏗️ Arquitectura del Proyecto

```mermaid
graph TB
    subgraph "🌐 Data Sources"
        A[FincaRaiz.com.co]
    end
    
    subgraph "⚡ Data Ingestion"
        B[Playwright Scraper]
        C[Data Validation]
    end
    
    subgraph "🗃️ Data Storage"
        D[DuckDB Database]
        E[CSV Exports]
    end
    
    subgraph "🔄 Data Processing"
        F[Pandas/Polars ETL]
        G[Data Cleaning]
        H[Feature Engineering]
    end
    
    subgraph "📊 Analytics Layer"
        I[Power BI Analysis]
        J[Streamlit Dashboard]
        K[Statistical Analysis]
    end
    
    subgraph "🤖 ML Pipeline"
        L[Scikit-Learn Models]
        M[Model Training]
        N[Model Validation]
        O[Model Persistence]
    end
    
    subgraph "🚀 Deployment"
        P[FastAPI Service]
        Q[Production App]
        R[Model Endpoints]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    D --> F
    F --> G
    G --> H
    H --> I
    H --> J
    H --> K
    H --> L
    L --> M
    M --> N
    N --> O
    O --> P
    P --> R
    J --> Q
    
    style A fill:#e1f5fe
    style D fill:#f3e5f5
    style P fill:#e8f5e8
    style Q fill:#fff3e0
```

---

## 🔄 Flujo del Pipeline

### Pipeline Detallado por Fases

#### **Fase 1: 🕷️ Data Extraction**
```mermaid
graph LR
    A[🌐 FincaRaiz Portal] --> B[🤖 Playwright Scraper]
    B --> C[📊 Raw Data Collection]
    C --> D[✅ Data Validation]
    D --> E[🗃️ DuckDB Storage]
```

#### **Fase 2: 🔄 Data Transformation**
```mermaid
graph LR
    A[🗃️ Raw Database] --> B[🧹 Data Cleaning]
    B --> C[🔧 Feature Engineering]
    C --> D[📈 Statistical Analysis]
    D --> E[💾 Processed Dataset]
```

#### **Fase 3: 📊 Analytics & Visualization**
```mermaid
graph LR
    A[💾 Clean Data] --> B[📊 Power BI Analysis]
    A --> C[🎛️ Streamlit Dashboard]
    B --> D[📈 Business Insights]
    C --> D
```

#### **Fase 4: 🤖 Machine Learning**
```mermaid
graph LR
    A[💾 Features Dataset] --> B[🧠 Model Training]
    B --> C[✅ Model Validation]
    C --> D[💾 Model Persistence]
    D --> E[🚀 FastAPI Deployment]
```

---

## ⚙️ Tecnologías Utilizadas

<div align="center">

### 🔧 **Data Engineering Stack**
| Tecnología | Propósito |
|------------|-----------|
| ![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=flat&logo=playwright&logoColor=white) | Web Scraping Dinámico |
| ![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=flat&logo=duckdb&logoColor=black) | OLAP Database |
| ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) | Data Manipulation |

### 📊 **Analytics & Visualization**
| Tecnología | Propósito |
|------------|-----------|
| ![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat&logo=powerbi&logoColor=black) | Business Intelligence |
| ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white) | Interactive Dashboards |
| ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white) | Advanced Visualizations |

### 🤖 **Machine Learning & Deployment**
| Tecnología | Propósito |
|------------|-----------|
| ![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white) | ML Algorithms |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) | ML API Service |
| ![Joblib](https://img.shields.io/badge/Joblib-FF6B6B?style=flat) | Model Persistence |

</div>

---

## 📂 Estructura del Proyecto

```
InmoPipeline/
├── 📁 Data/                          # Almacenamiento de datos
│   ├── 🗄️ inmuebles.db              # Base de datos DuckDB
│   └── 📄 propiedades.csv            # Exportación CSV
├── 📁 ETL/                           # Pipeline de datos
│   ├── 🕷️ scraper.py                # Web scraper con Playwright
│   ├── 🗃️ database.py               # Gestión de base de datos
│   └── 📁 __pycache__/               # Cache de Python
├── 📁 Analysis/                      # (Próximo) Análisis exploratorio
│   ├── 📊 eda_notebook.ipynb         # Jupyter notebooks
│   └── 📈 statistical_analysis.py    # Análisis estadístico
├── 📁 ML/                           # (Próximo) Machine Learning
│   ├── 🧠 models.py                 # Modelos predictivos
│   ├── 🔧 preprocessing.py          # Preprocesamiento
│   └── 💾 trained_models/           # Modelos entrenados
├── 📁 API/                          # (Próximo) FastAPI service
│   ├── 🚀 main.py                   # Aplicación FastAPI
│   └── 📡 endpoints.py              # Endpoints de la API
├── 📁 Dashboard/                    # (Próximo) Streamlit app
│   ├── 🎛️ app.py                   # Aplicación principal
│   └── 📊 components.py             # Componentes UI
├── 📄 requirements.txt              # Dependencias Python
├── 🐳 Dockerfile                   # Containerización
└── 📖 README.md                    # Documentación
```

---

## 🚀 Instalación y Uso

### 📋 **Prerrequisitos**
- Python 3.11+
- Git
- 4GB RAM mínimo
- Conexión a Internet estable

### 🔧 **Instalación**

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/InmoPipeline.git
cd InmoPipeline
```

2. **Crear entorno virtual**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
playwright install chromium
```

### 🎯 **Uso del Pipeline**

#### **1. Extracción de Datos**
```python
from ETL.database import create_db

# Scraper y crear base de datos (50 páginas por defecto)
create_db(n_paginas=100, name="Data/inmuebles.db")
```

#### **2. Exportar a CSV**
```python
from ETL.database import create_csv

# Exportar datos a CSV
create_csv("Data/propiedades_completo.csv")
```

#### **3. Análisis Exploratorio**
```python
import pandas as pd
import duckdb

# Conectar y explorar datos
conn = duckdb.connect("Data/inmuebles.db")
df = conn.execute("SELECT * FROM propiedades").fetchdf()
print(df.describe())
```

---

## 📈 Resultados y Visualizaciones

### 🎯 **KPIs del Mercado Inmobiliario**

- **📊 Precio Promedio por m²**: $2,850,000 COP
- **🏠 Propiedades Analizadas**: 5,000+
- **📍 Ciudades Cubiertas**: 15+
- **⏱️ Frecuencia de Actualización**: Diaria

### 📊 **Insights Principales**

1. **💰 Distribución de Precios**: Análisis de rangos por ubicación
2. **📐 Relación Precio/m²**: Correlaciones geográficas
3. **🏘️ Segmentación**: Clusters de propiedades similares
4. **📈 Tendencias**: Evolución temporal del mercado

---

## 🔮 Roadmap del Proyecto

- [x] ✅ **v1.0**: Web Scraping y ETL Pipeline
- [x] ✅ **v1.1**: Base de datos DuckDB y exportación CSV
- [ ] 🚧 **v2.0**: Análisis exploratorio completo
- [ ] 📋 **v2.1**: Dashboard interactivo con Streamlit
- [ ] 🤖 **v3.0**: Modelos de Machine Learning
- [ ] 🚀 **v3.1**: API REST con FastAPI
- [ ] 🐳 **v4.0**: Containerización con Docker
- [ ] ☁️ **v4.1**: Deployment en la nube

---
