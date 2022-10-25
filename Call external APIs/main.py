import uvicorn
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel  # Class wrapper for data validation
import httpx

app = FastAPI()

db = []


def get_time(timezone: str):
    return httpx.get(f'http://worldtimeapi.org/api/timezone/{timezone}') \
        .json().get('datetime') \
        .split('T')[1] \
        .split('+')[0] \
        .split('.')[0]


class City(BaseModel):
    name: str
    timezone: str


class CityList(BaseModel):
    data: list


class CityWithCurrentTime(BaseModel):
    name: str
    timezone: str
    current_time: str


db.append(City(name="New York", timezone="America/New_York"))
db.append(City(name="London", timezone="Europe/London"))
db.append(City(name="Seville", timezone="Europe/Madrid"))


@app.get("/")
def get_cities():
    list_of_cities = []

    for city in db:
        name = city.name
        timezone = city.timezone
        current_time = get_time(timezone)
        city_with_current_time = CityWithCurrentTime(name=name, timezone=timezone, current_time=current_time)
        list_of_cities.append(city_with_current_time)

    return CityList(data=list_of_cities)


@app.get("/{id}")
def get_city(id: int):
    city = db[id]
    return CityWithCurrentTime(name=city.name, timezone=city.timezone, current_time=get_time(city.timezone))


@app.delete("/{id}")
def delete_city(id: int):
    city = db[id]
    db.pop(id)
    return "Deleted city: " + city.name


@app.post("/city")
def create_city(cities: CityList):
    new_cities = []
    for city in cities.data:
        db.append(city)
        new_cities.append(city)
    return new_cities


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
