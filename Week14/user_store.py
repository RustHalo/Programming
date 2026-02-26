import json

class UserStore:
    def __init__(self, file_path):
        self.file_path= file_path

    def load(self):
        users= []
        try:
            with open(self.file_path, "r")as file:
                #read each line as seperate json object
                for line in file:
                    if line.strip():
                        users.append(json.loads(line))

            return users
        except FileNotFoundError:
            #return empty list if file doesn't exist
            return []
        
    #write users as json lines
    def save(self, users):
        with open (self.file_path, "w") as file:
            for user in users:
                file.write(json.dumps(user) + "\n")

    #return a user dict or none
    def find_by_id(self, user_id):
        users= self.load()
        for user in users:
            if user.get("id") == user_id:
                return user
        return None
    
    ##Extension##

    #Implement a method to update a user by id, returning success status
    def update_user(self, user_id, updated_data):
        users= self.load()
        for i, user in enumerate(users):
            if user.get("id") == user_id:
                #update specific field
                users[i].update(updated_data)
                self.save(users)
                return True #success
        return False #user not found
    
    #Implement a method to remove a user by ID, returning a success status.
    def delete_user(self, user_id):
        users= self.load()
        for i, user in enumerate(users):
            if user.get("id") == user_id:
                del users[i]
                self.save(users)
                return True #success
        return False #user not found
    
