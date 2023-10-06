import math
import re
import time

from operation_user import UserOperation
from model_customer import Customer


class CustomerOperation:
    """Contains operations related to the Customer.
    Instance variables: user_op - UserOperation object."""

    user_op = UserOperation()

    def validate_email(self, user_email):
        """Validates the email address.
        Arguments: user_email.
        Return True/ False."""
        regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+(\.\w+)?(\.\w+)?$"
        if re.search(regex, user_email):
            return True
        else:
            return False

    def validate_mobile(self, user_mobile):
        """Validates the mobile number.
        Arguments: user_mobile.
        Return True/ False."""
        if user_mobile.isdigit() and len(user_mobile) == 10:
            if user_mobile.startswith("04"):
                return True
            elif user_mobile.startswith("03"):
                return True
            else:
                return False
        else:
            return False

    def register_customer(self, user_name, user_password, user_email,
                          user_mobile):
        """Registers a new customer.
        Arguments: user_name, user_password, user_email, user_mobile.
        Return True/ False to indicate whether registration was successful."""

        if not self.user_op.validate_username(user_name):
            return False
        elif self.user_op.check_username_exist(user_name):
            return False
        elif not self.user_op.validate_password(user_password):
            return False
        elif not self.validate_email(user_email):
            return False
        elif not self.validate_mobile(user_mobile):
            return False
        else:
            user_id = self.user_op.generate_unique_user_id()
            user_register_time = time.strftime("%d-%m-%Y_%H:%M:%S")
            # Create new Customer object with validated attributes
            user_password = self.user_op.encrypt_password(user_password)
            new_customer = Customer(user_id=user_id, user_name=user_name,
                                    user_password=user_password,
                                    user_email=user_email,
                                    user_mobile=user_mobile,
                                    user_register_time=user_register_time,
                                    user_role="customer")
            # Write new customer to users.txt
            try:
                user_file = open("data/users.txt", "a", encoding="utf-8")
                user_file.write(str(new_customer) + "\n")
            except FileNotFoundError:
                user_file = open("data/users.txt", "w", encoding="utf-8")
                user_file.write(str(new_customer) + "\n")
            except Exception:
                return False
            finally:
                user_file.close()
            return True

    def update_profile(self, attribute_name, value, customer_object):
        """Updates the customer profile.
        Arguments: attribute_name, value, customer_object.
        Return True/ False to indicate whether update was successful."""
        try:
            file = open("data/users.txt", "r", encoding="utf-8")
            user_list = file.readlines()
        except FileNotFoundError:
            file = open("data/users.txt", "w", encoding="utf-8")
            user_list = []
            return False
        except Exception:
            return False
        finally:
            file.close()
        for user in user_list:
            # Check if customer exists
            if "'user_id':'" + str(customer_object.user_id) in user:
                # Extract attributes for later use
                # Remove curly braces from user string
                trimmed_user = user.replace("{", "").replace("}", "")
                # Save the name, password, email, mobile, user_role
                param_list = trimmed_user.split(",")
                user_id = param_list[0].split(":")[1].replace("'", "")
                user_name = param_list[1].split(":")[1].replace("'", "")
                user_password = param_list[2].split(":")[1].replace("'", "")
                register_time = param_list[3].split(":", 1)[1].replace("'", "")
                user_role = param_list[4].split(":")[1].replace("'", "")
                user_email = param_list[5].split(":")[1].replace("'", "")
                user_mobile = param_list[6].split(":")[1].replace("'", "")
                # Remove remaining curly brace and new line character
                user_mobile = user_mobile.replace("}", "").replace("\n", "")
                if attribute_name == "user_name":
                    if self.user_op.validate_username(value):
                        if self.user_op.check_username_exist(value):
                            return False
                        else:
                            user_name = value
                    else:
                        return False
                elif attribute_name == "user_password":
                    if self.user_op.validate_password(value):
                        value = self.user_op.encrypt_password(value)
                        user_password = value
                    else:
                        return False
                elif attribute_name == "user_email":
                    if self.validate_email(value):
                        user_email = value
                    else:
                        return False
                elif attribute_name == "user_mobile":
                    if self.validate_mobile(value):
                        user_mobile = value
                    else:
                        return False
                else:
                    return False

        # Remove the customer for replacement
        user_list.remove(user)
        try:
            file = open("data/users.txt", "w", encoding="utf-8")
            file.writelines(user_list)
        except FileNotFoundError:
            file = open("data/users.txt", "w", encoding="utf-8")
            file.writelines(user_list)
        except Exception:
            return False
        finally:
            file.close()

        # Create new Customer object with updated attributes
        try:
            updated_customer = Customer(user_id=user_id,
                                        user_name=user_name,
                                        user_password=user_password,
                                        user_email=user_email,
                                        user_mobile=user_mobile,
                                        user_register_time=register_time,
                                        user_role=user_role)
        except Exception:
            return False
        # Write updated customer to users.txt
        try:
            file = open("data/users.txt", "a", encoding="utf-8")
            file.write(str(updated_customer) + "\n")
        except FileNotFoundError:
            file = open("data/users.txt", "w", encoding="utf-8")
            file.write(str(updated_customer) + "\n")
        except Exception:
            return False
        finally:
            file.close()
        return True

    def delete_customer(self, customer_id):
        """Deletes the given customer.
        Arguments: customer_id.
        Return True/ False to indicate whether deletion was successful."""
        try:
            file = open("data/users.txt", "r", encoding="utf-8")
            user_list = file.readlines()
        except FileNotFoundError:
            file = open("data/users.txt", "w", encoding="utf-8")
            user_list = []
            return False
        except Exception:
            return False
        finally:
            file.close()
        for user in user_list:
            # Check if customer exists
            if (str(customer_id) in user and str(customer_id)[:2] == "u_"
                and str(customer_id)[2:].isdigit()
                    and len(str(customer_id)) == 12):
                user_list.remove(user)
                # Rewrite the file with the updated list
                try:
                    file = open("data/users.txt", "w", encoding="utf-8")
                    file.writelines(user_list)
                except FileNotFoundError:
                    file = open("data/users.txt", "x", encoding="utf-8")
                    file.writelines(user_list)
                except Exception:
                    return False
                finally:
                    file.close()
                return True
        return False

    def get_customer_list(self, page_number):
        """Get a list of customers within a given page range.
        Arguments: page_number.
        Return a tuple containing a list of customers, current page number, 
        and total pages."""
        try:
            file = open("data/users.txt", "r", encoding="utf-8")
            user_list = file.readlines()
        except FileNotFoundError:
            file = open("data/users.txt", "w", encoding="utf-8")
            user_list = []
        except Exception:
            return Exception
        finally:
            file.close()
        # Remove admins from list
        for user in user_list:
            if "'user_role':'customer'" not in user:
                user_list.remove(user)
        try:
            total_page = math.ceil(len(user_list) / 10)
        except Exception:
            return Exception
        # First customer on page
        low_customer = (page_number * 10) - 10
        # Last customer on page
        if total_page > 1:
            high_customer = (page_number * 10) - 1
        else:
            high_customer = len(user_list) - 1
        # Return the customers on the page
        users_returned = user_list[low_customer:high_customer + 1]
        return (users_returned, f"Page {page_number} of {total_page}")

    def delete_all_customers(self):
        """Deletes all customers."""
        try:
            file = open("data/users.txt", "r", encoding="utf-8")
            user_list = file.readlines()
        except FileNotFoundError:
            file = open("data/users.txt", "w", encoding="utf-8")
            user_list = []
        except Exception:
            return Exception
        finally:
            file.close()

        # Remove all customers from list
        new_user_list = []
        for user in user_list:
            if "'user_role':'customer'" not in user:
                new_user_list.append(user)
            else:
                continue

        # Rewrite the file with the updated list
        try:
            file = open("data/users.txt", "w", encoding="utf-8")
            file.writelines(new_user_list)
        except FileNotFoundError:
            file = open("data/users.txt", "x", encoding="utf-8")
            file.writelines(new_user_list)
        except Exception:
            return Exception
        finally:
            file.close()
