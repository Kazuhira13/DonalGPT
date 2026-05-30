import unicodedata
import re

from preguntas_entrenamiento import INTENCIONES


PRIORIDAD_INTENCIONES = {
    "clientes_por_departamento": 0.45,
    "vehiculos_por_marca": 0.45,
    "vehiculos_mas_atendidos": 0.45,
    "materiales_bajo_stock": 0.50,
    "total_ordenes": 0.45,
    "ventas_recientes": 0.45,

    "top_sucursal": 0.55,
    "ventas_por_mes": 0.55,
    "top_clientes_gasto": 0.50,
    "top_marcas_atendidas": 0.50,
    "producto_mas_utilizado": 0.40,
    "top_empleado_ordenes": 0.40,

    "ordenes_por_empleado": 0.30,
}


def normalizar(texto):
    texto = texto.lower().strip()

    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

    texto = re.sub(r'[^a-z0-9ñ\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto


def detectar_intencion(pregunta):
    pregunta_normalizada = normalizar(pregunta)
    palabras_pregunta = set(pregunta_normalizada.split())

    mejores_coincidencias = []

    for intencion, ejemplos in INTENCIONES.items():
        mejor_puntaje = 0

        for ejemplo in ejemplos:
            ejemplo_normalizado = normalizar(ejemplo)
            palabras_ejemplo = set(ejemplo_normalizado.split())

            if not palabras_ejemplo:
                continue

            palabras_encontradas = palabras_pregunta.intersection(palabras_ejemplo)

            puntaje = len(palabras_encontradas) / len(palabras_ejemplo)

            if ejemplo_normalizado in pregunta_normalizada:
                puntaje += 1.0

            if intencion in PRIORIDAD_INTENCIONES:
                puntaje += PRIORIDAD_INTENCIONES[intencion]

            mejor_puntaje = max(mejor_puntaje, puntaje)

        if mejor_puntaje >= 0.60:
            mejores_coincidencias.append((mejor_puntaje, intencion))

    if mejores_coincidencias:
        mejores_coincidencias.sort(reverse=True)
        return mejores_coincidencias[0][1]

    return None