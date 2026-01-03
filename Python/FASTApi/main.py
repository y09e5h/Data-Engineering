from fastapi import FastAPI
app = FastAPI()
@app.get("/{name}")
async def hello(name):
    return {"message": f"Hello {name}"}

@app.get("/")
async def hello():
    return {"message": "Hello World"}

food_items = {
  "Italy": [
    {"name": "Pizza", "type": "Flatbread", "description": "Traditional Neapolitan style with tomato and mozzarella."},
    {"name": "Pasta", "type": "Starch", "description": "Various shapes served with diverse regional sauces."}
  ],
  "Mexico": [
    {"name": "Tacos", "type": "Street Food", "description": "Corn or wheat tortillas filled with various meats and salsas."},
    {"name": "Mole Poblano", "type": "Sauce/Stew", "description": "Rich, dark sauce featuring chili and chocolate."}
  ],
  "Japan": [
    {"name": "Sushi", "type": "Seafood", "description": "Vinegared rice paired with fresh raw fish or vegetables."},
    {"name": "Ramen", "type": "Noodle Soup", "description": "Wheat noodles in a savory meat or fish-based broth."}
  ],
  "France": [
    {"name": "Pot-au-feu", "type": "Stew", "description": "Classic beef stew with vegetables, often considered a national dish."},
    {"name": "Crêpe", "type": "Pancake", "description": "Thin pancakes with sweet or savory fillings."}
  ],
  "India": [
    {"name": "Biryani", "type": "Rice Dish", "description": "Spiced rice mixed with marinated meat or vegetables."},
    {"name": "Chicken Tikka Masala", "type": "Curry", "description": "Roasted marinated chicken chunks in a spiced sauce."}
  ]
}
@app.get("/get_item/{name}")
async def get_item(name: str):
    if name in food_items:
        return food_items.get(name)
    else:
        return {"message": "Item not found"}

cupon_code={
    1:'10%',
    2:'20%',
    3:'30%',
    4:'40%'
}
@app.get("/get_cupon/{code}")
async def get_cupon(code: int):
    return {"discount" : cupon_code.get(code)}
