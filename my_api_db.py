from fastapi import FastAPI, HTTPException, status
from decouple import config
from supabase import create_client, Client
from pydantic import BaseModel

url=config("SUPABASE_URL")
key=config("SUPABASE_KEY")


app=FastAPI()

supabase: Client = create_client(url, key)
@app.get("/recipes/")
def get_recipes():
   recipes=supabase.table("tb_api_recipes").select("*").execute()
   return recipes.data

@app.get("/recipe/{recipe_id}")
def get_recipe(recipe_id: int):
   recipe=supabase.table("tb_api_recipes").select("*").eq("id", recipe_id).execute()
   if not recipe.data:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
   return recipe.data[0]


class  Recipe(BaseModel):
   ingredients: str
   recipe: str


@app.post("/recipe/", status_code=status.HTTP_201_CREATED)
def create_recipe(recipe: Recipe):
   new_recipe=supabase.table("tb_api_recipes").insert({"ingredients":recipe.ingredients,"recipe":recipe.recipe}).execute()
   return new_recipe.data[0]

@app.delete("/recipe/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int):
   recipe=supabase.table("tb_api_recipes").select("*").eq("id", recipe_id).execute()
   if not recipe.data:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
   supabase.table("tb_api_recipes").delete().eq("id", recipe_id).execute()
   return {"detail": "Recipe deleted successfully"} 

@app.put("/recipe/{recipe_id}", status_code=status.HTTP_200_OK )
def update_recipe(recipe_id: int, recipe: Recipe):
   existing_recipe=supabase.table("tb_api_recipes").select("*").eq("id", recipe_id).execute()
   if not existing_recipe.data:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
   if recipe.ingredients != existing_recipe.data[0]["ingredients"]:
      updated_recipe = supabase.table("tb_api_recipes").update({"ingredients": recipe.ingredients}).eq("id", recipe_id).execute()

   if recipe.recipe != existing_recipe.data[0]["recipe"]:
      updated_recipe = supabase.table("tb_api_recipes").update({"recipe": recipe.recipe}).eq("id", recipe_id).execute()
   return updated_recipe.data[0]