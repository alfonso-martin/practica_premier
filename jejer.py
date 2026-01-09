import json
import pandas as pd
import matplotlib.pyplot as plt


# ================================
#   MENÚ PRINCIPAL
# ================================

def menu():
    while True:
        print("\n--- Menú de gráficas ---")
        print("1. Top 5 equipos con más victorias")
        print("2. Equipo más goleador")
        print("3. Equipo menos goleador")
        print("4. Equipo con más remontadas")
        print("5. Equipo con más victorias como local y como visitante")
        print("6. Estadísticas de un equipo concreto")
        print("7. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            graficaVictorias(data)

        elif opcion == "2":
            graficaMasGoleador(data)

        elif opcion == "3":
            graficaMenosGoleador(data)

        elif opcion == "4":
            graficaRemontadas(data)

        elif opcion == "5":
            print("Opción no implementada aún")

        elif opcion == "6":
            print("Opción no implementada aún")

        elif opcion == "7":
            print("Saliendo...")
            break

        else:
            print("Opción no válida, intenta de nuevo.")


# ================================
#   GANADOR DEL PARTIDO
# ================================

def ganador(row):
    if row["score.ft"][0] > row["score.ft"][1]:
        return row["team1"]
    elif row["score.ft"][0] < row["score.ft"][1]:
        return row["team2"]
    else:
        return None


# ================================
#   OPCIÓN 1: TOP 5 VICTORIAS
# ================================

def graficaVictorias(data):
    partidos = pd.json_normalize(data, record_path=["matches"])
    partidos["winner"] = partidos.apply(ganador, axis=1)

    victorias = partidos["winner"].value_counts().head(5)

    equipos = victorias.index
    victorias_num = victorias.values

    plt.figure(figsize=(10, 6))
    plt.barh(equipos, victorias_num, color="mediumslateblue")
    plt.gca().invert_yaxis()

    plt.title("Top 5 equipos con más victorias")
    plt.xlabel("Victorias")
    plt.ylabel("Equipo")

    for i, v in enumerate(victorias_num):
        plt.text(v + 0.1, i, str(v), va="center")

    plt.show()


# ================================
#   OPCIÓN 2: EQUIPO MÁS GOLEADOR
# ================================

def graficaMasGoleador(data):
    partidos = pd.json_normalize(data, record_path=["matches"])

    goles = {}

    for _, row in partidos.iterrows():
        local = row["team1"]
        visitante = row["team2"]
        gl, gv = row["score.ft"]

        goles[local] = goles.get(local, 0) + gl
        goles[visitante] = goles.get(visitante, 0) + gv

    # Preparar ECDF
    valores = sorted(goles.values())
    n = len(valores)
    y = [(i + 1) / n for i in range(n)]

    # Equipo más goleador
    equipo_max = max(goles, key=goles.get)
    goles_max = goles[equipo_max]

    # Posición en la ECDF
    y_max = y[valores.index(goles_max)]

    # Gráfica ECDF (más grande)
    plt.figure(figsize=(12, 7), dpi=120)
    plt.step(valores, y, where="post")
    plt.scatter(goles_max, y_max, color="red", zorder=3)

    plt.text(
        goles_max,
        y_max,
        f"  {equipo_max}",
        fontsize=11,
        color="red",
        verticalalignment="bottom"
    )

    plt.xlabel("Goles")
    plt.ylabel("")
    plt.title("Equipo más goleador")
    plt.grid(True)

    plt.tight_layout()
    plt.show()





# ================================
#   OPCIÓN 3: EQUIPO MENOS GOLEADOR
# ================================

def graficaMenosGoleador(data):
    partidos = pd.json_normalize(data, record_path=["matches"])

    goles = {}

    # Calcular goles a favor por equipo
    for _, row in partidos.iterrows():
        local = row["team1"]
        visitante = row["team2"]
        gl, gv = row["score.ft"]

        goles[local] = goles.get(local, 0) + gl
        goles[visitante] = goles.get(visitante, 0) + gv

    # Equipo menos goleador
    equipo = min(goles, key=goles.get)
    valor = goles[equipo]

    # Gráfica STEM (un solo punto)
    plt.figure()
    plt.stem([equipo], [valor])
    plt.xlabel("Equipo")
    plt.ylabel("Goles")
    plt.title("Equipo menos goleador")
    plt.show()




# ================================
#   OPCIÓN 4: EQUIPO CON MÁS REMONTADAS
# ================================

def graficaRemontadas(data):
    partidos = pd.json_normalize(data, record_path=["matches"])

    remontadas = {}

    for _, row in partidos.iterrows():
        local = row["team1"]
        visitante = row["team2"]

        ht = row["score.ht"] if isinstance(row["score.ht"], list) else [0, 0]
        ft = row["score.ft"]

        gl_ht, gv_ht = ht
        gl_ft, gv_ft = ft

        if gl_ht < gv_ht and gl_ft > gv_ft:
            remontadas[local] = remontadas.get(local, 0) + 1

        if gv_ht < gl_ht and gv_ft > gl_ft:
            remontadas[visitante] = remontadas.get(visitante, 0) + 1

    equipo = max(remontadas, key=remontadas.get)
    valor = remontadas[equipo]

    plt.figure()
    plt.bar(equipo, valor, color="orange")
    plt.title("Equipo con más remontadas")
    plt.ylabel("Remontadas")
    plt.show()



# ================================
#   CARGA DEL JSON Y EJECUCIÓN
# ================================

with open("premier.json", "r", encoding="utf-8") as f:
    data = json.load(f)

menu()
