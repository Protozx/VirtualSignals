import requests

class WebScraper:
    def __init__(self):
        self.html_content = None

    def fetch_html(self, url):
        try:
            # Realiza una solicitud HTTP GET para obtener el contenido HTML de la URL
            response = requests.get(url)
            
            # Verifica si la solicitud fue exitosa (código de respuesta 200)
            if response.status_code == 200:
                self.html_content = response.text
                print("HTML descargado con éxito.")
            else:
                print(f"Error al descargar el HTML. Código de respuesta: {response.status_code}")
        except Exception as e:
            print(f"Error al realizar la solicitud HTTP: {e}")

    def save_to_file(self, file_path):
        if self.html_content:
            try:
                # Escribe el contenido HTML en un archivo .txt
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.html_content)
                print(f"Contenido HTML guardado en {file_path}")
            except Exception as e:
                print(f"Error al escribir en el archivo: {e}")
        else:
            print("No hay contenido HTML para guardar.")

# Ejemplo de uso:
if __name__ == "__main__":
    scraper = WebScraper()
    url = "https://sweetalert2.github.io/#timerProgressBar"
    file_path = "webpagina.txt"
    
    scraper.fetch_html(url)
    scraper.save_to_file(file_path)
