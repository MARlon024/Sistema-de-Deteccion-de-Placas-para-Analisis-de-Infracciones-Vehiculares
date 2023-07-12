import pandas as pd
import plotly.express as px
import time

# Cargar el archivo CSV
# df = pd.read_csv('number_plate_info.csv')


def plot_infracciones_por_gravedad(df):
    # Convertir la columna 'Fecha' al formato de fecha
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%y')

    # Extraer el año de la columna 'Fecha'
    df['Año'] = df['Fecha'].dt.year

    # Calcular la cantidad de infracciones por nivel de gravedad y año
    df_grouped = df.groupby(['Nivel de gravedad', 'Año']
                            ).size().reset_index(name='Cantidad')

    # Generar la gráfica
    fig = px.line(df_grouped, x='Año', y='Cantidad', color='Nivel de gravedad', markers=True,
                  title='Evolución de la cantidad de infracciones por nivel de gravedad por año')

    # Mostrar la gráfica
    fig.show()


def tendencia_4_infracciones(df, anho_inicio, anho_fin):
    # Convertir la columna 'Fecha' al tipo de dato 'datetime'
    df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True)

    # Filtrar los datos solo desde el anho_inicio al anho_fin
    df = df[(df['Fecha'].dt.year >= anho_inicio)
            & (df['Fecha'].dt.year <= anho_fin)]

    # Contar la cantidad de ocurrencias de cada tipo de infracción
    top_infracciones = df['Infraccion'].value_counts().nlargest(
        4).index.tolist()

    # Filtrar los datos para mantener solo las 4 infracciones más frecuentes
    df_top_infracciones = df[df['Infraccion'].isin(top_infracciones)]

    # Agrupar por tipo de infracción y año, y contar la cantidad de ocurrencias
    df_grouped = df_top_infracciones.groupby(
        ['Infraccion', df_top_infracciones['Fecha'].dt.year]).size().reset_index(name='Cantidad')

    # Crear la gráfica de tendencia
    fig = px.line(df_grouped, x='Fecha', y='Cantidad', color='Infraccion',
                  title=f'Tendencia de las 4 infracciones más frecuentes ({anho_inicio}-{anho_fin})')

    # Mostrar la gráfica
    fig.show()


def monto_total_por_infraccion(df, anho_inicio, anho_fin):
    # Convertir la columna 'Fecha' al tipo de dato 'datetime'
    df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True)

    # Filtrar los datos solo desde el anho_inicio al anho_fin
    df = df[(df['Fecha'].dt.year >= anho_inicio)
            & (df['Fecha'].dt.year <= anho_fin)]

    # Agrupar por tipo de infracción y año, y calcular el monto total recaudado
    df_grouped = df.groupby(['Infraccion', df['Fecha'].dt.year])[
        'Costo'].sum().reset_index()

    # Crear la gráfica de barras
    fig = px.bar(df_grouped, x='Infraccion', y='Costo', color='Fecha',
                 barmode='group', title='Monto total recaudado por tipo de infracción y año')

    # Mostrar la gráfica
    fig.show()


def monto_total_por_infraccionYAnho(df):
    # Convertir la columna 'Fecha' al tipo de dato 'datetime'
    df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True)

    # Filtrar los datos solo desde el 2017 al 2023
    df = df[(df['Fecha'].dt.year >= 2017) & (df['Fecha'].dt.year <= 2023)]

    # Solicitar al usuario el año y el rango de meses
    year = int(input("Ingrese el año (2017-2023): "))
    start_month = int(input("Ingrese el mes de inicio (1-12): "))
    end_month = int(input("Ingrese el mes de fin (1-12): "))

    # Filtrar los datos por el año y rango de meses especificado
    df_filtered = df[
        (df['Fecha'].dt.year == year) &
        (df['Fecha'].dt.month >= start_month) &
        (df['Fecha'].dt.month <= end_month)
    ]

    # Agrupar por tipo de infracción y año, y calcular el monto total recaudado
    df_grouped = df_filtered.groupby(['Infraccion', df_filtered['Fecha'].dt.year])[
        'Costo'].sum().reset_index()

    # Convertir la columna 'Fecha' a tipo de dato categórico
    df_grouped['Fecha'] = df_grouped['Fecha'].astype(str)

    # Crear la gráfica de barras
    fig = px.bar(df_grouped, x='Infraccion', y='Costo', color='Fecha', barmode='group',
                 title=f"Monto total recaudado por tipo de infracción y año ({year}, Meses {start_month}-{end_month})")

    # Mostrar la gráfica
    fig.show()


def tendencia_todas_infracciones(df, anho_inicio, anho_fin):
    # Convertir la columna 'Fecha' al tipo de dato 'datetime'
    df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True)

    # Filtrar los datos solo desde el anho_inicio al anho_fin
    df = df[(df['Fecha'].dt.year >= anho_inicio)
            & (df['Fecha'].dt.year <= anho_fin)]

    # Contar la cantidad de ocurrencias de cada tipo de infracción
    infracciones_frecuentes = df['Infraccion'].value_counts().index.tolist()

    # Filtrar los datos para mantener solo las infracciones más frecuentes
    df_infracciones_frecuentes = df[df['Infraccion'].isin(
        infracciones_frecuentes)]

    # Agrupar por tipo de infracción y año, y contar la cantidad de ocurrencias
    df_grouped = df_infracciones_frecuentes.groupby(
        ['Infraccion', df_infracciones_frecuentes['Fecha'].dt.year]).size().reset_index(name='Cantidad')

    # Crear la gráfica de tendencia
    fig = px.line(df_grouped, x='Fecha', y='Cantidad', color='Infraccion',
                  title=f'Tendencia de las infracciones más frecuentes ({anho_inicio}-{anho_fin})')

    # Mostrar la gráfica
    fig.show()


df = pd.read_csv('number_plate_info.csv')
#tendencia_todas_infracciones(df, 2017, 2023)

tendencia_4_infracciones(df, 2017, 2023)

# Llamar a la función monto_total_por_infraccion para generar la gráfica de monto total
monto_total_por_infraccion(df, 2017, 2023)
