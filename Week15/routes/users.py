from fastapi import APIRouter, HTTPException
from schema import User, UserCreate
from user_store import UserStore

#create APIRouter
router= APIRouter()

store= UserStore("users.db")

#api endpoints#

#create user
@router.post("/", response_model=User)
def create_user(user: UserCreate):
    users= store.load()

    #generate next id
    new_id= 1 if not users else max(u["id"] for u in users) +1
    new_user= {"id": new_id, "name": user.name}

    users.append(new_user)
    store.save(users)
    return new_user

#get all users
@router.get("/")
def get_all_users():
    return store.load()

#search user 
@router.get("/search")
def search_users(q: str):
    users= store.load()
    results= [u for u in users if q.lower() in u["name"].lower()]
    return results

#get user by id
@router.get("/{id}")
def get_user(id: int):
    user= store.find_by_id(id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User Not Found")
    
#update user
@router.put("/{id}", response_model=User)
def update_user(id: int, updated_user: UserCreate):

    update_data= updated_user.model_dump()
    success= store.update_user(id, update_data)

    if not success:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    return store.find_by_id(id)

#delete user
@router.delete("/{id}")
def delete_user(id: int):
    success= store.delete_user(id)

    if not success:
        raise HTTPException(status_code=404, detail="User Not Found")
    return {"message": "User Deleted Successfully"}



