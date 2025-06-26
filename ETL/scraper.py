import time
from playwright.sync_api import sync_playwright

# Definimos la url base
URL: str = "https://www.fincaraiz.com.co/venta/pagina"

# Definimos las listas
titulos,enlaces,precios,habitaciones,baños,metros = [],[],[],[],[],[]

def scrapear(N_pagina: int = 1) -> list:
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
            new_url = f"{URL}{pagina}"  # Modificamos la url
            page.goto(new_url)

            # Espera explícita hasta que aparezca al menos un contenedor de propiedad
            try:
                page.wait_for_selector("div.listingCard", timeout=10000)  # Espera hasta 10 segundos
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
                
                # Procesamos el bloque de detalles si existe
                if detalles:
                    texto = detalles.inner_text()
                    try:
                        habitaciones_data = texto.split("Habs.")[0].strip()
                        baños_data = texto.split("Habs.")[1].split("Baños")[0].strip()
                        metros_data = texto.split("Baños")[1].replace("m²", "").strip()
                    except (IndexError, AttributeError):
                        print("⚠ No se pudo parsear correctamente los detalles, verificar estructura.")
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
                habitaciones.append(habitaciones_data)
                baños.append(baños_data)
                metros.append(metros_data)
    
        browser.close()
        final = time.perf_counter() - inicio
    data = {
        "titulos": titulos,
        "enlaces": enlaces,
        "precios": precios,
        "habitaciones": habitaciones,
        "baños": baños,
        "metros_cuadrados": metros
    }
    return [final/60 , data]
    
if __name__ == "__main__":
    resultado = scrapear(10)
    print(f"tiempo{resultado[0]}")
    print(f" Data: {resultado[1]}")