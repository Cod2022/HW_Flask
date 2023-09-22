# Необходимо создать базу данных для интернет-магазина. База данных должна
# состоять из трех таблиц: товары, заказы и пользователи. Таблица товары должна
# содержать информацию о доступных товарах, их описаниях и ценах. Таблица
# пользователи должна содержать информацию о зарегистрированных
# пользователях магазина. Таблица заказы должна содержать информацию о
# заказах, сделанных пользователями.
# ○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
# имя, фамилия, адрес электронной почты и пароль.
# ○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
# название, описание и цена.
# ○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
# пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
# заказа.

# Создайте модели pydantic для получения новых данных и
# возврата существующих в БД для каждой из трёх таблиц
# (итого шесть моделей).
# Реализуйте CRUD операции для каждой из таблиц через
# создание маршрутов, REST API (итого 15 маршрутов).
# ○ Чтение всех
# ○ Чтение одного
# ○ Запись
# ○ Изменение
# ○ Удаление

import databases 
import sqlalchemy
from fastapi import FastAPI 
from pydantic import BaseModel, Field
from typing import List

DATABASE_URL = "sqlite:///mydatabase.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table( 
    "users", 
    metadata, 
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True), 
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(32)), 
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(12)),
    )

products = sqlalchemy.Table( 
    "products", 
    metadata, 
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True), 
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("description", sqlalchemy.String(256)),
    sqlalchemy.Column("price", sqlalchemy.Float()), 
    )

engine = sqlalchemy.create_engine( 
    DATABASE_URL, connect_args={"check_same_thread": False}
    ) 
metadata.create_all(engine)

app = FastAPI()

class UserIn(BaseModel):
    name: str = Field(max_length=32) 
    email: str = Field(max_length=128)

class User(BaseModel):
    id: int 
    name: str = Field(max_length=32) 
    email: str = Field(max_length=128)

class ProductIn(BaseModel):
    name: str = Field(max_length=32)
    description: str = Field(max_length=128)
    price: float = Field()

class Product(BaseModel):
    id : int
    name: str = Field(max_length=32)
    description: str = Field(max_length=128)
    price: float = Field()



# @app.get("/fake_users/{count}") 
# async def create_note(count: int): 
#     for i in range(count): 
#         query = users.insert().values(name=f'user{i}', surname=f'surname{i}', email=f'mail{i}@mail.ru', password=f'password{i}') 
#         await database.execute(query) 
#     return {'message': f'{count} fake users created'}

# @app.get("/fake_products/{count}") 
# async def create_note(count: int): 
#     for i in range(count): 
#         query = products.insert().values(name=f'product{i}', description=f'description{i}', price= i * 2) 
#         await database.execute(query) 
#     return {'message': f'{count} fake products created'}


@app.post("/users/", response_model=User) 
async def create_user(user: UserIn): 
    query = users.insert().values(name=user.name, email=user.email)
    last_record_id = await database.execute(query) 
    return {**user.dict(), "id": last_record_id}


@app.get("/users/", response_model=List[User]) 
async def read_users(): 
    query = users.select() 
    return await database.fetch_all(query)

@app.get("/users/{user_id}",response_model=User)
async def read_user(user_id:int): 
    query=users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User) 
async def update_user(user_id: int, new_user: UserIn): 
    query = users.update().where(users.c.id == user_id).values(**new_user.dict()) 
    await database.execute(query) 
    return {**new_user.dict(), "id": user_id}

@app.delete("/users/{user_id}") 
async def delete_user(user_id: int): 
    query = users.delete().where(users.c.id == user_id) 
    await database.execute(query) 
    return {'message': 'User deleted'}

@app.post("/products/", response_model=Product) 
async def create_product(product: ProductIn): 
    query = products.insert().values(name=product.name, description=product.description, price=product.price)
    last_record_id = await database.execute(query) 
    return {**product.dict(), "id": last_record_id}

@app.get("/products/", response_model=List[Product]) 
async def read_products(): 
    query = products.select() 
    return await database.fetch_all(query)

@app.get("/products/{product_id}",response_model=Product)
async def read_product(product_id:int): 
    query=products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)

@app.put("/products/{product_id}", response_model=Product) 
async def update_product(product_id: int, new_product: ProductIn): 
    query = products.update().where(products.c.id == product_id).values(**new_product.dict()) 
    await database.execute(query) 
    return {**new_product.dict(), "id": product_id}

@app.delete("/products/{product_id}") 
async def delete_product(product_id: int): 
    query = products.delete().where(products.c.id == product_id) 
    await database.execute(query) 
    return {'message': 'Product deleted'}