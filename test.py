import psycopg2

try:
    conn = psycopg2.connect("postgresql://fred:johnfred@localhost/flask_app_db")
    print("Conexión exitosa a la base de datos")
    conn.close()
except Exception as e:
    print("Error al conectar a la base de datos:", e)