import pandas as pd
import requests
from bs4 import BeautifulSoup


class TableExtractor:
    def __init__(self, url):
        self.url = url

    def extract_table(self):
        response = requests.get(self.url, verify=False)
        content = response.content

        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find('table')
        dataframe = pd.read_html(str(table))[0]

        return dataframe

    def filter_columns(self, dataframe, columns):
        dataframe_filtered = dataframe.iloc[:, columns]
        return dataframe_filtered

    def save_to_csv(self, dataframe, filename):
        dataframe.to_csv(filename, index=False)
        print("Archivo CSV guardado exitosamente.")


# URL de la página ASPX
url = "https://www.sat.gob.pe/websitev8/modulos/contenidos/mult_papeletas_ti_rntv2.aspx"

# Crear instancia de la clase TableExtractor
table_extractor = TableExtractor(url)

# Extraer la tabla
table = table_extractor.extract_table()

# Definir las columnas deseadas
# desired_columns = [0, 1, 3]
desired_columns = [0, 3]

# Filtrar las columnas de la tabla
filtered_table = table_extractor.filter_columns(table, desired_columns)

# Guardar la tabla filtrada en un archivo CSV

table_extractor.save_to_csv(filtered_table, "tabla_SAT.csv")
