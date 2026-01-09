import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# Menú principal
def menu():
    while True:
        print("\n---------------- Menú de gráficas ----------------")
        print("1. Clasificacion final de la Premier")
        print("2. Equipo más goleador")
        print("3. Equipo menos goleador")
        print("4. Equipo con más remontadas")
        print("5. Equipo con más victorias como local y/o visitante")
        print("6. Comparacion de dos equipos")
        print("7. Salir")
        print("----------------------------------------------------")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            graficaVictorias(data)
            
        elif opcion == "2":
            graficaVictorias(data)
            
        elif opcion == "3":
            graficaVictorias(data)
            
        elif opcion == "4":
            graficaVictorias(data)
            
        elif opcion == "5":
            graficaVictorias(data)
            
        elif opcion == "6":
            partidos = pd.json_normalize(data, record_path=["matches"])
            equipos = sorted(
                pd.concat([partidos["team1"], partidos["team2"]]).unique()
            )

            print("\nEquipos disponibles:")
            for e in equipos:
                print("-", e)

            equipo1 = input("\nSelecciona el primer equipo: ")
            equipo2 = input("Selecciona el segundo equipo: ")

            if equipo1 in equipos and equipo2 in equipos and equipo1 != equipo2:
                compararEquipos(data, equipo1, equipo2)
            else:
                print("Selección inválida de equipos.")
            

        elif opcion == "7":
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")



# Sacar ganador del partido
def ganador(row):
    if row["score.ft"][0] > row["score.ft"][1]:
        return row["team1"]
    elif row["score.ft"][0] < row["score.ft"][1]:
        return row["team2"]
    else:
        return None
    


# Sacar grafico completo de clasificacion de la premier
def graficaVictorias(data):
    # Normalizar partidos
    partidos = pd.json_normalize(data, record_path=["matches"])

    # Determinar ganador
    partidos["winner"] = partidos.apply(ganador, axis=1)

    # Equipos (usando los mismos campos que ganador)
    equipos = pd.concat([
        partidos["team1"],
        partidos["team2"]
    ]).unique()

    tabla = pd.DataFrame(index=equipos, columns=["Victorias", "Empates", "Derrotas"])
    tabla = tabla.fillna(0)

    # Contabilizar resultados
    for _, p in partidos.iterrows():
        team1 = p["team1"]
        team2 = p["team2"]
        win = p["winner"]

        if win is None:
            tabla.loc[team1, "Empates"] += 1
            tabla.loc[team2, "Empates"] += 1
        else:
            tabla.loc[win, "Victorias"] += 1
            perdedor = team2 if win == team1 else team1
            tabla.loc[perdedor, "Derrotas"] += 1

    # Ordenar clasificación
    tabla = tabla.sort_values("Victorias", ascending=False)

    # Datos
    equipos = tabla.index
    v = tabla["Victorias"]
    e = tabla["Empates"]
    d = tabla["Derrotas"]

    gap = 0.6  # espacio visual entre sectores

    plt.figure(figsize=(12, 7))

    # Barras horizontales segmentadas con separación
    plt.barh(equipos, v, height=0.45, label="Victorias")
    plt.barh(equipos, e, left=v + gap, height=0.45, label="Empates")
    plt.barh(equipos, d, left=v + e + 2*gap, height=0.45, label="Derrotas")

    plt.gca().invert_yaxis()

    plt.title("Clasificación final de la Premier", fontsize=16)
    plt.xlabel("Partidos")
    plt.ylabel("Equipo")
    plt.legend()

    # Ocultar eje X porque hay gaps artificiales
    # plt.xticks([])

    plt.tight_layout()
    plt.show()



def compararEquipos(data, equipo1, equipo2):
    partidos = pd.json_normalize(data, record_path=["matches"])

    stats = {
        equipo1: {"Victorias": 0, "Empates": 0, "Derrotas": 0},
        equipo2: {"Victorias": 0, "Empates": 0, "Derrotas": 0}
    }

    for _, p in partidos.iterrows():
        t1, t2 = p["team1"], p["team2"]
        g1, g2 = p["score.ft"]

        # Equipo 1
        if equipo1 == t1 or equipo1 == t2:
            if g1 == g2:
                stats[equipo1]["Empates"] += 1
            elif (equipo1 == t1 and g1 > g2) or (equipo1 == t2 and g2 > g1):
                stats[equipo1]["Victorias"] += 1
            else:
                stats[equipo1]["Derrotas"] += 1

        # Equipo 2
        if equipo2 == t1 or equipo2 == t2:
            if g1 == g2:
                stats[equipo2]["Empates"] += 1
            elif (equipo2 == t1 and g1 > g2) or (equipo2 == t2 and g2 > g1):
                stats[equipo2]["Victorias"] += 1
            else:
                stats[equipo2]["Derrotas"] += 1

    df = pd.DataFrame(stats).T

    # Gráfica
    df.plot(
    kind="bar",
    stacked=True,
    figsize=(9, 6)
)

plt.title(f"Comparación de resultados: {equipo1} vs {equipo2}")
plt.xlabel("Equipo")
plt.ylabel("Partidos")
plt.xticks(rotation=0)
plt.legend(title="Resultado")
plt.tight_layout()
plt.show()




# Cargar datos JSON
BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "premier.json"\

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)


menu()