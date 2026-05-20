import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="basedatos_prueba"
)

print("Conectado")

cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiantes INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    apellido VARCHAR(20) NOT NULL,
    correo VARCHAR(50) NOT NULL,
    edad INT NOT NULL
)
""")

print("Tabla creada")
