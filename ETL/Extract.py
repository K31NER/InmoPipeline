import re
import time
from playwright.sync_api import sync_playwright

# Definimos la url base
URL: str = "https://www.fincaraiz.com.co/venta/pagina"

# Definimos las listas
titulos,enlaces,precios,habitaciones_list,baños_list,metros_list = [],[],[],[],[],[]


def scrapear(url_base:str = URL,N_pagina: int = 1) -> list:
    """ Scrapea los datos de fincaraiz de x nuemero de paginas
    
    Parametros: 
    
    - N_pagina: numero de pagians a revisar -> int
    
    retorna:
    
    - indice 0: tiempo de ejecucion -> str
    - indice 1: datos guardatos -> dict 
    """
    
    with sync_playwright() as p:
        inicio = time.perf_counter()
        # Configuramos el navegador
        browser = p.chromium.launch(headless=True) # Definimos el navegador
        page = browser.new_page() # Creamosuna nueva pagina

        # recorremos cada pagina
        for pagina in range(1, N_pagina + 1):
            new_url = f"{url_base}{pagina}"  # Modificamos la url
            page.goto(new_url)

            # Espera explícita hasta que aparezca al menos un contenedor de propiedad
            try:
                page.wait_for_selector("div.listingCard", timeout=60000)  # Espera hasta 10 segundos
            except:
                print(f"No se encontraron propiedades en la página {pagina}")
                continue
            
            # Definimos la propiedas a recorrer
            propiedades = page.query_selector_all("div.listingCard")

            print(f"Página {pagina}: {len(propiedades)} propiedades encontradas")
            
            # Recorremos cada dato en la propiedad
            for propiedad in propiedades:
                
                # Definimos su selector
                precio = propiedad.query_selector("span.ant-typography.price strong")
                link = propiedad.query_selector("a.lc-data")
                detalles = propiedad.query_selector("div.lc-typologyTag")
                
                # Limpiamos los datos del html
                precio_limpio = precio.inner_text() if precio else "N/A"
                titulo = link.get_attribute("title") if link else "N/A"
                href = link.get_attribute("href") if link else "N/A"
                
                # Inicializamos por cada propiedad
                ambientes = 0
                habitaciones = 0
                baños = 0
                metros = 0
                
                # Procesamos el bloque de detalles si existe
                if detalles:
                    texto = detalles.inner_text()
                    
                    # Buscamos los valores en base a sus palabras clave
                    match_ambiente = re.search(r"(\d+)\s+Ambiente", texto)
                    match_habs = re.search(r"(\d+)\s*Habs?", texto)
                    match_banos = re.search(r"(\d+)\s*Baños?", texto)
                    match_metros = re.search(r"(\d+(\.\d+)?)\s*m²", texto) 

                    if match_ambiente:
                        ambientes = match_ambiente.group(1) # Devolvemos el valor
                    if match_habs:
                        habitaciones = match_habs.group(1)
                    if match_banos:
                        baños = match_banos.group(1)
                    if match_metros:
                        metros = match_metros.group(1)

                # Consolidación
                habitaciones_final = habitaciones if habitaciones != "N/A" else ambientes
                
                """ 
                # Imprimimos o guardamos los resultados
                print(f"Título: {titulo}")
                print(f"Enlace: {href}")
                print(f"Precio: {precio_limpio}")
                print(f"Habitaciones: {habitaciones_data}")
                print(f"Baños: {baños_data}")
                print(f"Metros cuadrados: {metros_data}")
                """
                
                # Agregas los datos a cada lista
                titulos.append(titulo)
                enlaces.append(f"https://www.fincaraiz.com.co{href}")
                precios.append(precio_limpio)
                habitaciones_list.append(habitaciones_final)
                baños_list.append(baños)
                metros_list.append(metros)
    
        browser.close()
        final = time.perf_counter() - inicio
    
    # Preparamos los datos
    data = {
        "titulos": titulos,
        "enlaces": enlaces,
        "precios": precios,
        "habitaciones": habitaciones_list,
        "baños": baños_list,
        "metros_cuadrados": metros_list
    }
    return [final/60 , data]
    
if __name__ == "__main__":
    resultado = scrapear(24)
    #df = pd.DataFrame(resultado[1])
    #print(f"tiempo{resultado[0]}")
    #print(f" Data: {resultado[1]}")
   