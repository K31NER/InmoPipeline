import joblib
import duckdb
import unicodedata
import numpy as np
import pandas as pd

DB_PATH = "Data/inmuebles.db"
MODEL_PATH = "ML/model.pkl"

# Diccionario de costes
region_cost = {
    "Caribe": 0.7,      
    "Amazonía": 0.6,    
    "Pacífico": 0.8,     
    "Orinoquía": 0.75,   
    "Andina": 1.0,       
}

# Diccionario para mapear entrada normalizada a nombre correcto
regiones_map = {
    "caribe": "Caribe",
    "amazonia": "Amazonia",
    "pacifico": "Pacífico",
    "orinoquia": "Orinoquía",
    "andina": "Andina",
    "insular": "Insular",
    "desconocido": "desconocido"
}

def load_model(model_path=MODEL_PATH):
    """ Cargamos el modelo 
    
    Parametros:
    - Path donde se encuantra el modelo
    
    Retorna:
    - model : modelo 
    - model_data : datos relevantes del modelo
    
    """
    
    print("🔄 Cargando modelo...")
    try:
        modelo_info = joblib.load(MODEL_PATH)
        
        # Obtenemos el modelo
        model = modelo_info['model']
        
        model_data = {
            "Version": "1.0",
            "Fecha de entrenamiento": "05/07/25",
            "R² (Entrenamiento)": modelo_info["R2"],
            "MSE (Entrenamiento)": modelo_info["MSE"],
            "Datos de entrenamiento": modelo_info["Datos"],
            "Error absoluto(Prueba externa)": "19.44% con 282 datos nuevos" ,
            "Features":modelo_info["feature_columns"],
            "Fuente de los datos": "Web scrapyn - fincaraiz | API Colombia - regiones",
            "Nota": {"Tipo de modelo" : modelo_info["nota"],
                    "Limitaciones": "No considera ubicación geográfica exacta ni estrato",},
        }
        return model ,model_data
    
    
    except Exception as e:
        print(f"❌ Error al cargar modelo: {e}")
        

def get_predict(metros_cuadrados:int, habitaciones:int 
                ,baños:int, region:str,model) -> int:
    """Predice el precio de una propiedad en base a los parametros 
    
    Parametros:
    - metros cuadrados: numero de metros cuadros
    - habitacones : numero de habitaciones
    - baños: numero de baños
    - region: region donde se encuentra el inmueble 
    - model: modelo de machine learning para hcer las predicciones
    
    Return:
    
    - precio: Prediccion del precio
    """
    
    # Validaciones para evitar devision de cero
    habitaciones = 0.1 if habitaciones == 0 else habitaciones
    baños = 0.1 if baños == 0 else baños
    
    # Features (Replicamos lo que hicmos para calcularlas)
    costo_vida = region_cost.get(region, 0.1)
    densidad = (habitaciones + baños) / metros_cuadrados
    hab_x_baños = habitaciones * baños
    m2_x_costo_vida = metros_cuadrados * costo_vida
    log_metros_cuadrados = np.log1p(metros_cuadrados)
    
    # Preparamos el dataframe con el orden correcto para enviar al modelo
    features = pd.DataFrame([{
        'habitaciones': habitaciones,
        'baños': baños,
        'metros_cuadrados': metros_cuadrados,
        'costo_vida': costo_vida,
        'densidad': densidad,
        'hab_x_baños': hab_x_baños,
        'm2_x_costo_vida': m2_x_costo_vida,
        'log_metros_cuadrados': log_metros_cuadrados
    }])
    
    # Predicción
    log_precio = model.predict(features)[0] # Obtenemos el primer indice
    precio_real = np.expm1(log_precio) # Volvemos entero
    
    return precio_real

def normalizar_texto(texto: str) -> str:
    """ Elimina las tildes y pone en minisculas
    
    Parametros:
    - texto: recibe un str para normalizar
    
    Return:
    - texto_normalizado: Devuelve el texto sin tildes y en minusculas
    """
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()

def get_distinct_city(db_path:str = DB_PATH) -> pd.DataFrame:
    """ Obtiene todas las ciudades unicas de la base de datos 
    
    Parametros:
    - db_path : ruta de la base de datos. = Definida por defecto
    
    Return
    - data.values: devuelce un array numpy de las ciudades unicas.
    """
    db = duckdb.connect(db_path)
    data = db.execute("SELECT DISTINCT(ciudad_normalizada) FROM propiedades").fetch_df()
    return data.values

if __name__ == "__main__":
    df = get_distinct_city(DB_PATH)
    print(df)
    """ 
    model = load_model(MODEL_PATH)
    if model is not None:
        nuevo_precio = get_predict(150, 2, 1, "Caribe", model)
        print(f"$ {nuevo_precio:,.2f} COP")
    else:
        print("No se pudo cargar el modelo.")
    """

