import unicodedata
import re

from preguntas_entrenamiento import INTENCIONES


PRIORIDAD_INTENCIONES = {
    "clientes_por_departamento": 0.45,
    "vehiculos_por_marca": 0.45,
    "vehiculos_mas_atendidos": 0.45,
    "materiales_bajo_stock": 0.45,
    "total_ordenes": 0.45,
    "ventas_recientes": 0.45,
    "mano_obra_mas_cara": 0.55,
    "cotizacion_mas_alta": 0.55,
    "material_mas_comprado": 0.55,
    "departamento_mas_ventas": 0.55,
    "proveedor_mas_pedidos": 0.55,
    "proveedor_mas_cotizaciones": 0.55,

    "top_sucursal": 0.40,
    "top_clientes_gasto": 0.40,
    "top_marcas_atendidas": 0.40,
    "producto_mas_utilizado": 0.40,
    "top_empleado_ordenes": 0.40,
    "ordenes_por_empleado": 0.30,
    "ventas_anio_actual": 0.60,
    "clientes_telefonos": 0.60,
    "materiales_bajo_stock": 0.60,
    "vehiculos_mas_atendidos": 0.60,
    "mano_obra_mas_cara": 0.60,
    "documentos_fiscales_por_anio": 0.65,
    "ordenes_trabajo": 0.45,
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


def contiene(texto, palabras):
    return all(palabra in texto for palabra in palabras)


def detectar_regla_directa(pregunta_normalizada):
    """Reglas fuertes para preguntas humanas que el detector por similitud puede confundir."""

    # Seguridad: si el usuario pide modificar datos, no es consulta válida.
    acciones_peligrosas = [
        "crea", "crear", "borra", "borrar", "elimina", "eliminar",
        "actualiza", "actualizar", "modifica", "modificar", "inserta", "insertar",
        "drop", "delete", "update", "insert", "alter", "truncate"
    ]
    if any(palabra in pregunta_normalizada.split() for palabra in acciones_peligrosas):
        return None

    if "proveedor" in pregunta_normalizada and "cotizacion" in pregunta_normalizada and any(x in pregunta_normalizada for x in ["mas", "mayor"]):
        return "proveedor_mas_cotizaciones"

    if "proveedor" in pregunta_normalizada and "pedido" in pregunta_normalizada and any(x in pregunta_normalizada for x in ["mas", "mayor", "recibe"]):
        return "proveedor_mas_pedidos"

    if "departamento" in pregunta_normalizada and any(x in pregunta_normalizada for x in ["venta", "ventas", "ingreso", "ingresos", "facturacion"]):
        return "departamento_mas_ventas"

    if "sucursal" in pregunta_normalizada and any(x in pregunta_normalizada for x in ["venta", "ventas", "vende", "vendio", "ingreso", "ingresos", "dinero", "rentable"]):
        return "top_sucursal"

    if "cliente" in pregunta_normalizada and any(x in pregunta_normalizada for x in ["gasto", "gastado", "dinero", "rentable", "deja"]):
        return "top_clientes_gasto"

    if any(x in pregunta_normalizada for x in ["material", "producto", "repuesto"]):
        if any(x in pregunta_normalizada for x in ["compra", "comprado", "compras"]):
            return "material_mas_comprado"
        if any(x in pregunta_normalizada for x in ["utilizado", "usado", "usa", "consume", "consumido"]):
            return "producto_mas_utilizado"

    if "cotizacion" in pregunta_normalizada and any(x in pregunta_normalizada for x in ["alta", "mayor", "monto", "cara"]):
        return "cotizacion_mas_alta"

    if "diagnostico" in pregunta_normalizada and any(x in pregunta_normalizada for x in ["costoso", "caro", "precio"]):
        return "mano_obra_mas_cara"

    if "mano de obra" in pregunta_normalizada and any(x in pregunta_normalizada for x in ["cara", "caro", "mayor precio"]):
        return "mano_obra_mas_cara"

    if "tipo" in pregunta_normalizada and "pago" in pregunta_normalizada and any(x in pregunta_normalizada for x in ["mas", "usa", "usado"]):
        return "tipo_pago_mas_usado"

    if "diagnostico" in pregunta_normalizada and any(x in pregunta_normalizada for x in ["aparece", "frecuente", "repite", "mas"]):
        return "diagnostico_mas_frecuente"
    
    if (
        ("factura" in pregunta_normalizada or "facturas" in pregunta_normalizada or "documento fiscal" in pregunta_normalizada or "documentos fiscales" in pregunta_normalizada)
        and ("anio" in pregunta_normalizada or "año" in pregunta_normalizada or re.search(r"\b20\d{2}\b", pregunta_normalizada))
    ):
        return "documentos_fiscales_por_anio"

    if (
        ("vehiculo" in pregunta_normalizada or "vehiculos" in pregunta_normalizada or "carro" in pregunta_normalizada or "auto" in pregunta_normalizada)
        and ("orden" in pregunta_normalizada or "ordenes" in pregunta_normalizada or "trabajo" in pregunta_normalizada)
    ):
        return "vehiculos_mas_atendidos"

    return None


def detectar_intencion(pregunta):
    pregunta_normalizada = normalizar(pregunta)

    intencion_directa = detectar_regla_directa(pregunta_normalizada)
    if intencion_directa:
        return intencion_directa

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