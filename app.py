from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ai_service import generar_sql, interpretar_resultado
from security import consulta_es_segura, pregunta_es_peligrosa
from db import ejecutar_consulta


app = FastAPI(
    title="DonaldGPT API",
    description="Sistema inteligente para consultar DonaldV2 con lenguaje natural",
    version="1.0.0"
)


class ConsultaRequest(BaseModel):
    pregunta: str


def obtener_metricas():
    try:
        documentos = ejecutar_consulta("SELECT COUNT(*) AS Total FROM DocumentoFiscal").iloc[0]["Total"]
        vendido = ejecutar_consulta("SELECT SUM(ValorTotal) AS Total FROM DocumentoFiscal").iloc[0]["Total"]
        ordenes = ejecutar_consulta("SELECT COUNT(*) AS Total FROM OrdeDeTrabajo").iloc[0]["Total"]
        clientes = ejecutar_consulta("SELECT COUNT(*) AS Total FROM Cliente").iloc[0]["Total"]

        return {
            "documentos": f"{int(documentos):,}",
            "vendido": f"Q{float(vendido):,.2f}",
            "ordenes": f"{int(ordenes):,}",
            "clientes": f"{int(clientes):,}",
            "estado": "Conectado"
        }
    except Exception:
        return {
            "documentos": "N/D",
            "vendido": "N/D",
            "ordenes": "N/D",
            "clientes": "N/D",
            "estado": "Sin conexión"
        }


@app.get("/", response_class=HTMLResponse)
def home():
    metricas = obtener_metricas()

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>DonaldGPT</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background:
                radial-gradient(circle at top left, rgba(34,197,94,.10), transparent 28%),
                radial-gradient(circle at top right, rgba(59,130,246,.10), transparent 25%),
                #0f172a;
            color: white;
        }}

        .layout {{
            display: grid;
            grid-template-columns: 260px 1fr;
            min-height: 100vh;
        }}

        .sidebar {{
            background: rgba(2, 6, 23, 0.75);
            border-right: 1px solid rgba(148, 163, 184, 0.16);
            padding: 28px 22px;
            position: sticky;
            top: 0;
            height: 100vh;
        }}

        .brand {{
            margin-bottom: 28px;
        }}

        .brand h1 {{
            margin: 0;
            font-size: 28px;
        }}

        .brand p {{
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.5;
        }}

        .nav-item {{
            padding: 12px 14px;
            border-radius: 12px;
            background: transparent;
            color: #cbd5e1;
            margin-bottom: 8px;
            font-size: 14px;
        }}

        .nav-item.active {{
            background: #1e293b;
            color: #ffffff;
            border-left: 4px solid #22c55e;
        }}

        .safe-box {{
            position: absolute;
            bottom: 24px;
            left: 22px;
            right: 22px;
            background: #0f172a;
            border: 1px solid rgba(34,197,94,.35);
            border-radius: 16px;
            padding: 16px;
            color: #bbf7d0;
            font-size: 13px;
            line-height: 1.5;
        }}

        .main {{
            padding: 38px;
            max-width: 1350px;
            width: 100%;
            margin: auto;
            animation: fadeIn .6s ease;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(12px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .topbar {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 20px;
            margin-bottom: 24px;
        }}

        .topbar h2 {{
            font-size: 30px;
            margin: 0 0 8px;
        }}

        .topbar p {{
            color: #cbd5e1;
            margin: 0;
        }}

        .system-status {{
            background: #111827;
            border: 1px solid rgba(148, 163, 184, 0.18);
            padding: 12px 18px;
            border-radius: 14px;
            font-size: 14px;
            color: #d1fae5;
            box-shadow: 0 10px 30px rgba(0,0,0,.25);
            white-space: nowrap;
        }}

        .dot {{
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #22c55e;
            border-radius: 50%;
            margin-right: 8px;
            box-shadow: 0 0 12px #22c55e;
        }}

        .metrics {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}

        .metric {{
            background: linear-gradient(145deg, #111827, #172033);
            padding: 22px;
            border-radius: 18px;
            box-shadow: 0 18px 35px rgba(0,0,0,.25);
            border: 1px solid rgba(148, 163, 184, 0.12);
            transition: transform .2s ease, border .2s ease;
        }}

        .metric:hover {{
            transform: translateY(-4px);
            border: 1px solid rgba(34, 197, 94, 0.35);
        }}

        .metric span {{
            color: #94a3b8;
            font-size: 14px;
        }}

        .metric h2 {{
            margin: 8px 0 0;
            font-size: 25px;
        }}

        .query-card, .panel {{
            background: linear-gradient(145deg, #111827, #151f32);
            padding: 24px;
            border-radius: 20px;
            box-shadow: 0 20px 45px rgba(0,0,0,.38);
            border: 1px solid rgba(148, 163, 184, 0.12);
        }}

        .query-card {{
            margin-bottom: 22px;
        }}

        textarea {{
            width: 100%;
            height: 115px;
            border-radius: 14px;
            border: 1px solid #334155;
            background: #f8fafc;
            padding: 15px;
            font-size: 16px;
            margin-top: 12px;
            resize: vertical;
            outline: none;
        }}

        textarea:focus {{
            border: 2px solid #22c55e;
            box-shadow: 0 0 0 4px rgba(34,197,94,.15);
        }}

        button {{
            margin-top: 15px;
            padding: 13px 22px;
            border: none;
            border-radius: 10px;
            background: #22c55e;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: transform .15s ease, background .15s ease;
        }}

        button:hover {{
            background: #16a34a;
            transform: translateY(-2px);
        }}

        .btn-secondary {{
            background: #334155;
            margin-left: 8px;
        }}

        .btn-secondary:hover {{
            background: #475569;
        }}

        .quick-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 14px;
        }}

        .quick-buttons button {{
            background: #334155;
            padding: 10px 14px;
            font-size: 14px;
            margin-top: 0;
        }}

        .quick-buttons button:hover {{
            background: #475569;
        }}

        .loader {{
            display: none;
            margin-top: 15px;
            padding: 14px;
            background: #020617;
            border-radius: 12px;
            color: #cbd5e1;
            border: 1px solid rgba(148, 163, 184, 0.18);
        }}

        .spinner {{
            display: inline-block;
            width: 14px;
            height: 14px;
            border: 3px solid #334155;
            border-top: 3px solid #22c55e;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-right: 10px;
            vertical-align: middle;
        }}

        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        .results-grid {{
            display: grid;
            grid-template-columns: 1.15fr .85fr;
            gap: 20px;
        }}

        pre {{
            background: #020617;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 12px;
            overflow-x: auto;
            white-space: pre-wrap;
            border: 1px solid rgba(148, 163, 184, 0.12);
            min-height: 82px;
        }}

        .table-wrapper {{
            width: 100%;
            max-height: 460px;
            overflow: auto;
            border-radius: 12px;
            border: 1px solid #334155;
            background: white;
            margin-top: 15px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            color: #111827;
            min-width: 800px;
        }}

        th, td {{
            padding: 10px;
            border: 1px solid #ddd;
            font-size: 14px;
        }}

        th {{
            background: #e5e7eb;
            position: sticky;
            top: 0;
            z-index: 2;
        }}

        tr:nth-child(even) {{
            background: #f8fafc;
        }}

        tr:hover {{
            background: #dcfce7;
        }}

        a {{
            color: #93c5fd;
        }}

        .status {{
            margin-top: 10px;
            color: #cbd5e1;
        }}

        .chart-box {{
            background: white;
            border-radius: 14px;
            padding: 15px;
            animation: fadeIn .5s ease;
            min-height: 260px;
        }}

        .analysis-box {{
            margin-top: 18px;
            background: #020617;
            border-left: 5px solid #22c55e;
            padding: 18px;
            border-radius: 12px;
            color: #e5e7eb;
            line-height: 1.5;
            animation: fadeIn .5s ease;
        }}

        .history {{
            margin-top: 18px;
            padding: 18px;
            background: #0b1220;
            border-radius: 16px;
            border: 1px solid rgba(148, 163, 184, 0.12);
        }}

        .history h3 {{
            margin-top: 0;
        }}

        .history-item {{
            display: block;
            margin: 8px 0;
            padding: 10px 12px;
            border-radius: 10px;
            background: #1e293b;
            color: #dbeafe;
            cursor: pointer;
            font-size: 13px;
        }}

        .history-item:hover {{
            background: #334155;
        }}

        .footer {{
            text-align: center;
            color: #64748b;
            font-size: 13px;
            margin-top: 28px;
            padding-bottom: 18px;
        }}

        @media (max-width: 1100px) {{
            .layout {{
                grid-template-columns: 1fr;
            }}

            .sidebar {{
                position: relative;
                height: auto;
            }}

            .safe-box {{
                position: relative;
                bottom: auto;
                left: auto;
                right: auto;
                margin-top: 20px;
            }}

            .results-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        @media (max-width: 800px) {{
            .metrics {{
                grid-template-columns: repeat(2, 1fr);
            }}

            .topbar {{
                flex-direction: column;
            }}
        }}

        @media (max-width: 600px) {{
            .main {{
                padding: 20px;
            }}

            .metrics {{
                grid-template-columns: 1fr;
            }}

            button {{
                width: 100%;
            }}

            .quick-buttons button {{
                width: auto;
            }}
        }}
    </style>
</head>

<body>
    <div class="layout">
        <aside class="sidebar">
            <div class="brand">
                <h1>DonaldGPT</h1>
                <p>Asistente inteligente para consultar DonaldV2 con lenguaje natural.</p>
            </div>

            <div class="nav-item active">Inicio</div>
            <div class="nav-item"><a href="/docs" target="_blank">Swagger API</a></div>

            <div class="safe-box">
                <strong>Sistema protegido</strong><br>
                Solo se permiten consultas SELECT. Las operaciones DROP, DELETE, UPDATE e INSERT son bloqueadas.
            </div>
        </aside>

        <main class="main">
            <div class="topbar">
                <div>
                    <h2>Asistente virtual de la base de datos</h2>
                    <p>Consulta información de DonaldV2 usando lenguaje natural, sin escribir SQL manualmente.</p>
                </div>

                <div class="system-status">
                    <span class="dot"></span> SQL Server: {metricas["estado"]}
                </div>
            </div>

            <div class="metrics">
                <div class="metric">
                    <span>Documentos fiscales</span>
                    <h2>{metricas["documentos"]}</h2>
                </div>
                <div class="metric">
                    <span>Total vendido</span>
                    <h2>{metricas["vendido"]}</h2>
                </div>
                <div class="metric">
                    <span>Órdenes de trabajo</span>
                    <h2>{metricas["ordenes"]}</h2>
                </div>
                <div class="metric">
                    <span>Clientes</span>
                    <h2>{metricas["clientes"]}</h2>
                </div>
            </div>

            <section class="query-card">
                <h2>Consulta en lenguaje natural</h2>
                <p style="color:#94a3b8;">Escribe una pregunta sobre ventas, clientes, vehículos, sucursales, productos u órdenes de trabajo.</p>

                <textarea id="pregunta" placeholder="Ejemplo: ¿Cuál fue la sucursal con más ventas en 2026?"></textarea>

                <div class="quick-buttons">
                    <button onclick="preguntaRapida('¿Cuál es el total vendido?')">Total vendido</button>
                    <button onclick="preguntaRapida('Muéstrame las 10 ventas más recientes')">Ventas recientes</button>
                    <button onclick="preguntaRapida('¿Cuál fue la sucursal con más ventas en 2026?')">Top sucursal</button>
                    <button onclick="preguntaRapida('¿Cuál fue el producto más utilizado?')">Top producto</button>
                    <button onclick="preguntaRapida('¿Cuál fue la marca de vehículo más atendida?')">Top marca</button>
                </div>

                <button onclick="consultar()">Consultar</button>
                <button class="btn-secondary" onclick="limpiarTodo()">Limpiar</button>

                <div class="loader" id="loader">
                    <span class="spinner"></span>
                    DonaldGPT está generando SQL, ejecutando la consulta e interpretando el resultado...
                </div>

                <div class="status" id="estado"></div>
            </section>

            <section class="results-grid">
                <div class="panel">
                    <h3>SQL generado</h3>
                    <pre id="sql">Aquí aparecerá el SQL generado...</pre>

                    <h3>Resultado</h3>
                    <div id="resultado">Aquí aparecerán los resultados...</div>
                </div>

                <div>
                    <div class="panel">
                        <h3>Gráfica automática</h3>
                        <div class="chart-box">
                            <canvas id="grafica"></canvas>
                        </div>

                        <h3>Análisis del resultado</h3>
                        <div class="analysis-box" id="analisis">
                            Aquí aparecerá la interpretación de DonaldGPT...
                        </div>
                    </div>

                    <div class="history">
                        <h3>Consultas recientes</h3>
                        <div id="historial">Todavía no hay consultas recientes.</div>
                    </div>
                </div>
            </section>

            <div class="footer">
                DonaldGPT © 2026 · Proyecto Final Base de Datos II · IA local + SQL Server
            </div>
        </main>
    </div>

    <script>
        function preguntaRapida(texto) {{
            document.getElementById("pregunta").value = texto;
            consultar();
        }}

        function limpiarTodo() {{
            document.getElementById("pregunta").value = "";
            document.getElementById("sql").textContent = "Aquí aparecerá el SQL generado...";
            document.getElementById("resultado").innerHTML = "Aquí aparecerán los resultados...";
            document.getElementById("analisis").innerHTML = "Aquí aparecerá la interpretación de DonaldGPT...";
            document.getElementById("estado").textContent = "";

            if (window.miGrafica) {{
                window.miGrafica.destroy();
            }}
        }}

        function guardarHistorial(pregunta) {{
            let historial = JSON.parse(localStorage.getItem("donaldgpt_historial") || "[]");

            historial = historial.filter(item => item !== pregunta);
            historial.unshift(pregunta);
            historial = historial.slice(0, 6);

            localStorage.setItem("donaldgpt_historial", JSON.stringify(historial));
            pintarHistorial();
        }}

        function pintarHistorial() {{
            const contenedor = document.getElementById("historial");
            let historial = JSON.parse(localStorage.getItem("donaldgpt_historial") || "[]");

            if (historial.length === 0) {{
                contenedor.innerHTML = "Todavía no hay consultas recientes.";
                return;
            }}

            let html = "";

            historial.forEach(item => {{
                html += `<span class="history-item" onclick="preguntaRapida('${{item.replace(/'/g, "\\\\'")}}')">${{item}}</span>`;
            }});

            contenedor.innerHTML = html;
        }}

        function generarGrafica(data) {{
            try {{
                if (!data.resultados || data.resultados.length === 0) {{
                    return;
                }}

                const columnas = Object.keys(data.resultados[0]);

                const columnasNumericasPrioridad = [
                    "TotalClientes",
                    "TotalVehiculos",
                    "TotalOrdenes",
                    "TotalGastado",
                    "TotalVendido",
                    "UnidadesUtilizadas",
                    "Valor",
                    "ValorTotal"
                ];

                let columnaValor = columnasNumericasPrioridad.find(col => columnas.includes(col));

                if (!columnaValor) {{
                    columnaValor = columnas.find(col =>
                        data.resultados.every(row => !isNaN(Number(row[col])))
                    );
                }}

                if (!columnaValor) {{
                    return;
                }}

                const columnasTextoPrioridad = [
                    "Departamento",
                    "Marca",
                    "Producto",
                    "Placa",
                    "Linea",
                    "NombreSucursal",
                    "TipoPago",
                    "Diagnostico",
                    "PrimerNombre"
                ];

                let columnaLabel = columnasTextoPrioridad.find(col =>
                    columnas.includes(col) && col !== columnaValor
                );

                if (!columnaLabel) {{
                    columnaLabel = columnas.find(col => col !== columnaValor);
                }}

                if (!columnaLabel) {{
                    return;
                }}

                const datos = data.resultados.slice(0, 15);
                const labels = datos.map(row => row[columnaLabel]);
                const valores = datos.map(row => Number(row[columnaValor]));

                if (!valores.every(v => !isNaN(v))) {{
                    return;
                }}

                const ctx = document.getElementById("grafica");

                if (window.miGrafica) {{
                    window.miGrafica.destroy();
                }}

                window.miGrafica = new Chart(ctx, {{
                    type: "bar",
                    data: {{
                        labels: labels,
                        datasets: [{{
                            label: columnaValor,
                            data: valores
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        plugins: {{
                            legend: {{
                                display: true
                            }},
                            title: {{
                                display: true,
                                text: "Gráfica automática del resultado"
                            }}
                        }},
                        scales: {{
                            y: {{
                                beginAtZero: true
                            }}
                        }}
                    }}
                }});
            }} catch (e) {{
                console.log("No se pudo generar gráfica", e);
            }}
        }}

        async function consultar() {{
            const pregunta = document.getElementById("pregunta").value;
            const sqlBox = document.getElementById("sql");
            const resultado = document.getElementById("resultado");
            const estado = document.getElementById("estado");
            const analisis = document.getElementById("analisis");
            const loader = document.getElementById("loader");

            if (!pregunta.trim()) {{
                estado.textContent = "Escribe una pregunta primero.";
                return;
            }}

            loader.style.display = "block";
            sqlBox.textContent = "Generando SQL...";
            resultado.innerHTML = "Esperando resultados...";
            analisis.innerHTML = "Generando interpretación...";
            estado.textContent = "Procesando consulta con IA local...";

            if (window.miGrafica) {{
                window.miGrafica.destroy();
            }}

            try {{
                const response = await fetch("/api/consultar", {{
                    method: "POST",
                    headers: {{
                        "Content-Type": "application/json"
                    }},
                    body: JSON.stringify({{ pregunta }})
                }});

                const data = await response.json();

                loader.style.display = "none";

                if (data.ok === false) {{
                    estado.textContent = "La consulta no pudo ejecutarse.";
                    sqlBox.textContent = data.sql || "Error";
                    resultado.innerHTML = "<b>Error:</b> " + data.detail;
                    analisis.innerHTML = data.analisis || "No se pudo generar análisis.";
                    return;
                }}

                guardarHistorial(pregunta);

                estado.textContent = "Consulta ejecutada correctamente. Filas devueltas: " + data.total_filas;
                sqlBox.textContent = data.sql;
                analisis.innerHTML = data.analisis || "No se generó interpretación.";

                if (data.resultados.length === 0) {{
                    resultado.innerHTML = "Sin resultados.";
                    return;
                }}

                let html = "<div class='table-wrapper'><table><thead><tr>";

                Object.keys(data.resultados[0]).forEach(col => {{
                    html += `<th>${{col}}</th>`;
                }});

                html += "</tr></thead><tbody>";

                data.resultados.forEach(row => {{
                    html += "<tr>";

                    Object.values(row).forEach(value => {{
                        html += `<td>${{value}}</td>`;
                    }});

                    html += "</tr>";
                }});

                html += "</tbody></table></div>";

                resultado.innerHTML = html;
                generarGrafica(data);

            }} catch (error) {{
                loader.style.display = "none";
                estado.textContent = "Error inesperado.";
                sqlBox.textContent = "Error";
                resultado.innerHTML = "<b>Error:</b> " + error;
                analisis.innerHTML = "No se pudo generar análisis.";
            }}
        }}

        document.addEventListener("DOMContentLoaded", function () {{
            pintarHistorial();

            const textarea = document.getElementById("pregunta");

            textarea.addEventListener("keydown", function(event) {{
                if (event.key === "Enter" && event.ctrlKey) {{
                    event.preventDefault();
                    consultar();
                }}
            }});
        }});
    </script>
</body>
</html>
    """


@app.post("/api/consultar")
def consultar(request: ConsultaRequest):
    try:
        pregunta_limpia = request.pregunta.strip().lower()

        saludos_o_texto_no_consulta = [
            "hola",
            "buenos dias",
            "buenos días",
            "buenas tardes",
            "buenas noches",
            "hey",
            "que tal",
            "qué tal",
            "como estas",
            "cómo estás",
            "gracias",
            "ok"
        ]

        if pregunta_limpia in saludos_o_texto_no_consulta:
            return {
                "ok": False,
                "sql": "No se generó SQL.",
                "detail": "Escribe una pregunta relacionada con la base de datos DonaldV2.",
                "resultados": [],
                "analisis": "DonaldGPT está listo para responder consultas sobre ventas, clientes, vehículos, sucursales, productos y órdenes de trabajo."
            }

        if pregunta_es_peligrosa(request.pregunta):
            return {
                "ok": False,
                "sql": "No se generó SQL.",
                "detail": "La pregunta fue bloqueada porque intenta realizar una acción no permitida.",
                "resultados": [],
                "analisis": "DonaldGPT solo permite consultas de lectura tipo SELECT para proteger la base de datos."
            }

        sql = generar_sql(request.pregunta)

        if sql.strip().upper() == "NO_SQL":
            return {
                "ok": False,
                "sql": "No se generó SQL.",
                "detail": "No entendí una consulta válida relacionada con DonaldV2.",
                "resultados": [],
                "analisis": "Puedes preguntar sobre ventas, documentos fiscales, clientes, vehículos, sucursales, productos, marcas u órdenes de trabajo."
            }

        if not consulta_es_segura(sql):
            return {
                "ok": False,
                "sql": sql,
                "detail": "Consulta bloqueada por seguridad.",
                "resultados": [],
                "analisis": "La consulta fue bloqueada porque no cumple las reglas de solo lectura."
            }

        df = ejecutar_consulta(sql)
        resultados = df.fillna("").to_dict(orient="records")

        analisis = interpretar_resultado(
            request.pregunta,
            sql,
            resultados
        )

        return {
            "ok": True,
            "pregunta": request.pregunta,
            "sql": sql,
            "total_filas": len(resultados),
            "resultados": resultados,
            "analisis": analisis
        }

    except Exception as e:
        return {
            "ok": False,
            "sql": "Error",
            "detail": str(e),
            "resultados": [],
            "analisis": "No se pudo interpretar el resultado debido a un error."
        }