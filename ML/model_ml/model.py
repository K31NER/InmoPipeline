import joblib 
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score,mean_squared_error
from sklearn.model_selection import cross_val_score, train_test_split,KFold

CSV_PATH = "Data/propiedades.csv"
MODEL_PATH = "ML/Randomforest_2.pkl"

# Costo de vida basado en region y su salirio promedio
region_cost = {
    "Caribe": 0.7,       # "Más bajo" costo de vida, salario ~1.8 M COP → valor base
    "Amazonía": 0.6,     # "Muy bajo", salario ~1.6 M COP
    "Pacífico": 0.8,     # "Bajo", salario ~1.7 M COP
    "Orinoquía": 0.75,   # "Bajo‑medio", salario ~1.7 M COP
    "Andina": 1.0,       # "Alto", salario ~2.25 M COP
}

def load_data(CSV_PATH):
    return pd.read_csv(CSV_PATH)

def clean_df(df):
    # Borramos las columas que no usaremos
    df.drop(columns=["titulos","enlaces","ciudades"],inplace=True)

    # Limpiamos el dataset
    df = df[
        (df["metros_cuadrados"] > 0) & 
        (df["region"].ne("desconocido"))
        ]

    # Penalizamos los inmubeles sin habitaciones ni baños
    df["habitaciones"] = np.where(df["habitaciones"] == 0,0.1,df["habitaciones"])
    df["baños"] = np.where(df["baños"] == 0 , 0.1 , df["baños"])
    
    return df
# _____________________Creamos nuevas feactures_____________________

def new_features(df):
    # mapeamos el costo de vida 
    df["costo_vida"] = df["region"].map(region_cost).fillna(0.1)

    df["densidad"] = (df["habitaciones"] + df["baños"]) / df["metros_cuadrados"]

    df["hab_x_baños"] = df["habitaciones"] * df["baños"]

    df["m2_x_costo_vida"] = df["metros_cuadrados"] * df["costo_vida"]

    df["log_metros_cuadrados"] = np.log1p(df["metros_cuadrados"])

    # Escalomos el precio para evitar problems de pesos
    df["log_precios"] = np.log1p(df["precios"]) 
    
    return df

# _________________ Preparar datos para entrenar________________________________
def prepare_data(df):
    X = df.drop(columns=["precios", "region", "log_precios"])
    y = df["log_precios"]
    return train_test_split(X, y, test_size=0.33, random_state=42, shuffle=True)

# ______________________ Modelo _________________________________
def train_model(X_train, y_train):
    model = RandomForestRegressor(
        n_estimators=500,
        max_depth=30,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model

# _________________________________ Validacion de rendimiento ____________________
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    importancias = model.feature_importances_
    return y_pred, r2, mse, importancias

def cross_validation(model, X, y, k=5):
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=kf, scoring="r2", n_jobs=-1)
    print(f"\n🔁 R² por fold: {scores}")
    print(f"📊 R² promedio: {scores.mean():.4f} ± {scores.std():.4f}")
    
def test_cross_validation(df,model):
    X = df.drop(columns=["precios","log_precios","region"])
    Y = df["log_precios"]
    
    model_cruzado = model
    cross_validation(model_cruzado,X,Y,k=5)
    
# Creamos un DataFrame para asociar nombres de variables e importancias
def feature_importance_df(X, importancias):
    return pd.DataFrame({
        "Característica": X.columns,
        "Importancia": importancias
    }).sort_values(by="Importancia", ascending=False)

# ___________ Guardamos el modelo __________________________--
def save_model(model, feature_columns, region_cost,r2,mse, path):
    modelo_info = {
        "model": model,
        "feature_columns": feature_columns,
        "region_cost": region_cost,
        "R2": f"{r2:,.4f}",
        "MSE": f"{mse:,.4f}",
        "Datos": len(df),
        "nota":"Modelo ajustado con Random Forest para predicción de precios inmobiliarios."
    }
    joblib.dump(modelo_info, path)
    print(f"\n✅ Modelo guardado en {path} con features: {feature_columns}")

if __name__ == "__main__":
    df = load_data(CSV_PATH)
    df = clean_df(df)
    df = new_features(df)
    
    X_train, X_test, y_train, y_test = prepare_data(df)
    model = train_model(X_train, y_train)
    
    y_pred, r2, mse, importancias = evaluate_model(model, X_test, y_test)
    
    print("\n📊 Resultados del modelo:")
    print(f"R²: {r2:.4f}")
    print(f"Error cuadrático medio: {mse:.4f}")
    
    importancia_df = feature_importance_df(X_train, importancias)
    print("\n🔥 Importancia de características:")
    print(importancia_df)
    save_model(model, X_train.columns.tolist(), region_cost, r2,mse,"model.pkl")
    
    """ 
    print("\n ________________Test validacion cruzada__________________ \n")
    
    model_cross = RandomForestRegressor(
        n_estimators=500,
        max_depth=30,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    )
    test_cross_validation(df,model_cross)
    
    #save_model(model, X_train.columns.tolist(), region_cost, "test_model.pkl")
    """