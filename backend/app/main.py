from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Testing Starter API")

class Item(BaseModel):
    id: int
    name: str

# In-memory "DB"
ITEMS = {
    1: Item(id=1, name="Alpha"),
    2: Item(id=2, name="Beta")
}

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = ITEMS.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    if item.id in ITEMS:
        raise HTTPException(status_code=400, detail="Item already exists")
    ITEMS[item.id] = item
    return item


# Para la solución de la prueba unitaria "test_items_exercise.py"

@app.get("/items", response_model=List[Item])
def listar_items(q: Optional[str] = None) -> List[Item]:
    todos = list(ITEMS.values())
    if q is None:
        return todos
    minusculas = q.lower()
    items_filtrados = [
        item for item in todos
        if minusculas in item.name.lower()]
    return items_filtrados


# Para la solución de la prueba unitaria "test_price_exercise.py"

def get_exchange_rate():
    return 3900.0

class Price(BaseModel):
    usd: int
    rate: float
    cop: float

@app.get("/price/{usd}", response_model=Price)
def get_price(usd: int, rate: float = Depends(get_exchange_rate)):
    if usd < 0:
        raise HTTPException(status_code=400, detail="Valor no valido (negativo)")
    cop = usd * rate
    return Price(usd=usd, rate=rate, cop=cop)