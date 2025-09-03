import uvicorn
from fastapi import FastAPI, Body
from fastapi.params import Query

app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"}
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    return [hotel for hotel in hotels if hotel["title"] == title and hotel["id"] == id]


@app.delete("/hotels/{hotel_id}")
def delete_hotels(
        hotel_id: int
):
    global hotels

    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]

    return {"status": "No content"}


@app.post("/hotels")
def create_hotel(title: str = Body(), name: str = Body()):
    global hotels

    hotels.append({"id": hotels[-1]["id"] + 1, "title": title, "name": name})

    return {"status": "Created"}

@app.patch("/hotels/{hotel_id}")
def patch_hotel(hotel_id: int, title: str | None = Body(default=None), name: str | None = Body(default=None)):
    global hotels

    if not any([title, name]):
        return {"status": "No content"}

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name

            return {"status": "OK", "hotel": hotel}

    return {"status": "Not found"}


@app.put("/hotels/{hotel_id}")
def put_hotel(hotel_id: int, title: str | None = Body(), name: str | None = Body()):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name

            return {"status": "OK", "hotel": hotel}

    return {"status": "Not found"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
