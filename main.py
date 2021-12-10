# Python
from typing import Optional
# La clase Enum nos permite generar enumeraciones de strings en este caso necesarias para generar las validaciones
# del atributo hair_color
from enum import Enum

# Pydantic
# Importamos Field de la libreria pydantic para generar validaciones directamente en la clase de los modelos
from pydantic import BaseModel, Field, HttpUrl, EmailStr, PaymentCardNumber

# FastAPI
# Importar las clases y metodos
from fastapi import FastAPI,  status , UploadFile, HTTPException
# Importar el tipo de datos soportados
from fastapi import Body, Query, Path, Form, Header, Cookie, File

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

class PersonBase(BaseModel):
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


class Person(PersonBase):
    # Utilizando la herencia de la programación orientada a objetos podemos eliminar el código duplicado
    # en este caso en particular se crean dos clases adicionales, en la primera heredamos todo de 'PersonBase'
    # y en la clase person obtenemos la contraseña 
    password: str = Field(
        ..., 
        min_length=8,
        example= 'HolaSoyNico')


class PersonOut(PersonBase):
    # Como esta es la clase de respuesta, no necesitamos ingresar nada, como buena practica generamos un pass
    pass    

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length= 20,
        example = 'Nicolasimplant'
    )

# Path operation decorator, este decorador utiliza el metodo .get() para modificar la funcion home, que será el lugar al cual 
# ingresaran los usuarios de nuesta app y retorna un archivo JSON

# Para usar la clase status necesitamos ingresarlo como parametro en el decorador, se espera la respuesta 200
@app.get(
    path= '/', 
    status_code=status.HTTP_200_OK,
    tags=['Home'])
def home():
    '''
    Home

    This path operator make a initial message Hello World

    - Parameters:
        - **Nothing**
    
    Return a dictionary or JSON objetc

    '''
    
    return {'Hello':'World'}

# Request and response body


# La manera adecuada de manejar las contraseñas en nuestro codigo es utilizando el atributo
# response model al interior de nuestro decorador, este atributo hace que en la respuesta se envíen todos los datos
# con excepcion de la contraseña
# Con el decorador status se espera tener la respuesta 201 dado que estamos creando un usuario

@app.post(
    path='/person/new', 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=['Persons'],
    summary='Create person in the app')

# Request Body, debido a la notación (...) indica que el parametro o el atributo son obligatorios
def create_person(person: Person = Body(...)):
    '''
    Create Person

    This path operation creates a person in the app an save the information in the database

    Parameters:
    - Request Body Parameter
        - **person: Person** : A person model with first name, last name, age, hair color and marital status
    
    Returns a person model with first name, last name, age, hair color and marital status   
    ''' 
    return person

# Validation query parameters
# Nuevamente se espera encontar una respuesta 200 unicamente

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary= 'show person user in app')

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

    '''
    Show Person

    Show a person on the endpoint with a query

    - Parameters:
        - **Name** : This parameter is optional and the default value is None or null
        - **Age**  : Is not optional, and it will be a integer number 

    Return a dictionary or JSON object with key name and value age 
    
    '''
    return {name: age}


# Validaciones: Path Parameters

# Creamos una lista con los supuestos ususarios registrados
persons = [1,2,3,4,5]

@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_302_FOUND,
    tags=['Persons'],
    summary= 'Find person from id in the app')

# En este caso marcamos como obligatorio el parametro person_id, y con la propiedad gt o "Greater than" garantizamos que
# no admita un id igual o menor que cero

def show_person(
    person_id: int = Path(
        ...,
        title='Person id',
        gt=0,
        description='This is the person id, It\'s required',
        example=123
        )
):  # Si el person id no se encuentra en la lista generada, se levantará una excepcion

    '''
    Show person

    Show person finded for his user id, in case of user id is not in list of users raise an execption

    - Parameters :
        - **person_id** : It will be a integer number and is necesary for search user
    
    Return a dict or JSON object with a message exist

    '''
    if person_id not in persons:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= 'This person doesn\'t exist'
        )
    return {person_id: 'It exists!'} 


# Validaciones Request Body

@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_302_FOUND,
    tags=['Persons'],
    summary= 'Update person location')

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

    '''
    Update Person

    This path update person location with the infomation from inputs user

    - Parameters :
        - **Person_id** : Similar of show person this path requires user id to search and update information
    
    Return a dict or JSON object nested class person and class location
    '''



    # Generamos un único diccionario para retornar los archivos JSON con el resultado de los 2 request body "person & location"   
    
    results = person.dict()
    results.update(location.dict())

    # Si bien los diccionarios en python se pueden combinar de con una sintaxis mas sencilla como:
    # "person.dict() & location.dict()" FastAPI no soporta un este tipo de declaraciones, por lo tanto debe ser de la manera 
    # más clasica 
    
    return results

# FORMS

# Nueva path operation function que tendrá por defecto el endpoint /login para implementar los formularios en python
# se debe instalar previamente la librería python-multiparts

@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary= 'User Login'
)
def login(
    username:str = Form(...),
    password:str = Form(...)):

    '''
    Login

    This path is part of a endpoint login / logout and needs a form to work

    - Parameters:
        - **Username** : User nickname from his acount
        - **password** : User password from his acount
    
    Return the class LoginOut with acount username

    '''
    
    # Dado que el unico formato de salida permitido son los diccionarios, debemos instanciar la clase para 
    # garantizar el formato de respuesta
    return LoginOut(username = username)


# Cookies and headers parameters

# Creamos una nueva path operations

@app.post(
    path= '/contact',
    status_code=status.HTTP_200_OK,
    tags=['Contact'],
    summary= 'Contact with us'
)

# Funcion que recibe el formulario de contacto.
def contact(

    first_name:str = Form(
        ...,
        max_length=20,
        min_length=1,        
    ),

    last_name:str = Form(
    ...,
    max_length=20,
    min_length=1
    ),

    email :EmailStr = Form(...),

    message: str = Form(
        ...,
        min_length=20
    ),

    user_agent:Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    '''
    Contact

    This path make a form to user contact with the support system app 

    - Parameters :
        - **first_name** : From user acount
        - **last_name**  : From user acount
        - **Email**      : From user acount
        - **Message**    : Max 20 characters and describe your problem or suggest
    
    Return the header from user navigator 
    
    '''
    return user_agent


# Generamos el path operator para la subida de archivos
@app.post(
    path='/post-image',
    tags=['Images'],
    summary= ' Upload a file'
)

def post_image(
    image: UploadFile = File(...)
):
    '''
    Post Image

    This path is for a user maked file uploads

    - Parameters:
        - **Image** : File user wants upload to app

    Return a description of a propertys from file: name, format, and size
    
    '''
    return {
        # Atributos de la imagen cargada:
        'filename': image.filename,               # Nombre de la imagen
        'format'  : image.content_type,           # Formato de la imagen
        'size(kb)': round(len(image.file.read())/1024, ndigits=1)   # tamaño de la imagen, en este caso utilizamos las funciones nativas read()
                                                  #  para leer el archivo en formato bytecode y con len() obtenemos su tamaño  
    }