print(type(4.2))

name= "Marshall"
age= 25

print(name, age, "years old")

print(f"Hello {name}, you are {age} years old")

#input() Function ALWAYS as a String
username=input("Enter your username:")
print("Welcome", username)

x=15
print(int(x) - 5)
Marshall_is_student= False  
print(bool(Marshall_is_student))

user_age= input("Enter your Age:")
if not user_age.isdigit():
    print("Error: Invalid Input.")
else:
    print(f"You are {user_age} years old.")

is_valid= (age>=18)
is_student= True
if is_valid and is_student:
    print("Access Granted.")
else:
    print("Access Denied.")