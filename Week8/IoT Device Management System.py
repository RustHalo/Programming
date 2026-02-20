import datetime

class Device:
    #new IoT device
    def __init__(self, device_id, device_type, owner):
        if not device_id or not device_type:
            raise ValueError("Device ID and Type cannot be empty.")
            
        self.device_id = device_id
        self.device_type = device_type
        self.owner = owner  #user object from Exercise1
        self.__firmware_version = "1.0.0"
        self.__last_security_scan = datetime.datetime.now()
        self.__is_active = True
        self.__is_quarantined = False
        self.__activity_log = []

    #log device interactions
    def log_interaction(self, action, user):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__activity_log.append(f"[{timestamp}] {user.username}: {action}")
    
    #compliance
    def check_compliance(self):
        if self.__is_quarantined:
            return False
            
        days_since_scan = (datetime.datetime.now() - self.__last_security_scan).days
        if days_since_scan > 30:
            return False
        return True

    #update timestamp
    def run_security_scan(self, user):
        self.__last_security_scan = datetime.datetime.now()
        self.log_interaction("Security scan completed", user)

    #update firmware 
    def update_firmware(self, new_version, user):
        self.__firmware_version = new_version
        self.log_interaction(f"Firmware updated to {new_version}", user)

    #user has control permission?
    def authorise_access(self, user, override=False):
        if not self.__is_active:
            self.log_interaction("Access denied: Device is inactive", user)
            return False

        is_admin = user.check_privileges() == "admin"
        is_owner = self.owner.username == user.username

        # Admin override logic
        if override and is_admin:
            self.log_interaction("Admin override used for access", user)
            return True
            
        # Standard access logic
        if (is_owner or is_admin) and self.check_compliance():
            self.log_interaction("Access granted", user)
            return True
            
        self.log_interaction("Access denied: Compliance failure or unauthorized", user)
        return False
        
    def set_quarantine(self, status):
        """Sets the quarantine status of the device."""
        self.__is_quarantined = status


class DeviceManager:
    def __init__(self):
        self.devices = {}

    #add device to manager
    def add_device(self, device):
        self.devices[device.device_id] = device

    #remove device (admin)
    def remove_device(self, device_id, admin_user):
        if admin_user.check_privileges() == "admin":
            if device_id in self.devices:
                del self.devices[device_id]
        else:
            raise PermissionError("Only admins can remove devices.")

    #isolate compromised device (admin)
    def quarantine_device(self, device_id, admin_user):
        if admin_user.check_privileges() == "admin":
            if device_id in self.devices:
                self.devices[device_id].set_quarantine(True)
                self.devices[device_id].log_interaction("Device Quarantined", admin_user)
        else:
            raise PermissionError("Only admins can quarantine devices.")

    #compliance report
    def generate_security_report(self, admin_user):
        if admin_user.check_privileges() != "admin":
            raise PermissionError("Only admins can generate reports.")
            
        report = []
        for d_id, device in self.devices.items():
            status = "Compliant" if device.check_compliance() else "Non-Compliant"
            report.append(f"Device: {d_id} | Type: {device.device_type} | Owner: {device.owner.username} | Status: {status}")
        return "\n".join(report)
    

