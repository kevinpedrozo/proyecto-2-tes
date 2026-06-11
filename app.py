from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise Exception("No se encontró la variable MONGO_URI")

client = MongoClient(MONGO_URI)

# TU BASE DE DATOS
db = client["prueba"]

# TU COLECCIÓN
coleccion_usuarios = db["testing"]


@app.route("/")
def index():

    total = coleccion_usuarios.count_documents({})

    return render_template(
        "index.html",
        total=total
    )


@app.route("/registrar", methods=["POST"])
def registrar():

    nombre = request.form.get("nombre")
    correo = request.form.get("correo")
    telefono = request.form.get("telefono")
    ciudad = request.form.get("ciudad")

    coleccion_usuarios.insert_one({
        "nombre": nombre,
        "correo": correo,
        "telefono": telefono,
        "ciudad": ciudad,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    return redirect("/usuarios")


@app.route("/usuarios")
def usuarios():

    lista_usuarios = list(
        coleccion_usuarios.find()
    )

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios
    )


@app.route("/buscar")
def buscar():

    nombre = request.args.get("nombre", "")

    resultados = list(
        coleccion_usuarios.find({
            "nombre": {
                "$regex": nombre,
                "$options": "i"
            }
        })
    )

    return render_template(
        "usuarios.html",
        usuarios=resultados
    )


@app.route("/eliminar/<id>")
def eliminar(id):

    coleccion_usuarios.delete_one({
        "_id": ObjectId(id)
    })

    return redirect("/usuarios")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
