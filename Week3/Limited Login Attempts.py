correct_pin = "56345"
attempts = 0
max_attempts = 3
Login_successful = False

while attempts < max_attempts:
    print(f"Attempt {attempts +1} of {max_attempts}")
    entered_pin= input("Enter Your PIN:")
    
    if entered_pin == correct_pin:
        print("PIN Accepted! Welcome.")
        Login_successful= True
        break
    else:
        print("Incorrect PIN.")
        attempts += 1

if not Login_successful:
    print("Too many incorrect attempts. Account Blocked.")