class IOInterface:
    """Handle all input and output to the user."""

    def get_user_input(self, message, num_of_args):
        """Receive user input.
        Arguments: message, num_of_args.
        Return a list of three strings (args)."""

        user_input = input(f"{message}")
        args = user_input.split(" ")
        while len(args) < num_of_args:
            args.append("")
        return args[:num_of_args]

    def main_menu(self):
        """Display the main menu."""

        print("\nWelcome to PyCommerce!\n\n"
              "Please select one of the following options by entering the "
              "number associated with your selection:\n"
              "1. Login\n"
              "2. Register\n"
              "3. Quit\n")

    def admin_menu(self):
        """Display the admin menu."""

        print("\nWelcome, admin!\n\n"
              "Please select one of the following options by entering the "
              "number associated with your selection:\n"
              "1. Show Products\n"
              "2. Add Customers\n"
              "3. Show Customers\n"
              "4. Show Orders\n"
              "5. Generate Test Data\n"
              "6. Generate All Statistical Figures\n"
              "7. Delete All Data\n"
              "8. Logout\n")

    def customer_menu(self):
        """Display the customer menu."""

        print("\nWelcome, customer!\n\n"
              "Please select one of the following options by entering the "
              "number associated with your selection:\n"
              "1. Show Profile\n"
              "2. Update Profile\n"
              "3. Show Products (if you would like to enter a particular "
              "search keyword, please enter 3 followed by a space, then your "
              "keyword)\n"
              "4. Show Order History\n"
              "5. Generate All Consumption Figures\n"
              "6. Logout\n")

    def show_list(self, user_role, list_type, object_list):
        """Print a customer, order or product list.
        Arguments: user_role, list_type, object_list."""

        if user_role == "admin":
            if list_type == "customer":
                print("\nCustomer List:\n")
                if object_list == []:
                    return []
                else:
                    for customer in object_list:
                        if type(customer) == list:
                            for cust in customer:
                                print(cust)
                        else:
                            print(customer)
            elif list_type == "order":
                print("\nOrder List:\n")
                if object_list == []:
                    return []
                else:
                    for order in object_list:
                        if type(order) == list:
                            for o in order:
                                print(o)
                        else:
                            print(order)
            elif list_type == "product":
                print("\nProduct List:\n")
                if object_list == []:
                    return []
                else:
                    for product in object_list:
                        if type(product) == list:
                            for pro in product:
                                print(pro)
                        else:
                            print(product)
        elif user_role == "customer":
            if list_type == "order":
                print("\nOrder History:\n")
                if object_list == []:
                    return []
                else:
                    for order in object_list:
                        if type(order) == list:
                            for o in order:
                                print(o)
                        else:
                            print(order)
            elif list_type == "product":
                print("\nProduct List:\n")
                if object_list == []:
                    return []
                else:
                    for product in object_list:
                        if type(product) == list:
                            for pro in product:
                                print(pro)
                        else:
                            print(product)

    def print_error_message(self, error_source, error_message):
        """Print error message to show where error has occurred.
        Arguments: error_source, error_message."""

        print(f"\n{error_source} Error: {error_message}\n")

    def print_message(self, message):
        """Print a message to the user.
        Arguments: message."""

        print(f"\n{message}\n")

    def print_object(self, target_object):
        """Print an object.
        Arguments: object."""

        print(f"\n{target_object}\n")
