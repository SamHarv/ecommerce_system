import time

from model_admin import Admin
from operation_user import UserOperation


class AdminOperation:
    """Contains all the operations related to the admin."""

    user_op = UserOperation()

    def register_admin(self, user_name, user_password):
        """Registers a new admin.
        Arguments: user_name, user_password.
        Return True/ False to indicate whether registration was successful."""

        if not self.user_op.validate_username(user_name):
            return False
        elif self.user_op.check_username_exist(user_name):
            return False
        elif not self.user_op.validate_password(user_password):
            return False
        admin_id = self.user_op.generate_unique_user_id()
        admin_register_time = time.strftime("%d-%m-%Y_%H:%M:%S")
        # Encrypt password
        user_password = self.user_op.encrypt_password(user_password)
        # create admin object
        admin = Admin(user_id=admin_id, user_name=user_name,
                      user_password=user_password,
                      user_register_time=admin_register_time,
                      user_role="admin")
        # write to file
        try:
            file = open("data/users.txt", "a", encoding="utf-8")
            file.write(str(admin) + "\n")
        except FileNotFoundError:
            file = open("data/users.txt", "w", encoding="utf-8")
            file.write(str(admin) + "\n")
        except Exception as e:
            return False
        finally:
            file.close()
        return True
