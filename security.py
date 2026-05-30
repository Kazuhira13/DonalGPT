import re


def pregunta_es_peligrosa(pregunta):
    pregunta = pregunta.lower()

    palabras_peligrosas = [
        "drop",
        "delete",
        "elimina",
        "eliminar",
        "borra",
        "borrar",
        "update",
        "actualiza",
        "actualizar",
        "insert",
        "inserta",
        "insertar",
        "truncate",
        "alter",
        "modifica",
        "modificar",
        "create",
        "crear tabla",
        "exec",
        "execute"
    ]

    return any(palabra in pregunta for palabra in palabras_peligrosas)


def consulta_es_segura(sql):
    if not sql or not sql.strip():
        return False

    if sql.strip().upper() == "NO_SQL":
        return False

    sql_limpio = sql.strip().lower()

    if not sql_limpio.startswith("select"):
        return False

    palabras_bloqueadas = [
        "drop", "delete", "update", "insert", "alter",
        "truncate", "exec", "execute", "merge", "create",
        "grant", "revoke", "backup", "restore", "shutdown",
        "xp_", "sp_", "dbcc"
    ]

    for palabra in palabras_bloqueadas:
        patron = r"\b" + re.escape(palabra) + r"\b"
        if re.search(patron, sql_limpio):
            return False

    simbolos_peligrosos = [
        "--",
        "/*",
        "*/"
    ]

    for simbolo in simbolos_peligrosos:
        if simbolo in sql_limpio:
            return False

    if sql_limpio.count(";") > 1:
        return False

    return True