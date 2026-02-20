import hashlib
import datetime

class User:
    def __init__(self, username, password, privilege_level="standard"):
        """Initializes a new user with private attributes to ensure encapsulation."""
        self.username = username
        #private attributes to prevent direct manipulation
        self.__password_hash = self.__hash_password(password)
        self.__privilege_level = self.__validate_privilege(privilege_level)
        self.__login_attempts = 0
        self.__account_status = "active"
        self.__activity_log = []
        
        self.log_activity("Account created.")
    #SHA-256 hash
    def __hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    #privilege level input
    def __validate_privilege(self, level):
        valid_levels = ["admin", "standard", "guest"]
        if level.lower() in valid_levels:
            return level.lower()
        raise ValueError("Invalid privilege level. Must be admin, standard, or guest.")
    #Auth and handling
    def authenticate(self, password):
        if self.__account_status == "locked":
            self.log_activity("Failed login attempt - Account is locked.")
            print("Account is locked. Please contact an administrator.")
            return False

        if self.__password_hash == self.__hash_password(password):
            self.reset_login_attempts()
            self.log_activity("Successful login.")
            return True
        else:
            self.__login_attempts += 1
            self.log_activity(f"Failed login attempt ({self.__login_attempts}/3).")
            if self.__login_attempts >= 3:
                self.lock_account()
            return False
    #user's privilege level safely returned
    def check_privileges(self):
        return self.__privilege_level
    #lock account
    def lock_account(self):
        self.__account_status = "locked"
        self.log_activity("Account locked due to too many failed attempts.")

    #unlock account
    def unlock_account(self, admin_user):
        if admin_user.check_privileges() == "admin":
            self.__account_status = "active"
            self.reset_login_attempts()
            self.log_activity(f"Account unlocked by admin: {admin_user.username}.")
        else:
            self.log_activity("Unauthorized unlock attempt.")
            raise PermissionError("Only admins can unlock accounts.")

    #reset login attempt counter
    def reset_login_attempts(self):
        self.__login_attempts = 0
    #allows privilege escalation only through authorized admin validation
    def escalate_privilege(self, new_level, admin_user):
        if admin_user.check_privileges() == "admin":
            self.__privilege_level = self.__validate_privilege(new_level)
            self.log_activity(f"Privilege escalated to {new_level} by {admin_user.username}.")
        else:
            self.log_activity("Unauthorized privilege escalation attempt.")
            raise PermissionError("Only admins can escalate privileges.")
    #timestamp
    def log_activity(self, action):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__activity_log.append(f"[{timestamp}] {action}")

    #displays user information without exposing sensitive data
    def display_user_info(self):
        return {
            "Username": self.username,
            "Privilege Level": self.__privilege_level,
            "Account Status": self.__account_status}


