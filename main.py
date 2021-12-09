# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Body, Query, Path

# Inicializamos la variable con una instancia de fastAPI, de esta manera se crea un objeto de la clase fastAPI y se asigna
# la variable app

app = FastAPI()

# Crear los modelos

class Location(BaseModel):

    city: str
    state: str
    country: str

class Person(BaseModel):

    first_name : str
    last_name : str
    age: int

    # Los siguientes son valores opcionales
    hair_color : Optional[str] = None
    is_married: Optional[bool] = None

# Path operation decorator, este decorador utiliza el metodo .get() para modificar la funcion home, que será el lugar al cual 
# ingresaran los usuarios de nuesta app y retorna un archivo JSON

@app.get('/')
def home():
    return {'Hello':'World'}

# Request and response body

@app.post('/person/new')
# Request Body, debido a la notación (...) indica que el parametro o el atributo son obligatorios
def create_person(person: Person = Body(...)): 
    return person

# Validation query parameters

@app.get("/person/detail")

    # Funcion para mostrar persona en el endpoint, por default el nombre sera nulo o "None", y sus carateristicas son
    # de tipo string con un mínimo de un caracter y un maximo de 50. Si bien lo ideal es que un query parameter sea opcional
    # existen casos en los que puede ser obligatorio

def show_person(
    name: Optional[str] = Query(

        None,
        min_length=1,
        max_length=50,
        title= 'Person Name',
        description='This is the person name. It\'s between 1 and 50 characters',

        ),

    age : int = Query(
        ...,
        title='Person age',
        description='This is the person age. It\'s requiered'
        )
    ):
    return {name: age}


# Validaciones: Path Parameters

@app.get('/person/detail/{person_id}')

# En este caso marcamos como obligatorio el parametro person_id, y con la propiedad pt o "Greater than" garantizamos que
# no admita un id igual o menor que cero

def show_person(
    person_id: int = Path(
        ...,
        title='Person id',
        gt=0,
        description='This is the person id, It\'s required'
        )
):
    return {person_id: 'It exists!'} 


# Validaciones Request Body

@app.put('/person/{person_id}')

# Cada vez que un usuario haga una peticion de tipo .put() en este endpoint en particular con un usuario
# y un id especifico podrá actualizar el contenido a traves de un request body

def update_person(
    person_id:int = Path(
        ...,
        title='Person ID',
        description='This is the person ID',
        gt= 0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):

    # Generamos un único diccionario para retornar los archivos JSON con el resultado de los 2 request body "person & location"   
    
    results = person.dict()
    results.update(location.dict())

    # Si bien los diccionarios en python se pueden combinar de con una sintaxis mas sencilla como:
    # "person.dict() & location.dict()" FastAPI no soporta un este tipo de declaraciones, por lo tanto debe ser de la manera 
    # más clasica 
    
    return results
