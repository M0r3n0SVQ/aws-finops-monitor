"""Configuración compartida de pytest."""
import sys
import os

# Añade la raíz del proyecto al path para que los tests puedan importar monitor.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))