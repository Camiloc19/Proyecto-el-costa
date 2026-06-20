"""Exporta taller_el_costa (esquema + datos) a un archivo .sql para desplegar en AWS."""
import mysql.connector

con = mysql.connector.connect(host="localhost", user="root", password="", database="taller_el_costa")
cur = con.cursor()
cur.execute("SHOW TABLES")
tablas = [t[0] for t in cur.fetchall()]

out = []
out.append("-- Dump de taller_el_costa generado para despliegue AWS")
out.append("SET FOREIGN_KEY_CHECKS=0;")
out.append("SET NAMES utf8mb4;")
out.append("")


def esc(v):
    if v is None:
        return "NULL"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v).replace("\\", "\\\\").replace("'", "''")
    return "'" + s + "'"


for t in tablas:
    cur.execute("SHOW CREATE TABLE `%s`" % t)
    create = cur.fetchone()[1]
    out.append("DROP TABLE IF EXISTS `%s`;" % t)
    out.append(create + ";")
    out.append("")
    cur.execute("SELECT * FROM `%s`" % t)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    if rows:
        collist = ", ".join("`%s`" % c for c in cols)
        for r in rows:
            vals = ", ".join(esc(v) for v in r)
            out.append("INSERT INTO `%s` (%s) VALUES (%s);" % (t, collist, vals))
        out.append("")

out.append("SET FOREIGN_KEY_CHECKS=1;")
con.close()

with open("deploy/taller_el_costa.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Dump escrito: deploy/taller_el_costa.sql")
print("Tablas exportadas:", len(tablas))
