import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Menú principal
def menu():
    while True:
        print("\n--- Menú de gráficas ---")
        print("1. Top 5 equipos con más victorias")
        print("2. Equipo mas goleador")
        print("3. Equipo menos goleador")
        print("4. Equipo con más remontadas")
        print("5. Equipo con más victorias")
        print("6. Estadisticas de un equipo concreto")
        print("7. Salir")
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
            graficaVictorias(data)
            
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
    

def graficaVictorias(data):
    # Extraer la lista de partidos y normalizarla
    partidos = pd.json_normalize(data, record_path=["matches"])

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




with open(r"C:\Users\Alumno\Desktop\PRACTICA_PREMIER\premier.json", "r", encoding="utf-8") as f:
    data = json.load(f)


menu()