from fastapi import FastAPI, Path,HTTPException,status
from typing import Optional
from pydantic import BaseModel

users={1:{"name":"John","age":30,"city":"New York","job":"Engineer"},
       2:{"name":"Jane","age":25,"city":"San Francisco","job":"Designer"},
       3:{"name":"Mike","age":35,"city":"Chicago","job":"Manager"}}


app=FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello this is the root path!my first api"}   

@app.get("/Users/{user_id}")
def get_user(user_id: int=Path(..., title="The ID of the user to get", ge=0, le=1000)):
    if user_id not in users :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") 
    return users[user_id]