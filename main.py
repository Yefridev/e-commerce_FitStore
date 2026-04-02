from fastapi import FastAPI

app = FastAPI()

@app.get("/products")
def get_products():
    return [
        {
            "id": 1,
            "name": "Camiseta Slim",
            "price": 75000,
            "color": "Negro",
            "talla": "L",
        },

        {
            "id": 2,
            "name": "Camiseta Oversize",
            "price": 90000,
            "color": "Gris",
            "talla": "M",
        }
    ]
