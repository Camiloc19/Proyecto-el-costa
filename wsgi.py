"""Punto de entrada para gunicorn en producción: gunicorn wsgi:app"""
from Controlador.controlador import app

if __name__ == "__main__":
    app.run()
