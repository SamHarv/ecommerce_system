import time

from model_admin import Admin
from operation_user import UserOperation


class AdminOperation:
    """Contains all the operations related to the admin"""

    user_op = UserOperation()
    
    def register_admin(self, user_name, user_password):
        """Registers a new admin
        Arguments: user_name, user_password
        Return True/ False to indicate whether registration was successful"""
        
        if not self.user_op.validate_username(user_name):
            print("Invalid username! Username must contain at least five " 
                  "characters and only contain letters and underscores.")
            return False
        elif self.user_op.check_username_exist(user_name):
            print("Username already exists!")
            return False
        elif not self.user_op.validate_password(user_password):
            print("Invalid password! Password must contain at least five " 
                  "characters consisting of at least one uppercase  or "
                  "lowercase letter, and at least one number.")
            return False
        admin_id = self.user_op.generate_unique_user_id()
        admin_register_time = time.strftime("%d-%m-%Y_%H:%M:%S")
        # create admin object
        admin = Admin(user_id=admin_id, user_name=user_name, 
                      user_password=user_password, 
                      user_register_time=admin_register_time, 
                      user_role="admin")
        # write to file
        file = open("data/users.txt", "a")
        file.write(str(admin) + "\n")
        file.close()
        print("Success! Admin registered.")
        return True