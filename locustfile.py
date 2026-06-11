from locust import HttpUser, task, between
import random
import time


class SistemaUsuarios(HttpUser):

    wait_time = between(1, 3)

    @task(3)
    def home_page(self):

        self.client.get("/")

    @task(2)
    def consulta_usuarios(self):

        self.client.get("/usuarios")

    @task(1)
    def registrar_usuario(self):

        timestamp = int(time.time() * 1000)

        nombre = f"Usuario{random.randint(1,9999)}"

        correo = f"usuario{timestamp}@correo.com"

        telefono = str(
            random.randint(
                3000000000,
                3999999999
            )
        )

        ciudad = random.choice([
            "Bogotá",
            "Medellín",
            "Cali",
            "Barranquilla",
            "Cartagena"
        ])

        self.client.post(
            "/registrar",
            data={
                "nombre": nombre,
                "correo": correo,
                "telefono": telefono,
                "ciudad": ciudad
            }
        )
