SCHEMA_CONTEXT = """
BASE DE DATOS: DonaldV2

REGLA CRÍTICA:
- Nunca inventar tablas.
- Nunca inventar columnas.
- Nunca inventar relaciones.
- Usar únicamente el esquema real de DonaldV2.
- Si la pregunta no puede responderse con las tablas y columnas existentes, responder exactamente: NO_SQL.
- Nunca generar INSERT, UPDATE, DELETE, DROP, CREATE, ALTER ni TRUNCATE.
- Solo generar consultas SELECT.

IMPORTANTE SOBRE DocumentoFiscal:
- DocumentoFiscal tiene millones de registros.
- Para consultas de ventas, facturación o ingresos, usar filtros por fecha cuando el usuario mencione año, mes o rango.
- Evitar SELECT * FROM DocumentoFiscal.
- Para listados usar TOP 100 como máximo.
- Para totales usar SUM(ValorTotal).
- Para cantidades usar COUNT.
- Para rankings usar GROUP BY y ORDER BY DESC.

SINÓNIMOS IMPORTANTES:
- ventas, facturas, documentos fiscales, ingresos = DocumentoFiscal.
- total vendido = SUM(DocumentoFiscal.ValorTotal).
- fecha de venta = DocumentoFiscal.FechaEmision.
- clientes = Cliente unido con SocioNegocio.
- empleados = Empleado unido con SocioNegocio.
- proveedores = Proveedor unido con SocioNegocio.
- teléfonos de clientes = Cliente -> SocioNegocio -> SocioNegocioTelefono.
- vehículos, carros, autos = Automovil.
- servicios, trabajos, órdenes = OrdeDeTrabajo.
- sucursal más rentable = sucursal con más ventas.
- sucursal que produce más ingresos = sucursal con más ventas.
- mejor cliente = cliente que más gastó.
- quién me deja más dinero = cliente que más gastó.
- marca favorita de clientes = marca más atendida.
- vehículo más atendido = vehículo con más órdenes.
- materiales que debo comprar = materiales con menor Saldo.
- producto más utilizado = Material unido con DetalleMaterial.

TABLAS Y COLUMNAS:

Cliente:
- CodigoCliente
- CodigoSocio

SocioNegocio:
- CodigoSocio
- PrimerNombre
- SegundoNombre
- PrimerApellido
- SegundoApellido
- FechaNacimiento
- CUI
- NIT
- RazonSocial
- Genero
- CodigoTipoSocioNegocio

SocioNegocioTelefono:
- CodigoSocio
- CodigoSocioNegocioTelefono
- Numero
- CodigoTipoTelefono

SocioNegocioDireccion:
- CodigoSocioNegocioDireccion
- Calle
- Avenida
- Otro
- Zona
- Colonia
- CodigoMunicipio
- DepartamentoCodigo
- CodigoTipoDireccion
- CodigoSocioNegocio

Empleado:
- CodigoEmpleado
- CodigoSocio

Proveedor:
- CodigoProveedor
- CodigoSocio

Automovil:
- CodigoAutomovil
- Placa
- Color
- VIN
- Motor
- Modelo
- CodigoLinea
- CodigoMarca

Marca:
- CodigoMarca
- Descripcion

Linea:
- CodigoMarca
- CodigoLinea
- Descripcion

Cita:
- NumeroCita
- CodigoSucursal
- CodigoCliente
- FechaCita
- FechaRecepcion
- Observaciones
- CodigoEmpleado
- CodigoAutomovil

OrdeDeTrabajo:
- NumeroOrden
- FechaOrden
- Estado
- NumeroCita

DetalleManoDeObra:
- NumeroOrden
- NumeroManoDeObra
- Unidades
- CodigoManoObra
- FechaInicio
- FechaFin
- CodigoEmpleado
- Serie
- Numero
- CodigoTipoDocumentoFiscal

DocumentoFiscal:
- CodigoTipoDocumentoFiscal
- Serie
- Numero
- FechaEmision
- NIT
- ValorTotal
- IVA
- Estado

Material:
- CodigoMaterial
- Descripcion
- PrecioCosto
- PrecioVenta
- Saldo

DetalleMaterial:
- NumeroOrden
- NumeroManoDeObra
- CodigoMaterial
- NumeroDetalleMaterial
- Unidades
- PrecioVenta

Sucursal:
- CodigoSucursal
- NombreSucursal
- CodigoTaller

SucursalDireccion:
- CodigoSucursal
- CodigoSucursalDireccion
- Calle
- Avenida
- Otro
- Zona
- Colonia
- CodigoMunicipio
- DepartamentoCodigo
- CodigoTipoDireccion

Departamento:
- CodigoDepartamento
- Descripcion

Municipio:
- DepartamentoCodigo
- CodigoMunicipio
- Descripcion

Diagnostico:
- NumeroDiagnostico
- NumeroCita
- CodigoDiagnostico

TipoDiagnostico:
- CodigoDiagnostico
- Descripcion

DetallePago:
- Serie
- Numero
- CodigoTipoDocumentoFiscal
- NumeroPago
- Valor
- CodigoTipoPago

TipoPago:
- CodigoTipoPago
- Descripcion

ManoObra:
- CodigoManoObra
- Descripcion
- Precio

Taller:
- CodigoTaller
- RazonSocial
- NombreComercial
- NIT

RELACIONES REALES:

Cliente.CodigoSocio = SocioNegocio.CodigoSocio
Empleado.CodigoSocio = SocioNegocio.CodigoSocio
Proveedor.CodigoSocio = SocioNegocio.CodigoSocio

SocioNegocioTelefono.CodigoSocio = SocioNegocio.CodigoSocio
SocioNegocioDireccion.CodigoSocioNegocio = SocioNegocio.CodigoSocio

SocioNegocioDireccion.DepartamentoCodigo = Municipio.DepartamentoCodigo
SocioNegocioDireccion.CodigoMunicipio = Municipio.CodigoMunicipio
Municipio.DepartamentoCodigo = Departamento.CodigoDepartamento

Cita.CodigoSucursal = Sucursal.CodigoSucursal
Cita.CodigoCliente = Cliente.CodigoCliente
Cita.CodigoEmpleado = Empleado.CodigoEmpleado
Cita.CodigoAutomovil = Automovil.CodigoAutomovil

OrdeDeTrabajo.NumeroCita = Cita.NumeroCita

Automovil.CodigoMarca = Linea.CodigoMarca
Automovil.CodigoLinea = Linea.CodigoLinea
Linea.CodigoMarca = Marca.CodigoMarca

DetalleManoDeObra.NumeroOrden = OrdeDeTrabajo.NumeroOrden
DetalleManoDeObra.CodigoEmpleado = Empleado.CodigoEmpleado
DetalleManoDeObra.CodigoManoObra = ManoObra.CodigoManoObra

DetalleManoDeObra.CodigoTipoDocumentoFiscal = DocumentoFiscal.CodigoTipoDocumentoFiscal
DetalleManoDeObra.Serie = DocumentoFiscal.Serie
DetalleManoDeObra.Numero = DocumentoFiscal.Numero

DetalleMaterial.NumeroOrden = DetalleManoDeObra.NumeroOrden
DetalleMaterial.NumeroManoDeObra = DetalleManoDeObra.NumeroManoDeObra
DetalleMaterial.CodigoMaterial = Material.CodigoMaterial

DetallePago.CodigoTipoDocumentoFiscal = DocumentoFiscal.CodigoTipoDocumentoFiscal
DetallePago.Serie = DocumentoFiscal.Serie
DetallePago.Numero = DocumentoFiscal.Numero
DetallePago.CodigoTipoPago = TipoPago.CodigoTipoPago

Diagnostico.NumeroCita = Cita.NumeroCita
Diagnostico.CodigoDiagnostico = TipoDiagnostico.CodigoDiagnostico

Sucursal.CodigoTaller = Taller.CodigoTaller
SucursalDireccion.CodigoSucursal = Sucursal.CodigoSucursal
SucursalDireccion.DepartamentoCodigo = Municipio.DepartamentoCodigo
SucursalDireccion.CodigoMunicipio = Municipio.CodigoMunicipio

CONSULTAS EJEMPLO CORRECTAS:

Pregunta:
¿Cuál es la sucursal que más vende?

SQL:
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

Pregunta:
¿Quién es mi mejor cliente?

SQL:
SELECT TOP 10
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

Pregunta:
¿Qué marca se atiende más?

SQL:
SELECT TOP 100
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

Pregunta:
¿Cuál es el vehículo más atendido?

SQL:
SELECT TOP 1
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

Pregunta:
¿Qué departamento tiene más clientes?

SQL:
SELECT TOP 100
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

Pregunta:
Quiero ver los números de teléfono de los clientes.

SQL:
SELECT TOP 100
    c.CodigoCliente,
    sn.PrimerNombre,
    sn.PrimerApellido,
    sn.NIT,
    st.Numero AS Telefono
FROM Cliente c
INNER JOIN SocioNegocio sn
    ON c.CodigoSocio = sn.CodigoSocio
INNER JOIN SocioNegocioTelefono st
    ON sn.CodigoSocio = st.CodigoSocio;

Pregunta:
¿Qué materiales debo comprar esta semana?

SQL:
SELECT TOP 100
    Descripcion,
    Saldo AS Stock
FROM Material
ORDER BY Saldo ASC;

Pregunta:
¿Cuánto vendimos este año?

SQL:
SELECT
    SUM(ValorTotal) AS TotalVendido
FROM DocumentoFiscal
WHERE YEAR(FechaEmision) = YEAR(GETDATE());

Pregunta:
¿Cuál es el producto más utilizado?

SQL:
SELECT TOP 1
    m.Descripcion AS Producto,
    SUM(dm.Unidades) AS UnidadesUtilizadas
FROM Material m
INNER JOIN DetalleMaterial dm
    ON m.CodigoMaterial = dm.CodigoMaterial
GROUP BY m.Descripcion
ORDER BY UnidadesUtilizadas DESC;

Pregunta:
Ventas por mes en 2025.

SQL:
SELECT
    YEAR(df.FechaEmision) AS Anio,
    MONTH(df.FechaEmision) AS Mes,
    SUM(df.ValorTotal) AS TotalVendido
FROM DocumentoFiscal df
WHERE YEAR(df.FechaEmision) = 2025
GROUP BY YEAR(df.FechaEmision), MONTH(df.FechaEmision)
ORDER BY Anio, Mes;

IMPORTANTE:
Si la pregunta pide crear, borrar, modificar, actualizar, eliminar o insertar datos:
Responder exactamente:
NO_SQL
"""