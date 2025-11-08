passwords= ["Pass123",
            "SecurePassword1",
            "weak",
            "MyP@ssw0rd",
            "NOLOWER123"]

compliant_count = 0
non_compliant_count = 0

print("Validating Passwords...")

for password in passwords:
    
    fail_reasons = []
    
    has_uppercase = False
    has_lowercase = False
    has_digit = False

    if len(password) < 8:
        fail_reasons.append("Too short")

    for char in password:
        if char.isupper():
            has_uppercase = True
        elif char.islower():
            has_lowercase = True
        elif char.isdigit():
            has_digit = True
    
    if not has_uppercase:
        fail_reasons.append("No uppercase")
        
    if not has_lowercase:
        fail_reasons.append("No lowercase letters")
        
    if not has_digit:
        fail_reasons.append("No digits")

    if not fail_reasons:
        print(f"PASS: '{password}' - Meets all requirements")
        compliant_count += 1
    else:
        reason_string = ", ".join(fail_reasons)
        print(f"FAIL: '{password}' - {reason_string}")
        non_compliant_count += 1

print(f"Summary: {compliant_count} compliant, {non_compliant_count} non-compliant")