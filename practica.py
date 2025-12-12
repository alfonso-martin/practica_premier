import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def ganador(row):
    if row["score.ft"][0] > row["score.ft"][1]:
        return row["team1"]
    elif row["score.ft"][0] < row["score.ft"][1]:
        return row["team2"]
    else:
        return None



with open(r"C:\Users\Alumno\Desktop\PRACTICA_PREMIER\premier.json", "r", encoding="utf-8") as f:
    data = json.load(f)


# Extraer la lista de partidos y normalizarla
partidos = pd.json_normalize(data, record_path=["matches"])

"""
print(df)


jornada = df["round"]
equipo_local = df["team1"]
equipo_visitante = df["team2"]
resultado_ht = df["score.ht"]
resultado_ft = df["score.ft"]


print(jornada)
print(equipo_local)
print(resultado_ft)
"""


partidos["winner"] = partidos.apply(ganador, axis=1)
victorias = partidos["winner"].value_counts().head(5)  # Top 5


# Datos: nombres de los equipos y sus victorias
equipos = victorias.index
victorias_num = victorias.values

# Crear gráfico de barras horizontal
plt.figure(figsize=(10,6))
plt.barh(equipos, victorias_num, color='mediumslateblue')

# Poner el equipo con más victorias arriba
plt.gca().invert_yaxis()

# Títulos
plt.title("Top 5 equipos con más victorias", fontsize=16)
plt.xlabel("Victorias")
plt.ylabel("Equipo")

# Mostrar número de victorias al lado de cada barra
for i, v in enumerate(victorias_num):
    plt.text(v + 0.1, i, str(v), va='center')

# Mostrar gráfico
plt.show()