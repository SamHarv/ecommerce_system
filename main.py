import os

from io_interface import IOInterface
from operation_admin import AdminOperation
from operation_product import ProductOperation
from operation_user import UserOperation
from operation_customer import CustomerOperation
from operation_order import OrderOperation


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
        input = self.io.get_user_input("", 1)

        flag = True
        while flag:
            if input[0] == "1":
                # Login
                user_name = self.io.get_user_input(
                    "\nPlease enter your username:\n", 1)
                password = self.io.get_user_input(
                    "\nPlease enter your password:\n", 1)
                # Get user object
                self.user = self.op_user.login(user_name[0], password[0])
                # Customer path
                if self.user.user_role == "customer":
                    self.customer_control()
                    flag = False
                # Admin path
                elif self.user.user_role == "admin":
                    self.admin_control()
                    flag = False
                else:
                    self.io.print_error_message("UserOperation.login",
                                                "Invalid username or "
                                                "password.")
            elif input[0] == "2":
                # Register
                self.io.print_message(
                    "Register\n\nPlease register a new account.")
                # Choose user role for registration
                account_type = self.io.get_user_input("Would you like to "
                                                      "register for a "
                                                      "customer account, or "
                                                      "an admin account?\n"
                                                      "1. Admin\n"
                                                      "2. Customer\n", 1)
                # Admin registration
                if account_type[0] == "1":
                    user_name = self.io.get_user_input("\nPlease enter a "
                                                       "username:\n",
                                                       1)
                    password = self.io.get_user_input(
                        "\nPlease enter a password:\n", 1)
                    # Create admin object
                    admin_reg = self.op_admin.register_admin(
                        user_name[0], password[0])
                    if admin_reg:
                        self.io.print_message("\nRegistration successful!\n")
                        self.user = self.op_user.login(
                            user_name[0], password[0])
                        # Admin path if successful
                        self.admin_control()
                        flag = False
                    else:
                        self.io.print_error_message("AdminOperation.register_"
                                                    "admin. Invalid username "
                                                    "or password.")
                elif account_type[0] == "2":
                    user_name = self.io.get_user_input("\nPlease enter a "
                                                       "username:\n", 1)
                    password = self.io.get_user_input(
                        "\nPlease enter a password:\n", 1)
                    email = self.io.get_user_input("\nPlease enter your email "
                                                   "address:\n", 1)
                    mobile = self.io.get_user_input("\nPlease enter your "
                                                    "mobile phone "
                                                    "number:\n", 1)
                    # Create customer object
                    cust_reg = self.op_cust.register_customer(user_name[0],
                                                              password[0],
                                                              email[0],
                                                              mobile[0])
                    if cust_reg:
                        self.io.print_message("\nRegistration successful!\n")
                        self.user = self.op_user.login(
                            user_name[0], password[0])
                        # Customer path if successful
                        self.customer_control()
                        flag = False
                    else:
                        self.io.print_error_message("UserOperation.register_"
                                                    "customer. Invalid "
                                                    "username or password.")

            elif input[0] == "3":
                # Quit
                self.io.print_message("\nThank you for using PyCommerce!\n")
                os._exit(0)
            else:
                # Loop back on error
                self.io.print_error_message("IOInterface.get_user_input",
                                            "Invalid input. Please try "
                                            "again.\n")

    def customer_control(self):
        """Control the customer process for all users."""
        self.io.customer_menu()
        input = self.io.get_user_input("", 2)

        flag = True
        while flag:
            if input[0] == "1":
                # Show Profile
                self.io.print_message("Show Profile")
                self.io.print_object(self.user)
                flag = False
                self.customer_control()

            elif input[0] == "2":
                # Update Profile
                self.io.print_message("Update Profile")
                attribute_selection = self.io.get_user_input("Which part of "
                                                             "your profile "
                                                             "would you like "
                                                             "to update?\n"
                                                             "1. Username\n"
                                                             "2. Password\n"
                                                             "3. Email\n"
                                                             "4. Mobile\n", 1)
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
                    self.customer_control()
                # New value for attribute
                value = self.io.get_user_input("Please enter the new value:\n",
                                               1)
                # Update profile
                prof_update = self.op_cust.update_profile(attribute, value[0],
                                                          self.user)
                if prof_update:
                    self.io.print_message("\nProfile updated successfully!\n")
                    flag = False
                    self.customer_control()
                else:
                    self.io.print_error_message("CustomerOperation.update_"
                                                "profile",
                                                "Invalid input. Please try "
                                                "again.\n")
                    self.customer_control()

            elif input[0] == "3":
                # Show Products
                keyword = input[1]  # Accept keyword if entered
                self.io.print_message("Show Products")
                if keyword == "":
                    # Show all first page of products with no filter
                    self.io.show_list(
                        self.user.user_role, "product",
                        self.op_pro.get_product_list(1))
                    page = 1

                    while True:
                        selection = self.io.get_user_input("\nPlease select "
                                                           "from the following"
                                                           " options:\n"
                                                           "1. Next Page\n"
                                                           "2. Previous Page\n"
                                                           "3. Return to "
                                                           "Customer Menu\n",
                                                           1)
                        if selection[0] == "1":
                            # Stay on page if next does not exist
                            if page >= int(self.op_pro.get_product_list(
                                    page)[1].split(" ")[3]):
                                self.io.show_list(
                                    self.user.user_role, "product",
                                    self.op_pro.get_product_list(page))
                            else:
                                page += 1  # Next page
                                self.io.show_list(
                                    self.user.user_role, "product",
                                    self.op_pro.get_product_list(page))
                        elif selection[0] == "2":
                            # Stay on page if previous does not exist
                            if page <= 1:
                                self.io.show_list(
                                    self.user.user_role, "product",
                                    self.op_pro.get_product_list(page))
                            else:
                                page -= 1  # Previous page
                                self.io.show_list(
                                    self.user.user_role, "product",
                                    self.op_pro.get_product_list(page))
                        elif selection[0] == "3":
                            self.customer_control()
                            break

                else:
                    # Check whether a result was found for keyword
                    result = self.io.show_list(self.user.user_role, "product",
                                               self.op_pro.
                                               get_product_list_by_keyword(
                                                   keyword))

                    if result == []:
                        self.io.print_message("No products found for your "
                                              "keyword.")
                    else:
                        # Show filtered search results
                        result
                flag = False
                self.customer_control()

            elif input[0] == "4":
                # Show Order History
                self.io.print_message("Show Order History")
                page = 1
                result = self.op_order.get_order_list(self.user.user_id, page)
                # Check that orders exist for customer
                if result[0] == []:
                    self.io.print_message("No orders found.")
                    flag = False
                    self.customer_control()
                else:
                    # Show first page of orders
                    self.io.show_list(self.user.user_role, "order",
                                      self.op_order.get_order_list(
                                          self.user.user_id, page))
                while True:
                    selection = self.io.get_user_input("\nPlease select "
                                                       "from the following"
                                                       " options:\n"
                                                       "1. Next Page\n"
                                                       "2. Previous Page\n"
                                                       "3. Return to "
                                                       "Customer Menu\n",
                                                       1)
                    if selection[0] == "1":
                        # Stay on page if next does not exist
                        if page >= int(self.op_order.get_order_list(
                                self.user.user_id, page)[1].split(" ")[3]):
                            self.io.show_list(
                                self.user.user_role, "order",
                                self.op_order.get_order_list(
                                    self.user.user_id, page))
                        else:
                            page += 1  # Next page
                            self.io.show_list(
                                self.user.user_role, "order",
                                self.op_order.get_order_list(
                                    self.user.user_id, page))
                    elif selection[0] == "2":
                        # Stay on page if previous does not exist
                        if page <= 1:
                            self.io.show_list(
                                self.user.user_role, "order",
                                self.op_order.get_order_list(
                                    self.user.user_id, page))
                        else:
                            page -= 1  # Previous page
                            self.io.show_list(
                                self.user.user_role, "order",
                                self.op_order.get_order_list(
                                    self.user.user_id, page))
                    elif selection[0] == "3":
                        self.customer_control()
                        break
                flag = False

            elif input[0] == "5":
                # Generate Statistical Figures
                self.io.print_message("Generating Consumption Figures...")
                self.op_order.generate_single_customer_consumption_figure(
                    self.user.user_id)
                self.op_order.generate_all_customers_consumption_figure()
                self.io.print_message("Figures generated successfully!")
                flag = False
                self.customer_control()

            elif input[0] == "6":
                # Logout
                self.io.print_message("Logged out.")
                flag = False
                self.user = None
                self.login_control()

            else:
                # Loop back
                self.io.print_error_message("IOInterface.get_user_input",
                                            "Invalid input. Please try again."
                                            "\n")

    def admin_control(self):
        """Control the admin process."""

        self.io.admin_menu()
        admin_input = self.io.get_user_input("", 1)

        flag = True
        while flag:

            if admin_input[0] == "1":
                # Show Products
                choice = self.io.get_user_input("Show Products\n\n"
                                                "Please select from the "
                                                "following options:\n"
                                                "1. Show All Products\n"
                                                "2. Show Products by Keyword\n"
                                                "3. Show Product by Product ID"
                                                "\n"
                                                "4. Delete a Product by ID\n"
                                                "5. Return to Admin Menu\n", 1)
                if choice[0] == "1":
                    # Show all first page of products with no filter
                    self.io.show_list(
                        self.user.user_role, "product",
                        self.op_pro.get_product_list(1))
                    page = 1

                    while True:
                        selection = self.io.get_user_input("\nPlease select "
                                                           "from the following"
                                                           " options:\n"
                                                           "1. Next Page\n"
                                                           "2. Previous Page\n"
                                                           "3. Return to "
                                                           "Admin Menu\n",
                                                           1)
                        if selection[0] == "1":
                            # Stay on page if next does not exist
                            if page >= int(self.op_pro.get_product_list(
                                    page)[1].split(" ")[3]):
                                self.io.show_list(
                                    self.user.user_role, "product",
                                    self.op_pro.get_product_list(page))
                            else:
                                page += 1  # Next page
                                self.io.show_list(
                                    self.user.user_role, "product",
                                    self.op_pro.get_product_list(page))
                        elif selection[0] == "2":
                            # Stay on page if previous does not exist
                            if page <= 1:
                                self.io.show_list(
                                    self.user.user_role, "product",
                                    self.op_pro.get_product_list(page))
                            else:
                                page -= 1  # Previous page
                                self.io.show_list(
                                    self.user.user_role, "product",
                                    self.op_pro.get_product_list(page))
                        elif selection[0] == "3":
                            self.admin_control()
                            break

                elif choice[0] == "2":
                    # Show Products by Keyword
                    keyword = self.io.get_user_input("Please enter a keyword "
                                                     "to search for:\n", 1)
                    # Check whether a result was found for keyword
                    result = self.io.show_list(self.user.user_role, "product",
                                               self.op_pro.
                                               get_product_list_by_keyword(
                                                   keyword[0]))

                    if result == []:
                        self.io.print_message("No products found for your "
                                              "keyword.")
                    else:
                        # Show filtered search results
                        result

                elif choice[0] == "3":
                    # Show Product by Product ID
                    product_id = self.io.get_user_input("Please enter a "
                                                        "product ID:\n", 1)
                    # Check whether a result was found for product_id
                    result = self.io.print_message(self.op_pro.
                                                   get_product_by_id(
                                                       product_id[0]))

                    if result == []:
                        self.io.print_message("No products found for your "
                                              "product ID.")
                    else:
                        # Show filtered search results
                        result

                elif choice[0] == "4":
                    # Delete a Product by ID
                    product_id = self.io.get_user_input("Please enter a "
                                                        "product ID:\n", 1)
                    # Check whether a result was found for product_id
                    result = self.io.print_message(self.op_pro.
                                                   get_product_by_id(
                                                       product_id[0]))

                    if result == []:
                        self.io.print_message("No products found for your "
                                              "product ID.")
                    else:
                        # Show filtered search results
                        result
                        # Delete product
                        self.op_pro.delete_product(product_id[0])
                        self.io.print_message("Product deleted successfully!")

                elif choice[0] == "5":
                    # Return to Admin Menu
                    self.admin_control()
                    break

            elif admin_input[0] == "2":
                # Add Customers
                self.io.print_message("Add Customers")
                flag = True
                while flag:
                    # Enter attributes
                    user_name = self.io.get_user_input("\nPlease enter a "
                                                       "username for your new "
                                                       "customer:\n", 1)[0]
                    user_password = self.io.get_user_input("\nPlease enter a "
                                                           "password for your "
                                                           "new customer:\n",
                                                           1)[0]
                    user_email = self.io.get_user_input("\nPlease enter an "
                                                        "email address for "
                                                        "your new customer:\n",
                                                        1)[0]
                    user_mobile = self.io.get_user_input("\nPlease enter a "
                                                         "mobile phone number "
                                                         "for your new "
                                                         "customer:\n", 1)[0]
                    # Create new customer object
                    self.op_cust.register_customer(user_name, user_password,
                                                   user_email, user_mobile)
                    self.io.print_message("\nCustomer added successfully!\n")

                    # Action whether to create another customer
                    go_on = self.io.get_user_input("\nWould you like to add "
                                                   "another customer?\n"
                                                   "1. Yes\n"
                                                   "2. No\n", 1)[0]
                    if go_on == "1":
                        continue
                    elif go_on == "2":
                        flag = False
                        self.admin_control()
                        break

            elif admin_input[0] == "3":
                # Show Customers
                self.io.print_message("Show Customers")
                # Select customer action
                customer_action = self.io.get_user_input("Please select from "
                                                         "the following "
                                                         "options:\n"
                                                         "1. Show All "
                                                         "Customers\n"
                                                         "2. Delete a "
                                                         "Customer by ID\n"
                                                         "3. Return to "
                                                         "Admin Menu\n", 1)[0]
                if customer_action == "1":
                    # Show all customers
                    page = 1
                    self.io.show_list(self.user.user_role, "customer",
                                      self.op_cust.get_customer_list(page))
                    while True:
                        selection = self.io.get_user_input("\nPlease select "
                                                           "from the following"
                                                           " options:\n"
                                                           "1. Next Page\n"
                                                           "2. Previous Page\n"
                                                           "3. Return to "
                                                           "Admin Menu\n",
                                                           1)
                        if selection[0] == "1":
                            # Stay on page if next does not exist
                            if page >= int(self.op_cust.get_customer_list(
                                    page)[1].split(" ")[3]):
                                self.io.show_list(
                                    self.user.user_role, "customer",
                                    self.op_cust.get_customer_list(page))
                            else:
                                page += 1  # Next page
                                self.io.show_list(
                                    self.user.user_role, "customer",
                                    self.op_cust.get_customer_list(page))
                        elif selection[0] == "2":
                            # Stay on page if previous does not exist
                            if page <= 1:
                                self.io.show_list(
                                    self.user.user_role, "customer",
                                    self.op_cust.get_customer_list(page))
                            else:
                                page -= 1  # Previous page
                                self.io.show_list(
                                    self.user.user_role, "customer",
                                    self.op_cust.get_customer_list(page))
                        elif selection[0] == "3":
                            self.admin_control()
                            break

                elif customer_action == "2":

                    # Delete customer by customer ID
                    customer_id = self.io.get_user_input("Please enter a "
                                                         "customer ID:\n",
                                                         1)[0]

                    # Delete Customer
                    deletion = self.op_cust.delete_customer(customer_id)
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

            elif admin_input[0] == "4":
                # Show Orders
                self.io.print_message("Show Orders")

                # Select order action
                order_action = self.io.get_user_input("Please select from "
                                                      "the following "
                                                      "options:\n"
                                                      "1. Show All "
                                                      "Orders\n"
                                                      "2. Delete an "
                                                      "Order by ID\n"
                                                      "3. Return to "
                                                      "Admin Menu\n", 1)[0]

                if order_action == "1":

                    # Show All Orders
                    page = 1
                    result = self.op_order.get_order_list("all", page)
                    # Check that orders exist
                    if result[0] == []:
                        self.io.print_message("No orders found.")
                        flag = False
                        self.admin_control()
                    else:
                        # Show first page of orders
                        self.io.show_list(self.user.user_role, "order",
                                          self.op_order.get_order_list(
                                              "all", page))
                    while True:
                        selection = self.io.get_user_input("\nPlease select "
                                                           "from the following"
                                                           " options:\n"
                                                           "1. Next Page\n"
                                                           "2. Previous Page\n"
                                                           "3. Return to "
                                                           "Admin Menu\n",
                                                           1)
                        if selection[0] == "1":
                            # Stay on page if next does not exist
                            if page >= int(self.op_order.get_order_list(
                                    "all", page)[1].split(" ")[3]):
                                self.io.show_list(
                                    self.user.user_role, "order",
                                    self.op_order.get_order_list(
                                        "all", page))
                            else:
                                page += 1  # Next page
                                self.io.show_list(
                                    self.user.user_role, "order",
                                    self.op_order.get_order_list(
                                        "all", page))
                        elif selection[0] == "2":
                            # Stay on page if previous does not exist
                            if page <= 1:
                                self.io.show_list(
                                    self.user.user_role, "order",
                                    self.op_order.get_order_list(
                                        "all", page))
                            else:
                                page -= 1  # Previous page
                                self.io.show_list(
                                    self.user.user_role, "order",
                                    self.op_order.get_order_list(
                                        "all", page))
                        elif selection[0] == "3":
                            self.admin_control()
                            break

                elif order_action == "2":

                    # Delete an Order by ID
                    order_id = self.io.get_user_input("Please enter an "
                                                      "order ID:\n", 1)[0]

                    # Delete Order
                    deletion = self.op_order.delete_order(order_id)
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

            elif admin_input[0] == "5":
                # Generate Test Data
                self.io.print_message("Generating Test Data...")
                self.op_order.generate_test_order_data()
                self.io.print_message("Test Data Generated Successfully!")
                self.admin_control()
                break

            elif admin_input[0] == "6":
                # Generate All Statistical Figures
                self.io.print_message("Generating Consumption Figures...")
                self.op_order.generate_all_customers_consumption_figure()
                self.op_pro.generate_category_figure()
                self.op_pro.generate_discount_figure()
                self.op_pro.generate_discount_likes_count_figure()
                self.op_pro.generate_likes_count_figure()
                self.io.print_message("Figures generated successfully and "
                                      "saved to data/figure")
                self.admin_control()
                break

            elif admin_input[0] == "7":
                # Delete All Data
                self.io.print_message("Deleting All Data...")
                self.op_pro.delete_all_products()
                self.op_order.delete_all_orders()
                self.op_cust.delete_all_customers()
                self.io.print_message("All Data Deleted Successfully!")
                self.admin_control()
                break

            elif admin_input[0] == "8":
                # Logout
                print("Logged out.")
                flag = False
                self.user = None
                self.login_control()

    def main(self):
        """The main function to start the program"""

        self.op_pro.extract_products_from_files()
        self.login_control()


if __name__ == "__main__":
    main = Main()
    main.main()
