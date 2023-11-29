import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def aplicar_pca(ruta_archivo_csv: str, n_componentes: int =2) -> tuple:
    """
    Aplica Análisis de Componentes Principales (PCA) seguido de una regresión logística a un conjunto de datos.

    Args:
        ruta_archivo_csv (str): Ruta del archivo CSV que contiene los datos a analizar. El archivo debe tener una columna 'label'.
        n_componentes (int, opcional): Número de componentes principales a utilizar en el PCA. Por defecto es 2.

    Returns:
        tuple: Una tupla que contiene:
               - accuracy (float): La precisión (accuracy) del modelo de regresión logística.
               - componentes_principales (numpy.ndarray): Array con los componentes principales obtenidos del PCA.

    Raises:
        FileNotFoundError: Si el archivo CSV no se encuentra en la ruta proporcionada.
        ValueError: Si la columna 'label' no está presente en el archivo CSV.
        Exception: Para otros tipos de errores inesperados.
    """


    try:
        # Cargar los datos desde un archivo CSV
        datos = pd.read_csv(ruta_archivo_csv)

        # Verificar si 'label' está en las columnas
        if 'label' not in datos.columns:
            raise ValueError("'label' no se encuentra en el archivo CSV")

        # Separar las características y las etiquetas
        etiquetas = datos['label']
        caracteristicas = datos.drop('label', axis=1)

        # Normalizar las características
        caracteristicas_normalizadas = StandardScaler().fit_transform(caracteristicas)

        # Aplicar PCA
        pca = PCA(n_components=n_componentes)
        componentes_principales = pca.fit_transform(caracteristicas_normalizadas)

        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(componentes_principales, etiquetas, test_size=0.3, random_state=42)

        # Crear y entrenar el modelo de regresión logística
        modelo = LogisticRegression()
        modelo.fit(X_train, y_train)

        # Realizar predicciones en el conjunto de prueba
        predicciones = modelo.predict(X_test)

        # Calcular y devolver el accuracy
        accuracy = accuracy_score(y_test, predicciones)
        return accuracy, componentes_principales

    except FileNotFoundError:
        print(f"Error: El archivo {ruta_archivo_csv} no se encontró.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    print("\t\t\t***ANÁLISIS DE COMPONENTES PRINCIPALES CON REGRESIÓN LOGÍSTICA***")

    for i in range(2, 6):
        print(f"\n >>> PCA con {i} componentes")
        try:
            accuracy, componentes = aplicar_pca('scop.csv', n_componentes=i)
            print(f"Accuracy con {i} componentes: {accuracy:.2f}")
            print("Componentes Principales:")
            print(componentes)
        except Exception as e:
            print(f"Error al procesar PCA con {i} componentes: {e}")
