from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import os

app = Flask(__name__)

# Obtener URI de MongoDB desde Render
MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise Exception("No se encontró la variable de entorno MONGO_URI")

# Conexión a MongoDB
client = MongoClient(MONGO_URI)

db = client["registro_db"]
coleccion_usuarios = db["usuarios"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registrar", methods=["POST"])
def registrar():

    nombre = request.form.get("nombre")
    correo = request.form.get("correo")

    if not nombre or not correo:
        return "Todos los campos son obligatorios"

    coleccion_usuarios.insert_one({
        "nombre": nombre,
        "correo": correo
    })

    return redirect("/usuarios")


@app.route("/usuarios")
def usuarios():

    lista_usuarios = list(
        coleccion_usuarios.find(
            {},
            {"_id": 0}
        )
    )

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)