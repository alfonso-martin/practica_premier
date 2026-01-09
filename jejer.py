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

    goles = {}  #Diccionario para almacenar goles a favor por equipo

    # Calcular goles a favor por equipo
    for _, row in partidos.iterrows():
        local = row["team1"]    #Equipo local
        visitante = row["team2"]    #Equipo visitante
        gl, gv = row["score.ft"]    #Goles al final del partido

        goles[local] = goles.get(local, 0) + gl #Sumar goles locales
        goles[visitante] = goles.get(visitante, 0) + gv #Sumar goles visitantes

    # Cálculo de ECDF (Empirical Cumulative Distribution Function)
    valores = sorted(goles.values())    #Valores de goles a favor
    n = len(valores)    # Número de equipos
    y = [(i + 1) / n for i in range(n)] #Valores ECDF

    # Equipo más goleador
    equipo_max = max(goles, key=goles.get)
    goles_max = goles[equipo_max]

    # Posición en la ECDF
    y_max = y[valores.index(goles_max)]

    # Gráfica ECDF (más grande)
    plt.figure(figsize=(12, 7), dpi=120)    #Tamaño de la figura
    plt.step(valores, y, where="post") #Dibuja la ECDF
    plt.scatter(goles_max, y_max, color="red", zorder=3)    #Punto del equipo más goleador

    #Mostrar nombre del equipo más goleador con formato personalizado
    plt.text(
        goles_max,
        y_max,
        f"  {equipo_max}",
        fontsize=11,
        color="red",
        verticalalignment="bottom"
    )

    #Diferentes etiquetas y titulo de la gráfica
    plt.xlabel("Goles")
    plt.ylabel("")
    plt.title("Equipo más goleador")
    plt.grid(True)
    plt.yticks(range(0,1))
    plt.tight_layout()
    plt.show()





# ================================
#   OPCIÓN 3: EQUIPO MENOS GOLEADOR
# ================================

def graficaMenosGoleador(data):
    partidos = pd.json_normalize(data, record_path=["matches"])

    goles = {}  #Diccionario para almacenar goles a favor por equipo

    #Calcular goles a favor por equipo
    for _, row in partidos.iterrows():
        local = row["team1"]
        visitante = row["team2"]
        gl, gv = row["score.ft"]

        goles[local] = goles.get(local, 0) + gl
        goles[visitante] = goles.get(visitante, 0) + gv

    #Equipo menos goleador
    equipo = min(goles, key=goles.get)
    valor = goles[equipo]

    #Etiquetas y título de la gráfica STEM
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

    # Calcular remontadas por equipo
    for _, fila in partidos.iterrows():
        equipo_local = fila["team1"]
        equipo_visitante = fila["team2"]

        resultado_descanso = fila["score.ht"] if isinstance(fila["score.ht"], list) else [0, 0]   # Goles al descanso
        resultado_final = fila["score.ft"]    # Goles al final del partido

        goles_local_descanso, goles_visitante_descanso = resultado_descanso     #Primer valor asignado a goles_local_descanso Y segundo A goles_visitante_descanso
        goles_local_final, goles_visitante_final = resultado_final

        #Equipo pierde al descanso y gana al final
        if goles_local_descanso < goles_visitante_descanso and goles_local_final > goles_visitante_final:
            remontadas[equipo_local] = remontadas.get(equipo_local, 0) + 1

        #Equipo visitante pierde al descanso y gana al final
        if goles_visitante_descanso < goles_local_descanso and goles_visitante_final > goles_local_final:
            remontadas[equipo_visitante] = remontadas.get(equipo_visitante, 0) + 1

    #Equipo con más remontadas
    equipo_mas_remontadas = max(remontadas, key=remontadas.get)
    numero_remontadas = remontadas[equipo_mas_remontadas]

    eje_x = [1]
    eje_y = [numero_remontadas]

    plt.figure()
    plt.stem(eje_x, eje_y, linefmt='g-', markerfmt='go', basefmt=' ')
    plt.xticks([1], ["Equipo con más remontadas"])
    plt.yticks(range(0, numero_remontadas + 2, 1))
    plt.ylabel("Remontadas")
    plt.title("Equipo con más remontadas")

    # Mostrar nombre del equipo
    plt.text(1, numero_remontadas, f"  {equipo_mas_remontadas}", ha="left", va="bottom")

    plt.show()


# ================================
#   CARGA DEL JSON Y EJECUCIÓN
# ================================

with open("premier.json", "r", encoding="utf-8") as f:
    data = json.load(f)

menu()
