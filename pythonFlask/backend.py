# backend.py

from flask import Flask, jsonify

app = Flask(__name__)

# Модель товара
class Product:
    def __init__(self, id, name, price, description):
        self.id = id
        self.name = name
        self.price = price
        self.description = description

# Пример данных о товарах (можно заменить на данные из базы данных)
products_data = [
    {"id": 1, "name": "Product 1", "price": 10.99, "description": "Description for Product 1"},
    {"id": 2, "name": "Product 2", "price": 19.99, "description": "Description for Product 2"},
    {"id": 3, "name": "Product 3", "price": 29.99, "description": "Description for Product 3"}
]

# Преобразование данных о товарах в объекты Product
products = [Product(**data) for data in products_data]

# Маршрут для получения списка товаров
@app.route('/api/products')
def get_products():
    return jsonify([product.__dict__ for product in products])

# Добавляем маршрут для корневого URL
@app.route('/')
def index():
    return 'Welcome to the online store!'

if __name__ == '__main__':
    app.run(debug=True)
