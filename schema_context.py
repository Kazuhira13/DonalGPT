SCHEMA_CONTEXT = """
BASE DE DATOS: DonaldV2

IMPORTANTE:
- El nombre correcto de la tabla de órdenes es OrdeDeTrabajo.
- Usar sintaxis SQL Server.
- Solo generar consultas SELECT.
- No inventar tablas ni columnas.

IMPORTANTE SOBRE DocumentoFiscal:
- DocumentoFiscal tiene millones de registros.
- Para consultas de ventas, facturación o ingresos, siempre usar filtros por fecha cuando el usuario mencione año, mes, trimestre o rango.
- Evitar SELECT * FROM DocumentoFiscal.
- Para listados de ventas o documentos fiscales usar TOP 100 como máximo.
- Para consultas de totales usar SUM(ValorTotal).
- Para consultas agrupadas usar GROUP BY con sucursal, cliente, año, mes, departamento o marca según corresponda.

TABLAS PRINCIPALES:

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

Cliente:
- CodigoCliente
- CodigoSocio

Empleado:
- CodigoEmpleado
- CodigoSocio

Proveedor:
- CodigoProveedor
- CodigoSocio

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

Diagnostico:
- NumeroDiagnostico
- NumeroCita
- CodigoDiagnostico

TipoDiagnostico:
- CodigoDiagnostico
- Descripcion

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

ManoObra:
- CodigoManoObra
- Descripcion
- Precio

DetalleMaterial:
- NumeroOrden
- NumeroManoDeObra
- CodigoMaterial
- NumeroDetalleMaterial
- Unidades
- PrecioVenta

Material:
- CodigoMaterial
- Descripcion
- PrecioCosto
- PrecioVenta
- Saldo

DocumentoFiscal:
- CodigoTipoDocumentoFiscal
- Serie
- Numero
- FechaEmision
- NIT
- ValorTotal
- IVA
- Estado

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

Sucursal:
- CodigoSucursal
- NombreSucursal
- CodigoTaller

Taller:
- CodigoTaller
- RazonSocial
- NombreComercial
- NIT

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

Cotizacion:
- NumeroRequision
- NumeroCotizacion
- FechaCotizacion
- CodigoProveedore

Requisicion:
- NumeroRequision
- FechaRequisicion
- CodigoSucursal
- CodigoEmpleado

Pedido:
- NumeroRequision
- NumeroCotizacion
- NumeroPedido

DetallePedido:
- NumeroPedido
- LineaPedido
- CodigoMaterial
- Unidades
- UnidadesRecibidas
- PrecioCompra

VISTAS DISPONIBLES:

vAutomovil:
- CodigoAutomovil
- Placa
- Modelo
- Marca
- Linea

vEmpleados:
- CodigoEmpleado
- NombreEmpleado

vClientess:
- CodigoCliente
- NombreEmpleado

vProveedor:
- CodigoProveedor
- nombreproveedor

vProveedores:
- CodigoProveedor
- Nombre
- NIT

RELACIONES REALES IMPORTANTES:

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
DetalleManoDeObra.CodigoManoObra = ManoObra.CodigoManoObra
DetalleManoDeObra.CodigoEmpleado = Empleado.CodigoEmpleado
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

Cotizacion.NumeroRequision = Requisicion.NumeroRequision
Cotizacion.CodigoProveedore = Proveedor.CodigoProveedor

Pedido.NumeroRequision = Cotizacion.NumeroRequision
Pedido.NumeroCotizacion = Cotizacion.NumeroCotizacion

DetallePedido.NumeroPedido = Pedido.NumeroPedido
DetallePedido.CodigoMaterial = Material.CodigoMaterial

Requisicion.CodigoSucursal = Sucursal.CodigoSucursal
Requisicion.CodigoEmpleado = Empleado.CodigoEmpleado

SINÓNIMOS Y REGLAS DE NEGOCIO:

- ventas, facturas, documentos fiscales, ingresos = DocumentoFiscal.
- total vendido = SUM(DocumentoFiscal.ValorTotal).
- IVA incluido = DocumentoFiscal.ValorTotal.
- fecha de venta = DocumentoFiscal.FechaEmision.
- clientes = Cliente unido con SocioNegocio.
- empleados, asesores, mecánicos, trabajadores = Empleado unido con SocioNegocio.
- proveedores = Proveedor unido con SocioNegocio.
- teléfonos = SocioNegocioTelefono.Numero.
- vehículos, carros, autos = Automovil.
- placa = Automovil.Placa.
- servicios, trabajos, órdenes = OrdeDeTrabajo.
- sucursal = Sucursal.NombreSucursal.
- taller = Taller.
- productos, repuestos, materiales, insumos = Material.
- producto más usado = Material unido con DetalleMaterial usando SUM(DetalleMaterial.Unidades).
- mano de obra = ManoObra y DetalleManoDeObra.
- pagos = DetallePago unido con DocumentoFiscal y TipoPago.
- diagnósticos = Diagnostico unido con TipoDiagnostico.
- historial de vehículo = Automovil -> Cita -> OrdeDeTrabajo.
- ventas por sucursal = Sucursal -> Cita -> OrdeDeTrabajo -> DetalleManoDeObra -> DocumentoFiscal.
- ventas por departamento o municipio = DocumentoFiscal -> DetalleManoDeObra -> OrdeDeTrabajo -> Cita -> Sucursal -> SucursalDireccion -> Municipio -> Departamento.
- marca más atendida = Marca -> Linea -> Automovil -> Cita -> OrdeDeTrabajo.
- cliente que más gastó = Cliente -> SocioNegocio -> Cita -> OrdeDeTrabajo -> DetalleManoDeObra -> DocumentoFiscal.
- empleado con más órdenes = Empleado -> SocioNegocio -> Cita -> OrdeDeTrabajo.
- vehículos de un cliente = Cliente -> Cita -> Automovil.
- servicios de un vehículo = Automovil -> Cita -> OrdeDeTrabajo -> DetalleManoDeObra -> ManoObra.

CONSULTAS EJEMPLO CORRECTAS:

Pregunta:
¿Cuál fue la sucursal con más ventas en 2026?

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
WHERE YEAR(df.FechaEmision) = 2026
GROUP BY s.NombreSucursal
ORDER BY TotalVendido DESC;

Pregunta:
¿Cuál es el total vendido?

SQL:
SELECT
    SUM(ValorTotal) AS TotalVendido
FROM DocumentoFiscal;

Pregunta:
Muéstrame las ventas más recientes.

SQL:
SELECT TOP 10
    Serie,
    Numero,
    CodigoTipoDocumentoFiscal,
    FechaEmision,
    NIT,
    ValorTotal,
    IVA,
    Estado
FROM DocumentoFiscal
ORDER BY FechaEmision DESC;

Pregunta:
¿Cuál fue la marca de vehículo más atendida?

SQL:
SELECT TOP 1
    m.Descripcion AS Marca,
    COUNT(ot.NumeroOrden) AS TotalServicios
FROM Marca m
INNER JOIN Linea l
    ON m.CodigoMarca = l.CodigoMarca
INNER JOIN Automovil a
    ON l.CodigoMarca = a.CodigoMarca
    AND l.CodigoLinea = a.CodigoLinea
INNER JOIN Cita c
    ON a.CodigoAutomovil = c.CodigoAutomovil
INNER JOIN OrdeDeTrabajo ot
    ON c.NumeroCita = ot.NumeroCita
GROUP BY m.Descripcion
ORDER BY TotalServicios DESC;

Pregunta:
¿Cuál fue el producto más utilizado?

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
Muéstrame el historial del vehículo con placa P123ABC.

SQL:
SELECT TOP 100
    a.Placa,
    c.NumeroCita,
    c.FechaCita,
    ot.NumeroOrden,
    ot.FechaOrden,
    ot.Estado
FROM Automovil a
INNER JOIN Cita c
    ON a.CodigoAutomovil = c.CodigoAutomovil
INNER JOIN OrdeDeTrabajo ot
    ON c.NumeroCita = ot.NumeroCita
WHERE a.Placa = 'P123ABC'
ORDER BY ot.FechaOrden DESC;

Pregunta:
Muéstrame los pagos realizados.

SQL:
SELECT TOP 100
    df.Serie,
    df.Numero,
    df.FechaEmision,
    df.NIT,
    df.ValorTotal,
    dp.NumeroPago,
    dp.Valor AS ValorPago,
    tp.Descripcion AS TipoPago
FROM DetallePago dp
INNER JOIN DocumentoFiscal df
    ON dp.CodigoTipoDocumentoFiscal = df.CodigoTipoDocumentoFiscal
    AND dp.Serie = df.Serie
    AND dp.Numero = df.Numero
INNER JOIN TipoPago tp
    ON dp.CodigoTipoPago = tp.CodigoTipoPago;

Pregunta:
Muéstrame los diagnósticos.

SQL:
SELECT TOP 100
    d.NumeroDiagnostico,
    d.NumeroCita,
    td.Descripcion AS Diagnostico
FROM Diagnostico d
INNER JOIN TipoDiagnostico td
    ON d.CodigoDiagnostico = td.CodigoDiagnostico;

FORMAS COMUNES DE PEDIR DATOS:

- "quiero ver la tabla clientes" = Cliente unido con SocioNegocio.
- "muéstrame clientes" = Cliente unido con SocioNegocio.
- "ver empleados" = Empleado unido con SocioNegocio.
- "muéstrame proveedores" = Proveedor unido con SocioNegocio.
- "quiero ver vehículos" = Automovil o vAutomovil.
- "muéstrame carros" = Automovil o vAutomovil.
- "quiero ver ventas" = DocumentoFiscal.
- "quiero ver productos" = Material.
- "quiero ver pagos" = DetallePago unido con DocumentoFiscal y TipoPago.
- "quiero ver diagnósticos" = Diagnostico unido con TipoDiagnostico.

PREGUNTAS MAL ESCRITAS:

- Si el usuario escribe "quiero ver la los nombres de los clientes", interpretar como "quiero ver los nombres de los clientes".
- Si escribe "nit de 10 clientes", interpretar como "dame 10 NIT de clientes".
- Si escribe "telefonos cliente nit CF-1", interpretar como "muestra el teléfono del cliente con NIT CF-1".
- Si escribe "ordenes", interpretar como OrdeDeTrabajo.
"""