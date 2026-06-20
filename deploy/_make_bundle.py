"""Empaqueta la app en un zip dentro del workdir del MCP para subir a S3."""
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKDIR = r"C:\Users\angie\AppData\Local\Temp\aws-api-mcp\workdir"
OUT = os.path.join(WORKDIR, "taller_app.zip")

INCLUDE_DIRS = ["Controlador", "Modelo", "Vista", "static"]
INCLUDE_FILES = ["main.py", "wsgi.py", "requirements.txt"]
EXCLUDE_PARTS = {"__pycache__", ".git"}


def add_file(zf, abspath, arcname):
    zf.write(abspath, arcname)


with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in INCLUDE_FILES:
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            add_file(zf, p, f)
    for d in INCLUDE_DIRS:
        base = os.path.join(ROOT, d)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [x for x in dirnames if x not in EXCLUDE_PARTS]
            for fn in filenames:
                if fn.endswith(".pyc"):
                    continue
                abspath = os.path.join(dirpath, fn)
                arcname = os.path.relpath(abspath, ROOT).replace("\\", "/")
                add_file(zf, abspath, arcname)

# copia del dump SQL al workdir tambien
import shutil
shutil.copy(os.path.join(ROOT, "deploy", "taller_el_costa.sql"),
            os.path.join(WORKDIR, "taller_el_costa.sql"))

size = os.path.getsize(OUT)
print("Zip creado:", OUT, "(%d KB)" % (size // 1024))
with zipfile.ZipFile(OUT) as zf:
    print("Archivos en el zip:", len(zf.namelist()))
    for n in zf.namelist():
        print("  ", n)
