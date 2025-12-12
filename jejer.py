import json
import pandas as pd

# Abrir y cargar el archivo.json
with open("premier.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Normalizar la lista de partidos
df = pd.json_normalize(data, record_path=["matches"])

# Mostrar todos los datos [jornada, fecha, hora, equipoLocal, equipoVisitante, finPrimeraParte, resultadoFinal]
print(df)

# Extraer las columanas de los datos para tratarlas mas adelante
jornada = df["round"]   # Sacamos la jornada
equipo_local = df["team1"]  # Sacamos el equipo local
equipo_visitante = df["team2"]  # Sacamos el euipo vsitante
resultado_ht = df["score.ht"]   # Sacamos el resultado cuando acaba la primera parte
resultado_ft = df["score.ft"]   # Sacamos el resultado final

# Diferentes prints
# print(jornada)
# print(equipo_local)
# print(equipo_visitante)
# print(resultado_ft)
# print(resultado_ht)

# Creamos un conjunto para evitar duplicados
equipos = set()
# recorremos las filas de todo el archivo
for row in df.itertuples(): #intertuples() recorre filas que no se va a modificar (Sacado de ChatGPT)
    equipos.add(row.team1)
    equipos.add(row.team2)
# Convertimos el conjunto a una lista
equipos = list(equipos)


victorias = {e: 0 for e in equipos}
goles_favor = {e: 0 for e in equipos}
goles_contra = {e: 0 for e in equipos}
remontadas = {e: 0 for e in equipos}

for _, row in df.iterrows():
    local = row["team1"]
    visitante = row["team2"]

    # Algunos partidos no tienen score.ht, así que controlamos ese caso
    if isinstance(row["score.ht"], list):
        gl_ht, gv_ht = row["score.ht"]
    else:
        gl_ht, gv_ht = 0, 0

    gl_ft, gv_ft = row["score.ft"]

    # Goles a favor y en contra
    goles_favor[local] += gl_ft
    goles_contra[local] += gv_ft

    goles_favor[visitante] += gv_ft
    goles_contra[visitante] += gl_ft

    # Victorias
    if gl_ft > gv_ft:
        victorias[local] += 1
    elif gv_ft > gl_ft:
        victorias[visitante] += 1

    # Remontadas
    # Local perdía al descanso y gana al final
    if gl_ht < gv_ht and gl_ft > gv_ft:
        remontadas[local] += 1
    # Visitante perdía al descanso y gana al final
    if gv_ht < gl_ht and gv_ft > gl_ft:
        remontadas[visitante] += 1

# ================================
#        RESULTADOS FINALES
# ================================

equipo_mas_victorias = max(victorias, key=victorias.get)
equipo_mas_goles = max(goles_favor, key=goles_favor.get)
equipo_menos_goles = min(goles_favor, key=goles_favor.get)
equipo_mas_remontadas = max(remontadas, key=remontadas.get)

print("\n==============================")
print("        RESULTADOS LIGA")
print("==============================")

print("Equipo con más victorias:")
print("  ", equipo_mas_victorias, "-", victorias[equipo_mas_victorias], "victorias")

print("\nEquipo más goleador:")
print("  ", equipo_mas_goles, "-", goles_favor[equipo_mas_goles], "goles")

print("\nEquipo menos goleador:")
print("  ", equipo_menos_goles, "-", goles_favor[equipo_menos_goles], "goles")

print("\nEquipo con más remontadas:")
print("  ", equipo_mas_remontadas, "-", remontadas[equipo_mas_remontadas], "remontadas")

print("\n==============================")
