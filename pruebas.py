import matplotlib.pyplot as plt

data = [
    {"equipo": "Equipo A", "victorias": 18, "empates": 6, "derrotas": 4},
    {"equipo": "Equipo B", "victorias": 15, "empates": 8, "derrotas": 5},
    {"equipo": "Equipo C", "victorias": 10, "empates": 10, "derrotas": 8}
]

equipos = [d["equipo"] for d in data]
v = [d["victorias"] for d in data]
e = [d["empates"] for d in data]
d = [d["derrotas"] for d in data]

gap = 0.6  # tamaño del espacio entre sectores

# Primer bloque
plt.barh(equipos, v, label="Victorias", height=0.4)

# Segundo bloque (con gap)
left_empates = [vi + gap for vi in v]
plt.barh(equipos, e, left=left_empates, label="Empates", height=0.4)

# Tercer bloque (con gap acumulado)
left_derrotas = [vi + ei + 2*gap for vi, ei in zip(v, e)]
plt.barh(equipos, d, left=left_derrotas, label="Derrotas",height=0.4)

plt.xlabel("Partidos")
plt.title("Resultados por equipo")
plt.legend()
plt.tight_layout()
plt.show()
