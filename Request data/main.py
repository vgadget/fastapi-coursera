import uvicorn
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel  # Class wrapper for data validation

app = FastAPI()

db = []


class City(BaseModel):
    name: str
    timezone: str


class CityList(BaseModel):
    data: list


db.append(City(name="New York", timezone="America/New_York"))
db.append(City(name="London", timezone="Europe/London"))
db.append(City(name="Seville", timezone="Europe/Madrid"))


@app.get("/")
def get_cities():
    return db


@app.post("/city")
def create_city(cities: CityList):
    new_cities = []
    for city in cities.data:
        db.append(city)
        new_cities.append(city)
    return new_cities


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
