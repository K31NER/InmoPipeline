import pandas as pd
from Extract import scrapear
from Transform import add_regiones, clean_data

URL_viviendas:str = "https://www.fincaraiz.com.co/proyectos-vivienda/pagina"

def create_validate_data(url:str,pagianas:int,csv_name:str):
    """ Relaliza un scapreo de una seccion diferente para obtener datos 
    para validar el porcentaje de error del modelo 
    
    Parametros:
    
    - url : pagina a scrapear
    - paginas: Numero de paginas a scrapear
    - csv_name: Nombre del archivo csv
    
    """
    
    resultado = scrapear(url,pagianas)
    df = pd.DataFrame(resultado[1])
    df_clean = clean_data(df)
    df_regiones = add_regiones(df_clean)
    df_regiones.to_csv(f"Data/{csv_name}.csv")
    return f"csv creado con exito en la ruta Data/{csv_name}.csv"
    
if __name__ == "__main__":
    print(create_validate_data(URL_viviendas,20,"validate_data"))