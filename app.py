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

# Base de datos
db = client["prueba"]

# Colección
coleccion_usuarios = db["testing"]


# ==========================
# PÁGINA PRINCIPAL
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
# REGISTRAR USUARIO
# ==========================

@app.route("/registrar", methods=["POST"])
def registrar():

    nombre = request.form.get("nombre")
    correo = request.form.get("correo")
    telefono = request.form.get("telefono")
    ciudad = request.form.get("ciudad")

    # Verificar correo duplicado
    existe = coleccion_usuarios.find_one({
        "correo": correo
    })

    if existe:
        return """
        <h2 style='color:red;text-align:center;'>
        El correo ya se encuentra registrado
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
# LISTAR USUARIOS
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
# BUSCAR USUARIOS
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
# ELIMINAR USUARIO
# ==========================

@app.route("/eliminar/<id>")
def eliminar(id):

    coleccion_usuarios.delete_one({
        "_id": ObjectId(id)
    })

    return redirect("/usuarios")


# ==========================
# ACERCA DEL SISTEMA
# ==========================

@app.route("/acerca")
def acerca():

    total = coleccion_usuarios.count_documents({})

    return render_template(
        "acerca.html",
        total=total
    )


# ==========================
# API REST
# ==========================

@app.route("/api/usuarios")
def api_usuarios():

    usuarios = list(
        coleccion_usuarios.find(
            {},
            {"_id": 0}
        )
    )

    return {
        "total_usuarios": len(usuarios),
        "usuarios": usuarios
    }


# ==========================
# EJECUCIÓN
# ==========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
