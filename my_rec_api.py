
import re
from fastapi import FastAPI, HTTPException,status,Path
from pydantic import BaseModel
from typing import  Optional

recipes = {1: {"name": "Pasta Carbonara", "ingredients": ["pasta", "eggs", "cheese", "bacon"], "instructions": "Boil pasta. Cook bacon. Mix eggs and cheese. Combine all."},
           2: {"name": "Chicken Curry", "ingredients": ["chicken", "curry powder", "coconut milk"], "instructions": "Cook chicken. Add curry powder and coconut milk. Simmer."},
           3: {"name": "Beef Tacos", "ingredients": ["beef", "taco shells", "lettuce", "cheese"], "instructions": "Cook beef. Fill taco shells with beef, lettuce, and cheese."}
          }


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, this is the root path of my recipe API!"}

@app.get("/recipe/{recipe_id}")
def get_recipe_byid(recipe_id: int = Path(..., title="The ID of the recipe", ge=0, le=10000)):
    if recipe_id not in recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipes[recipe_id]


class Recipe(BaseModel):
    name: str
    ingredients: list
    instructions: str

class UpdateRecipe(BaseModel):
    name: Optional[str] = None
    ingredients: Optional[list] = None
    instructions: Optional[str] = None


@app.post("/recipe/{recipe_id}",status_code=status.HTTP_201_CREATED )
def create_recipe(recipe_id:int ,recipe: Recipe):
    if recipe_id in recipes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Recipe ID already exists")
    recipes[recipe_id] = recipe.dict()
    return recipes[recipe_id]

@app.put("/recipe/{recipe_id}")
def update_recipe(recipe_id: int, recipe: UpdateRecipe):    
    if recipe_id not in recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    currect_recipe = recipes[recipe_id]
    if recipe.name is not None:
        currect_recipe["name"] = recipe.name
    if recipe.ingredients is not None:
        currect_recipe["ingredients"] = recipe.ingredients 
    if recipe.instructions is not None:
        currect_recipe["instructions"] = recipe.instructions
    return currect_recipe


@app.delete("/recipe/{recipe_id}",status_code=status.HTTP_204_NO_CONTENT)    
def delete_recipe(recipe_id: int):
    if recipe_id not in recipes:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    deleted_recipe = recipes.pop(recipe_id)
    return {"detail": "Recipe deleted successfully", "recipe": deleted_recipe}    
    
@app.get("/recipe/name/{recipe_name}")
def get_recipe__byname(recipe_name: str):
    for recipe in recipes.values():
         if compare(recipe["name"].lower(), recipe_name.lower())==True:
            return recipe
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")


def compare(reDB_recipe_name: str,user_recipe_name: str):
     if reDB_recipe_name == user_recipe_name.lower():
        return True
