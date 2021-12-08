from fastapi import FastAPI

# Inicializamos la variable con una instancia de fastAPI, de esta manera se crea un objeto de la clase fastAPI y se asigna
# la variable app
app = FastAPI()

# Path operation decorator, este decorador utiliza el metodo .get() para modificar la funcion home, que será el lugar al cual 
# ingresaran los usuarios de nuesta app y retorna un archivo JSON
@app.get('/')
def home():
    return {'Hello':'World'}