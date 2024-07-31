import pandas as pd
import joblib

from pydantic import BaseModel
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

class CarPrices(BaseModel):
    make: str
    model: str
    year_of_manufacture: int
    color: str
    condition: str
    mileage: float
    engine_size: float
    registered_city: str
    selling_condition: str
    bought_condition: str
    city: str
    body_type: str
    fuel_type: str  
    transmission: str

class CarPriceModel:
    """
    model to predict the prices of cars from car45.com
    """

    def __init__(self):
        self.data = pd.read_csv("data/car_data.csv")
        self.model_fpath_ = "model/car_prediction_model.pickle"

        try:
            self.model = joblib.load(self.model_fpath_)
        except Exception:
            self.model = self.train_model()
            joblib.dump(self.model, self.model_fpath_)

    def preprocessor(self):
        numerical_features = ["mileage", "engine_size"]
        categorical_features = [
            "make",
            "model",
            "color",
            "condition",
            "registered_city",
            "selling_condition",
            "bought_condition",
            "city",
            "body_type",
            "fuel_type",
            "transmission",
        ]

        numerical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="mean")),
                ("scaler", StandardScaler()),
            ]
        )

        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numerical_transformer, numerical_features),
                ("cat", categorical_transformer, categorical_features),
            ]
        )

        return preprocessor

    def train_model(self):
        preprocessor = self.preprocessor()
        X = self.data.drop("price", axis=1)
        y = self.data["price"]

        model = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", RandomForestRegressor(random_state=42)),
            ]
        )

        model.fit(X, y)

        return model
    
    def predict(self, data):
        data = pd.DataFrame([data])
        preprocessor = self.model.named_steps['preprocessor']
        X_processed = preprocessor.transform(data)
        prediction = self.model.named_steps['model'].predict(X_processed)

        return prediction[0]
        