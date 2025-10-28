import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import sys
from datetime import datetime

# --- 0. Configuración Global ---
MAPA_IMAGEN = 'mapa.png' 
INFINITO = float('inf') # Costo para rutas prohibidas
HORAS_PICO = [7, 8, 12, 13, 17, 18, 19] 
FACTOR_TRAFICO = 1.5 

# --- 1. Crear el Grafo Dirigido ---
G = nx.DiGraph()


posiciones = {
    'A': (1575, 43),
    'B': (1498, 45),
    'C': (1192, 138),
    'D': (1192, 235),
    'E': (994, 205),
    'F': (747, 13),
    'G': (449, 152),
    'H': (236, 140),
    'I': (72, 427),
    'J': (66, 460),
    'K': (1, 549),
    'L': (1, 587),
    'M': (1539, 358),
    'N': (1237, 378),
    'O': (1179, 374),
    'P': (1128, 394),
    'Q': (1006, 382),
    'R': (792, 483),
    'S': (448, 613),
    'T': (732, 502),
    'U': (688, 470),
    'V': (453, 545),
    'W': (137, 444),
    'X': (109, 504)
}

# Formato: (Nodo_Inicio, Nodo_Fin, Costo_Liviano, Costo_Pesado, Es_Sensible_Al_Tráfico)
calles = [
    ('A', 'B', 3.5, 3.5, True),# Calle con semáforo
    ('B', 'C', 1.0, 2.0, True),
    ('C', 'D', 1.5, 2.0, True), 
    ('D', 'E', 1.5, 2.5, False),
    ('E', 'F', 3.5, 3.5, True),      # Calle con semáforo
    ('F', 'G', 3.5, 3.5, True),
    ('G', 'H', 2.0, INFINITO, False), # Una vía, prohibida para pesados
    ('H', 'I', 2.0, 2.0, True),
    ('I', 'J', 2.5, 2.5, True),
    ('J', 'K', 3.0, 3.0, False)
    # ...Añade todas tus calles aquí
]

# --- 3. Cargar Datos en el Grafo ---
for u, v, liviano, pesado, sensible in calles:
    G.add_edge(u, v, 
               costo_liviano=liviano, 
               costo_pesado=pesado,
               sensible_al_trafico=sensible)

# --- 4. Función de Costo Dinámico ---
def crear_calculador_de_costo(tipo_de_peso_elegido, hora_actual):
    es_hora_pico = hora_actual in HORAS_PICO
    
    def funcion_de_peso_dinamico(u, v, data_edge):
        costo_base = data_edge[tipo_de_peso_elegido]
        
        if costo_base == INFINITO:
            return INFINITO
            
        es_sensible = data_edge.get('sensible_al_trafico', False)
        
        if es_hora_pico and es_sensible:
            return costo_base * FACTOR_TRAFICO
        else:
            return costo_base
            
    return funcion_de_peso_dinamico

# --- 5. Preparación de la Visualización ---
try:
    with Image.open(MAPA_IMAGEN) as img:
        img_height = img.height
except FileNotFoundError:
    print(f"--- ¡ERROR GRAVE! ---")
    print(f"No se pudo encontrar la imagen '{MAPA_IMAGEN}'.")
    print("Asegúrate de que esté en la misma carpeta que tu script 'optimizador.py'.")
    sys.exit(1)
posiciones_ajustadas = posiciones 

# --- 6. Interfaz de Usuario (Terminal) ---
print("--- Optimizador de Rutas de San Marcos (Proyecto M. Discreta) ---")

hora_actual = datetime.now().hour
print(f"Hora actual detectada: {hora_actual}:00 horas.")
if hora_actual in HORAS_PICO:
    print(f"ESTADO: Hora Pico. Se aplicará penalización por tráfico (x{FACTOR_TRAFICO}).\n")
else:
    print("ESTADO: Hora Normal. No se aplicarán penalizaciones por tráfico.\n")

print(f"Nodos (intersecciones) disponibles en el mapa: {list(G.nodes())}")
print("¿Qué tipo de transporte desea optimizar?")
print("  1: Transporte Liviano")
print("  2: Transporte Pesado")

tipo_transporte = ""
while tipo_transporte not in ['1', '2']:
    tipo_transporte = input("Seleccione (1 o 2): ")

if tipo_transporte == '1':
    tipo_de_peso = 'costo_liviano'
    titulo_transporte = "Liviano"
    print("\nCalculando ruta para: TRANSPORTE LIVIANO")
else:
    tipo_de_peso = 'costo_pesado'
    titulo_transporte = "Pesado"
    print("\nCalculando ruta para: TRANSPORTE PESADO")

# Validar inicio
while True:
    punto_inicio = input(f"Ingrese nodo de inicio (ej. A): ").upper()
    if punto_inicio in G.nodes(): break
    else: print(f"Nodo '{punto_inicio}' no encontrado. Intente de nuevo.")

# Validar fin
while True:
    punto_destino = input(f"Ingrese nodo de destino (ej. F): ").upper()
    if punto_destino in G.nodes(): break
    else: print(f"Nodo '{punto_destino}' no encontrado. Intente de nuevo.")

# --- 7. Calcular la Ruta Óptima ---
funcion_de_peso = crear_calculador_de_costo(tipo_de_peso, hora_actual)

try:
    ruta_optima = nx.dijkstra_path(G, punto_inicio, punto_destino, weight=funcion_de_peso)
    costo_total = nx.dijkstra_path_length(G, punto_inicio, punto_destino, weight=funcion_de_peso)

    print(f"\n--- ¡RUTA ENCONTRADA! ---")
    print(f"Ruta más eficiente: {' -> '.join(ruta_optima)}")
    print(f"Costo (tiempo) total: {costo_total:.2f} unidades")

    # --- 8. Generar la Visualización (La Magia) ---
    print("\nGenerando minimapa con la ruta...")
    
    img = Image.open(MAPA_IMAGEN)
    img_array = np.array(img)
    fig, ax = plt.subplots(figsize=(12, 12)) # Tamaño de la ventana
    ax.imshow(img_array) # Mostrar la imagen de fondo

    # Dibujar Nodos y Etiquetas
    nx.draw_networkx_nodes(G, pos=posiciones_ajustadas, ax=ax, node_size=300, node_color='skyblue', alpha=0.9)
    nx.draw_networkx_labels(G, pos=posiciones_ajustadas, ax=ax, font_size=9, font_weight='bold')
    
    # Dibujar Aristas de la Ruta Óptima
    aristas_ruta = list(zip(ruta_optima[:-1], ruta_optima[1:]))
    nx.draw_networkx_edges(G, pos=posiciones_ajustadas, ax=ax, edgelist=aristas_ruta, 
                           edge_color='red', width=3, arrows=True, arrowsize=20)
    
    # Título del mapa
    titulo = f"Ruta Óptima de {punto_inicio} a {punto_destino} (T. {titulo_transporte})"
    if hora_actual in HORAS_PICO:
        titulo += " - ¡Optimizado para Hora Pico!"

    ax.set_title(titulo, fontsize=16, color='darkblue')
    ax.set_xticks([]) # Ocultar ejes
    ax.set_yticks([]) # Ocultar ejes
    plt.tight_layout()
    plt.show() # ¡Abrir la ventana con el mapa!

except nx.NetworkXNoPath:
    print(f"\n--- ERROR ---")
    print(f"No se encontró ninguna ruta posible entre {punto_inicio} y {punto_destino}.")
    if tipo_de_peso == 'costo_pesado':
        print("Causa probable: La ruta está bloqueada por calles no aptas para transporte pesado.")

except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")