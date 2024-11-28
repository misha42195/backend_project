import uvicorn
from fastapi import FastAPI, Body
from fastapi import Query

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]


@app.get("/hotels")
def get_hotel(
    id: int | None = Query(default=None, description="Id отеля"),
    title: str | None = Query(default=None, description="Название отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    return hotels_


@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        title: title
    })
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def full_update_hotels(
    hotel_id: int = int,
    title: str = Body(None),
    name: str = Body(None)
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title is not None:
        hotel["title"] = title
    if name is not None:
        hotel["name"] = name
    return {"status": "OK"}


@app.patch(
    "/hotels/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Параметры title и name не обязательны")
def update_hotel(
    hotel_id: int,
    title: str | None = Body(),
    name: str | None = Body()
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["name"] = name
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(
    hotel_id: int,
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return hotel


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
