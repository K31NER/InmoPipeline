<div align="center">

<img src="img/logo.png" alt="InmoPipeline Logo" width="200"/>

# 🏡 InmoPipeline
### *Pipeline Completo de Análisis del Mercado Inmobiliario Colombiano*

![Status](https://img.shields.io/badge/Status-Production-brightgreen?style=flat-square)
![Model](https://img.shields.io/badge/Model_R²-70.07%25-blue?style=flat-square)
![Validation](https://img.shields.io/badge/External_Error-19.44%25-orange?style=flat-square)
![API](https://img.shields.io/badge/API-Live-success?style=flat-square&logo=render)
![Tests](https://img.shields.io/badge/Tests-282_Properties-informational?style=flat-square)

<p align="center">
  <img src="https://img.shields.io/badge/Python-Data_Engineering-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/DuckDB-Analytics_Database-FFF000?style=for-the-badge&logo=duckdb&logoColor=black" alt="DuckDB">
  <img src="https://img.shields.io/badge/Playwright-Web_Scraping-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-Interactive_Dashboards-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Scikit_Learn-Machine_Learning-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/FastAPI-ML_&_MCP_Server-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/n8n-Workflow_Automation-EA4B71?style=for-the-badge&logo=n8n&logoColor=white" alt="n8n">
  <img src="https://img.shields.io/badge/Render-Cloud_Deployment-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Render">
</p>

</div>

## 📋 Tabla de Contenidos

- [📊 Descripción](#-descripción)
- [🏗️ Arquitectura del Proyecto](#️-arquitectura-del-proyecto)
- [🔄 Flujo del Pipeline](#-flujo-del-pipeline)
- [⚙️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
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
- **Dashboards Interactivos**: Visualizaciones dinámicas con Streamlit
- **KPIs del Mercado**: Métricas clave del sector inmobiliario

### 🤖 **Ciencia de Datos**
- **Machine Learning**: Modelo Random Forest entrenado con **R² = 0.7007** y **MSE = 0.197**
- **Validación Externa**: Testeo con **282 propiedades nuevas** obtenidas por web scraping
- **Error Absoluto**: **19.44%** en datos reales (concordante con métricas de entrenamiento)
- **API de Predicción**: Endpoints REST desplegados en **Render Cloud** ↗️ [**inmopipeline.onrender.com**](https://inmopipeline.onrender.com)
- **Automatización**: Workflows inteligentes con **n8n** para consultas automatizadas

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
        I[Streamlit EDA]
        J[Statistical Analysis]
        K[Interactive Dashboard]
    end
    
    subgraph "🤖 ML Pipeline"
        L[Scikit-Learn Models]
        M[Model Training]
        N[Model Validation]
        O[Model Persistence]
    end
    
    subgraph "🚀 Deployment"
        P[FastAPI Service]
        Q[Render Cloud]
        R[Model Endpoints]
        S[n8n Workflows]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    E --> F
    F --> G
    G --> H
    H --> I
    H --> J
    H --> K
    D --> L
    L --> M
    M --> N
    N --> O
    O --> P
    P --> Q
    P --> R
    I --> S
    S --> Q
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
    A[💾 Clean Data] --> B[🎛️ Streamlit EDA]
    A --> C[📈 Statistical Analysis]
    B --> D[📈 Business Insights]
    C --> D
```

#### **Fase 4: 🤖 Machine Learning**
```mermaid
graph LR
    A[💾 Features Dataset] --> B[🧠 Model Training]
    B --> C[✅ Model Validation]
    C --> D[� External Testing]
    D --> E[�💾 Model Persistence]
    E --> F[🚀 Render Deployment]
    F --> G[🔄 n8n Automation]
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
| ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white) | Interactive Dashboards |

### 🤖 **Machine Learning & Deployment**
| Tecnología | Propósito |
|------------|-----------|
| ![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white) | Random Forest (R²=0.7007) |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) | ML & MCP API Server |
| ![Render](https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white) | Cloud Deployment |
| ![n8n](https://img.shields.io/badge/n8n-EA4B71?style=flat&logo=n8n&logoColor=white) | Workflow Automation |
| ![Joblib](https://img.shields.io/badge/Joblib-FF6B6B?style=flat) | Model Persistence |

</div>

---

## 📊 Métricas y Rendimiento del Modelo

<div align="center">

### 🎯 **Resultados de Entrenamiento**
| Métrica | Valor | Descripción |
|---------|--------|-------------|
| **R² Score** | `0.7007` | El modelo explica el 70% de la varianza en precios |
| **MSE** | `0.1966` | Error cuadrático medio en escala logarítmica |
| **Datos de Entrenamiento** | `1,050` | Propiedades utilizadas para entrenamiento |
| **Features** | `8` | Variables predictivas optimizadas |

### 🔍 **Validación Externa**
| Métrica | Valor | Descripción |
|---------|--------|-------------|
| **Datos de Prueba** | `282` | Propiedades nuevas obtenidas por web scraping |
| **Error Absoluto Promedio** | `19.44%` | Error en predicciones con datos reales |
| **Consistencia** | `✅ Validado` | Error concuerda con métricas de entrenamiento |
| **Rango de Confianza** | `70-80%` | Precisión esperada en predicciones |

<div align="center">
<img src="img/validacion/porcentaje_error.png" alt="Distribución de Errores de Validación" width="600"/>
<p><em>Distribución del porcentaje de error en 282 propiedades de validación externa</em></p>
</div>

</div>

---

## 🤖 Modelo de Machine Learning

### 📋 **Especificaciones Técnicas**

**Algoritmo**: Random Forest Regressor  
**Optimización**: Grid Search con validación cruzada (K=5)  
**Target**: Precios en escala logarítmica (`log1p`)  

#### **Hiperparámetros Optimizados**
```python
RandomForestRegressor(
    n_estimators=500,      # Árboles en el bosque
    max_depth=30,          # Profundidad máxima
    min_samples_split=5,   # Mínimo para dividir nodo
    min_samples_leaf=2,    # Mínimo en hoja
    max_features="sqrt",   # Features por división
    random_state=42,       # Reproducibilidad
    n_jobs=-1             # Paralelización
)
```

#### **Features Engineering**
| Feature | Descripción | Importancia |
|---------|-------------|------------|
| `metros_cuadrados` | Área de la propiedad | 26.5% |
| `log_metros_cuadrados` | Área en escala logarítmica | 22.6% |
| `m2_x_costo_vida` | Interacción área-región | 17.7% |
| `densidad` | (hab + baños) / m² | 12.1% |
| `baños` | Número de baños | 9.2% |
| `hab_x_baños` | Interacción habitaciones-baños | 6.3% |
| `habitaciones` | Número de habitaciones | 3.6% |
| `costo_vida` | Factor regional | 2.0% |

### 🎯 **Validación y Pruebas**

#### **Métricas de Entrenamiento**
- **Datos**: 1,050 propiedades procesadas
- **División**: 67% entrenamiento, 33% validación
- **R² Score**: 0.7007 (70.07% de varianza explicada)
- **RMSE**: 0.4433 (en escala logarítmica)
- **MAE**: 0.3291 (en escala logarítmica)

#### **Validación Externa Rigurosa**
- **Datos nuevos**: 282 propiedades obtenidas por web scraping independiente
- **Error absoluto promedio**: 19.44%
- **Rango de error**: 5.8% - 25.0%
- **Consistencia**: ✅ Error concordante con R² (0.30 faltante ≈ 19% error)

<div align="center">
<img src="img/validacion/Real_vs_prediccion.png" alt="Comparación Precios Reales vs Predicciones" width="700"/>
<p><em>Análisis comparativo entre precios reales del mercado y predicciones del modelo</em></p>
</div>

---

## 🔄 Automatización con n8n

### 🤖 **Agente Inmobiliario IA**

Implementamos un workflow inteligente en **n8n** que actúa como un agente de consultas inmobiliarias automatizado:

#### **Características del Agente**
- **Modelo LLM**: Google Gemini 2.5 Pro
- **Protocolo**: Model Context Protocol (MCP)
- **Endpoints**: Conectado a API de InmoPipeline
- **Capacidades**: Consultas automáticas sin intervención humana

#### **Funcionalidades Disponibles**
1. **📍 Consultas por Región**: `/propiedades_region/{region}`
2. **🏙️ Consultas por Ciudad**: `/propiedades_ciudad/{ciudad}`  
3. **🎯 Predicción de Precios**: `/model` (ML endpoint)
4. **📊 Información del Modelo**: Métricas y rendimiento automático

#### **Workflow n8n**
```mermaid
graph LR
    A[💬 Chat Input] --> B[🤖 Gemini Agent]
    B --> C[🔗 MCP Client]
    C --> D[🌐 API InmoPipeline]
    D --> E[📊 Response Processing]
    E --> F[💬 Chat Output]
```

**Ejemplo de Uso**:
> *Usuario*: "¿Cuánto cuesta un apartamento de 80m² con 3 habitaciones en Bogotá?"  
> *Agente*: Ejecuta automáticamente `/model` → Responde con predicción + métricas del modelo

<div align="center">
<img src="img/n8n agent/agent.png" alt="Agente Inmobiliario IA con n8n" width="800"/>
<p><em>Interfaz del agente inmobiliario IA desarrollado en n8n con Google Gemini</em></p>
</div>

---

## 🔮 Roadmap del Proyecto

- [x] ✅ **v1.0**: Web Scraping y ETL Pipeline
- [x] ✅ **v1.1**: Base de datos DuckDB y exportación CSV
- [x] ✅ **v2.0**: Análisis exploratorio completo con Streamlit
- [x] ✅ **v2.1**: Dashboard interactivo con métricas y visualizaciones
- [x] ✅ **v3.0**: Modelo Random Forest entrenado (R²=0.7007)
- [x] ✅ **v3.1**: Validación externa con 282 propiedades (19.44% error)
- [x] ✅ **v3.2**: API REST con FastAPI desplegada en Render
- [x] ✅ **v3.3**: Automatización con n8n workflows
- [ ] � **v4.0**: Containerización con Docker
- [ ] 📋 **v4.1**: CI/CD Pipeline automatizado
- [ ] 🔄 **v4.2**: Reentrenamiento automático del modelo

---

## 🌐 Enlaces y Recursos

- 🚀 **API en Producción**: [inmopipeline.onrender.com](https://inmopipeline.onrender.com)
- 📊 **Dashboard Streamlit**: [inmopipeline.streamlit.app](https://inmopipeline.streamlit.app)
- 🔄 **Workflows n8n**: Automatización de consultas inmobiliarias
- 📈 **Documentación API**: [/docs](https://inmopipeline.onrender.com/docs) (Swagger UI)
- 🔗 **MCP Server**: [/mcp](https://inmopipeline.onrender.com/mcp) (Model Context Protocol)

---

## 🏆 Resultados Destacados

### 📈 **Logros del Proyecto**

- ✅ **Pipeline End-to-End Completo**: Desde web scraping hasta predicción en producción
- ✅ **Modelo Validado Externamente**: 19.44% error absoluto con datos reales nuevos
- ✅ **Precisión Robusta**: R² = 0.7007 confirmado en 282 propiedades independientes
- ✅ **Automatización Inteligente**: Agente IA con n8n para consultas automáticas
- ✅ **Despliegue en Producción**: API funcionando 24/7 en Render Cloud
- ✅ **Concordancia de Métricas**: Error externo consistente con métricas de entrenamiento

### 🎯 **Casos de Uso Validados**

| Tipo de Propiedad | Predicción Promedio | Precisión |
|-------------------|-------------------|-----------|
| Apartamentos urbanos | $400M - $600M COP | ±15-20% |
| Casas residenciales | $600M - $1.2B COP | ±18-25% |
| Propiedades premium | $1B+ COP | ±20-30% |

### 🔬 **Validación Científica**

El modelo ha sido rigurosamente validado:
- **Entrenamiento**: 1,050 propiedades con validación cruzada K=5
- **Testing externo**: 282 propiedades completamente nuevas
- **Error coherente**: 19.44% externo vs 30% esperado del R² faltante
- **Distribución de errores**: Normal, sin sesgos sistemáticos

---

## 📸 Galería de Resultados

### 🎯 **Visualizaciones del Modelo**

<div align="center">

| Métrica de Validación | Análisis de Precisión |
|:---------------------:|:---------------------:|
| <img src="img/validacion/porcentaje_error.png" alt="Distribución de Errores" width="400"/> | <img src="img/validacion/Precio real.png" alt="Análisis de Precios" width="400"/> |
| *Distribución del error absoluto en validación externa* | *Precio real del inmueble* |

---

## 👥 Contribuciones

Este proyecto fue desarrollado como parte de un pipeline completo de ingeniería y ciencia de datos, integrando:

- **Data Engineering**: ETL automatizado y almacenamiento optimizado
- **Machine Learning**: Modelo predictivo con validación externa rigurosa  
- **MLOps**: Despliegue automatizado y monitoreo en producción
- **Automation**: Workflows inteligentes con n8n y MCP

---

<div align="center">

**🚀 InmoPipeline - Análisis Inmobiliario Inteligente**  
*Desarrollado con ❤️ para el mercado inmobiliario colombiano*

[![API Status](https://img.shields.io/badge/API-Check_Status-blue?style=for-the-badge&logo=render)](https://inmopipeline.onrender.com)
[![Documentation](https://img.shields.io/badge/Docs-API_Reference-green?style=for-the-badge&logo=swagger)](https://inmopipeline.onrender.com/docs)

</div>
