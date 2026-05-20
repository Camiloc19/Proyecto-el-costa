import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="taller_el_costa"
)

print("Conectado")

cursor = conexion.cursor()
cursor.execute("select * from vehiculos")

for fila in cursor:
    print(fila)
