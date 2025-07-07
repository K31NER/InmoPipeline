import joblib 
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import KFold, cross_val_score

CSV_PATH = "Data/propiedades.csv"
MODEL_PATH = "ML/Randomforest_2.pkl"

region_cost = {
    "Caribe": 0.7,
    "Amazonía": 0.6,
    "Pacífico": 0.8,
    "Orinoquía": 0.75,
    "Andina": 1.0,
}

def load_data(CSV_PATH):
    return pd.read_csv(CSV_PATH)

def clean_df(df):
    df.drop(columns=["titulos", "enlaces", "ciudades"], inplace=True)
    df = df[(df["metros_cuadrados"] > 0) & (df["region"].ne("desconocido"))]
    df["habitaciones"] = np.where(df["habitaciones"] == 0, 0.1, df["habitaciones"])
    df["baños"] = np.where(df["baños"] == 0, 0.1, df["baños"])
    return df

def new_features(df):
    df["costo_vida"] = df["region"].map(region_cost).fillna(0.1)
    df["densidad"] = (df["habitaciones"] + df["baños"]) / df["metros_cuadrados"]
    df["hab_x_baños"] = df["habitaciones"] * df["baños"]
    df["m2_x_costo_vida"] = df["metros_cuadrados"] * df["costo_vida"]
    df["log_metros_cuadrados"] = np.log1p(df["metros_cuadrados"])
    df["log_precios"] = np.log1p(df["precios"])
    return df

def prepare_data(df):
    X = df.drop(columns=["precios", "region", "log_precios"])
    y = df["log_precios"]
    return X, y

def train_model(X, y):
    model = RandomForestRegressor(
        n_estimators=500,
        max_depth=30,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, y)
    return model

def cross_validation(model, X, y, k=5):
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=kf, scoring="r2", n_jobs=-1)
    print(f"\n🔁 R² por fold: {scores}")
    print(f"📊 R² promedio: {scores.mean():.4f} ± {scores.std():.4f}")

def feature_importance_df(X, importancias):
    return pd.DataFrame({
        "Característica": X.columns,
        "Importancia": importancias
    }).sort_values(by="Importancia", ascending=False)

def save_model(model, feature_columns, region_cost, path):
    modelo_info = {
        "model": model,
        "feature_columns": feature_columns,
        "region_cost": region_cost
    }
    joblib.dump(modelo_info, path)
    print(f"\n✅ Modelo guardado en {path} con features: {feature_columns}")

if __name__ == "__main__":
    df = load_data(CSV_PATH)
    df = clean_df(df)
    df = new_features(df)
    
    X, y = prepare_data(df)
    
    model = RandomForestRegressor(
        n_estimators=500,
        max_depth=30,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    )

    cross_validation(model, X, y, k=5)

    # Entrenas un modelo final sobre todo el dataset para guardar
    model_final = train_model(X, y)
    importancias = model_final.feature_importances_
    
    importancia_df = feature_importance_df(X, importancias)
    print("\n🔥 Importancia de características:")
    print(importancia_df)

    #save_model(model_final, X.columns.tolist(), region_cost, MODEL_PATH)
