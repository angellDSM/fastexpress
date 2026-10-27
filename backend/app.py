"""API REST de FastExpress.

GET  /             -> interfaz web (frontend/index.html)
POST /api/cotizar  -> calcula la tarifa
"""
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from backend.tarifa import EnvioInvalido, calcular_tarifa

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = Flask(__name__)


@app.get("/")
def inicio():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.post("/api/cotizar")
def cotizar():
    datos = request.get_json(silent=True) or {}
    try:
        peso = float(datos.get("peso"))
    except (TypeError, ValueError):
        return jsonify({"error": "El peso debe ser numérico"}), 400
    try:
        resultado = calcular_tarifa(peso, datos.get("tipo_cliente"), datos.get("tipo_envio"))
    except EnvioInvalido as e:
        return jsonify({"error": str(e)}), 422
    return jsonify(resultado), 200


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True)
