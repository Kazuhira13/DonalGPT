import pyodbc
import pandas as pd


def get_connection():
    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=192.168.1.103;"
        "DATABASE=DonaldV2;"
        "UID=DonaldGPTUser;"
        "PWD=DonaldGPT12345.;"
        "TrustServerCertificate=yes;"
        "Encrypt=no;"
    )

    return pyodbc.connect(connection_string)


def ejecutar_consulta(sql):
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df