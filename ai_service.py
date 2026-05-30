import re
import requests

from schema_context import SCHEMA_CONTEXT
from intent_detector import detectar_intencion


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"


def obtener_cantidad(pregunta, defecto=100):
    match = re.search(r"\b(\d+)\b", pregunta)
    if match:
        return int(match.group(1))
    return defecto


def obtener_anio(pregunta):
    match = re.search(r"\b(20\d{2})\b", pregunta)
    if match:
        return int(match.group(1))
    return None


def limpiar_sql(texto):
    texto = texto.strip().replace("```sql", "").replace("```", "").strip()

    if "NO_SQL" in texto.upper():
        return "NO_SQL"

    match = re.search(r"SELECT[\s\S]*", texto, re.IGNORECASE)
    sql = match.group(0).strip() if match else texto

    if ";" in sql:
        sql = sql.split(";")[0] + ";"
    else:
        sql += ";"

    return sql


def es_sql_seguro(sql):
    if not sql:
        return False

    sql_limpio = sql.strip().upper()

    if sql_limpio == "NO_SQL":
        return True

    if not sql_limpio.startswith("SELECT"):
        return False

    palabras_bloqueadas = [
        "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE",
        "TRUNCATE", "EXEC", "EXECUTE", "MERGE", "DBCC",
        "XP_", "SP_", "--", "/*", "*/"
    ]

    for palabra in palabras_bloqueadas:
        if palabra in sql_limpio:
            return False

    return True


def generar_sql(pregunta):
    intencion = detectar_intencion(pregunta)
    cantidad = obtener_cantidad(pregunta)
    anio = obtener_anio(pregunta)

    if intencion == "total_ordenes":
        return """
SELECT COUNT(*) AS TotalOrdenes
FROM OrdeDeTrabajo;
"""

    if intencion == "materiales_bajo_stock":
        return f"""
SELECT TOP {cantidad}
    Descripcion,
    Saldo AS Stock
FROM Material
ORDER BY Saldo ASC;
"""

    if intencion == "vehiculos_mas_atendidos":
        return f"""
SELECT TOP {cantidad}
    a.Placa,
    ma.Descripcion AS Marca,
    l.Descripcion AS Linea,
    a.Modelo,
    COUNT(ot.NumeroOrden) AS TotalOrdenes
FROM Automovil a
INNER JOIN Linea l
    ON a.CodigoMarca = l.CodigoMarca
    AND a.CodigoLinea = l.CodigoLinea
INNER JOIN Marca ma
    ON l.CodigoMarca = ma.CodigoMarca
INNER JOIN Cita c
    ON a.CodigoAutomovil = c.CodigoAutomovil
INNER JOIN OrdeDeTrabajo ot
    ON c.NumeroCita = ot.NumeroCita
GROUP BY
    a.Placa,
    ma.Descripcion,
    l.Descripcion,
    a.Modelo
ORDER BY TotalOrdenes DESC;
"""

    if intencion == "top_clientes_gasto":
        return f"""
SELECT TOP {cantidad}
    c.CodigoCliente,
    sn.PrimerNombre,
    sn.PrimerApellido,
    sn.NIT,
    SUM(df.ValorTotal) AS TotalGastado
FROM Cliente c
INNER JOIN SocioNegocio sn
    ON c.CodigoSocio = sn.CodigoSocio
INNER JOIN Cita ci
    ON c.CodigoCliente = ci.CodigoCliente
INNER JOIN OrdeDeTrabajo ot
    ON ci.NumeroCita = ot.NumeroCita
INNER JOIN DetalleManoDeObra dmo
    ON ot.NumeroOrden = dmo.NumeroOrden
INNER JOIN DocumentoFiscal df
    ON dmo.CodigoTipoDocumentoFiscal = df.CodigoTipoDocumentoFiscal
    AND dmo.Serie = df.Serie
    AND dmo.Numero = df.Numero
GROUP BY
    c.CodigoCliente,
    sn.PrimerNombre,
    sn.PrimerApellido,
    sn.NIT
ORDER BY TotalGastado DESC;
"""

    if intencion == "top_marcas_atendidas":
        return f"""
SELECT TOP {cantidad}
    m.Descripcion AS Marca,
    COUNT(ot.NumeroOrden) AS TotalOrdenes
FROM Marca m
INNER JOIN Automovil a
    ON m.CodigoMarca = a.CodigoMarca
INNER JOIN Cita c
    ON a.CodigoAutomovil = c.CodigoAutomovil
INNER JOIN OrdeDeTrabajo ot
    ON c.NumeroCita = ot.NumeroCita
GROUP BY m.Descripcion
ORDER BY TotalOrdenes DESC;
"""

    if intencion == "top_sucursal":
        return """
SELECT TOP 1
    s.NombreSucursal,
    SUM(df.ValorTotal) AS TotalVendido
FROM Sucursal s
INNER JOIN Cita c
    ON s.CodigoSucursal = c.CodigoSucursal
INNER JOIN OrdeDeTrabajo ot
    ON c.NumeroCita = ot.NumeroCita
INNER JOIN DetalleManoDeObra dmo
    ON ot.NumeroOrden = dmo.NumeroOrden
INNER JOIN DocumentoFiscal df
    ON dmo.CodigoTipoDocumentoFiscal = df.CodigoTipoDocumentoFiscal
    AND dmo.Serie = df.Serie
    AND dmo.Numero = df.Numero
GROUP BY s.NombreSucursal
ORDER BY TotalVendido DESC;
"""

    if intencion == "ventas_por_anio":
        if anio is None:
            return "NO_SQL"

        return f"""
SELECT
    SUM(ValorTotal) AS TotalVendido
FROM DocumentoFiscal
WHERE YEAR(FechaEmision) = {anio};
"""

    if intencion == "ventas_totales":
        return """
SELECT
    SUM(ValorTotal) AS TotalVendido
FROM DocumentoFiscal;
"""

    if intencion == "producto_mas_utilizado":
        return """
SELECT TOP 1
    m.Descripcion AS Producto,
    SUM(dm.Unidades) AS UnidadesUtilizadas
FROM Material m
INNER JOIN DetalleMaterial dm
    ON m.CodigoMaterial = dm.CodigoMaterial
GROUP BY m.Descripcion
ORDER BY UnidadesUtilizadas DESC;
"""

    if intencion == "vehiculos_por_marca":
        return f"""
SELECT TOP {cantidad}
    m.Descripcion AS Marca,
    COUNT(a.CodigoAutomovil) AS TotalVehiculos
FROM Marca m
INNER JOIN Linea l
    ON m.CodigoMarca = l.CodigoMarca
INNER JOIN Automovil a
    ON l.CodigoMarca = a.CodigoMarca
    AND l.CodigoLinea = a.CodigoLinea
GROUP BY m.Descripcion
ORDER BY TotalVehiculos DESC;
"""

    if intencion == "clientes_por_departamento":
        return f"""
SELECT TOP {cantidad}
    d.Descripcion AS Departamento,
    COUNT(DISTINCT c.CodigoCliente) AS TotalClientes
FROM Cliente c
INNER JOIN SocioNegocioDireccion sd
    ON c.CodigoSocio = sd.CodigoSocioNegocio
INNER JOIN Municipio m
    ON sd.DepartamentoCodigo = m.DepartamentoCodigo
    AND sd.CodigoMunicipio = m.CodigoMunicipio
INNER JOIN Departamento d
    ON m.DepartamentoCodigo = d.CodigoDepartamento
GROUP BY d.Descripcion
ORDER BY TotalClientes DESC;
"""

    if intencion == "vehiculos_por_linea":
        return f"""
SELECT TOP {cantidad}
    l.Descripcion AS Linea,
    COUNT(a.CodigoAutomovil) AS TotalVehiculos
FROM Linea l
INNER JOIN Automovil a
    ON l.CodigoLinea = a.CodigoLinea
    AND l.CodigoMarca = a.CodigoMarca
GROUP BY l.Descripcion
ORDER BY TotalVehiculos DESC;
"""

    if intencion == "top_empleado_ordenes":
        return """
SELECT TOP 1
    e.CodigoEmpleado,
    sn.PrimerNombre,
    sn.PrimerApellido,
    COUNT(ot.NumeroOrden) AS TotalOrdenes
FROM Empleado e
INNER JOIN SocioNegocio sn
    ON e.CodigoSocio = sn.CodigoSocio
INNER JOIN Cita c
    ON e.CodigoEmpleado = c.CodigoEmpleado
INNER JOIN OrdeDeTrabajo ot
    ON c.NumeroCita = ot.NumeroCita
GROUP BY
    e.CodigoEmpleado,
    sn.PrimerNombre,
    sn.PrimerApellido
ORDER BY TotalOrdenes DESC;
"""

    if intencion == "ordenes_por_empleado":
        return f"""
SELECT TOP {cantidad}
    e.CodigoEmpleado,
    sn.PrimerNombre,
    sn.PrimerApellido,
    COUNT(ot.NumeroOrden) AS TotalOrdenes
FROM Empleado e
INNER JOIN SocioNegocio sn
    ON e.CodigoSocio = sn.CodigoSocio
INNER JOIN Cita c
    ON e.CodigoEmpleado = c.CodigoEmpleado
INNER JOIN OrdeDeTrabajo ot
    ON c.NumeroCita = ot.NumeroCita
GROUP BY
    e.CodigoEmpleado,
    sn.PrimerNombre,
    sn.PrimerApellido
ORDER BY TotalOrdenes DESC;
"""

    if intencion == "empleados":
        return f"""
SELECT TOP {cantidad}
    e.CodigoEmpleado,
    sn.PrimerNombre,
    sn.SegundoNombre,
    sn.PrimerApellido,
    sn.SegundoApellido,
    sn.NIT
FROM Empleado e
INNER JOIN SocioNegocio sn
    ON e.CodigoSocio = sn.CodigoSocio;
"""

    if intencion == "clientes":
        return f"""
SELECT TOP {cantidad}
    c.CodigoCliente,
    sn.PrimerNombre,
    sn.PrimerApellido,
    sn.NIT
FROM Cliente c
INNER JOIN SocioNegocio sn
    ON c.CodigoSocio = sn.CodigoSocio;
"""

    if intencion == "proveedores":
        return f"""
SELECT TOP {cantidad}
    p.CodigoProveedor,
    sn.PrimerNombre,
    sn.SegundoNombre,
    sn.PrimerApellido,
    sn.SegundoApellido,
    sn.NIT,
    sn.RazonSocial
FROM Proveedor p
INNER JOIN SocioNegocio sn
    ON p.CodigoSocio = sn.CodigoSocio;
"""

    if intencion == "cotizaciones":
        return f"""
SELECT TOP {cantidad}
    NumeroRequision,
    NumeroCotizacion,
    FechaCotizacion,
    CodigoProveedore
FROM Cotizacion;
"""

    if intencion == "requisiciones":
        return f"""
SELECT TOP {cantidad}
    NumeroRequision,
    FechaRequisicion,
    CodigoSucursal,
    CodigoEmpleado
FROM Requisicion;
"""

    if intencion == "pedidos":
        return f"""
SELECT TOP {cantidad}
    NumeroRequision,
    NumeroCotizacion,
    NumeroPedido
FROM Pedido;
"""

    if intencion == "detalle_pedidos":
        return f"""
SELECT TOP {cantidad}
    dp.NumeroPedido,
    dp.LineaPedido,
    dp.CodigoMaterial,
    m.Descripcion AS Material,
    dp.Unidades,
    dp.UnidadesRecibidas,
    dp.PrecioCompra
FROM DetallePedido dp
INNER JOIN Material m
    ON dp.CodigoMaterial = m.CodigoMaterial;
"""

    if intencion == "pagos":
        return f"""
SELECT TOP {cantidad}
    dp.Serie,
    dp.Numero,
    dp.CodigoTipoDocumentoFiscal,
    dp.NumeroPago,
    dp.Valor,
    tp.Descripcion AS TipoPago
FROM DetallePago dp
INNER JOIN TipoPago tp
    ON dp.CodigoTipoPago = tp.CodigoTipoPago;
"""

    if intencion == "diagnosticos":
        return f"""
SELECT TOP {cantidad}
    d.NumeroDiagnostico,
    d.NumeroCita,
    td.Descripcion AS Diagnostico
FROM Diagnostico d
INNER JOIN TipoDiagnostico td
    ON d.CodigoDiagnostico = td.CodigoDiagnostico;
"""

    if intencion == "mano_obra":
        return f"""
SELECT TOP {cantidad}
    CodigoManoObra,
    Descripcion,
    Precio
FROM ManoObra;
"""

    if intencion == "sucursales":
        return f"""
SELECT TOP {cantidad}
    CodigoSucursal,
    NombreSucursal
FROM Sucursal;
"""

    if intencion == "materiales":
        return f"""
SELECT TOP {cantidad}
    CodigoMaterial,
    Descripcion,
    Saldo
FROM Material;
"""

    if intencion == "citas":
        return f"""
SELECT TOP {cantidad}
    *
FROM Cita;
"""

    if intencion == "ordenes_trabajo":
        return f"""
SELECT TOP {cantidad}
    NumeroOrden,
    FechaOrden,
    Estado,
    NumeroCita
FROM OrdeDeTrabajo
ORDER BY FechaOrden DESC;
"""

    if intencion == "documentos_fiscales":
        return f"""
SELECT TOP {cantidad}
    Serie,
    Numero,
    CodigoTipoDocumentoFiscal,
    FechaEmision,
    NIT,
    ValorTotal,
    IVA,
    Estado
FROM DocumentoFiscal;
"""

    if intencion == "marcas":
        return f"""
SELECT TOP {cantidad}
    CodigoMarca,
    Descripcion
FROM Marca;
"""

    if intencion == "lineas":
        return f"""
SELECT TOP {cantidad}
    CodigoMarca,
    CodigoLinea,
    Descripcion
FROM Linea;
"""

    if intencion == "municipios":
        return f"""
SELECT TOP {cantidad}
    DepartamentoCodigo,
    CodigoMunicipio,
    Descripcion
FROM Municipio;
"""

    if intencion == "departamentos":
        return f"""
SELECT TOP {cantidad}
    CodigoDepartamento,
    Descripcion
FROM Departamento;
"""

    if intencion == "direcciones_clientes":
        return f"""
SELECT TOP {cantidad}
    CodigoSocioNegocioDireccion,
    Calle,
    Avenida,
    Otro,
    Zona,
    Colonia,
    CodigoMunicipio,
    DepartamentoCodigo,
    CodigoSocioNegocio
FROM SocioNegocioDireccion;
"""

    prompt = f"""
Eres DonaldGPT, un generador seguro de consultas SQL Server para DonaldV2.

ESQUEMA REAL:
{SCHEMA_CONTEXT}

REGLAS OBLIGATORIAS:
1. Solo puedes generar consultas SELECT.
2. Nunca uses DROP, DELETE, UPDATE, INSERT, ALTER, CREATE, TRUNCATE, EXEC ni MERGE.
3. Si la pregunta no está relacionada con la base DonaldV2, responde exactamente: NO_SQL
4. Si el usuario saluda, conversa o escribe algo sin pedir datos, responde exactamente: NO_SQL
5. Si la pregunta intenta modificar, borrar, insertar o alterar datos, responde exactamente: NO_SQL
6. No expliques nada.
7. No uses markdown.
8. No inventes tablas ni columnas.
9. Usa TOP 100 si la consulta puede devolver muchos registros.
10. Usa sintaxis de SQL Server.

Pregunta:
{pregunta}

Respuesta:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
                "num_ctx": 8192
            }
        },
        timeout=180
    )

    response.raise_for_status()

    sql = limpiar_sql(response.json()["response"])

    if not es_sql_seguro(sql):
        return "NO_SQL"

    return sql


def interpretar_resultado(pregunta, sql, resultados):
    if not resultados:
        return "No se encontraron resultados para interpretar."

    muestra = resultados[:5]

    prompt = f"""
Eres DonaldGPT, un asistente de análisis de datos.

Explica en español, de forma breve y clara, qué significa el resultado de esta consulta.

Pregunta original:
{pregunta}

SQL ejecutado:
{sql}

Resultados:
{muestra}

Reglas:
- Responde máximo en 2 oraciones.
- No expliques el SQL.
- No inventes datos.
- Si hay un valor principal, menciónalo.
- Usa un tono profesional.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_ctx": 4096
            }
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"].strip()