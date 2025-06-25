# 🏡 InmoPipeline

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-ETL%20Storage-yellow.svg)](https://duckdb.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Web%20Scraping-brightgreen.svg)](https://playwright.dev/python/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-orange.svg)](https://powerbi.microsoft.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interactive%20App-ff4b4b.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange.svg)](https://scikit-learn.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-ML%20API-009688.svg)](https://fastapi.tiangolo.com/)

---

## 📊 Descripción

**InmoPipeline** es un proyecto completo de ciclo de datos centrado en el mercado inmobiliario colombiano. Aborda las tres áreas clave del ecosistema de datos:

- **Ingeniería de Datos:** Recolección, almacenamiento y transformación de datos desde portales inmobiliarios.
- **Análisis de Datos:** Exploración, visualización y construcción de dashboards interactivos.
- **Ciencia de Datos:** Modelado predictivo para estimación de precios y clasificación de propiedades.

---

## ⚙️ Tecnologías utilizadas

- **Playwright:** Web scraping dinámico.
- **DuckDB:** Almacenamiento y consultas eficientes tipo SQL.
- **Pandas/Polars:** Limpieza y manipulación de datos.
- **Power BI:** Prototipado rápido de dashboards.
- **Streamlit:** Visualización final automatizada e interactiva.
- **Scikit-Learn:** Modelado predictivo (regresión, clustering).
- **FastAPI:** Exposición de modelos ML mediante API REST.

---

## 🔁 Flujo del Proyecto

```mermaid
graph TD
  A[Web Scraping - FincaRaiz] --> B[Base de Datos - DuckDB]
  B --> C[Transformación & Limpieza - Pandas/Polars]
  C --> D[Análisis Exploratorio - Power BI]
  C --> E[Análisis Exploratorio - Streamlit]
  C --> F[Modelado Predictivo - Scikit-Learn]
  F --> G[Exportación Modelo - Joblib]
  G --> H[API de Predicción - FastAPI]
  H --> I[Dashboard Final - Streamlit]
