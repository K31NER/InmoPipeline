import duckdb 
import pandas as pd
from Extract import scrapear
from Transform import clean_data

def create_db(n_paginas:int = 50, name:str = "Data/inmuebles.db"):
    """ Crea y llena la base de datos con los datos obtenidos del scraper
    
    Parametros:
    - n_paginas: numero de paginas a buscar por defecto 50
    - name: nombre de la conexion que termine en .db por defecto es inmuebles.db
    """
    
    conn = None # Definimos la conexion vacia
    try: 
        # generamos la conexion
        conn = duckdb.connect(name)

        # Obtenemos los datos
        datos = scrapear(n_paginas)

        # Mostramos el tiempo que demoro en scrapear
        print(f"Tiempo transcurrido: {datos[0]:.2f} minutos")
        
        df = pd.DataFrame(datos[1])# Generamos el dataframe
        
        # Limpiamos los datos
        clean_df = clean_data(df)
        
        # Registramos el DataFrame en DuckDB
        conn.register("df", clean_df)

        # Insertas el DataFrame como tabla (crea o reemplaza)
        conn.execute("CREATE TABLE IF NOT EXISTS propiedades AS SELECT * FROM df")

        # Verificas que se guardó correctamente
        print(conn.execute("SELECT * FROM propiedades LIMIT 5").fetchdf())
        
        print(f"Base de datos '{name}' generada correctamente.")

    except Exception as e:
        print(f"Error durante la creación de la base de datos: {e}")
    finally:
        if conn: 
            # Cerramos la conexion
            conn.close()


def create_csv(file_name: str ,connection: str = "Data/inmuebles.db") -> str:
    """ Crea un archivo csv con los datos almacenados en la base de datos 
    
    Parametros:
    - file_name: Nombre el archivo csv
    - connection: nombre de la conexion de base de datos con la extension
    
    Retorna: 
    - message: mensaje informativo sobre el estado de la creacion
    """
    
    try:
        # Realizamos la conexión
        conn = duckdb.connect(connection)

        # Obtenemos todos los registros
        result = conn.execute("SELECT * FROM propiedades").fetch_df()

        # Guardamos como CSV
        result.to_csv(f"Data/{file_name}.csv", index=False)

        message = "Se generó correctamente el archivo CSV."

    except duckdb.CatalogException as e:
        message = f"Error en la consulta SQL: {e}"

    except duckdb.IOException as e:
        message = f"Error al acceder al archivo o base de datos: {e}"

    except Exception as e:
        message = f"Ocurrió un error inesperado: {e}"

    finally:
        try:
            conn.close()
        except:
            pass 

    return {"Message": message}

if __name__ == "__main__":
    #print(create_db())
    print(create_csv("inmuebles"))