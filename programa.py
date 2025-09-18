import pygame
import sys
import os
import random
import math

# --- Configuración inicial ---
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 1000, 750
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Un resumen de tu vida ❤️")

# Colores y fuentes
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
fuente_titulo = pygame.font.SysFont("Arial", 50, bold=True)
fuente_subtitulo = pygame.font.SysFont("Arial", 25)
fuente_oracion = pygame.font.SysFont("Arial", 22)
fuente_final_linea1 = pygame.font.SysFont("Arial", 50, bold=True)
fuente_final_linea2 = pygame.font.SysFont("Arial", 40, bold=True)

# --- Contenido de la presentación ---
oraciones = [
    "Hoy quiero agradecerte por todo lo que significas en mi vida.",
    "Cada recuerdo que compartimos lo llevo guardado como un tesoro en mi mente.",
    "Tu presencia marcó mi historia y eso nunca se borrará.",
    "Gracias por tus sonrisas, tus palabras y los momentos que me hicieron sentir feliz.",
    "No guardo rencor, porque contigo aprendí y crecí de una forma especial.",
    "Cada instante a tu lado dejó una huella que llevaré siempre conmigo.",
    "Los recuerdos permanecen intactos.",
    "Me quedo con lo bueno, con lo sincero y con lo verdadero de lo que vivimos.",
    "Tus gestos, tus miradas y tus abrazos seguirán acompañándome en el corazón.",
    "Gracias por enseñarme lo valioso de amar sin medida.",
    "Lo nuestro fue único, y eso lo recordaré siempre con gratitud.",
    "No hay dolor cuando pienso en ti, solo cariño y recuerdos imborrables.",
    "En lo más profundo de mi corazón tendrás un lugar que nadie podrá ocupar.",
    "Te deseo lo mejor en cada paso que des, porque lo mereces.",
    "Hoy, más que nunca quiero decirte gracias por haber sido parte de mi vida."
]

# --- Cargar recursos ---

# Portada
titulo = fuente_titulo.render("UN RESUMEN DE TU VIDA", True, BLANCO)
subtitulo = fuente_subtitulo.render("Presiona la barra espaciadora para empezar", True, BLANCO)
titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 40))
subtitulo_rect = subtitulo.get_rect(center=(ANCHO // 2, ALTO // 2 + 20))

# Música
try:
    pygame.mixer.music.load("alma_dinamita.mp3")
    pygame.mixer.music.play(-1)
except pygame.error:
    print(
        "Error: No se pudo cargar el archivo de música. Asegúrate de que 'alma_dinamita.mp3' esté en la misma carpeta.")

# Fotos
ruta_fotos = "fotos"
nombres_archivos_fotos = sorted([f for f in os.listdir(ruta_fotos) if f.endswith(('.jpg', '.png'))])
fotos = []
for nombre_archivo in nombres_archivos_fotos:
    ruta_completa = os.path.join(ruta_fotos, nombre_archivo)
    try:
        imagen = pygame.image.load(ruta_completa).convert_alpha()
        fotos.append(imagen)
    except pygame.error as e:
        print(f"Error al cargar la imagen {nombre_archivo}: {e}")

total_fotos = len(fotos)
if total_fotos != 15:
    print(
        f"Advertencia: Se encontraron {total_fotos} fotos en lugar de 15. Esto podría afectar el orden de las oraciones.")
indice_foto_actual = 0
tiempo_cambio = 5000  # 5 segundos
ultimo_cambio = pygame.time.get_ticks()

# Fondo de corazones
try:
    imagen_corazon = pygame.image.load("corazon.png").convert_alpha()
    imagen_corazon = pygame.transform.scale(imagen_corazon, (30, 30))
    corazones_fondo = []
    for _ in range(50):
        x = random.randint(0, ANCHO)
        y = random.randint(ALTO, ALTO + 500)
        velocidad = random.uniform(0.5, 2.5)
        corazones_fondo.append([x, y, velocidad])
except pygame.error:
    imagen_corazon = None
    print("Error: No se pudo cargar la imagen del corazón. Se usará un fondo estático.")


def ajustar_imagen(imagen):
    # Obtener las dimensiones de la imagen y la ventana
    ancho_img, alto_img = imagen.get_size()
    ratio_img = ancho_img / alto_img
    ratio_ventana = ANCHO / ALTO

    # Calcular nuevas dimensiones para que la imagen se ajuste sin distorsionarse
    if ratio_img > ratio_ventana:
        nueva_ancho = ANCHO
        nueva_alto = int(ANCHO / ratio_img)
    else:
        nueva_alto = ALTO
        nueva_ancho = int(ALTO * ratio_img)

    return pygame.transform.scale(imagen, (nueva_ancho, nueva_alto))


# --- Funciones de transición ---

def transicion_fade_in(ventana, foto, texto, progreso):
    # Efecto de desvanecimiento simple para la foto y el texto
    alfa = int(255 * progreso)

    # Dibujar foto
    foto.set_alpha(alfa)
    foto_rect = foto.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
    ventana.blit(foto, foto_rect)

    # Dibujar texto
    texto_renderizado = fuente_oracion.render(texto, True, BLANCO)
    texto_renderizado.set_alpha(alfa)
    texto_rect = texto_renderizado.get_rect(center=(ANCHO // 2, ALTO - 50))
    ventana.blit(texto_renderizado, texto_rect)


def transicion_slide_in_up(ventana, foto, texto, progreso):
    # Efecto de deslizar desde abajo
    y_pos_foto = ALTO * (1.0 - progreso)

    foto_rect = foto.get_rect(center=(ANCHO // 2, y_pos_foto - 50))
    ventana.blit(foto, foto_rect)

    texto_renderizado = fuente_oracion.render(texto, True, BLANCO)
    texto_rect = texto_renderizado.get_rect(center=(ANCHO // 2, ALTO - 50))
    ventana.blit(texto_renderizado, texto_rect)


def transicion_rotacion_fade(ventana, foto, texto, progreso):
    # Efecto de rotación y desvanecimiento
    angulo = 360 * (1.0 - progreso)
    alfa = int(255 * progreso)

    foto_rotada = pygame.transform.rotate(foto, angulo)
    foto_rotada.set_alpha(alfa)
    foto_rect = foto_rotada.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
    ventana.blit(foto_rotada, foto_rect)

    texto_renderizado = fuente_oracion.render(texto, True, BLANCO)
    texto_renderizado.set_alpha(alfa)
    texto_rect = texto_renderizado.get_rect(center=(ANCHO // 2, ALTO - 50))
    ventana.blit(texto_renderizado, texto_rect)


# Lista de transiciones disponibles
transiciones = [transicion_fade_in, transicion_slide_in_up, transicion_rotacion_fade]
transicion_actual = random.choice(transiciones)

# --- Bucle principal del juego ---
corriendo = True
mostrar_portada = True
mostrar_final = False
tiempo_inicio_transicion = 0
duracion_transicion = 1000  # 1 segundo

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and mostrar_portada:
                mostrar_portada = False
                tiempo_inicio_transicion = pygame.time.get_ticks()
            if evento.key == pygame.K_ESCAPE:
                corriendo = False

    # Actualizar fondo de corazones
    if not mostrar_portada and not mostrar_final and imagen_corazon:
        ventana.fill(NEGRO)
        for corazon in corazones_fondo:
            corazon[1] -= corazon[2]
            if corazon[1] < -30:
                corazon[1] = ALTO + random.randint(0, 200)
                corazon[0] = random.randint(0, ANCHO)
            ventana.blit(imagen_corazon, (corazon[0], corazon[1]))

    # Lógica de la aplicación
    tiempo_actual = pygame.time.get_ticks()

    if mostrar_portada:
        ventana.fill(NEGRO)
        ventana.blit(titulo, titulo_rect)
        ventana.blit(subtitulo, subtitulo_rect)

    elif mostrar_final:
        ventana.fill(NEGRO)
        mensaje_final_1 = fuente_final_linea1.render("GRACIAS POR TODO...", True, BLANCO)
        mensaje_final_2 = fuente_final_linea2.render("TE AMO", True, BLANCO)

        rect1 = mensaje_final_1.get_rect(center=(ANCHO // 2, ALTO // 2 - 30))
        rect2 = mensaje_final_2.get_rect(center=(ANCHO // 2, ALTO // 2 + 30))

        ventana.blit(mensaje_final_1, rect1)
        ventana.blit(mensaje_final_2, rect2)

    else:
        # Lógica para cambiar de foto y oración
        if tiempo_actual - ultimo_cambio > tiempo_cambio:
            ultimo_cambio = tiempo_actual

            if indice_foto_actual == total_fotos - 1:
                mostrar_final = True
            else:
                indice_foto_actual = (indice_foto_actual + 1)
                tiempo_inicio_transicion = tiempo_actual
                transicion_actual = random.choice(transiciones)

        # Ajustar la imagen y la oración
        foto_original = fotos[indice_foto_actual]
        foto_ajustada = ajustar_imagen(foto_original)
        oracion_a_mostrar = oraciones[indice_foto_actual]

        # Transición
        if tiempo_actual - tiempo_inicio_transicion < duracion_transicion:
            progreso_transicion = (tiempo_actual - tiempo_inicio_transicion) / duracion_transicion
            transicion_actual(ventana, foto_ajustada, oracion_a_mostrar, progreso_transicion)
        else:
            # Si la transición ha terminado, simplemente mostrar la foto y la oración
            foto_ajustada_rect = foto_ajustada.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
            ventana.blit(foto_ajustada, foto_ajustada_rect)

            texto_renderizado = fuente_oracion.render(oracion_a_mostrar, True, BLANCO)
            texto_rect = texto_renderizado.get_rect(center=(ANCHO // 2, ALTO - 50))
            ventana.blit(texto_renderizado, texto_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()