import json
import pandas as pd


with open(r"C:\Users\Alumno\Desktop\a.martin\OPT\EjerciciosPython\PRACTICA\premier.json", "r", encoding="utf-8") as f:
    data = json.load(f)


# Extraer la lista de partidos y normalizarla
df = pd.json_normalize(data, record_path=["matches"])


print(df)


jornada = df["round"]
equipo_local = df["team1"]
equipo_visitante = df["team2"]
resultado_ht = df["score.ht"]
resultado_ft = df["score.ft"]


print(jornada)
print(equipo_local)
print(resultado_ft)


