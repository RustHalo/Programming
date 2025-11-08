login_attempts = [
("Adele", "success"),
("Bob", "failed"),
("Bob", "failed"),
("Charlie", "success"),
("Bob", "failed"),
("Adele", "failed"),
("Charlie", "failed")]

failed_counts ={}

for username, status in login_attempts:
    if status == "failed":
        if username not in failed_counts:
            failed_counts[username]= 1
        else:
            failed_counts [username]+= 1

for username, count in failed_counts.items():
    if count >=3:
        print(f"ALERT!: User '{username}' has {count} failed login attempts")

print("Security Check complete.")