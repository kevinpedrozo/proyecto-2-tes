from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os

app = Flask(__name__)

# ==========================
# CONEXIÓN A MONGODB
# ==========================

MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise Exception("No se encontró la variable MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["prueba"]
coleccion_usuarios = db["testing"]

# ==========================
# HOME
# ==========================

@app.route("/")
def index():

    total = coleccion_usuarios.count_documents({})

    fecha = datetime.now().strftime("%d/%m/%Y")

    return render_template(
        "index.html",
        total=total,
        fecha=fecha
    )

# ==========================
# REGISTRAR
# ==========================

@app.route("/registrar", methods=["POST"])
def registrar():

    nombre = request.form.get("nombre")
    correo = request.form.get("correo")
    telefono = request.form.get("telefono")
    ciudad = request.form.get("ciudad")

    existe = coleccion_usuarios.find_one({
        "correo": correo
    })

    if existe:
        return """
        <h2 style='text-align:center;color:red'>
        Este correo ya está registrado
        </h2>
        <center>
        <a href='/'>Volver</a>
        </center>
        """

    coleccion_usuarios.insert_one({
        "nombre": nombre,
        "correo": correo,
        "telefono": telefono,
        "ciudad": ciudad,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    return redirect("/usuarios")

# ==========================
# USUARIOS
# ==========================

@app.route("/usuarios")
def usuarios():

    lista_usuarios = list(
        coleccion_usuarios.find()
    )

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios,
        total=len(lista_usuarios)
    )

# ==========================
# BUSCAR
# ==========================

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
        usuarios=resultados,
        total=len(resultados)
    )

# ==========================
# ELIMINAR
# ==========================

@app.route("/eliminar/<id>")
def eliminar(id):

    coleccion_usuarios.delete_one({
        "_id": ObjectId(id)
    })

    return redirect("/usuarios")

# ==========================
# ACERCA
# ==========================

@app.route("/acerca")
def acerca():

    total = coleccion_usuarios.count_documents({})

    return render_template(
        "acerca.html",
        total=total
    )

# ==========================
# TABLA VISUAL
# ==========================

@app.route("/tabla")
def tabla():

    usuarios = list(
        coleccion_usuarios.find()
    )

    return render_template(
        "tabla.html",
        usuarios=usuarios
    )

# ==========================
# API USUARIOS
# REDIRIGE A TABLA
# ==========================

@app.route("/api/usuarios")
def api_usuarios():

    return redirect("/tabla")

# ==========================
# MAIN
# ==========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
