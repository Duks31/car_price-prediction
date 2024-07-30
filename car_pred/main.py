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

# Sample Request
# {
#     "make": "Mercedes-Benz",
#     "model": "M Class",
#     "year_of_manufacture": 2018,
#     "color": "White",
#     "condition": "Nigerian Used",
#     "mileage": 69224.0,
#     "engine_size": 800009.0,    
#     "registered_city": "LAGOS",
#     "selling_condition": "Registered",
#     "bought_condition": "Imported",
#     "city": "Lekki",
#     "body_type": "SUV",
#     "fuel_type": "Petrol",
#     "transmission": "Automatic"
# }