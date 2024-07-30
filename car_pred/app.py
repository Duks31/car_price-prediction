import pandas as pd
import gradio as gr
import warnings
from model import CarPriceModel, CarPrices

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

data = pd.read_csv("data/car_data.csv")

unique_values = {
    "make": list(data["make"].unique()),
    "model": list(data["model"].unique()),
    "color": list(data["color"].unique()),
    "condition": list(data["condition"].unique()),
    "registered_city": list(data["registered_city"].unique()),
    "selling_condition": list(data["selling_condition"].unique()),
    "bought_condition": list(data["bought_condition"].unique()),
    "city": list(data["city"].unique()),
    "body_type": list(data["body_type"].unique()),
    "fuel_type": list(data["fuel_type"].unique()),
    "transmission": list(data["transmission"].unique()),
}


def predict_car_price(
    make,
    model,
    year_of_manufacture,
    color,
    condition,
    mileage,
    engine_size,
    registered_city,
    selling_condition,
    bought_condition,
    city,
    body_type,
    fuel_type,
    transmission,
):
    car = CarPrices(
        make=make,
        model=model,
        year_of_manufacture=int(year_of_manufacture),
        color=color,
        condition=condition,
        mileage=float(mileage),
        engine_size=float(engine_size),
        registered_city=registered_city,
        selling_condition=selling_condition,
        bought_condition=bought_condition,
        city=city,
        body_type=body_type,
        fuel_type=fuel_type,
        transmission=transmission,
    )

    car_model = CarPriceModel()

    prediction = car_model.predict(car.model_dump())
    formatted_prediction = f"₦{prediction:,.2f}"
    return formatted_prediction


with gr.Blocks() as interface:
    gr.Markdown(
        "# Car Price Prediction\nPredict the price of a car based on its features."
    )

    with gr.Tab("Basic Information"):
        make = gr.Dropdown(label="Make", choices=unique_values["make"])
        model = gr.Dropdown(label="Model", choices=unique_values["model"])
        year_of_manufacture = gr.Number(label="Year of Manufacture")
        color = gr.Dropdown(label="Color", choices=unique_values["color"])
        condition = gr.Dropdown(label="Condition", choices=unique_values["condition"])

    with gr.Tab("Sepcifications"):
        mileage = gr.Number(label="Mileage")
        engine_size = gr.Number(label="Engine Size")

    with gr.Tab("Location Information"):
        registered_city = gr.Dropdown(
            label="Registered City", choices=unique_values["registered_city"]
        )
        city = gr.Dropdown(label="City", choices=unique_values["city"])

    with gr.Tab("Condition and Type"):
        selling_condition = gr.Dropdown(
            label="Selling Condition", choices=unique_values["selling_condition"]
        )
        bought_condition = gr.Dropdown(
            label="Bought Condition", choices=unique_values["bought_condition"]
        )
        body_type = gr.Dropdown(label="Body Type", choices=unique_values["body_type"])
        fuel_type = gr.Dropdown(label="Fuel Type", choices=unique_values["fuel_type"])
        transmission = gr.Dropdown(
            label="Transmission", choices=unique_values["transmission"]
        )

    predict_button = gr.Button("Predict Price")
    predicted_price = gr.Textbox(label="Predicted Price")

    predict_button.click(
        fn=predict_car_price,
        inputs=[
            make,
            model,
            year_of_manufacture,
            color,
            condition,
            mileage,
            engine_size,
            registered_city,
            selling_condition,
            bought_condition,
            city,
            body_type,
            fuel_type,
            transmission,
        ],
        outputs=predicted_price,
    )

interface.launch()
