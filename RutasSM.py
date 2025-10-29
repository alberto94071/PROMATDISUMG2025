import networkx as nx
import matplotlib 
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import sys
import os
from datetime import datetime
import tkinter as tk  
from tkinter import ttk 
from tkinter import messagebox 

# --- 0. Configuración Global ---
def get_asset_path(filename):
    """ Obtiene la ruta absoluta del archivo, 
        funciona para VScode y para el .exe de PyInstaller. """
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS

    return os.path.join(base_path, filename)
MAPA_IMAGEN = get_asset_path('mapa.png') 
INFINITO = float('inf') 
HORAS_PICO = [7, 8, 9, 12, 13, 17, 18] 
FACTOR_TRAFICO = 1.5 

# --- 1. Crear el Grafo Dirigido ---
G = nx.DiGraph()

# --- 2. Modelo de Datos ---
posiciones = {
    'A': (1575, 43), #el gallo
    'B': (1498, 45), #esquina de la delia, semáforo
    'C': (1516, 194), # pollo del campo
    'D': (1413, 67), #imprenta vasquez
    'E': (1417, 194), #Dumont
    'F': (1320, 97), #Taller de Moi
    'G': (1324, 194), #Esquina casa de Rony
    'H': (1524, 233), #Esquina del Sarita
    'I': (1419, 239), #Esquina del Pony
    'J': (1324, 241), #Flyng pizza
    'K': (1192, 235), #Casa de los obreros
    'L': (1194, 144), #Toril
    'M': (1142, 154), #Iglesia mormona
    'N': (1129, 225), #tacos walter
    'O': (1538, 314), #Esquina del billar
    'P': (1540, 359), #Suprema
    'Q': (1429, 367), #Gimnasio
    'R': (1427, 316), #Batres
    'S': (1328, 324), #La ventanita
    'T': (1330, 375), #Frappes
    'U': (1216, 326), #Transportes orozco
    'V': (1227, 377), #Acredicom
    'W': (1142, 387), #Semaforo candelero de oro
    'X': (1000, 389), #Miralvalle
    'Y': (797, 478), #Pasarela Aprofam
    'Z': (1002, 209), #Iglesia Mosquito
    'AA': (937, 144), #Deposito Cifuentes
    'AB': (866, 85), #Dominos pizza
    'AC': (734, 223), #Mundo de las fresas
    'AD': (749, 124), #Shukos
    'AE': (767, 20), #Escuela del mosquito
    'AF': (696, 472), #Palacio Maya
    'AG': (737, 507), #Little ceaser's
    'AH': (489, 598), #Texaco
    'AI': (493, 531), #Ulises rojas
    'AJ': (627, 481), #taller Mynor
    'AK': (657, 54), #Club cevichero
    'AL': (447, 156), #sail
    'AM': (420, 311), #Hall
    'AN': (242, 145), #Terminal de San Marcos
    'AO': (384, 521), #MegaPAca
    'AP': (133, 436), #Sat
    'AQ': (109, 504), #supermarq
    'AR': (62, 463), #Gobernacion
    'AS': (80, 381), #Esquina del IGSS
    'AT': (141, 288), #despensa san marcos
    'AU': (9, 544), #PARQUE!!!
}

calles = [
    ('A', 'B', 2.0, 2.0, True), #del gallo a la delia, liviano, pesado, trafico
    ('B', 'D', 3.5, 3.5, True), #de la delia a la imprenta vasquez , liviano, pesado , semáforo
    ('B', 'C', 3.5, INFINITO, True), #de la delia al pollo del campo , liviano, seáforo
    ('C', 'H', 1.0, INFINITO, True), #del pollo del campo a la esquina del sarita, liviano, tráfico
    ('C', 'E', 1.0, INFINITO, False), #del pollo del campo a la esquina de la Dumont, liviano, sin tráfico
    ('H', 'O', 1.5, INFINITO, True), #de la esquina del sarita a la esquina del billar, liviano, tráfico
    ('H', 'I', 1.5, INFINITO, True),#de la esquina del sarita a la esquina del pony, liviano, tráfico
    ('O', 'P', 3.5, INFINITO, True),#de la esquina del billar al suprema, semaforo, liviano, tráfico
    ('O', 'R', 3.5, INFINITO, True),#de la esquina del billar a la batres, semaforo, liviano, tráfico
    ('P', 'Q', 3.5, INFINITO, True),#del suprema al gimnasio, semaforo, liviano, tráfico
    ('D', 'E', 2.0, INFINITO, False),# de la imprenta vasquez a la dumont, liviano, tráfico
    ('D', 'F', 1.0, 1.0, True),#de la imprenta vasquez al taller de moi, liviano, pesado, tráfico
    ('E', 'I', 1.0, INFINITO, False),# de la dumont a la esquina del pony, liviano, sin tráfico
    ('E', 'G', 1.0, INFINITO, False), #de la dumont a la esquina de la casa de rony, liviano, sin tráfico
    ('I', 'R', 1.0, INFINITO, True), #de la esquina del pony a la batres, liviano, liviano, tráfico
    ('I', 'J', 1.5, INFINITO, True), #de la esquina del pony a la esquina de flying pizza, liviano
    ('R', 'Q', 2.0, INFINITO, True), #de la batres al gimnasio, liviano
    ('R', 'S', 2.0, INFINITO, True), #de la batres a la ventanita, liviano
    ('Q', 'T', 2.5, INFINITO, True), #del gimnasio a los frappes, liviano
    ('F', 'G', 1.0, INFINITO, False), #del taller del moi a la esquina de la casa de rony, liviano
    ('F', 'L', 2.0, 2.0, True), #del taller del moi al toril, pesado
    ('G', 'J', 1.0, INFINITO, True), #de la esquina de la casa de rony a la esquina de flyng
    ('J', 'K', 1.5, INFINITO, True), #de la flying a la casa de obreros
    ('J', 'S', 1.5, INFINITO, True), #de la flying a la ventanita
    ('S', 'U', 1.5, INFINITO, True), #de la ventanita a transportes orozco
    ('S', 'T', 1.5, INFINITO, True), #de la ventanita a los frappes
    ('T', 'V', 1.0, INFINITO, True), #de los frappes a acredicom
    ('L', 'K', 2.0, 2.0, True), #del toril a la casa de los obreros
    ('L', 'M', 2.0, INFINITO, False), #del toril a la iglesia mormona
    ('M', 'N', 1.0, INFINITO, False), # de la iglesia mormona a los tacos walter
    ('K', 'N', 1.5, 1.5, True), #de la casa de los obreros a los tacos walter
    ('U', 'W', 1.0, INFINITO, True), #de transportes orozco al antiguo candelero de oro
    ('V', 'W', 1.0, INFINITO, True), #de acredicom al antiguo candelero de oro
    ('W', 'X', 1.5, INFINITO, True), #del candelero de oro al miralvalle
    ('X', 'Y', 1.5, INFINITO, True), #del miralvalle a la pasarela de aprofam
    ('Y', 'AG', 3.5, INFINITO, True), #de la pasarela de aprofam a little ceaser's
    ('AG', 'AF', 1.0, 1.0, True), # de little ceaser's al palacio maya
    ('AG', 'AH', 1.5, 2.0, True), #de little ceasers a texaco
    ('N', 'Z', 3.5, 3.5, True), #de los tacos walter a la iglesia del mosquito
    ('Z', 'AA', 1.5, 1.5, True), #de la iglesia del mosquito a deposito cifuentes
    ('AA', 'AC', 1.5, 1.5, True), #del deposito cifuentes al mundo de las fresas
    ('AA', 'AB', 2.0, 2.0, True), #del deposito cifuentes a dominos pizza
    ('AB', 'AE', 2.0, 2.0, True), #de dominos a la escuela del mosquito
    ('AB', 'AD', 1.5, 1.5, True), #de dominos a los shukos
    ('AE', 'AK', 3.5, 3.5, True), #de la escuela del mosquito al club cevichero
    ('AE', 'AD', 3.5, 3.5, True), #de la escuela del mosquito a los shukos
    ('AD', 'AK', 2.0, 2.0, False), #de los shukos al club cevichero
    ('AD', 'AE', 2.0, 2.0, True), #de los shukos a la escuela del mosuqito
    ('AD', 'AC', 2.0, 2.0, True), #de los shukos al mundo de las fresas
    ('AC', 'AD', 2.0, 2.0, True), #del mundo de las fresas a los shukos
    ('AC', 'AF', 2.0, 2.0, True), #del mundo de las fresas al palacio maya
    ('AF', 'AC', 2.0, 2.0, True), #del palacio maya al mundo de las fresas 
    ('AF', 'AG', 1.0, 1.0, True), #del palacio maya a little
    ('AF', 'AJ', 1.5, 1.5, True), #del palacaio maya al taller de mynor
    ('AJ', 'AI', 1.0, 1.0, True), #del taller de mynor a la ulises
    ('AJ', 'AM', 1.0, INFINITO, False), #del taller de mynor al hall
    ('AI', 'AH', 1.0, 1.0, True), #de la ulises a la texaco
    ('AI', 'AO', 1.0, 1.0, True), #de la ulises a la megapaca
    ('AH', 'AU', 3.5, INFINITO, True), #de la texaco al parque
    ('AK', 'AL', 2.0, 2.0, True), #del club cevichero al sail
    ('AL', 'AM', 1.0, INFINITO, False), #del sail al hall
    ('AM', 'AO', 3.5, INFINITO, False), #del hall a la megapaca
    ('AO', 'AM', 3.5, INFINITO, False), #de la megapaca al hall
    ('AM', 'AL', 1.0, INFINITO, False), #del hall al sail
    ('AL', 'AN', 1.5, 1.5, True), #del sail a la terminal
    ('AM', 'AN', 1.5, INFINITO, False), #del hall a la terminal
    ('AO', 'AP', 1.5, 1.5, True), #de la megapaca a la sat
    ('AP', 'AQ', 1.5, INFINITO, True), #de la sat al supermarq
    ('AQ', 'AR', 1.0, INFINITO, True), #del supermarqe a gobernacion
    ('AR', 'AU', 2.0, 2.0, True), #degobernacion al parque
    ('AN', 'AT', 2.0, 2.0, True), #de la terminal a la despensa
    ('AT', 'AS', 3.5, 3.5, True), #de la despensa al igss
    ('AS', 'AR', 2.0, 2.0, True), #del igss a gobernacion


]

# --- 3. Cargar Datos en el Grafo ---
for u, v, liviano, pesado, sensible in calles:
    G.add_edge(u, v, costo_liviano=liviano, costo_pesado=pesado, sensible_al_trafico=sensible)

# --- 4. Función de Costo Dinámico ---
def crear_calculador_de_costo(tipo_de_peso_elegido, hora_actual):
    es_hora_pico = hora_actual in HORAS_PICO
    def funcion_de_peso_dinamico(u, v, data_edge):
        costo_base = data_edge[tipo_de_peso_elegido]
        if costo_base == INFINITO: return INFINITO
        es_sensible = data_edge.get('sensible_al_trafico', False)
        if es_hora_pico and es_sensible:
            return costo_base * FACTOR_TRAFICO
        else: return costo_base
    return funcion_de_peso_dinamico

# --- 5. Preparación de la Visualización ---
try:
    with Image.open(MAPA_IMAGEN) as img:
        img_height = img.height
except FileNotFoundError:
    tk.Tk().withdraw()
    messagebox.showerror("Error Crítico", 
                         f"ERROR: No se pudo encontrar la imagen '{MAPA_IMAGEN}'.\n\n"
                         "Asegúrate de que esté en la misma carpeta que el ejecutable.")
    sys.exit(1)
posiciones_ajustadas = posiciones 

# --- 6. Lógica de la GUI con tkinter --- 
def mostrar_mapa_con_ruta(ruta_optima, costo_total, punto_inicio, punto_destino, titulo_transporte, hora_actual):
    """ Función que encapsula la lógica de visualización del mapa (Matplotlib) """
    img = Image.open(MAPA_IMAGEN)
    img_array = np.array(img)
    
    # 1. Crear la figura (la ventana)
    fig = plt.figure(figsize=(12, 12)) 
    # 2. Crear los ejes (el lienzo) para que ocupen TODA la figura
    ax = fig.add_axes([0, 0, 1, 1]) 
    ax.axis('off') 
    ax.imshow(img_array, aspect='auto') 

    # Dibujar Nodos y Etiquetas 
    nx.draw_networkx_nodes(G, pos=posiciones_ajustadas, ax=ax, node_size=300, node_color='skyblue', alpha=0.9)
    nx.draw_networkx_labels(G, pos=posiciones_ajustadas, ax=ax, font_size=9, font_weight='bold')
    
    # Dibujar Aristas de la Ruta Óptima 
    aristas_ruta = list(zip(ruta_optima[:-1], ruta_optima[1:]))
    nx.draw_networkx_edges(G, pos=posiciones_ajustadas, ax=ax, edgelist=aristas_ruta, 
                           edge_color='red', width=3, arrows=True, arrowsize=20)
    
    # Poner el título en la barra de la ventana 
    titulo_mapa = f"Ruta Óptima de {punto_inicio} a {punto_destino} (T. {titulo_transporte})"
    if hora_actual in HORAS_PICO:
        titulo_mapa += " - ¡Optimizado para Hora Pico!"
    
    try:
        fig.canvas.manager.set_window_title(titulo_mapa)
    except AttributeError:
        pass 

    plt.show()

def on_calcular_ruta_click():
    punto_inicio = combo_inicio.get()
    punto_destino = combo_destino.get()
    
    if not punto_inicio or not punto_destino:
        messagebox.showerror("Error", "Por favor, selecciona un nodo de inicio y uno de destino.")
        return
    if punto_inicio == punto_destino:
        messagebox.showerror("Error", "El nodo de inicio y destino no pueden ser el mismo.")
        return

    # 'tipo_transporte' es una variable de tkinter (StringVar)
    tipo_elegido = tipo_transporte.get()
    
    tipo_de_peso = 'costo_liviano' if tipo_elegido == 'liviano' else 'costo_pesado'
    titulo_transporte = "Liviano" if tipo_elegido == 'liviano' else "Pesado"
    
    funcion_de_peso = crear_calculador_de_costo(tipo_de_peso, hora_actual)
    
    try:
        ruta_optima = nx.dijkstra_path(G, punto_inicio, punto_destino, weight=funcion_de_peso)
        costo_total = nx.dijkstra_path_length(G, punto_inicio, punto_destino, weight=funcion_de_peso)
        
        output_text = f"--- ¡RUTA ENCONTRADA! ---\n" \
                      f"Tipo de transporte: {titulo_transporte}\n" \
                      f"Ruta más eficiente: {' -> '.join(ruta_optima)}\n" \
                      f"Costo (tiempo) total: {costo_total:.2f} unidades\n"
        
        # Actualizar el texto de resultado
        texto_resultado.config(state=tk.NORMAL) # Habilitar para editar
        texto_resultado.delete('1.0', tk.END) # Borrar contenido anterior
        texto_resultado.insert(tk.END, output_text) # Insertar nuevo
        texto_resultado.config(state=tk.DISABLED) # Deshabilitar
        
        mostrar_mapa_con_ruta(ruta_optima, costo_total, punto_inicio, punto_destino, titulo_transporte, hora_actual)

    except nx.NetworkXNoPath:
        output_text = f"--- ERROR ---\n" \
                      f"No se encontró ninguna ruta posible entre {punto_inicio} y {punto_destino} " \
                      f"para transporte {titulo_transporte}.\n"
        if tipo_de_peso == 'costo_pesado':
            output_text += "Causa probable: La ruta está bloqueada por calles no aptas."
        messagebox.showerror("Error de Ruta", output_text)
    except Exception as e:
        messagebox.showerror("Error General", f"Ocurrió un error inesperado: {e}")

# --- Definición y ejecución de la GUI de tkinter ---

# Configuración de hora
hora_actual = datetime.now().hour
mensaje_hora = f"Hora actual: {hora_actual}:00. "
es_pico = hora_actual in HORAS_PICO
if es_pico:
    mensaje_hora += f"¡Es Hora Pico! Penalización por tráfico (x{FACTOR_TRAFICO})."
else:
    mensaje_hora += "Hora normal. Sin penalizaciones por tráfico."

# Crear la ventana principal
root = tk.Tk()
root.title("Optimización de Rutas")
root.geometry("600x600") # Tamaño de la ventana
root.resizable(False, False) # Evitar que se cambie el tamaño

# Crear un frame principal para organizar
frame = ttk.Frame(root, padding="10")
frame.pack(expand=True, fill=tk.BOTH)

# Título
label_titulo = ttk.Label(frame, text="Optimización de Rutas de San Marcos", font=("Helvetica", 14, "bold"))
label_titulo.pack(pady=5)

# Mensaje de hora
label_hora = ttk.Label(frame, text=mensaje_hora, font=("Helvetica", 9),
                       foreground='red' if es_pico else 'green')
label_hora.pack(pady=5)

ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=10)

# --- Frame de selección ---
frame_seleccion = ttk.Frame(frame)
frame_seleccion.pack(fill='x')

# Tipo de transporte
tipo_transporte = tk.StringVar(value="liviano") # Variable para guardar la selección
label_tipo = ttk.Label(frame_seleccion, text="Tipo de Transporte:")
label_tipo.pack(anchor='w')

radio_liviano = ttk.Radiobutton(frame_seleccion, text="🚗 Liviano", variable=tipo_transporte, value="liviano")
radio_liviano.pack(anchor='w', padx=20)
radio_pesado = ttk.Radiobutton(frame_seleccion, text="🚚 Pesado", variable=tipo_transporte, value="pesado")
radio_pesado.pack(anchor='w', padx=20)

# Nodos de inicio y fin
nodos_disponibles = sorted(list(G.nodes()))

label_inicio = ttk.Label(frame_seleccion, text="Nodo de Inicio:")
label_inicio.pack(anchor='w', pady=(10, 0))
combo_inicio = ttk.Combobox(frame_seleccion, values=nodos_disponibles, state="readonly")
combo_inicio.pack(fill='x', padx=20)
if nodos_disponibles:
    combo_inicio.current(0) # Seleccionar el primero por defecto

label_destino = ttk.Label(frame_seleccion, text="Nodo de Destino:")
label_destino.pack(anchor='w', pady=(10, 0))
combo_destino = ttk.Combobox(frame_seleccion, values=nodos_disponibles, state="readonly")
combo_destino.pack(fill='x', padx=20)
if len(nodos_disponibles) > 1:
    combo_destino.current(1) # Seleccionar el segundo por defecto

# Botón de cálculo
boton_calcular = ttk.Button(frame, text="Calcular Ruta", command=on_calcular_ruta_click)
boton_calcular.pack(pady=20, fill='x')

ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=10)

# --- Área de Resultado ---
label_resultado = ttk.Label(frame, text="Resultado:", font=("Helvetica", 10, "bold"))
label_resultado.pack(anchor='w')

texto_resultado = tk.Text(frame, height=8, state=tk.DISABLED, background="#d6ecff")
texto_resultado.pack(fill='x', expand=True)

# Iniciar el loop de la GUI
root.mainloop()