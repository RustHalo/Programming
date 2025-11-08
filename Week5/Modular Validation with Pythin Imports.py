import string
import random

def check_min_length(password, min_len=8):
    return len(password) >= min_len

def has_uppercase(password):
    return any(char.isupper() for char in password)

def has_lowercase(password):
    return any(char.islower() for char in password)

def has_digit(password):
    return any(char.isdigit() for char in password)

def has_special_char(password):
    return any(char in string.punctuation for char in password)

def validate_password(password):
    results= {
        "min_length": check_min_length(password),
        "uppercase": has_uppercase(password),
        "lowercase": has_lowercase(password),
        "digit": has_digit(password),
        "special_char": has_special_char(password)
    }
    results["is_valid"]= all(results.values())
    return results

def main():
    weak_hints= [
        "Hint: Try adding more Numbers or Symbols."
        "Hint: A good Password is longer than 8 charecter."
        "Hint: Mix in some uppercase and lowecase letters."
    ]

    user_password= input("Please enter a Password to validate:")
    validation_results= validate_password(user_password)

    print("\n--- Validation Report ---")
    print(f"Minimum length (8+): {'Met' if validation_results['min_length'] else 'Not met'}")
    print(f"Has uppercase:       {'Met' if validation_results['uppercase'] else 'Not met'}")
    print(f"Has lowercase:       {'Met' if validation_results['lowercase'] else 'Not met'}")
    print(f"Has digit:           {'Met' if validation_results['digit'] else 'Not met'}")
    print(f"Has special char:    {'Met' if validation_results['special_char'] else 'Not met'}")
    print("-------------------------")
    
    if validation_results["is_valid"]:
        print("Overall status: Strong")
    else:
        print("Overall status: Weak")
        print(random.choice(weak_hints))

if __name__ == "__main__":
    main()