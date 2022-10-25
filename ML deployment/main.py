import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel  # Class wrapper for data validation

app = FastAPI()
trained_model = None


class BankNote(BaseModel):
    variance: float
    skewness: float
    curtosis: float
    entropy: float


@app.post("/predict")
def predict_banknote(data: BankNote):
    data = data.dict()
    variance = data['variance']
    skewness = data['skewness']
    curtosis = data['curtosis']
    entropy = data['entropy']

    prediction = trained_model.predict([[variance, skewness, curtosis, entropy]])

    return {
        "prediction": "Real" if prediction[0] > 0.5 else "Fake"
    }


@app.get("/")
def index():
    return "Welcome to the Banknote Authentication API"


def train_model():

    # if model file exists, load it
    try:
        # Load the model
        model = pickle.load(open('model.pkl', 'rb'))
    except:
        # Read the data
        df = pd.read_csv('BankNote_Authentication.csv')
        # Split the data into X and y
        X = df.drop('class', axis=1)
        y = df['class']
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        # Train the model
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        # Save the model
        pickle.dump(model, open('model.pkl', 'wb'))
        # Predict the model
        y_predicted = model.predict(X_test)
        # Evaluate the model
        accuracy = accuracy_score(y_test, y_predicted)
        print(f'Accuracy: {accuracy}')

    return model


if __name__ == '__main__':
    trained_model = train_model()
    uvicorn.run(app, host="localhost", port=8000)
