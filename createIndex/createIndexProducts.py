import sqlite3
import requests


class CreateIndexProductsts:
    url = 'http://localhost:9200/products'

    def __init__(self):
        self.create_connection()
        self.create_index()

    def create_connection(self):
        self.connection = sqlite3.connect("C:/Users/T/PycharmProjects/pythonProject/shop.db")
        self.cursor = self.connection.cursor()

    def create_index(self):
        #requests.delete("http://localhost:9200/products")
        #requests.put("http://localhost:9200/products")
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()
        self.put_elements_in_index(products)

    def put_elements_in_index(self, products):
        for product in products:
            self.put_element_in_index(product)

    def put_element_in_index(self, product):
        response = requests.post('http://localhost:9200/products/_doc',
                                 json={'url': product[0],
                                       'name': product[1],
                                       'category': product[2],
                                       'price': product[3],
                                       'count_players': product[4],
                                       'time': product[5],
                                       'age': product[6],
                                       'description': product[7],
                                       'year': product[8],
                                       'producer': product[9],
                                       }
                                 )
