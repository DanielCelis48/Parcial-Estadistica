import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# DATOS DE LOS PEDIDOS
# ============================================================
# Los tipos de postre se representan con números:
# 1 = Cheesecake
# 2 = Tres leches
# 3 = Torta de chocolate

datos = [
    2, 2, 3, 1, 3, 3, 1, 3, 2, 3,
    3, 1, 3, 3, 3, 2, 2, 3, 3, 2,
    2, 2, 2, 3, 3, 2, 3, 2, 3, 2,
    1, 2, 3, 3, 3, 2, 3, 3, 3, 1,
    2, 2, 2, 2, 2, 3, 3, 3, 1, 2,
    3, 2, 1, 3, 2, 2, 3, 3, 2, 3,
    2, 1, 1, 3, 3, 2, 3, 2, 3, 2,
    1, 3, 3, 3, 3, 3, 2, 3, 3, 3,
    3, 2, 2, 3, 3, 1, 3, 3, 1, 3,
    3, 1, 2, 2, 2, 2, 3, 1, 1, 3
]

# Crear la base de datos con los 100 pedidos.
df = pd.DataFrame({
    "Pedido": range(1, 101),
    "Tipo_postre": datos
})

# Relacionar cada código con el nombre del postre.
nombres_postres = {
    1: "Cheesecake",
    2: "Tres leches",
    3: "Torta de chocolate"
}

df["Nombre_postre"] = df["Tipo_postre"].map(nombres_postres)


# ============================================================
# TABLA DE PEDIDOS
# ============================================================
fig_pedidos = go.Figure(data=[go.Table(
    header=dict(
        values=["Pedido", "Tipo de postre"],
        align="center"
    ),
    cells=dict(
        values=[df["Pedido"], df["Nombre_postre"]],
        align="center"
    )
)])

fig_pedidos.update_layout(
    title_text="Registro de pedidos",
    title_x=0.5,
    margin=dict(t=80, b=30)
)


# ============================================================
# TABLA DE FRECUENCIAS
# ============================================================
# value_counts() cuenta cuántas veces aparece cada tipo de postre.
# sort_index() ordena los resultados según el código 1, 2 y 3.
frecuencia = df["Tipo_postre"].value_counts().sort_index()

# fi = frecuencia absoluta.
# xi = código del postre.
# Fi = frecuencia acumulada.
# hi = frecuencia relativa.
# Hi = frecuencia relativa acumulada.
# xi_fi = producto entre el código y su frecuencia.
fi = frecuencia.values
xi = frecuencia.index
Fi = frecuencia.cumsum()
hi = fi / fi.sum()
Hi = hi.cumsum()
xi_fi = xi * fi

fig = go.Figure(data=[go.Table(
    header=dict(
        values=["Xi", "Postre", "fi", "Fi", "hi", "Hi", "%", "Xi × fi"],
        align="center"
    ),
    cells=dict(
        values=[
            xi,
            [nombres_postres[x] for x in xi],
            fi,
            Fi,
            hi.round(2),
            Hi.round(2),
            (hi * 100).round(0),
            xi_fi
        ],
        align="center"
    )
)])

fig.update_layout(
    title_text="Tabla de frecuencias agrupadas - Preferencia de postres",
    title_x=0.5,
    margin=dict(t=100, b=30)
)


# ============================================================
# CÁLCULO DE MEDIA, MEDIANA Y MODA
# ============================================================
n = fi.sum()

# La media se obtiene multiplicando cada valor por su frecuencia
# y dividiendo la suma entre el total de pedidos.
media = sum(xi * fi) / n

# Ordenar los datos permite encontrar la mediana.
datos_ordenados = df["Tipo_postre"].sort_values().to_numpy()

if n % 2 == 0:
    mediana = (datos_ordenados[n // 2 - 1] + datos_ordenados[n // 2]) / 2
else:
    mediana = datos_ordenados[n // 2]

# La moda es el valor que tiene la frecuencia más alta.
moda = frecuencia.idxmax()


# ============================================================
# TABLA DE CÁLCULOS
# ============================================================
fig_calculos = go.Figure(data=[go.Table(
    header=dict(
        values=["Medida", "Fórmula", "Cálculo", "Resultado"],
        align="center"
    ),
    cells=dict(
        values=[
            ["Media", "Mediana", "Moda"],
            [
                "x̄ = Σ(Xi × fi) / n",
                "Me = (dato₅₀ + dato₅₁) / 2",
                "Mo = valor con mayor frecuencia"
            ],
            [
                "(1×15 + 2×35 + 3×50) / 100",
                "(2 + 3) / 2",
                "máx(fi) = 50"
            ],
            [
                round(media, 2),
                mediana,
                f"{moda} = {nombres_postres[moda]}"
            ]
        ],
        align="center"
    )
)])

fig_calculos.update_layout(
    title_text="Cálculo de media, mediana y moda",
    title_x=0.5,
    margin=dict(t=100, b=30)
)


# ============================================================
# CREAR UN SOLO HTML CON LAS TRES TABLAS
# ============================================================
# Se colocan las tres tablas en diferentes posiciones verticales
# para mostrarlas juntas en un mismo archivo HTML.
fig_html = go.Figure()

tabla_pedidos = fig_pedidos.data[0]
tabla_frecuencias = fig.data[0]
tabla_calculos = fig_calculos.data[0]

# Tabla de pedidos.
tabla_pedidos.domain = dict(x=[0, 1], y=[0.55, 1])

# Tabla de frecuencias.
tabla_frecuencias.domain = dict(x=[0, 1], y=[0.30, 0.50])

# Tabla de media, mediana y moda.
tabla_calculos.domain = dict(x=[0, 1], y=[0, 0.25])

fig_html.add_trace(tabla_pedidos)
fig_html.add_trace(tabla_frecuencias)
fig_html.add_trace(tabla_calculos)

fig_html.write_html(
    "tabla_postres.html",
    auto_open=True
)


# ============================================================
# GRÁFICOS ESTADÍSTICOS
# ============================================================
fig_graficos = make_subplots(
    rows=2,
    cols=2,
    specs=[
        [{"type": "domain"}, {"type": "xy"}],
        [{"type": "xy"}, {"type": "xy"}]
    ],
    subplot_titles=(
        "Diagrama de pastel - Preferencia de postres",
        "Histograma - Preferencia de postres",
        "Gráfico de líneas - Preferencia de postres",
        "Diagrama de bigotes - Tipo de postre"
    )
)


# ============================================================
# 1. DIAGRAMA DE PASTEL
# ============================================================
fig_graficos.add_trace(
    go.Pie(
        labels=[nombres_postres[x] for x in frecuencia.index],
        values=frecuencia.values
    ),
    row=1,
    col=1
)


# ============================================================
# 2. HISTOGRAMA
# ============================================================
fig_graficos.add_trace(
    go.Histogram(
        x=df["Tipo_postre"],
        xbins=dict(
            start=0.5,
            end=3.5,
            size=1
        )
    ),
    row=1,
    col=2
)


# ============================================================
# 3. GRÁFICO DE LÍNEAS
# ============================================================
fig_graficos.add_trace(
    go.Scatter(
        x=[nombres_postres[x] for x in frecuencia.index],
        y=frecuencia.values,
        mode="lines+markers",
        name="Frecuencia"
    ),
    row=2,
    col=1
)


# ============================================================
# 4. DIAGRAMA DE BIGOTES
# ============================================================
# Calcular los cuartiles, el mínimo y el máximo.
Q1 = df["Tipo_postre"].quantile(0.25)
Q2 = df["Tipo_postre"].quantile(0.50)
Q3 = df["Tipo_postre"].quantile(0.75)

minimo = df["Tipo_postre"].min()
maximo = df["Tipo_postre"].max()

# El rango intercuartílico mide la distancia entre Q1 y Q3.
RIC = Q3 - Q1

# Estos límites permiten identificar posibles valores atípicos.
limite_inferior = Q1 - 1.5 * RIC
limite_superior = Q3 + 1.5 * RIC

fig_graficos.add_trace(
    go.Box(
        y=df["Tipo_postre"],
        name="Tipo de postre",
        boxpoints="all",
        quartilemethod="linear"
    ),
    row=2,
    col=2
)


# ============================================================
# MOSTRAR LOS VALORES SOBRE EL DIAGRAMA
# ============================================================
fig_graficos.add_annotation(
    x=0,
    y=minimo,
    text=f"<b>Mínimo = {minimo}</b>",
    showarrow=True,
    arrowhead=2,
    ax=-80,
    ay=0,
    row=2,
    col=2
)

fig_graficos.add_annotation(
    x=0,
    y=Q1,
    text=f"<b>Q1 = {Q1:.1f}</b>",
    showarrow=True,
    arrowhead=2,
    ax=80,
    ay=0,
    row=2,
    col=2
)

fig_graficos.add_annotation(
    x=0,
    y=Q2,
    text=f"<b>Mediana = {Q2:.1f}</b>",
    showarrow=True,
    arrowhead=2,
    ax=90,
    ay=0,
    row=2,
    col=2
)

fig_graficos.add_annotation(
    x=0,
    y=Q3,
    text=f"<b>Q3 = {Q3:.1f}</b>",
    showarrow=True,
    arrowhead=2,
    ax=-80,
    ay=0,
    row=2,
    col=2
)

fig_graficos.add_annotation(
    x=0,
    y=maximo,
    text=f"<b>Máximo = {maximo}</b>",
    showarrow=True,
    arrowhead=2,
    ax=80,
    ay=0,
    row=2,
    col=2
)

fig_graficos.add_annotation(
    x=0,
    y=1.45,
    text=f"<b>RIC = Q3 - Q1 = {RIC:.1f}</b>",
    showarrow=False,
    row=2,
    col=2
)


# ============================================================
# CONFIGURACIÓN DE LOS GRÁFICOS
# ============================================================
fig_graficos.update_xaxes(
    title_text="Tipo de postre",
    row=1,
    col=2
)

fig_graficos.update_yaxes(
    title_text="Frecuencia",
    row=1,
    col=2
)

fig_graficos.update_xaxes(
    title_text="Tipo de postre",
    row=2,
    col=1
)

fig_graficos.update_yaxes(
    title_text="Frecuencia",
    row=2,
    col=1
)

fig_graficos.update_yaxes(
    title_text="Código del postre",
    tickmode="array",
    tickvals=[1, 2, 3],
    ticktext=[
        "Cheesecake",
        "Tres leches",
        "Torta de chocolate"
    ],
    row=2,
    col=2
)


# ============================================================
# TÍTULO GENERAL
# ============================================================
fig_graficos.update_layout(
    title_text="Gráficos estadísticos - Preferencia de postres",
    title_x=0.5,
    height=900,
    width=1200,
    showlegend=False,
    margin=dict(t=100, b=50, l=50, r=50)
)


# ============================================================
# CREAR EL ARCHIVO HTML DE LOS GRÁFICOS
# ============================================================
fig_graficos.write_html(
    "graficos_postres.html",
    auto_open=False
)

print("======================================")
print("ARCHIVO DE GRÁFICOS CREADO")
print("======================================")
print("graficos_postres.html")
