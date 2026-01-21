import json
import pandas as pd
import matplotlib.pyplot as plt

# ================================
# Función para leer goles
# ================================
def leer_goles(puntuacion):
    try:
        if isinstance(puntuacion, list) and len(puntuacion) >= 2:
            return int(puntuacion[0]), int(puntuacion[1])
        return 0,0
    except:
        return 0,0

# ================================
# Menú
# ================================
def menu():
    while True:
        print("\n--- Menú de gráficas ---")
        print("1. Top 5 equipos con más victorias")
        print("2. Equipo más goleador")
        print("3. Equipo menos goleador")
        print("4. Equipo con más remontadas")
        print("5. Equipo con más victorias local/visitante")
        print("6. Comparación de dos equipos")
        print("7. Salir")
        opcion = input("Elige una opción: ")
        if opcion=="1":
            grafica_top_victorias(data)
        elif opcion=="2":
            grafica_mas_goleador(data)
        elif opcion=="3":
            grafica_menos_goleador(data)
        elif opcion=="4":
            grafica_mas_remontadas(data)
        elif opcion=="5":
            grafica_victorias_local_visitante(data)
        elif opcion=="6":
            grafica_comparacion_dos_equipos(data)
        elif opcion=="7":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")

# ================================
# Opción 1: Top 5 victorias
# ================================
def grafica_top_victorias(data):
    partidos = pd.json_normalize(data, record_path=["matches"])
    victorias = {}
    for partido in partidos.to_dict(orient="records"):
        gl, gv = leer_goles(partido["score.ft"])
        if gl>gv:
            victorias[partido["team1"]] = victorias.get(partido["team1"],0)+1
        elif gv>gl:
            victorias[partido["team2"]] = victorias.get(partido["team2"],0)+1
    top5 = sorted(victorias.items(), key=lambda x:x[1], reverse=True)[:5]
    equipos = [x[0] for x in top5]
    cantidad = [x[1] for x in top5]

    plt.figure(figsize=(10,6))
    plt.barh(equipos, cantidad, color="#4C72B0")
    plt.gca().invert_yaxis()
    plt.title("Top 5 equipos con más victorias")
    plt.xlabel("Victorias")
    plt.ylabel("Equipo")
    for i, v in enumerate(cantidad):
        plt.text(v+0.1, i, str(v), va="center")
    plt.tight_layout()
    plt.show()

# ================================
# Opción 2: Equipo más goleador
# ================================
def grafica_mas_goleador(data):
    partidos = pd.json_normalize(data, record_path=["matches"])
    goles = {}
    for partido in partidos.to_dict(orient="records"):
        local = partido["team1"]
        visitante = partido["team2"]
        gl, gv = leer_goles(partido["score.ft"])
        goles[local] = goles.get(local,0)+gl
        goles[visitante] = goles.get(visitante,0)+gv
    top5 = sorted(goles.items(), key=lambda x:x[1], reverse=True)[:5]
    equipos = [x[0] for x in top5]
    cantidad = [x[1] for x in top5]

    plt.figure(figsize=(10,6))
    plt.bar(equipos, cantidad, color="#2ca02c")
    plt.title("Top 5 equipos más goleadores")
    plt.ylabel("Goles a favor")
    plt.ylim(0, max(cantidad)*1.2)
    for i, g in enumerate(cantidad):
        plt.text(i, g+max(cantidad)*0.03, str(g), ha="center")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.show()

# ================================
# Opción 3: Equipo menos goleador
# ================================
def grafica_menos_goleador(data):
    partidos = pd.json_normalize(data, record_path=["matches"])
    goles = {}
    for partido in partidos.to_dict(orient="records"):
        local = partido["team1"]
        visitante = partido["team2"]
        gl, gv = leer_goles(partido["score.ft"])
        goles[local] = goles.get(local,0)+gl
        goles[visitante] = goles.get(visitante,0)+gv
    top5 = sorted(goles.items(), key=lambda x:x[1])[:5]
    equipos = [x[0] for x in top5]
    cantidad = [x[1] for x in top5]

    plt.figure(figsize=(10,6))
    plt.bar(equipos, cantidad, color="#d62728")
    plt.title("Top 5 equipos menos goleadores")
    plt.ylabel("Goles a favor")
    plt.ylim(0, max(cantidad)*1.2 if cantidad else 5)
    for i, g in enumerate(cantidad):
        plt.text(i, g+max(cantidad)*0.03, str(g), ha="center")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.show()

# ================================
# Opción 4: Equipo con más remontadas
# ================================
def grafica_mas_remontadas(data):
    partidos = pd.json_normalize(data, record_path=["matches"])
    remontadas = {}
    for partido in partidos.to_dict(orient="records"):
        gl_ht, gv_ht = leer_goles(partido.get("score.ht",[0,0]))
        gl_ft, gv_ft = leer_goles(partido.get("score.ft",[0,0]))
        local = partido["team1"]
        visitante = partido["team2"]
        if gl_ht<gv_ht and gl_ft>gv_ft:
            remontadas[local] = remontadas.get(local,0)+1
        if gv_ht<gl_ht and gv_ft>gl_ft:
            remontadas[visitante] = remontadas.get(visitante,0)+1
    if not remontadas:
        print("No hay remontadas registradas")
        return
    top5 = sorted(remontadas.items(), key=lambda x:x[1], reverse=True)[:5]
    equipos = [x[0] for x in top5]
    cantidad = [x[1] for x in top5]

    plt.figure(figsize=(10,6))
    plt.bar(equipos, cantidad, color="#9467bd")
    plt.title("Top 5 equipos con más remontadas")
    plt.ylabel("Remontadas")
    plt.ylim(0, max(cantidad)*1.25)
    for i, c in enumerate(cantidad):
        plt.text(i, c+0.1, str(c), ha="center")
    plt.tight_layout()
    plt.show()

# ================================
# Opción 5: Victórias local/visitante
# ================================
def grafica_victorias_local_visitante(data):
    partidos = pd.json_normalize(data, record_path=["matches"])
    vict_local = {}
    vict_visit = {}
    for partido in partidos.to_dict(orient="records"):
        gl, gv = leer_goles(partido["score.ft"])
        local = partido["team1"]
        visit = partido["team2"]
        if gl>gv:
            vict_local[local] = vict_local.get(local,0)+1
        elif gv>gl:
            vict_visit[visit] = vict_visit.get(visit,0)+1
    equipos = list(set(list(vict_local.keys())+list(vict_visit.keys())))
    val_local = [vict_local.get(e,0) for e in equipos]
    val_visit = [vict_visit.get(e,0) for e in equipos]

    plt.figure(figsize=(12,6))
    plt.bar([i-0.2 for i in range(len(equipos))], val_local, width=0.4, color="#4C72B0", label="Local")
    plt.bar([i+0.2 for i in range(len(equipos))], val_visit, width=0.4, color="#2ca02c", label="Visitante")
    plt.xticks(range(len(equipos)), equipos, rotation=25)
    plt.ylabel("Victorias")
    plt.title("Victorias local/visitante")
    plt.legend()
    plt.tight_layout()
    plt.show()

# ================================
# Opción 6: Comparación de dos equipos
# ================================
def grafica_comparacion_dos_equipos(data):
    partidos = pd.json_normalize(data, record_path=["matches"])
    eq1 = input("Nombre del primer equipo: ")
    eq2 = input("Nombre del segundo equipo: ")
    equipos = [eq1, eq2]
    gf = [0,0]
    gc = [0,0]
    for i, eq in enumerate(equipos):
        for partido in partidos.to_dict(orient="records"):
            gl, gv = leer_goles(partido["score.ft"])
            local = partido["team1"]
            visit = partido["team2"]
            if eq==local:
                gf[i] += gl
                gc[i] += gv
            elif eq==visit:
                gf[i] += gv
                gc[i] += gl
    plt.figure(figsize=(8,6))
    plt.bar([0,1], gf, width=0.4, color="#2ca02c", label="Goles a favor")
    plt.bar([0.4,1.4], gc, width=0.4, color="#d62728", label="Goles en contra")
    plt.xticks([0.2,1.2], equipos)
    plt.ylabel("Goles")
    plt.title("Comparación de goles entre equipos")
    plt.legend()
    plt.tight_layout()
    plt.show()

# ================================
# Cargar JSON y ejecutar menú
# ================================
with open("premier.json","r",encoding="utf-8") as f:
    data = json.load(f)

menu()