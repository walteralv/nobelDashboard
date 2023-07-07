import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from datetime import datetime

from db.db import dbAlumnos, dbDescuento, dbInformacion, dbPagos, areas


external_script = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]
app = dash.Dash(
    __name__,
    external_scripts=external_script,
)
app.scripts.config.serve_locally = True

server = app.server

df_Alumnos = pd.DataFrame(list(dbAlumnos.find({}))).set_index("_id")
df_Descuento = pd.DataFrame(list(dbDescuento.find({}))).set_index("_id")
df_Informacion = pd.DataFrame(list(dbInformacion.find({}))).set_index("_id")
df_Pagos = pd.DataFrame(list(dbPagos.find({}))).set_index("_id")
df_carreras = pd.DataFrame(list(areas.items()), columns=['carrera', 'area'])
df_Alumnos = df_Alumnos.merge(df_carreras, on='carrera')

num_alumnos = df_Alumnos.shape[0]
ganancias = df_Pagos["precio"].sum()
total_descontado = df_Descuento["descuento"].sum()

df_Pagos['fecha_pago'] = pd.to_datetime(df_Pagos['fecha_pago'])
current_month = datetime.now().month
filtered_df = df_Pagos[df_Pagos['fecha_pago'].dt.month == current_month]
ganancia_mes = filtered_df['precio'].sum()

"""
grouped_data = df_Pagos.groupby(df_Pagos['fecha_pago'].dt.date)['precio'].sum().reset_index()

# Sort the grouped data by date in ascending order
sorted_data = grouped_data.sort_values('fecha_pago')

fig1 = px.line(sorted_data, x='fecha_pago', y='precio')
fig1.update_layout(
    title='Payments Over Time',
    xaxis_title='Fecha de Pago',
    yaxis_title='Precio'
)
"""

# Creating the histogram
fig1 = px.histogram(df_Alumnos, x='edad', nbins=20, title='Distribución de Edades')
fig1.update_layout(xaxis_title='Edad', yaxis_title='Frecuencia')

# Grouping the data by 'carrera' and 'edad' and counting the occurrences
grouped_data = df_Alumnos.groupby(['area', 'edad']).size().reset_index(name='count')
fig2 = go.Figure()
for area in grouped_data['area'].unique():
    df_area = grouped_data[grouped_data['area'] == area]
    fig2.add_trace(go.Bar(
        x=df_area['edad'],
        y=df_area['count'],
        name=area
    ))
fig2.update_layout(
    title='Distribución de Alumnos por Area y Edad',
    xaxis_title='Edad',
    yaxis_title='Count',
    barmode='group'
)


# Count the occurrences of each carrera
carrera_counts = df_Alumnos['carrera'].value_counts()
# Get the top 10 most studied carreras and group the rest as "otros"
top_10_carreras = carrera_counts.head(5)
other_count = carrera_counts[5:].sum()
top_10_carreras['Otros'] = other_count

# Creating the bar chart
fig3 = go.Figure(data=[go.Pie(labels=top_10_carreras.index, values=top_10_carreras.values)])
fig3.update_layout(
    title='Las 5 carreras más estudiadas',
    xaxis_title='Carrera',
    yaxis_title='Cantidad de estudiantes',
    width=600,  # Set the width of the figure
    height=400,  # Set the height of the figure
    margin=dict(t=60, b=10, l=10, r=10),  # Set the padding/margin values
)

# Counting the occurrences of each area
df_area = df_Alumnos['area'].value_counts().reset_index()
df_area.columns = ['Area', 'Cantidad']

# Creating the pie chart
fig4 = px.pie(df_area, values='Cantidad', names='Area')
fig4.update_layout(
    title='Distribución de Registros por Área',
    width=600,  # Set the width of the figure
    height=400,  # Set the height of the figure
    margin=dict(t=60, b=10, l=10, r=10),  # Set the padding/margin values
)


# Fig 5
df_Pagos["num_cuotas"] = df_Pagos['cuotas'].dropna().map(lambda x: len(x))
frequencies = df_Pagos["num_cuotas"].dropna().value_counts()
# Crear el gráfico Pie
fig5 = go.Figure(data=go.Pie(labels=frequencies.index, values=frequencies.values))
fig5.update_layout(
    title="Distribución de Número de Cuotas",
    width=600,  # Set the width of the figure
    height=400,  # Set the height of the figure
    margin=dict(t=60, b=10, l=10, r=10),  # Set the padding/margin values
)

# Obtener las frecuencias de cada variable
frequencies = df_Informacion.drop("alumno_dni", axis=1).sum()
fig6 = go.Figure(data=go.Pie(labels=frequencies.index, values=frequencies.values))

# Personalizar el gráfico
fig6.update_layout(
    title="Como te enteraste de Nobel?",
    width=600,  # Set the width of the figure
    height=400,  # Set the height of the figure
    margin=dict(t=60, b=10, l=10, r=10),  # Set the padding/margin values
)

app.layout = html.Div(
    html.Div(
        children=[
            html.Div(
                children=[
                    html.H1(children="Nobel Dashboard", className=" py-3 text-5xl font-bold text-gray-800"),
                    html.Div(
                        children="",
                        className="text-left prose prose-lg text-2xl  py-3 text-gray-600",
                    ),
                ],
                className="w-full mx-14 px-16 shadow-lg bg-white -mt-14 px-6 container my-3 ",
            ),
            html.Div(
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                f"{num_alumnos}",
                                html.Br(),
                                html.Span("Total de Alumnos", className="text-l text-l font-bold text-center"),
                            ],
                            className="shadow-xl py-4 px-5 my-auto h-32 text-2xl bg-blue-950 text-white text-center font-bold ",
                        ),
                        html.Div(
                            children=[
                                f"S/ {ganancias}",
                                html.Br(),
                                html.Span("Ganancias Estimadas", className="text-l font-bold text-center"),
                            ],
                            className="shadow-xl py-4 px-5 my-auto h-32 text-2xl bg-lime-500 text-white text-center font-bold",
                        ),
                        html.Div(
                            children=[
                                f"S/ {total_descontado}",
                                html.Br(),
                                html.Span("Descuento Total", className="text-l font-bold text-center"),
                            ],
                            className="shadow-xl py-4 px-5 my-auto h-32 text-2xl bg-red-500 text-white text-center font-bold",
                        ),
                        html.Div(
                            children=[
                                f"S/ {ganancia_mes}",
                                html.Br(),
                                html.Span("Ganancia del Mes", className="text-l font-bold text-center"),
                            ],
                            className="shadow-xl py-4 px-5 my-auto h-32 text-2xl bg-blue-950 text-white text-center font-bold",
                        ),
                    ],
                    className="my-4 w-full grid grid-flow-rows grid-cols-1 lg:grid-cols-4 gap-y-4 lg:gap-[60px]",
                ),
                className="flex max-w-full justify-between items-center ",
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.Graph(id="carrerasMasEstudiadas", figure=fig3),
                        ],
                        className="w-full shadow-2xl rounded-sm",
                    ),
                    html.Div(
                        children=[
                            dcc.Graph(id="distribucionPorAreas", figure=fig4),
                        ],
                        className="w-full shadow-2xl rounded-sm",
                    ),
                    html.Div(
                        children=[
                            dcc.Graph(id="disEdad", figure=fig1),
                        ],
                        className="shadow-2xl rounded-sm",
                    ),
                    html.Div(
                        children=[
                            dcc.Graph(id="disEdadArea", figure=fig2),
                        ],
                        className="shadow-2xl rounded-sm",
                    ),
                    html.Div(
                        children=[
                            dcc.Graph(id="disEdadArea", figure=fig5),
                        ],
                        className="shadow-2xl rounded-sm",
                    ),
                    html.Div(
                        children=[
                            dcc.Graph(id="disInfo", figure=fig6),
                        ],
                        className="shadow-2xl rounded-sm",
                    )
                ],
                className="grid grid-cols-1 lg:grid-cols-2 gap-4",
            ),
            # html.Div(
            #     children=[
            #     ],
            #     className="flex ",
            # ),
        ],
        className="bg-[#ebeaee]  flex py-14 flex-col items-center justify-center ",
    ),
    className="bg-[#ebeaee] container mx-auto px-14 py-4",
)

if __name__ == "__main__":
    app.run_server(debug=True)