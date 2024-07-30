''' 
API for Car Price Prediction

This API is built using FastAPI and uvicorn. The API accepts a POST request with the following parameters:

- make: The make of the car
- model: The model of the car
- year_of_manufacture: The year the car was manufactured
- color: The color of the car
- condition: The condition of the car (Nigerian Used, Foreign Used, etc.)
- mileage: The mileage of the car
- engine_size: The engine size of the car
- registered_city: The city where the car is registered
- selling_condition: The condition of the car when it is being sold
- bought_condition: The condition of the car when it was bought
- city: The city where the car is located
- body_type: The body type of the car
- fuel_type: The fuel type of the car
- transmission: The transmission type of the car

this is a sample request to the API:
{
    "make": "Mercedes-Benz",
    "model": "M Class",
    "year_of_manufacture": 2018,
    "color": "White",
    "condition": "Nigerian Used",
    "mileage": 69224.0,
    "engine_size": 800009.0,    
    "registered_city": "LAGOS",
    "selling_condition": "Registered",
    "bought_condition": "Imported",
    "city": "Lekki",
    "body_type": "SUV",
    "fuel_type": "Petrol",
    "transmission": "Automatic"
}
'''

import uvicorn
from fastapi import FastAPI
from model import CarPrices, CarPriceModel

app = FastAPI()
model = CarPriceModel() 

@app.get("/")
def home():
    return { 'Message' : 'Welcome to the Car Price Prediction API' }

@app.post("/predict")
async def predict_price(car: CarPrices):
    data = car.model_dump()
    prediction = model.predict(data)

    return {"price": prediction}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port = 8000)