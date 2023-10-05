import datetime
import math
import random
import string
import time
import matplotlib.pyplot as plt

from model_order import Order
from operation_customer import CustomerOperation
from operation_user import UserOperation


class OrderOperation:
    """Contains all the operations related to the order."""

    op_customer = CustomerOperation()
    op_user = UserOperation()

    def generate_unique_order_id(self):
        """Generates a unique order id.
        Arguments: None.
        Return order_id."""
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
        """Creates an order.
        Arguments: customer_id, product_id, create_time.
        Return True/ False to indicate whether creation was successful."""
        order_id = self.generate_unique_order_id()
        # create order object
        order = Order(order_id=order_id, user_id=customer_id,
                      pro_id=product_id, order_time=create_time)
        # write to file
        file = open("data/orders.txt", "a")
        file.write(str(order) + "\n")
        file.close()
        return True
        # return False on exception

    def delete_order(self, order_id):
        """Deletes an order.
        Arguments: order_id.
        Return True/ False to indicate whether deletion was successful."""
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
                return True
        return False

    def get_order_list(self, customer_id, page_number):
        """Retrieve list of orders for a particular customer.
        Arguments: customer_id, page_number.
        Return tuple with a list of order objects, the page number, and the 
        total number of pages."""
        file = open("data/orders.txt", "r")
        order_list = file.readlines()
        file.close()
        orders = []
        for order in order_list:
            if customer_id == "all":
                orders.append(order)
            elif "'user_id':'" + str(customer_id) in order:
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
        return (orders_returned, f"Page {page_number} of {total_page}")

    def generate_test_order_data(self):
        """Randomly generate customers and orders."""

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
        Attributes: customer_id."""

        # Get orders associated with customer from orders.txt with customer_id
        file = open("data/orders.txt", "r")
        order_list = file.readlines()
        file.close()
        customer_orders = []
        for order in order_list:
            if "'user_id':'" + str(customer_id) in order:
                trimmed_order = order.replace(
                    "{", "").replace("}", "").replace("\n", "")
                customer_orders.append(trimmed_order)

        # Create list of orders for each month
        jan_orders = []
        feb_orders = []
        mar_orders = []
        apr_orders = []
        may_orders = []
        jun_orders = []
        jul_orders = []
        aug_orders = []
        sep_orders = []
        oct_orders = []
        nov_orders = []
        dec_orders = []

        # Add orders to their list according to month of order
        for order in customer_orders:
            trimmed_date = order.split(",")[3].split(":", 1)[
                1].replace("'", "")
            order_date = time.strptime(trimmed_date, "%d-%m-%Y_%H:%M:%S")
            month = order_date.tm_mon
            if month == 1:
                jan_orders.append(order)
            elif month == 2:
                feb_orders.append(order)
            elif month == 3:
                mar_orders.append(order)
            elif month == 4:
                apr_orders.append(order)
            elif month == 5:
                may_orders.append(order)
            elif month == 6:
                jun_orders.append(order)
            elif month == 7:
                jul_orders.append(order)
            elif month == 8:
                aug_orders.append(order)
            elif month == 9:
                sep_orders.append(order)
            elif month == 10:
                oct_orders.append(order)
            elif month == 11:
                nov_orders.append(order)
            elif month == 12:
                dec_orders.append(order)

        file = open("data/products.txt", "r")
        product_list = file.readlines()
        file.close()

        # Get January sum of orders
        jan_pro_id_list = []
        jan_price_list = []
        # Get each pro_id for the month
        for order in jan_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            jan_pro_id_list.append(pro_id)
        for pro_id in jan_pro_id_list:
            # Get the cost of each product based off pro_id
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    # get pro_current_price and convert to float
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    jan_price_list.append(price)
        # Get the sum of orders for the month
        jan_orders_sum = sum(jan_price_list)

        # Get February sum of orders as above (refactor if time permits)
        feb_pro_id_list = []
        feb_price_list = []
        for order in feb_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            feb_pro_id_list.append(pro_id)
        for pro_id in feb_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    feb_price_list.append(price)
        feb_orders_sum = sum(feb_price_list)

        # Get March sum of orders as above
        mar_pro_id_list = []
        mar_price_list = []
        for order in mar_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            mar_pro_id_list.append(pro_id)
        for pro_id in mar_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    mar_price_list.append(price)
        mar_orders_sum = sum(mar_price_list)

        # Get April sum of orders as above
        apr_pro_id_list = []
        apr_price_list = []
        for order in apr_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            apr_pro_id_list.append(pro_id)
        for pro_id in apr_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    apr_price_list.append(price)
        apr_orders_sum = sum(apr_price_list)

        # Get May sum of orders as above
        may_pro_id_list = []
        may_price_list = []
        for order in may_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            may_pro_id_list.append(pro_id)
        for pro_id in may_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    may_price_list.append(price)
        may_orders_sum = sum(apr_price_list)

        # Get June sum of orders as above
        jun_pro_id_list = []
        jun_price_list = []
        for order in jun_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            jun_pro_id_list.append(pro_id)
        for pro_id in jun_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    jun_price_list.append(price)
        jun_orders_sum = sum(jun_price_list)

        # Get July sum of orders as above
        jul_pro_id_list = []
        jul_price_list = []
        for order in jul_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            jul_pro_id_list.append(pro_id)
        for pro_id in jul_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    jul_price_list.append(price)
        jul_orders_sum = sum(jul_price_list)

        # Get August sum of orders as above
        aug_pro_id_list = []
        aug_price_list = []
        for order in aug_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            aug_pro_id_list.append(pro_id)
        for pro_id in aug_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    # get pro_current_price and convert to int
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    aug_price_list.append(price)
        aug_orders_sum = sum(aug_price_list)

        # Get September sum of orders as above
        sep_pro_id_list = []
        sep_price_list = []
        for order in sep_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            sep_pro_id_list.append(pro_id)
        for pro_id in sep_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace("{", "").replace(
                        "}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    sep_price_list.append(price)
        sep_orders_sum = sum(sep_price_list)

        # Get October sum of orders as above
        oct_pro_id_list = []
        oct_price_list = []
        for order in oct_orders:
            trimmed_orders = order.replace("{", "").replace(
                "}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            oct_pro_id_list.append(pro_id)
        for pro_id in oct_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace("{", "").replace(
                        "}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    oct_price_list.append(price)
        oct_orders_sum = sum(oct_price_list)

        # Get November sum of orders as above
        nov_pro_id_list = []
        nov_price_list = []
        for order in nov_orders:
            trimmed_orders = order.replace("{", "").replace(
                "}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            nov_pro_id_list.append(pro_id)
        for pro_id in nov_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace("{", "").replace(
                        "}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    nov_price_list.append(price)
        nov_orders_sum = sum(nov_price_list)

        # Get December sum of orders as above
        dec_pro_id_list = []
        dec_price_list = []
        for order in dec_orders:
            trimmed_orders = order.replace("{", "").replace(
                "}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            dec_pro_id_list.append(pro_id)
        for pro_id in dec_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace("{", "").replace(
                        "}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    dec_price_list.append(price)
        dec_orders_sum = sum(dec_price_list)

        # Add sum of each month to dictionary and limit to 2 decimal points
        month_sums = {"January": round(jan_orders_sum, 2),
                      "February": round(feb_orders_sum, 2),
                      "March": round(mar_orders_sum, 2),
                      "April": round(apr_orders_sum, 2),
                      "May": round(may_orders_sum, 2),
                      "June": round(jun_orders_sum, 2),
                      "July": round(jul_orders_sum, 2),
                      "August": round(aug_orders_sum, 2),
                      "September": round(sep_orders_sum, 2),
                      "October": round(oct_orders_sum, 2),
                      "November": round(nov_orders_sum, 2),
                      "December": round(dec_orders_sum, 2)}

        # Generate keys and values to lists for plotting
        month_title = list(month_sums.keys())
        month_values = list(month_sums.values())

        # Plot the graph
        # Clear canvas
        plt.clf()
        plt.tight_layout()
        plt.barh(month_title, month_values, color="cornflowerblue")
        plt.xlabel("Total Order Amount ($)")
        plt.ylabel("Month")
        plt.title("Total Order Amount per Month")
        plt.savefig("data/figure/single_customer_consumption_figure.png")

    def generate_all_customers_consumption_figure(self):
        """Generate chart showing total consumption per month for all 
        customers."""

        # Get orders from orders.txt
        file = open("data/orders.txt", "r")
        order_list = file.readlines()
        file.close()
        all_orders = []
        for order in order_list:
            trimmed_order = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            all_orders.append(trimmed_order)

        # Create list of orders for each month
        jan_orders = []
        feb_orders = []
        mar_orders = []
        apr_orders = []
        may_orders = []
        jun_orders = []
        jul_orders = []
        aug_orders = []
        sep_orders = []
        oct_orders = []
        nov_orders = []
        dec_orders = []

        # Add orders to their list according to month of order
        for order in all_orders:
            trimmed_date = order.split(",")[3].split(":", 1)[
                1].replace("'", "")
            order_date = time.strptime(trimmed_date, "%d-%m-%Y_%H:%M:%S")
            month = order_date.tm_mon
            if month == 1:
                jan_orders.append(order)
            elif month == 2:
                feb_orders.append(order)
            elif month == 3:
                mar_orders.append(order)
            elif month == 4:
                apr_orders.append(order)
            elif month == 5:
                may_orders.append(order)
            elif month == 6:
                jun_orders.append(order)
            elif month == 7:
                jul_orders.append(order)
            elif month == 8:
                aug_orders.append(order)
            elif month == 9:
                sep_orders.append(order)
            elif month == 10:
                oct_orders.append(order)
            elif month == 11:
                nov_orders.append(order)
            elif month == 12:
                dec_orders.append(order)

        file = open("data/products.txt", "r")
        product_list = file.readlines()
        file.close()

        # Get January sum of orders
        jan_pro_id_list = []
        jan_price_list = []
        # Get each pro_id for the month
        for order in jan_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            jan_pro_id_list.append(pro_id)
        for pro_id in jan_pro_id_list:
            # Get the cost of each product based off pro_id
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    # get pro_current_price and convert to float
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    jan_price_list.append(price)
        # Get the sum of orders for the month
        jan_orders_sum = sum(jan_price_list)

        # Get February sum of orders as above (refactor if time permits)
        feb_pro_id_list = []
        feb_price_list = []
        for order in feb_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            feb_pro_id_list.append(pro_id)
        for pro_id in feb_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    feb_price_list.append(price)
        feb_orders_sum = sum(feb_price_list)

        # Get March sum of orders as above
        mar_pro_id_list = []
        mar_price_list = []
        for order in mar_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            mar_pro_id_list.append(pro_id)
        for pro_id in mar_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    mar_price_list.append(price)
        mar_orders_sum = sum(mar_price_list)

        # Get April sum of orders as above
        apr_pro_id_list = []
        apr_price_list = []
        for order in apr_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            apr_pro_id_list.append(pro_id)
        for pro_id in apr_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    apr_price_list.append(price)
        apr_orders_sum = sum(apr_price_list)

        # Get May sum of orders as above
        may_pro_id_list = []
        may_price_list = []
        for order in may_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            may_pro_id_list.append(pro_id)
        for pro_id in may_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    may_price_list.append(price)
        may_orders_sum = sum(apr_price_list)

        # Get June sum of orders as above
        jun_pro_id_list = []
        jun_price_list = []
        for order in jun_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            jun_pro_id_list.append(pro_id)
        for pro_id in jun_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    jun_price_list.append(price)
        jun_orders_sum = sum(jun_price_list)

        # Get July sum of orders as above
        jul_pro_id_list = []
        jul_price_list = []
        for order in jul_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            jul_pro_id_list.append(pro_id)
        for pro_id in jul_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    jul_price_list.append(price)
        jul_orders_sum = sum(jul_price_list)

        # Get August sum of orders as above
        aug_pro_id_list = []
        aug_price_list = []
        for order in aug_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            aug_pro_id_list.append(pro_id)
        for pro_id in aug_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    # get pro_current_price and convert to int
                    trimmed_product = product.replace(
                        "{", "").replace("}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    aug_price_list.append(price)
        aug_orders_sum = sum(aug_price_list)

        # Get September sum of orders as above
        sep_pro_id_list = []
        sep_price_list = []
        for order in sep_orders:
            trimmed_orders = order.replace(
                "{", "").replace("}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            sep_pro_id_list.append(pro_id)
        for pro_id in sep_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace("{", "").replace(
                        "}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    sep_price_list.append(price)
        sep_orders_sum = sum(sep_price_list)

        # Get October sum of orders as above
        oct_pro_id_list = []
        oct_price_list = []
        for order in oct_orders:
            trimmed_orders = order.replace("{", "").replace(
                "}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            oct_pro_id_list.append(pro_id)
        for pro_id in oct_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace("{", "").replace(
                        "}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    oct_price_list.append(price)
        oct_orders_sum = sum(oct_price_list)

        # Get November sum of orders as above
        nov_pro_id_list = []
        nov_price_list = []
        for order in nov_orders:
            trimmed_orders = order.replace("{", "").replace(
                "}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            nov_pro_id_list.append(pro_id)
        for pro_id in nov_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace("{", "").replace(
                        "}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    nov_price_list.append(price)
        nov_orders_sum = sum(nov_price_list)

        # Get December sum of orders as above
        dec_pro_id_list = []
        dec_price_list = []
        for order in dec_orders:
            trimmed_orders = order.replace("{", "").replace(
                "}", "").replace("\n", "")
            pro_id = trimmed_orders.split(",")[2].split(":")[
                1].replace("'", "")
            dec_pro_id_list.append(pro_id)
        for pro_id in dec_pro_id_list:
            for product in product_list:
                if "'pro_id':'" + str(pro_id) in product:
                    trimmed_product = product.replace("{", "").replace(
                        "}", "").replace("\n", "")
                    price = trimmed_product.split(",")[4].split(":")[
                        1].replace("'", "")
                    price = float(price)
                    dec_price_list.append(price)
        dec_orders_sum = sum(dec_price_list)

        # Add sum of each month to dictionary and limit to 2 decimal points
        month_sums = {"January": round(jan_orders_sum, 2),
                      "February": round(feb_orders_sum, 2),
                      "March": round(mar_orders_sum, 2),
                      "April": round(apr_orders_sum, 2),
                      "May": round(may_orders_sum, 2),
                      "June": round(jun_orders_sum, 2),
                      "July": round(jul_orders_sum, 2),
                      "August": round(aug_orders_sum, 2),
                      "September": round(sep_orders_sum, 2),
                      "October": round(oct_orders_sum, 2),
                      "November": round(nov_orders_sum, 2),
                      "December": round(dec_orders_sum, 2)}

        # Generate keys and values to lists for plotting
        month_title = list(month_sums.keys())
        month_values = list(month_sums.values())

        # Plot the graph
        # Clear canvas
        plt.clf()
        plt.tight_layout()
        plt.barh(month_title, month_values, color="cornflowerblue")
        plt.xlabel("Total Order Amount ($)")
        plt.ylabel("Month")
        plt.title("Total Order Amount per Month")
        plt.tight_layout()
        plt.savefig("data/figure/all_customers_consumption_figure.png")

    def delete_all_orders(self):
        """Delete all orders from orders.txt."""

        file = open("data/orders.txt", "w")
        file.write("")
        file.close()
