import joblib
import numpy as np
import pandas as pd

MODEL_PATH = "model.pkl"

region_cost = {
    "Caribe": 0.7,      
    "Amazonía": 0.6,    
    "Pacífico": 0.8,     
    "Orinoquía": 0.75,   
    "Andina": 1.0,       
}

def load_model(model_path=MODEL_PATH):
    """ Cargamos el modelo 
    
    Parametros:
    - Path donde se encuantra el modelo
    
    Retorna:
    - model : modelo 
    - feature_columns: orden de las columnas
    - region_cost: coste de vida de cada region
    
    """
    
    print("🔄 Cargando modelo...")
    try:
        modelo_info = joblib.load(MODEL_PATH)
        
        # Obtenemos el modelo
        model = modelo_info['model']
        #feature_columns = modelo_info['feature_columns']
        #region_cost = modelo_info['region_cost']
        model_data = {
            "R²": modelo_info["R2"],
            "MSE": modelo_info["MSE"],
            "Datos": modelo_info["Datos"],
            "Nota": modelo_info["nota"]
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


if __name__ == "__main__":
    model = load_model(MODEL_PATH)
    if model is not None:
        nuevo_precio = get_predict(150, 2, 1, "Caribe", model)
        print(f"$ {nuevo_precio:,.2f} COP")
    else:
        print("No se pudo cargar el modelo.")