from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

from decouple import config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host=config("host"),
    port=config("port"),
    password=config("password"),
    decode_responses=True)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

@app.get('/products')
def products():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.post('/products', status_code=status.HTTP_201_CREATED)
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)

@app.delete('/products/{pk}', status_code=status.HTTP_204_NO_CONTENT)
def delete(pk: str):
    return Product.delete(pk)