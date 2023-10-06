import random
import re
import string

from model_admin import Admin
from model_customer import Customer


class UserOperation:
    """Contains all the operations related to a user object."""

    def generate_unique_user_id(self):
        """Generates a unique user id for a new user.
        Return user_id"""
        while True:
            user_id = "u_" + str(random.randint(1000000000, 9999999999))
            try:
                file = open("data/users.txt", "r", encoding="utf-8")
                data_string = file.read()
            except FileNotFoundError:
                file = open("data/users.txt", "w", encoding="utf-8")
                data_string = ""
            finally:
                file.close()
            # Check if user_id exists in users.txt
            if user_id not in data_string:
                break
        return user_id

    def encrypt_password(self, user_password):
        """Encrypt the user password.
        Argugments: user_password
        Return encrypted_password"""
        # Generate a random alphanumeric string twice the length of
        # user_password
        encrypted_string = ''.join(random.choices(string.ascii_letters
                                                  + string.digits,
                                                  k=len(user_password)*2))

        # Combine encrypted_string and user_password to create
        # encrypted_password
        encrypted_password = ""
        tracker = 0
        for i in range(len(encrypted_string + user_password)):
            # Add every third character from user_password
            if (i + 1) % 3 == 0:
                encrypted_password += user_password[i//3]
            else:
                encrypted_password += encrypted_string[tracker]
                tracker += 1

        # Add "^^" and "$$" to encrypted_password
        encrypted_password = "^^" + encrypted_password + "$$"
        return encrypted_password

    def decrypt_password(self, encrypted_password):
        """Decrypts the user password.
        Argugments: encrypted_password
        Return user_password"""
        # Remove "^^" and "$$" from encrypted_password
        encrypted_password = encrypted_password[2:-2]

        # Extract every third character from encrypted_password to get
        # user_password
        user_provided_password = ""
        for i in range(len(encrypted_password)):
            if (i + 1) % 3 == 0:
                user_provided_password += encrypted_password[i]
        return user_provided_password

    def check_username_exist(self, user_name):
        """Checks if the username already exists.
        Arguments: user_name.
        Return True/ False."""
        # Check whether user_name in users.txt
        try:
            file = open("data/users.txt", "r", encoding="utf-8")
            user_list = file.readlines()
        except FileNotFoundError:
            file = open("data/users.txt", "w", encoding="utf-8")
            user_list = []
        except Exception:
            return False
        finally:
            file.close()
        for user in user_list:
            if f"'user_name':'{user_name}'" in user:
                return True
        return False

    def validate_username(self, user_name):
        """Validates the username.
        Arguments: user_name.
        Return True/ False."""
        if len(user_name) < 5:
            return False
        # Check username contains only letters and underscores
        elif not re.match("^[a-zA-Z_]*$", user_name):
            return False
        else:
            return True

    def validate_password(self, user_password):
        """Validates the password.
        Arguments: user_password.
        Return True/ False."""
        if len(user_password) < 5:
            return False
        elif (re.search("[A-Z]", user_password) == None and
              re.search("[a-z]", user_password) == None):
            return False
        elif re.search("[0-9]", user_password) == None:
            return False
        else:
            return True

    def login(self, user_name, user_password):
        """Logs in the user.
        Arguments: user_name, user_password.
        Return Customer/ Admin object depending on authorisation."""
        try:
            file = open("data/users.txt", "r", encoding="utf-8")
            user_list = file.readlines()
        except FileNotFoundError:
            file = open("data/users.txt", "w", encoding="utf-8")
            user_list = []
            return "No users found, please register!"
        except Exception as e:
            return "No users found, please register!"
        finally:
            file.close()
        for user in user_list:
            # Remove curly braces from user string
            user = user.replace("{", "").replace("}", "")
            if (f"'user_name':'{user_name}'" in user):
                # Save the user_id, name, password, register_time, user_role
                param_list = user.split(",")
                user_id = param_list[0].split(":")[1].replace("'", "")
                name = param_list[1].split(":")[1].replace("'", "")
                password = param_list[2].split(":")[1].replace("'", "")
                password = self.decrypt_password(password)
                register_time = param_list[3].split(":", 1)[1].replace("'", "")
                user_role = param_list[4].split(":")[1].replace("'", "")
                # Remove remaining curly brace and new line character
                user_role = user_role.replace("}", "").replace("\n", "")
                # Check password
                if user_password != password:
                    return "Incorrect password!"
                else:
                    # Check if user is admin or customer
                    if user_role == "admin":
                        return Admin(user_id, name, password, register_time,
                                     user_role)
                    elif user_role == "customer":
                        # Save mobile and email
                        email = param_list[5].split(":")[1].replace("'", "")
                        mobile = param_list[6].split(":")[1].replace("'", "")
                        return Customer(user_id, name, password, email, mobile,
                                        register_time, user_role)
        return "User not found, please register!"
