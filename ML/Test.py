import pandas as pd
from utils import load_model,get_predict

# Ruta de los datos para validar
CSV_VALIDATE_PATH = "Data/validate_data.csv"

# Definimos la funcion para calcular el error absoluto
def validate_error(real_price:float,predict_price:float) -> float:
    """ Valida el porcentaje de error de cada prediccion en base a sus 2 precios
    
    Parametros:
    - real_price: precio real del inmueble
    - predict_price: prediccion de precio del inmueble
    
    Return:
    - porcentaje de error absoluto
    """
    if real_price <= 0:
        raise ValueError("El precio real debe ser mayor que cero.")
    return abs(predict_price - real_price) / real_price
    
def real_data(path:str):
    """ Obtiene la informacion real y la divide en 2 datos de entrada y precio real 
    
    Parametros:
    - path: direccion del csv con los datos de prueba
    
    Return:
    - entrada: datos que seran predecidos por el modelo
    - real_price: precio real de los inmubeles para realzizar validaciones
    """
    df = pd.read_csv(path)
    print(df.head())
    df.dropna(inplace=True)
    df = df[df["region"].ne("desconocido")]
    
    # Definimos los datos de entrada
    entrada = df[["habitaciones","baños","metros_cuadrados","region"]]
    
    # Definimos los datos reales de precios
    real_price = df["precios"]
    
    return entrada , real_price
    
def predict(model,entrada):
    """ Realiza predicciones sobre todos los datos para obtener el precio 
    
    Parametros:
    - model: modelo de machine learning a usar
    - entrada: dataframe que contenga las columans con los datos a usar
    """
    
    predicciones = []
    for i,row in entrada.iterrows():
        precio = get_predict(metros_cuadrados=row["metros_cuadrados"],
                            habitaciones=row["habitaciones"],
                            baños=row["baños"],
                            region=row["region"],
                            model=model)
        predicciones.append(precio)
        
    return pd.Series(predicciones)
    
def get_error_porcent(real_price ,predict_price ) -> pd.DataFrame:
    """ Crea un dataframe con los precios reales los predichos y el porcentaje de error 
    
    Parametros:
    - real_price: lista de precios reales
    - predict_price: lista de precios predichos por el modelo
    
    Return
    - df_error: dataframe con los 3 campos
    """
    
    # Reseteamos los indices para evitar nulos
    real_price = real_price.reset_index(drop=True)
    predict_price = predict_price.reset_index(drop=True) 
    
    # volvemos un dataframe
    df_error = pd.DataFrame({
        "real_price":real_price,
        "predict_price":predict_price
    })
    
    # Aplicamos la función fila por fila
    df_error["porcentaje_error"] = df_error.apply(
        lambda row: validate_error(row["real_price"], row["predict_price"]), axis=1
    )
    
    return df_error

if __name__ == "__main__":
    
    # Cargamos el modelo
    model,model_data = load_model()
    
    # Obtemos los datos reales 
    entrada, real_price = real_data(CSV_VALIDATE_PATH)
    
    print("\n Entrada \n")
    print(f"\n {entrada} \n")
    
    print("\n real price \n ")
    print(f"\n {real_price}")
    
    # Reliazamos las predicciones
    predict_price = predict(model,entrada)
    
    print("\n Prediciones \n")
    print(f"\n {predict_price} \n ")
    
    # Obtenemos los porcentajes
    df_error = get_error_porcent(real_price,predict_price)
    
    print("\n Lista de porcentajes \n")
    print(df_error)
    
    # mostramos el porcentaje de error
    promedio_error = df_error['porcentaje_error'].mean() * 100
    print(f"Porcentaje de error promedio: {promedio_error:.2f}%")
    
    # volvemos csv
    #df_error.to_csv("porcentaje_error.csv",encoding="utf-8")
    
    
    