import os

from io_interface import IOInterface
from operation_admin import AdminOperation
from operation_product import ProductOperation
from operation_user import UserOperation
from operation_customer import CustomerOperation
from operation_order import OrderOperation

"""
Name: Samuel Harvey
Student ID: 34217061
Creation date: 3 October 2023
Last modified: 6 October 2023
Description: PyCommerce is an information management system which can be 
accessed by customers and administrators to perform a range of different
actions such as viewing products, creating orders and adding customers.
"""


class Main:
    """The main class to start the program."""

    io = IOInterface()
    op_user = UserOperation()
    op_admin = AdminOperation()
    op_cust = CustomerOperation()
    op_pro = ProductOperation()
    op_order = OrderOperation()

    user = None

    def login_control(self):
        """Control the login process for all users."""
        self.io.main_menu()
        try:
            input = self.io.get_user_input("", 1)
        except Exception as e:
            self.io.print_error_message("IOInterface.get_user_input", e)
            self.login_control()

        flag = True
        while flag:
            if input[0] == "1":
                # Login
                user_name = self.io.get_user_input(
                    "\nPlease enter your username:\n", 1)
                password = self.io.get_user_input(
                    "\nPlease enter your password:\n", 1)
                # Get user object
                try:
                    self.user = self.op_user.login(user_name[0], password[0])
                except Exception as e:
                    self.io.print_error_message("UserOperation.login", e)
                    flag = False
                    self.login_control()
                if type(self.user) == str:
                    self.io.print_error_message("UserOperation.login",
                                                "Username and password "
                                                "combination not "
                                                "found.")
                    flag = False
                    self.login_control()
                # Customer path
                if self.user.user_role == "customer":
                    try:
                        self.customer_control()
                    except Exception as e:
                        self.io.print_error_message("Main.customer_control", e)
                    finally:
                        flag = False
                # Admin path
                elif self.user.user_role == "admin":
                    try:
                        self.admin_control()
                    except Exception as e:
                        self.io.print_error_message("Main.admin_control", e)
                    finally:
                        flag = False
                else:
                    self.io.print_error_message("UserOperation.login",
                                                "Invalid username or "
                                                "password.\nUsername must be "
                                                "at least 5 characters long "
                                                "and should only contain "
                                                "letters and underscores.\n"
                                                "Password must be at least 5 "
                                                "characters long and must "
                                                "contain at least one letter "
                                                "and one number.")
                    self.login_control()
                    flag = False
            elif input[0] == "2":
                # Register
                self.io.print_message(
                    "Register\n\nPlease register a new account.")
                # Choose user role for registration
                try:
                    account_type = self.io.get_user_input("Would you like to "
                                                          "register for a "
                                                          "customer account, "
                                                          "or "
                                                          "an admin account?\n"
                                                          "1. Admin\n"
                                                          "2. Customer\n", 1)
                except Exception as e:
                    self.io.print_error_message("IOInterface.get_user_input",
                                                e)
                    flag = False
                    self.login_control()
                # Admin registration
                if account_type[0] == "1":
                    try:
                        user_name = self.io.get_user_input("\nPlease enter a "
                                                           "username:\n",
                                                           1)
                        password = self.io.get_user_input(
                            "\nPlease enter a password:\n", 1)
                    except Exception as e:
                        self.io.print_error_message("IOInterface.get_user_inpu"
                                                    "t", e)
                        flag = False
                        self.login_control()
                    # Create admin object
                    try:
                        admin_reg = self.op_admin.register_admin(
                            user_name[0], password[0])
                    except Exception as e:
                        self.io.print_error_message("AdminOperation.register_"
                                                    "admin", e)
                        flag = False
                        self.login_control()
                    if admin_reg:
                        self.io.print_message("\nRegistration successful!\n")
                        self.user = self.op_user.login(
                            user_name[0], password[0])
                        # Admin path if successful
                        self.admin_control()
                        flag = False
                    else:
                        self.io.print_error_message("AdminOperation.register_"
                                                    "admin.", "Invalid "
                                                    "username or password.\n"
                                                    "Username must be "
                                                    "at least 5 characters "
                                                    "long and should only "
                                                    "contain letters and "
                                                    "underscores.\nPassword "
                                                    "must be at least 5 "
                                                    "characters long and must "
                                                    "contain at least one "
                                                    "letter and one number.")
                elif account_type[0] == "2":
                    try:
                        user_name = self.io.get_user_input("\nPlease enter a "
                                                           "username:\n", 1)
                        password = self.io.get_user_input(
                            "\nPlease enter a password:\n", 1)
                        email = self.io.get_user_input("\nPlease enter your "
                                                       "email address:\n", 1)
                        mobile = self.io.get_user_input("\nPlease enter your "
                                                        "mobile phone "
                                                        "number:\n", 1)
                    except Exception as e:
                        self.io.print_error_message("IOInterface.get_user_inpu"
                                                    "t", e)
                        flag = False
                        self.login_control()
                    # Create customer object
                    try:
                        cust_reg = self.op_cust.register_customer(user_name[0],
                                                                  password[0],
                                                                  email[0],
                                                                  mobile[0])
                    except Exception as e:
                        self.io.print_error_message("CustomerOperation.registe"
                                                    "r_customer", e)
                        flag = False
                        self.login_control()
                    if cust_reg:
                        self.io.print_message("\nRegistration successful!\n")
                        try:
                            self.user = self.op_user.login(
                                user_name[0], password[0])
                        except Exception as e:
                            self.io.print_error_message("UserOperation.login",
                                                        e)
                            flag = False
                            self.login_control()
                        # Customer path if successful
                        self.customer_control()
                        flag = False
                    else:
                        self.io.print_error_message("UserOperation.register_"
                                                    "customer.", "Invalid "
                                                    "username, password, "
                                                    "email, or mobile.\n"
                                                    "Username must be "
                                                    "at least 5 characters "
                                                    "long and should only "
                                                    "contain letters and "
                                                    "underscores.\nPassword "
                                                    "must be at least 5 "
                                                    "characters long and must "
                                                    "contain at least one "
                                                    "letter and one number.\n"
                                                    "Email must be a valid "
                                                    "email address.\nMobile "
                                                    "phone number must be "
                                                    "exactly 10 digits long "
                                                    "with no spaces.")

                else:
                    self.io.print_error_message("IOInterface.get_user_input",
                                                "Invalid input. Please try "
                                                "again.\n")

            elif input[0] == "3":
                # Quit
                self.io.print_message("\nThank you for using PyCommerce!\n")
                os._exit(0)
            else:
                # Loop back on error
                self.io.print_error_message("IOInterface.get_user_input",
                                            "Invalid input. Please try "
                                            "again.\n")
                flag = False
                self.login_control()

    def customer_control(self):
        """Control the customer process for all users."""
        self.io.customer_menu()
        try:
            input = self.io.get_user_input("", 2)
        except Exception as e:
            self.io.print_error_message("IOInterface.get_user_input", e)

        flag = True
        while flag:
            if input[0] == "1":
                # Show Profile
                self.io.print_message("Show Profile")
                try:
                    self.io.print_object(self.user)
                except Exception as e:
                    self.io.print_error_message("IOInterface.print_object", e)
                flag = False
                self.customer_control()

            elif input[0] == "2":
                # Update Profile
                self.io.print_message("Update Profile")
                try:
                    attribute_selection = self.io.get_user_input("Which part "
                                                                 "of your "
                                                                 "profile "
                                                                 "would you "
                                                                 "like to "
                                                                 "update?\n"
                                                                 "1. Username"
                                                                 "\n"
                                                                 "2. Password"
                                                                 "\n"
                                                                 "3. Email\n"
                                                                 "4. Mobile\n",
                                                                 1)
                except Exception as e:
                    self.io.print_error_message("IOInterface.get_user_input",
                                                e)
                    flag = False
                    self.customer_control()
                # Attribute to update
                if attribute_selection[0] == "1":
                    attribute = "user_name"
                elif attribute_selection[0] == "2":
                    attribute = "user_password"
                elif attribute_selection[0] == "3":
                    attribute = "user_email"
                elif attribute_selection[0] == "4":
                    attribute = "user_mobile"
                else:
                    self.io.print_error_message("IOInterface.get_user_input",
                                                "Invalid input. Please try "
                                                "again.\n")
                    flag = False
                    self.customer_control()
                # New value for attribute
                try:
                    value = self.io.get_user_input("Please enter the new value"
                                                   ":\n", 1)
                except Exception as e:
                    self.io.print_error_message("IOInterface.get_user_input",
                                                e)
                    flag = False
                    self.customer_control()
                # Update profile
                try:
                    prof_update = self.op_cust.update_profile(attribute,
                                                              value[0],
                                                              self.user)
                except Exception as e:
                    self.io.print_error_message("CustomerOperation.update_"
                                                "profile", e)
                    flag = False
                    self.customer_control()
                if prof_update:
                    self.io.print_message("\nProfile updated successfully!\n"
                                          "Please log out then back in to "
                                          "see changes.\n")
                    flag = False
                    self.customer_control()
                else:
                    self.io.print_error_message("CustomerOperation.update_"
                                                "profile. ",
                                                "Invalid "
                                                "username, password, "
                                                "email, or mobile.\n"
                                                "Username must be "
                                                "at least 5 characters "
                                                "long and should only "
                                                "contain letters and "
                                                "underscores.\nPassword "
                                                "must be at least 5 "
                                                "characters long and must "
                                                "contain at least one "
                                                "letter and one number.\n"
                                                "Email must be a valid "
                                                "email address.\nMobile "
                                                "phone number must be "
                                                "exactly 10 digits long "
                                                "with no spaces.")

                    self.customer_control()

            elif input[0] == "3":
                # Show Products

                try:
                    customer_choice = self.io.get_user_input("Please select "
                                                             "from the "
                                                             "options below:"
                                                             "\n1. Show "
                                                             "Products\n"
                                                             "2. Purchase a "
                                                             "Product by "
                                                             "Product "
                                                             "ID\n", 1)
                except Exception as e:
                    self.io.print_error_message("IOInterface.get_user_input",
                                                e)
                    flag = False
                    self.customer_control()

                if customer_choice[0] == "1":

                    # Show all products
                    try:
                        keyword = input[1]  # Accept keyword if entered
                    except IndexError:
                        keyword = ""
                    except Exception as e:
                        self.io.print_error_message("IOInterface.get_user_"
                                                    "input", e)
                        flag = False
                        self.customer_control()
                    self.io.print_message("Show Products")
                    if keyword == "":
                        # Show all first page of products with no filter
                        try:
                            self.io.show_list(
                                self.user.user_role, "product",
                                self.op_pro.get_product_list(1))
                        except Exception as e:
                            self.io.print_error_message(
                                "IOInterface.show_list", e)
                            flag = False
                            self.customer_control()
                        page = 1

                        while True:
                            try:
                                selection = self.io.get_user_input("\nPlease "
                                                                   "select "
                                                                   "from the "
                                                                   "following"
                                                                   " options:"
                                                                   "\n"
                                                                   "1. Next "
                                                                   "Page\n"
                                                                   "2. Previou"
                                                                   "s Page\n"
                                                                   "3. Return "
                                                                   "to "
                                                                   "Customer "
                                                                   "Menu\n", 1)
                            except Exception as e:
                                self.io.print_error_message("IOInterface.get_"
                                                            "user_input", e)
                                self.customer_control()
                                break

                            if selection[0] == "1":
                                # Stay on page if next does not exist
                                if page >= int(self.op_pro.get_product_list(
                                        page)[1].split(" ")[3]):
                                    try:
                                        self.io.show_list(
                                            self.user.user_role, "product",
                                            self.op_pro.get_product_list(page))
                                    except Exception as e:
                                        self.io.print_error_message(
                                            "IOInterface.show_list", e)
                                        break

                                else:
                                    page += 1  # Next page
                                    try:
                                        self.io.show_list(
                                            self.user.user_role, "product",
                                            self.op_pro.get_product_list(page))
                                    except Exception as e:
                                        self.io.print_error_message(
                                            "IOInterface.show_list", e)
                                        break
                            elif selection[0] == "2":
                                # Stay on page if previous does not exist
                                if page <= 1:
                                    try:
                                        self.io.show_list(
                                            self.user.user_role, "product",
                                            self.op_pro.get_product_list(page))
                                    except Exception as e:
                                        self.io.print_error_message(
                                            "IOInterface.show_list", e)
                                        break
                                else:
                                    page -= 1  # Previous page
                                    try:
                                        self.io.show_list(
                                            self.user.user_role, "product",
                                            self.op_pro.get_product_list(page))
                                    except Exception as e:
                                        self.io.print_error_message(
                                            "IOInterface.show_list", e)
                                        break
                            elif selection[0] == "3":
                                self.customer_control()
                                break

                            else:
                                self.io.print_error_message(
                                    "IOInterface.get_user_input",
                                    "Invalid input. Please try again.\n")

                    else:
                        # Check whether a result was found for keyword
                        try:
                            result = self.io.show_list(
                                self.user.user_role, "product", self.op_pro.
                                get_product_list_by_keyword(keyword))
                        except Exception as e:
                            self.io.print_error_message(
                                "IOInterface.show_list", e)
                            break

                        if result == []:
                            self.io.print_message("No products found for your "
                                                  "keyword.")
                        else:
                            # Show filtered search results
                            result
                    flag = False
                    self.customer_control()

                elif customer_choice[0] == "2":
                    # Purchase a Product by Product ID
                    try:
                        product_id = self.io.get_user_input("Please enter a "
                                                            "product ID:\n", 1)
                    except Exception as e:
                        self.io.print_error_message("IOInterface.get_user_"
                                                    "input", e)
                        break
                    # Check whether a result was found for product_id
                    try:
                        result = self.io.print_message(self.op_pro.
                                                       get_product_by_id(
                                                           product_id[0]))
                    except Exception as e:
                        self.io.print_error_message("IOInterface.print_"
                                                    "message", e)
                        break

                    if result == []:
                        self.io.print_error_message("IOInterface.print_"
                                                    "message", "No products "
                                                    "found for your product "
                                                    "ID. Please ensure your "
                                                    "product ID is seven "
                                                    "digits long and consists "
                                                    "of only numbers.")
                    else:
                        # Show filtered search results
                        result
                        # Create order
                        try:
                            self.op_order.create_an_order(self.user.user_id,
                                                          product_id[0])
                            self.io.print_message("Order created successfully"
                                                  "!")
                        except Exception as e:
                            self.io.print_error_message("OrderOperation."
                                                        "create_an_order", e)
                            break

                    flag = False
                    self.customer_control()

                else:
                    self.io.print_error_message("IOInterface.get_user_input",
                                                "Invalid input. Please try "
                                                "again.\n")

            elif input[0] == "4":
                # Show Order History
                self.io.print_message("Show Order History")
                page = 1
                try:
                    result = self.op_order.get_order_list(self.user.user_id,
                                                          page)
                except Exception as e:
                    self.io.print_error_message("OrderOperation.get_order_"
                                                "list", e)
                    flag = False
                    self.customer_control()
                # Check that orders exist for customer
                if result[0] == []:
                    self.io.print_message("No orders found.")
                    flag = False
                    self.customer_control()
                else:
                    # Show first page of orders
                    try:
                        self.io.show_list(self.user.user_role, "order",
                                          self.op_order.get_order_list(
                                              self.user.user_id, page))
                    except Exception as e:
                        self.io.print_error_message("IOInterface.show_list", e)
                        flag = False
                        self.customer_control()

                while True:
                    try:
                        selection = self.io.get_user_input("\nPlease select "
                                                           "from the following"
                                                           " options:\n"
                                                           "1. Next Page\n"
                                                           "2. Previous Page\n"
                                                           "3. Return to "
                                                           "Customer Menu\n",
                                                           1)
                    except Exception as e:
                        self.io.print_error_message("IOInterface.get_user_"
                                                    "input", e)
                        self.customer_control()
                        break

                    if selection[0] == "1":
                        # Stay on page if next does not exist
                        if page >= int(self.op_order.get_order_list(
                                self.user.user_id, page)[1].split(" ")[3]):
                            try:
                                self.io.show_list(
                                    self.user.user_role, "order",
                                    self.op_order.get_order_list(
                                        self.user.user_id, page))
                            except Exception as e:
                                self.io.print_error_message(
                                    "IOInterface.show_list", e)
                        else:
                            page += 1  # Next page
                            try:
                                self.io.show_list(
                                    self.user.user_role, "order",
                                    self.op_order.get_order_list(
                                        self.user.user_id, page))
                            except Exception as e:
                                self.io.print_error_message(
                                    "IOInterface.show_list", e)

                    elif selection[0] == "2":
                        # Stay on page if previous does not exist
                        if page <= 1:
                            try:
                                self.io.show_list(
                                    self.user.user_role, "order",
                                    self.op_order.get_order_list(
                                        self.user.user_id, page))
                            except Exception as e:
                                self.io.print_error_message(
                                    "IOInterface.show_list", e)
                        else:
                            page -= 1  # Previous page
                            try:
                                self.io.show_list(
                                    self.user.user_role, "order",
                                    self.op_order.get_order_list(
                                        self.user.user_id, page))
                            except Exception as e:
                                self.io.print_error_message(
                                    "IOInterface.show_list", e)
                    elif selection[0] == "3":
                        self.customer_control()
                        break
                    else:
                        self.io.print_error_message("IOInterface.get_user_"
                                                    "input", "Invalid input. "
                                                    "Please try again.\n")
                flag = False

            elif input[0] == "5":
                # Generate Statistical Figures
                self.io.print_message("Generating Consumption Figures...")
                try:
                    self.op_order.generate_single_customer_consumption_figure(
                        self.user.user_id)
                    self.op_order.generate_all_customers_consumption_figure()
                    self.io.print_message("Figures generated successfully!")
                except Exception as e:
                    self.io.print_error_message("OrderOperation.generate_"
                                                "single_customer_consumption_"
                                                "figure", e)
                flag = False
                self.customer_control()

            elif input[0] == "6":
                # Logout
                self.io.print_message("Logged out.")
                flag = False
                self.user = None
                try:
                    self.login_control()
                except Exception as e:
                    self.io.print_error_message("Main.login_control", e)

            else:
                # Loop back
                self.io.print_error_message("IOInterface.get_user_input",
                                            "Invalid input. Please try again."
                                            "\n")
                flag = False
                self.customer_control()

    def admin_control(self):
        """Control the admin process."""

        self.io.admin_menu()
        try:
            admin_input = self.io.get_user_input("", 1)
        except Exception as e:
            self.io.print_error_message("IOInterface.get_user_input", e)
            self.admin_control()

        flag = True
        while flag:

            if admin_input[0] == "1":
                # Show Products
                try:
                    choice = self.io.get_user_input("Show Products\n\n"
                                                    "Please select from the "
                                                    "following options:\n"
                                                    "1. Show All Products\n"
                                                    "2. Show Products by "
                                                    "Keyword\n"
                                                    "3. Show Product by "
                                                    "Product ID\n"
                                                    "4. Delete a Product by ID"
                                                    "\n"
                                                    "5. Return to Admin Menu\n", 1)
                except Exception as e:
                    self.io.print_error_message("IOInterface.get_user_input",
                                                e)
                    flag = False
                    self.admin_control()

                if choice[0] == "1":
                    # Show all first page of products with no filter
                    try:
                        self.io.show_list(
                            self.user.user_role, "product",
                            self.op_pro.get_product_list(1))
                    except Exception as e:
                        self.io.print_error_message("IOInterface.show_list", e)
                        flag = False
                        self.admin_control()
                    page = 1

                    while True:
                        try:
                            selection = self.io.get_user_input("\nPlease "
                                                               "select from "
                                                               "the following "
                                                               "options:\n"
                                                               "1. Next Page\n"
                                                               "2. Previous "
                                                               "Page\n"
                                                               "3. Return to "
                                                               "Admin Menu\n",
                                                               1)
                        except Exception as e:
                            self.io.print_error_message("IOInterface.get_user_"
                                                        "input", e)
                            self.admin_control()
                            break

                        if selection[0] == "1":
                            # Stay on page if next does not exist
                            if page >= int(self.op_pro.get_product_list(
                                    page)[1].split(" ")[3]):
                                try:
                                    self.io.show_list(
                                        self.user.user_role, "product",
                                        self.op_pro.get_product_list(page))
                                except Exception as e:
                                    self.io.print_error_message(
                                        "IOInterface.show_list", e)
                                    self.admin_control()
                                    break
                            else:
                                page += 1  # Next page
                                try:
                                    self.io.show_list(
                                        self.user.user_role, "product",
                                        self.op_pro.get_product_list(page))
                                except Exception as e:
                                    self.io.print_error_message(
                                        "IOInterface.show_list", e)
                                    self.admin_control()
                                    break
                        elif selection[0] == "2":
                            # Stay on page if previous does not exist
                            if page <= 1:
                                try:
                                    self.io.show_list(
                                        self.user.user_role, "product",
                                        self.op_pro.get_product_list(page))
                                except Exception as e:
                                    self.io.print_error_message(
                                        "IOInterface.show_list", e)
                                    self.admin_control()
                                    break
                            else:
                                page -= 1  # Previous page
                                try:
                                    self.io.show_list(
                                        self.user.user_role, "product",
                                        self.op_pro.get_product_list(page))
                                except Exception as e:
                                    self.io.print_error_message(
                                        "IOInterface.show_list", e)
                                    self.admin_control()
                                    break
                        elif selection[0] == "3":
                            self.admin_control()
                            break

                        else:
                            self.io.print_error_message(
                                "IOInterface.get_user_input",
                                "Invalid input. Please try again.\n")

                elif choice[0] == "2":
                    # Show Products by Keyword
                    try:
                        keyword = self.io.get_user_input("Please enter a "
                                                         "keyword to search "
                                                         "for:\n", 1)
                    except Exception as e:
                        self.io.print_error_message("IOInterface.get_user_"
                                                    "input", e)
                        flag = False
                        self.admin_control()

                    # Check whether a result was found for keyword
                    try:
                        result = self.io.show_list(self.user.user_role,
                                                   "product",
                                                   self.op_pro.
                                                   get_product_list_by_keyword(
                                                       keyword[0]))
                    except Exception as e:
                        self.io.print_error_message("IOInterface.show_list", e)
                        flag = False
                        self.admin_control()

                    if result == []:
                        self.io.print_message("No products found for your "
                                              "keyword.")
                    else:
                        # Show filtered search results
                        result

                elif choice[0] == "3":
                    # Show Product by Product ID
                    try:
                        product_id = self.io.get_user_input("Please enter a "
                                                            "product ID:\n", 1)
                        # Check whether a result was found for product_id
                        result = self.op_pro.get_product_by_id(product_id[0])

                    except Exception as e:
                        self.io.print_error_message("IOInterface.get_user_"
                                                    "input", e)
                        flag = False
                        self.admin_control()

                    if result == []:
                        self.io.print_error_message("No products found for "
                                                    "your product ID.",
                                                    "Please ensure your "
                                                    "product ID is seven "
                                                    "digits long and consists "
                                                    "of only numbers.")
                    else:
                        # Show filtered search results
                        self.io.print_object(result)

                elif choice[0] == "4":
                    # Delete a Product by ID
                    try:
                        product_id = self.io.get_user_input("Please enter a "
                                                            "product ID:\n", 1)
                        # Check whether a result was found for product_id
                        result = self.op_pro.get_product_by_id(product_id[0])
                    except Exception as e:
                        self.io.print_error_message("IOInterface.get_user_"
                                                    "input", e)
                        flag = False
                        self.admin_control()

                    if result == []:
                        self.io.print_error_message("No products found for "
                                                    "your product ID.",
                                                    "Please ensure your "
                                                    "product ID is seven "
                                                    "digits long and consists "
                                                    "of only numbers.")
                    else:
                        # Show filtered search results
                        self.io.print_object(result)
                        # Delete product
                        try:
                            self.op_pro.delete_product(product_id[0])
                        except Exception as e:
                            self.io.print_error_message("ProductOperation."
                                                        "delete_product", e)
                            flag = False
                            self.admin_control()
                        self.io.print_message("Product deleted successfully!")

                elif choice[0] == "5":
                    # Return to Admin Menu
                    self.admin_control()
                    break

                else:
                    # Loop back on error
                    self.io.print_error_message("IOInterface.get_user_input",
                                                "Invalid input. Please try "
                                                "again.\n")

            elif admin_input[0] == "2":
                # Add Customers
                self.io.print_message("Add Customers")
                while True:
                    # Enter attributes
                    try:
                        user_name = self.io.get_user_input("\nPlease enter a "
                                                           "username for your "
                                                           "new customer:\n",
                                                           1)[0]
                        user_password = self.io.get_user_input("\nPlease "
                                                               "enter a "
                                                               "password for "
                                                               "your new "
                                                               "customer:\n",
                                                               1)[0]
                        user_email = self.io.get_user_input("\nPlease enter "
                                                            "an email address "
                                                            "for your new "
                                                            "customer:\n",
                                                            1)[0]
                        user_mobile = self.io.get_user_input("\nPlease enter "
                                                             "a mobile phone "
                                                             "number for your "
                                                             "new customer:\n",
                                                             1)[0]
                    except Exception as e:
                        self.io.print_error_message("IOInterface.get_user_"
                                                    "input", e)
                        self.admin_control()
                        break

                    # Create new customer object
                    try:
                        rego = self.op_cust.register_customer(user_name,
                                                              user_password,
                                                              user_email,
                                                              user_mobile)
                    except Exception as e:
                        self.io.print_error_message("CustomerOperation.registe"
                                                    "r_customer", e)
                        self.admin_control()
                        break

                    if rego:
                        self.io.print_message("\nCustomer added "
                                              "successfully!\n")
                    else:
                        self.io.print_error_message("CustomerOperation.registe"
                                                    "r_customer", "Invalid "
                                                    "username, password, "
                                                    "email, or mobile.\n"
                                                    "Username must be "
                                                    "at least 5 characters "
                                                    "long and should only "
                                                    "contain letters and "
                                                    "underscores.\nPassword "
                                                    "must be at least 5 "
                                                    "characters long and must "
                                                    "contain at least one "
                                                    "letter and one number.\n"
                                                    "Email must be a valid "
                                                    "email address.\nMobile "
                                                    "phone number must be "
                                                    "exactly 10 digits long "
                                                    "with no spaces.")
                        self.admin_control()
                        break

                    another = True
                    while another:
                        # Action whether to create another customer
                        try:
                            go_on = self.io.get_user_input("\nWould you like "
                                                           "to add another "
                                                           "customer"
                                                           "?\n"
                                                           "1. Yes\n"
                                                           "2. No\n", 1)[0]
                        except Exception as e:
                            self.io.print_error_message("IOInterface.get_user_"
                                                        "input", e)
                        if go_on == "1":
                            another = False
                            continue
                        elif go_on == "2":
                            self.admin_control()
                            another = False
                            break
                        else:
                            self.io.print_error_message("IOInterface.get_user_"
                                                        "input", "Invalid "
                                                        "input. "
                                                        "Please try again.\n")

            elif admin_input[0] == "3":
                # Show Customers
                self.io.print_message("Show Customers")
                # Select customer action
                try:
                    customer_action = self.io.get_user_input("Please select "
                                                             "from the "
                                                             "following "
                                                             "options:\n"
                                                             "1. Show All "
                                                             "Customers\n"
                                                             "2. Delete a "
                                                             "Customer by ID\n"
                                                             "3. Return to "
                                                             "Admin Menu\n",
                                                             1)[0]
                except Exception as e:
                    self.io.print_error_message("IOInterface.get_user_"
                                                "input", e)
                    flag = False
                    self.admin_control()

                if customer_action == "1":
                    # Show all customers
                    page = 1
                    try:
                        self.io.show_list(self.user.user_role, "customer",
                                          self.op_cust.get_customer_list(page))
                    except Exception as e:
                        self.io.print_error_message("IOInterface.show_list", e)
                        flag = False
                        self.admin_control()

                    while True:
                        try:
                            selection = self.io.get_user_input("\nPlease "
                                                               "select from "
                                                               "the following "
                                                               "options:\n"
                                                               "1. Next Page\n"
                                                               "2. Previous "
                                                               "Page\n"
                                                               "3. Return to "
                                                               "Admin Menu\n",
                                                               1)
                        except Exception as e:
                            self.io.print_error_message("IOInterface.get_user_"
                                                        "input", e)
                            self.admin_control()
                            break

                        if selection[0] == "1":
                            # Stay on page if next does not exist
                            if page >= int(self.op_cust.get_customer_list(
                                    page)[1].split(" ")[3]):
                                try:
                                    self.io.show_list(
                                        self.user.user_role, "customer",
                                        self.op_cust.get_customer_list(page))
                                except Exception as e:
                                    self.io.print_error_message(
                                        "IOInterface.show_list", e)
                                    self.admin_control()
                                    break
                            else:
                                page += 1  # Next page
                                try:
                                    self.io.show_list(
                                        self.user.user_role, "customer",
                                        self.op_cust.get_customer_list(page))
                                except Exception as e:
                                    self.io.print_error_message(
                                        "IOInterface.show_list", e)
                                    self.admin_control()
                                    break
                        elif selection[0] == "2":
                            # Stay on page if previous does not exist
                            if page <= 1:
                                try:
                                    self.io.show_list(
                                        self.user.user_role, "customer",
                                        self.op_cust.get_customer_list(page))
                                except Exception as e:
                                    self.io.print_error_message(
                                        "IOInterface.show_list", e)
                                    self.admin_control()
                                    break
                            else:
                                page -= 1  # Previous page
                                try:
                                    self.io.show_list(
                                        self.user.user_role, "customer",
                                        self.op_cust.get_customer_list(page))
                                except Exception as e:
                                    self.io.print_error_message(
                                        "IOInterface.show_list", e)
                                    self.admin_control()
                                    break
                        elif selection[0] == "3":
                            self.admin_control()
                            break

                        else:
                            self.io.print_error_message(
                                "IOInterface.get_user_input",
                                "Invalid input. Please try again.\n")

                elif customer_action == "2":

                    # Delete customer by customer ID
                    try:
                        customer_id = self.io.get_user_input("Please enter a "
                                                             "customer ID:\n",
                                                             1)[0]
                    except Exception as e:
                        self.io.print_error_message("IOInterface.get_user_"
                                                    "input", e)
                        flag = False
                        self.admin_control()

                    # Delete Customer
                    try:
                        deletion = self.op_cust.delete_customer(customer_id)
                    except Exception as e:
                        self.io.print_error_message("CustomerOperation.delete_"
                                                    "customer", e)
                        flag = False
                        self.admin_control()
                    if deletion:
                        self.io.print_message("Customer deleted successfully!")
                    else:
                        self.io.print_error_message("CustomerOperation.delete_"
                                                    "customer", "Invalid "
                                                    "customer ID.")

                elif customer_action == "3":
                    # Return to Admin Menu
                    self.admin_control()
                    break

                else:
                    # Loop back
                    self.io.print_error_message("IOInterface.get_user_input",
                                                "Invalid input. Please try "
                                                "again.\n")

            elif admin_input[0] == "4":
                # Show Orders
                self.io.print_message("Show Orders")

                # Select order action
                try:
                    order_action = self.io.get_user_input("Please select from "
                                                          "the following "
                                                          "options:\n"
                                                          "1. Show All "
                                                          "Orders\n"
                                                          "2. Delete an "
                                                          "Order by ID\n"
                                                          "3. Return to "
                                                          "Admin Menu\n", 1)[0]
                except Exception as e:
                    self.io.print_error_message("IOInterface.get_user_"
                                                "input", e)
                    flag = False
                    self.admin_control()

                if order_action == "1":

                    # Show All Orders
                    page = 1
                    try:
                        result = self.op_order.get_order_list("all", page)
                    except Exception as e:
                        self.io.print_error_message("OrderOperation.get_order_"
                                                    "list", e)
                        flag = False
                        self.admin_control()
                    # Check that orders exist
                    if result[0] == []:
                        self.io.print_message("No orders found.")
                        flag = False
                        self.admin_control()
                    else:
                        # Show first page of orders
                        try:
                            self.io.show_list(self.user.user_role, "order",
                                              self.op_order.get_order_list(
                                                  "all", page))
                        except Exception as e:
                            self.io.print_error_message("IOInterface.show_"
                                                        "list", e)
                            flag = False
                            self.admin_control()
                    while True:
                        try:
                            selection = self.io.get_user_input("\nPlease "
                                                               "select from "
                                                               "the following "
                                                               "options:\n"
                                                               "1. Next Page\n"
                                                               "2. Previous "
                                                               "Page\n"
                                                               "3. Return to "
                                                               "Admin Menu\n",
                                                               1)
                        except Exception as e:
                            self.io.print_error_message("IOInterface.get_user_"
                                                        "input", e)
                            self.admin_control()
                            break

                        if selection[0] == "1":
                            # Stay on page if next does not exist
                            if page >= int(self.op_order.get_order_list(
                                    "all", page)[1].split(" ")[3]):
                                try:
                                    self.io.show_list(
                                        self.user.user_role, "order",
                                        self.op_order.get_order_list(
                                            "all", page))
                                except Exception as e:
                                    self.io.print_error_message(
                                        "IOInterface.show_list", e)
                                    self.admin_control()
                                    break
                            else:
                                page += 1  # Next page
                                try:
                                    self.io.show_list(
                                        self.user.user_role, "order",
                                        self.op_order.get_order_list(
                                            "all", page))
                                except Exception as e:
                                    self.io.print_error_message(
                                        "IOInterface.show_list", e)
                                    self.admin_control()
                                    break
                        elif selection[0] == "2":
                            # Stay on page if previous does not exist
                            if page <= 1:
                                try:
                                    self.io.show_list(
                                        self.user.user_role, "order",
                                        self.op_order.get_order_list(
                                            "all", page))
                                except Exception as e:
                                    self.io.print_error_message(
                                        "IOInterface.show_list", e)
                                    self.admin_control()
                                    break
                            else:
                                page -= 1  # Previous page
                                try:
                                    self.io.show_list(
                                        self.user.user_role, "order",
                                        self.op_order.get_order_list(
                                            "all", page))
                                except Exception as e:
                                    self.io.print_error_message(
                                        "IOInterface.show_list", e)
                                    self.admin_control()
                                    break
                        elif selection[0] == "3":
                            self.admin_control()
                            break

                        else:
                            self.io.print_error_message(
                                "IOInterface.get_user_input",
                                "Invalid input. Please try again.\n")

                elif order_action == "2":

                    # Delete an Order by ID
                    try:
                        order_id = self.io.get_user_input("Please enter an "
                                                          "order ID:\n", 1)[0]
                    except Exception as e:
                        self.io.print_error_message("IOInterface.get_user_"
                                                    "input", e)
                        flag = False
                        self.admin_control()

                    # Delete Order
                    try:
                        deletion = self.op_order.delete_order(order_id)
                    except Exception as e:
                        self.io.print_error_message("OrderOperation.delete_"
                                                    "order", e)
                        flag = False
                        self.admin_control()
                    if deletion:
                        self.io.print_message("Order deleted successfully"
                                              "!")
                    else:
                        self.io.print_error_message("OrderOperation.delete"
                                                    "_order", "Invalid "
                                                    "order ID.")

                elif order_action == "3":
                    # Return to Admin Menu
                    self.admin_control()
                    break

                else:
                    # Loop back
                    self.io.print_error_message("IOInterface.get_user_input",
                                                "Invalid input. Please try "
                                                "again.\n")

            elif admin_input[0] == "5":
                # Generate Test Data
                self.io.print_message("Generating Test Data...")
                try:
                    self.op_order.generate_test_order_data()
                except Exception as e:
                    self.io.print_error_message("OrderOperation.generate_"
                                                "test_order_data", e)
                    flag = False
                    self.admin_control()
                self.io.print_message("Test Data Generated Successfully!")
                flag = False
                self.admin_control()

            elif admin_input[0] == "6":
                # Generate All Statistical Figures
                self.io.print_message("Generating Consumption Figures...")
                try:
                    self.op_order.generate_all_customers_consumption_figure()
                except Exception as e:
                    self.io.print_error_message("OrderOperation.generate_"
                                                "all_customers_consumption_"
                                                "figure", e)
                    flag = False
                    self.admin_control()
                try:
                    self.op_pro.generate_category_figure()
                except Exception as e:
                    self.io.print_error_message("ProductOperation.generate_"
                                                "category_figure", e)
                    flag = False
                    self.admin_control()
                try:
                    self.op_pro.generate_discount_figure()
                except Exception as e:
                    self.io.print_error_message("ProductOperation.generate_"
                                                "discount_figure", e)
                    flag = False
                    self.admin_control()
                try:
                    self.op_pro.generate_discount_likes_count_figure()
                except Exception as e:
                    self.io.print_error_message("ProductOperation.generate_"
                                                "discount_likes_count_figure",
                                                e)
                    flag = False
                    self.admin_control()
                try:
                    self.op_pro.generate_likes_count_figure()
                except Exception as e:
                    self.io.print_error_message("ProductOperation.generate_"
                                                "likes_count_figure", e)
                    flag = False
                    self.admin_control()
                self.io.print_message("Figures generated successfully and "
                                      "saved to data/figure")
                self.admin_control()
                break

            elif admin_input[0] == "7":
                # Delete All Data
                self.io.print_message("Deleting All Data...")
                try:
                    self.op_pro.delete_all_products()
                except Exception as e:
                    self.io.print_error_message("ProductOperation.delete_"
                                                "all_products", e)
                    flag = False
                    self.admin_control()
                try:
                    self.op_order.delete_all_orders()
                except Exception as e:
                    self.io.print_error_message("OrderOperation.delete_"
                                                "all_orders", e)
                    flag = False
                    self.admin_control()
                try:
                    self.op_cust.delete_all_customers()
                except Exception as e:
                    self.io.print_error_message("CustomerOperation.delete_"
                                                "all_customers", e)
                    flag = False
                    self.admin_control()
                self.io.print_message("All Data Deleted Successfully!")
                flag = False
                self.admin_control()

            elif admin_input[0] == "8":
                # Logout
                print("Logged out.")
                flag = False
                self.user = None
                self.login_control()

            else:
                # Loop back
                self.io.print_error_message("IOInterface.get_user_input",
                                            "Invalid input. Please try again."
                                            "\n")
                flag = False
                self.admin_control()

    def main(self):
        """The main function to start the program"""
        try:
            self.op_pro.extract_products_from_files()
        except Exception as e:
            self.io.print_error_message("ProductOperation.extract_products_"
                                        "from_files", e)

        try:
            self.op_admin.register_admin("admin", "admin1")
        except Exception as e:
            self.io.print_error_message("AdminOperation.register_admin", e)

        try:
            self.login_control()
        except Exception as e:
            self.io.print_error_message("Main.login_control", e)


if __name__ == "__main__":
    main = Main()
    main.main()
