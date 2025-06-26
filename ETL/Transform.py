import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """ Obtiene las ciudades y limpia el campo de precio"""
    
    # Obtenemos solo la ciudad
    df["ciudades"] = df["titulos"].str.split(",").str[-1].str.strip()
    
    # Limpiamos el precio
    df["precios"] = (
        df["precios"]
        .str.replace("Desde", "", regex=False)
        .str.replace(r"[$\.]", "", regex=True)
        .str.strip()
    )
    
    # Volvemos el precio un valor numerico
    df["precios"] = pd.to_numeric(df["precios"],errors="coerce")

    return df
    

if __name__ == "__main__":
    df = pd.read_csv("Data/inmuebles.csv")
    #df_limpio = clean_data(df)
    print(df["metros_cuadrados"].head())
