import math
import random
import string
import time

from model_order import Order
from operation_customer import CustomerOperation
from operation_user import UserOperation


class OrderOperation:
    """Contains all the operations related to the order"""

    op_customer = CustomerOperation()
    op_user = UserOperation()

    def generate_unique_order_id(self):
        """Generates a unique order id
        Arguments: None
        Return order_id"""
        while True:
            order_id = "0_" + str(random.randint(10000, 99999))
            file = open("data/orders.txt", "r")
            data_string = file.read()
            file.close()
            # Check if user_id exists in users.txt
            if order_id not in data_string:
                break
        return order_id

    def create_an_order(self, customer_id, product_id,
                        create_time=time.strftime("%d-%m-%Y_%H:%M:%S")):
        """Creates an order
        Arguments: customer_id, product_id, create_time
        Return True/ False to indicate whether creation was successful"""
        order_id = self.generate_unique_order_id()
        # create order object
        order = Order(order_id=order_id, user_id=customer_id,
                      pro_id=product_id, order_time=create_time)
        # write to file
        file = open("data/orders.txt", "a")
        file.write(str(order) + "\n")
        file.close()
        #  print("Success! Order created.")
        return True
        # return False on exception

    def delete_order(self, order_id):
        """Deletes an order
        Arguments: order_id
        Return True/ False to indicate whether deletion was successful"""
        file = open("data/orders.txt", "r")
        order_list = file.readlines()
        file.close()
        for order in order_list:
            # Check if order exists
            if "'order_id':'" + str(order_id) in order:
                order_list.remove(order)
                file = open("data/orders.txt", "w")
                file.writelines(order_list)
                file.close()
                print("Success! Order deleted.")
                return True
        print("Order not found!")
        return False

    def get_order_list(self, customer_id, page_number):
        """Retrieve list of orders for a particular customer
        Arguments: customer_id, page_number
        Return tuple with a list of order objects, the page number, and the 
        total number of pages"""
        file = open("data/orders.txt", "r")
        order_list = file.readlines()
        file.close()
        orders = []
        for order in order_list:
            if "'user_id':'" + str(customer_id) in order:
                orders.append(order)
        # Calculate total number of pages
        total_page = math.ceil(len(orders) / 10)
        # First order on page
        low_order = (page_number * 10) - 10
        # Last order on page
        if total_page > 1:
            high_order = (page_number * 10) - 1
        else:
            high_order = len(orders) - 1
        # Return a tuple containing a list of orders, current page number, and
        # total pages
        orders_returned = orders[low_order:high_order + 1]
        return (orders_returned, page_number, total_page)

    def generate_test_order_data(self):
        """Randomly generate customers and orders"""

        # Randomly generate 10 customers
        for i in range(10):
            # Generate random string username
            user_name = ""
            for i in range(5):
                char = random.choice(string.ascii_letters)
                user_name += char

            # Generate random password
            user_password_list = []
            user_password = ""
            # Generate random letters
            for i in range(5):
                char = random.choice(string.ascii_letters)
                user_password_list.append(char)
            # Generate random integers
            for i in range(5):
                i = random.randint(0, 9)
                user_password_list.append(str(i))
            # Randomise the order of the list
            user_password_list = random.sample(
                user_password_list, len(user_password_list))
            # Convert list to string
            for character in user_password_list:
                user_password += character

            # Use randomly generated user_name to create unique email
            user_email = f"{user_name.lower()}@mail.com"

            # Generate random mobile number
            mobile_random = random.randint(10000000, 99999999)
            user_mobile = f"04{mobile_random}"

            # Register customer with the given random attributes
            self.op_customer.register_customer(user_name, user_password,
                                               user_email, user_mobile)

            # Read users into list
            file = open("data/users.txt", "r")
            user_list = file.readlines()
            file.close()

            # Read products into list
            file = open("data/products.txt", "r")
            product_list = file.readlines()
            file.close()

            # Create 50-200 random orders for each customer
            for i in range(random.randint(50, 200)):
                for user in user_list:
                    # Remove curly braces from user string
                    user.replace("{", "").replace("}", "")
                    # Get customer_id value based off user_name
                    if (f"'user_name':'{user_name}'" in user):
                        param_list = user.split(",")
                        customer_id = param_list[0].split(
                            ":")[1].replace("'", "")
                        break
                    else:
                        continue
                # Get product_id
                random_product = random.choice(product_list)
                random_product.replace("{", "").replace("}", "")
                param_list = random_product.split(",")
                product_id = param_list[0].split(":")[1].replace("'", "")

                # Get create_time
                month = random.randint(1, 12)
                day = random.randint(1, 28)
                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                create_time = f"{day}-{month}-2023_{hour}:{minute}:{second}"

                # Create random order
                self.create_an_order(customer_id, product_id, create_time)

    def generate_single_customer_consumption_figure(self, customer_id):
        """Generate a graph to show the user's consumption over 12 months
        Attributes: customer_id"""
        # get the customer from users.txt with customer_id (user_id)
        # get associated orders from orders.txt with user_id
        # Group orders into 12 monthly lists
        # get cost of orders from product.txt with pro_id
        # Add sum of orders for each month
        # Graph with matplotlib
        