import json
import os
from fastapi import APIRouter, HTTPException
from schema import User, UserCreate

#create APIRouter
router= APIRouter()

#text file for data persistence
file_path= "users.txt"


#helper functions#

#read user from json file/ return empty if none exist or empty
def read_users():
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

#write current list of users back to json file
def write_users(users):
    with open(file_path, "w") as f:
        json.dump(users, f, indent=4)

#next available id
def get_next_id(users):
    if not users:
        return 1
    return max(user["id"] for user in users) + 1 


#api endpoints#

#create user
@router.post("/", response_model=User)
def create_user(user: UserCreate):
    users= read_users()
    new_user= {"id": get_next_id(users), "name": user.name}
    users.append(new_user)
    write_users(users)
    return new_user

#get all users
@router.get("/")
def get_all_users():
    return read_users()

#search user by name (case insensitive)
@router.get("/search")
def search_users(q: str):
    users= read_users()
    results= [u for u in users if q.lower() in u["name"].lower()]
    return results

#get user by id
@router.get("/{id}")
def get_user(id: int):
    users= read_users()
    for user in users:
        if user["id"] == id:
            return user
        #error if user not found
    raise HTTPException(status_code=404, detail="User Not Found")
    
#update user
@router.put("{id}", response_model=User)
def update_user(id: int, updated_user: UserCreate):
    users= read_users()
    for user in users:
        if user["id"] == id:
            user["name"]= updated_user.name
            write_users(users)
            return user
    raise HTTPException(status_code=404, detail="User Not Found")
    
#delete user
@router.delete("/{id}")
def delete_user(id: int):
    users= read_users()
    for i, user in enumerate(users):
        if user["id"] == id:
            del users[i]
            write_users(users)
            return {"message": "User Deleted Successfully"}
    raise HTTPException(status_code=404, detail="User Not Found")


