# Python
from typing import Optional
# La clase Enum nos permite generar enumeraciones de strings en este caso necesarias para generar las validaciones
# del atributo hair_color
from enum import Enum

# Pydantic
# Importamos Field de la libreria pydantic para generar validaciones directamente en la clase de los modelos
from pydantic import BaseModel, Field, HttpUrl, EmailStr, PaymentCardNumber

# FastAPI
from fastapi import FastAPI, Body, Query, Path

# Inicializamos la variable con una instancia de fastAPI, de esta manera se crea un objeto de la clase fastAPI y se asigna
# la variable app

app = FastAPI()

# Crear los modelos

# Heredando en la clase HairColor la clase Enum

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red  = "red"
    green = "green"
    blue  = "blue"


class Location(BaseModel):

    city: str = Field(
        default= None,
        min_length = 1,
        max_length = 50,
        example = 'Bogota'
    )
    state: str = Field(
        default= None,
        min_length = 1,
        max_length = 50,
        example = 'Cundinamarca'
    )
    country: str = Field(
        default= None,
        min_length = 1,
        max_length = 50,
        example = 'Colombia'
    )

class Person(BaseModel):

    # Parametrizamos la informacion que debe tener cada uno de los atributos de nuestra clase
    # Utilizamos example para ingresar datos para realizar pruebas

    first_name : str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = 'Nicolas'
        )

    last_name : str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = 'Implant'
        )

    age: int = Field(
        ...,
        gt= 0,
        le=115,
        example = 25
    )

    email: EmailStr = Field(
        ...,
        title= 'User email',
        description= 'Email from user',
        example = 'nicolas@implant.com'
    )

    # Los siguientes son valores opcionales
    hair_color : Optional[HairColor] = Field(default=None, example = HairColor.black)    
    is_married: Optional[bool] = Field(default=None, example = False)

    # Validando tipos de datos especiales
    # credict_card: Optional[PaymentCardNumber] = Field(
    #     default=None,
    #     title= 'Credict Card Number',
    #     description= 'use if you want to link a credit card for your account')

    website: Optional[HttpUrl] = Field(
        default= None,
        title= 'User Website',
        description= 'use if you want to link your website in your account',
        example = 'https://www.google.com/'
        )

    # Se declara una clase para realizar las prubeas sobre fastAPI generando un ejemplo de prueba, 
    # sin embargo es posible realizarlo de manera distinta directamente en los atributos de la clase

    # class Config:
    #     schema_extra = {
    #         'example': {
    #             'first_name' : 'Nicolas',
    #             'last_name'  : 'Implant',
    #             'age' : 30,
    #             'email': 'nicolas@implant.com',
    #             'hair_color' : 'brown',
    #             'is_married': False
    #         }
    #     }

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
        example= 'Isabella'

        ),

    age : int = Query(
        ...,
        title='Person age',
        description='This is the person age. It\'s requiered',
        example=10
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
        description='This is the person id, It\'s required',
        example=123
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
        gt= 0,
        example=123
    ),
    person: Person = Body(...),
    location : Location = Body(...)    
):

    # Generamos un único diccionario para retornar los archivos JSON con el resultado de los 2 request body "person & location"   
    
    results = person.dict()
    results.update(location.dict())

    # Si bien los diccionarios en python se pueden combinar de con una sintaxis mas sencilla como:
    # "person.dict() & location.dict()" FastAPI no soporta un este tipo de declaraciones, por lo tanto debe ser de la manera 
    # más clasica 
    
    return results
