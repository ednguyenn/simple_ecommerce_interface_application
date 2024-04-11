import time, math, string, random

from operation_customer import CustomerOps
from operation_user import UserOps
from model_customer import Customer
from model_order import Order

import matplotlib.pyplot as plt

class OrderOps:
    def __init__(self):
        pass
    def generate_unique_order_id(self):
        """
        This method is used to generate and return a 5 digit unique order id
        starting with “o_” every time when a new order is created. All the
        order information is saved inside the database. It is required to check
        this file when generating a new order id to make sure there is no
        duplicate.
        :return: This method returns a string result such as o_12345.

        """
        try:
            with open('data/orders.txt', 'r') as file:
                lines= file.readlines()
                orders = [eval(line) for line in lines]
                while True:
                    five_digits_number = ''.join(str(random.randint(0, 9)) for _ in range(5))
                    unique_order_id = 'o_' + five_digits_number
                    if unique_order_id not in (order['order_id'] for order in orders):
                        return unique_order_id

            return unique_order_id
        except Exception as e:
            return False
    def create_an_order(self,customer_id,product_id, order_time,order_price):
        """
        Every time creating a new order, a unique order id needs to be
        generated. Use the time library to get the current time. The order
        data is saved into the data/orders.txt file.

        :param customer_id:
        :param product_id:
        :param create_time:
        :return:True/False
        """

        order_id= self.generate_unique_order_id()
        new_order = Order(order_id=order_id, user_id=customer_id, product_id=product_id, order_time=order_time,order_price=order_price)
        try:
            with open('data/orders.txt', 'a') as file:
                file.write(str(new_order) + '\n')
            return True
        except Exception as e:
            return False
        
    def delete_order(self, order_id):
        """
        This method deletes the order info from the data/orders.txt file based on the provided order_id.
        :return: True/False
        """
        # Read the file
        with open('data/orders.txt', 'r') as file:
            lines = file.readlines()

        # Iterate over lines and parsing them as dictionaries
        updated_lines = []
        deleted = False

        for line in lines:
            obj = eval(line)
            if obj['order_id'] == order_id:
                deleted = True
                continue
            updated_lines.append(obj)
        if not deleted:  # could not find the provided order ID
            return False
        # rewrite the file without the one just deleted
        with open('data/orders.txt', 'w') as file:
            file.writelines([str(line) + "\n" for line in updated_lines])
        return True

    def get_order_list(self, customer_id, page_number):
        """
        This method retrieves one page of orders from the database which
        belongs to the given customer. One page contains a maximum of 10 items.
        :param customer_id:
        :param page_number:
        :return:This function returns a tuple including a list of order objects and the total number of pages.
        For example, ([Order(), Order(), Order()...],page_number, total_page).
        """
        try:
            with open('data/orders.txt', 'r') as file:
                lines = file.readlines()
                orders = [eval(line) for line in lines]

                order_list = [order for order in orders if order['user_id']==customer_id ]

                #this is a first index in a requested page and total pages
                starting_index = (int(page_number)-1)*10
                total_pages = math.ceil(len(order_list) / 10)

                order_page =[]
                #print out the list of 10 objects with a given page number
                for _ in range(10):
                    order_page.append(order_list[starting_index])
                    starting_index +=1
                    if starting_index == len(order_list):
                        return order_page, page_number, total_pages

                return order_page,page_number,total_pages
        except Exception as e:
            return [], 1, 1  # Return empty list and default page numbers in case of an error

    def generate_test_order_data(self):
        """
        create 10 customers and randomly generate 50 to 200 orders for each customer
        """

        def generate_random_order_time():
            """
            Generate a random order time across different months of the year.
            """
            month = random.randint(1, 12)  # Random month
            day = random.randint(1, 28)  # Random day
            hour = random.randint(0, 23)  # Random hour
            minute = random.randint(0, 59)  # Random minute
            second = random.randint(0, 59)  # Random second
            year = time.localtime().tm_year  # Current year
            order_time = time.strftime("%d-%m-%Y_%H:%M:%S", (year, month, day, hour, minute, second, 0, 0, -1))
            return order_time


        def create_random_customer():
            """create random customer then register in files"""
            user_name = "user" + ''.join(random.choices(string.ascii_lowercase, k=4))       #create randome username
            user_password = "password" + str(random.randint(1000, 9999))        #random password
            user_email = f"{user_name}@testdata.com"            #randome email
            user_mobile = "04" + ''.join([str(random.randint(0, 9)) for _ in range(8)])     #random mobile

            user_ops = UserOps()
            user_id = user_ops.generate_unique_user_id()        #create user_id
            user_register_time = time.strftime("%d-%m-%Y_%H:%M:%S")

            customerops= CustomerOps()
            new_customer = Customer(user_id=user_id, user_name=user_name, user_password=user_password,
                                user_register_time=user_register_time, user_role="customer", user_email=user_email,
                                user_mobile=user_mobile)
            # register a new customer into file
            with open('data/users.txt', 'a') as file:
                    file.write(str(new_customer) + '\n')
            return user_id              #return a user_id as an argument for the next function



        def generate_orders_for_customer(customer_id):
            """
            Generate random orders for a given customer.
            """
            num_orders = random.randint(50, 200)  # Random number of orders between 50 and 200
            try:
                with open('data/products.txt') as file:
                    lines = file.readlines()
                    products = [eval(line) for line in lines]
                    #create a list of tuples holding pro_id and corresponding current price
                    set_pro_id_and_price = [ (product['pro_id'],product['pro_current_price']) for product in products]

                    #create a list of orders
                    for _ in range(num_orders):
                        order_time = generate_random_order_time()
                        product_id, order_price = random.choice(set_pro_id_and_price)

                        self.create_an_order(customer_id=customer_id, order_time=order_time,product_id=product_id,order_price=order_price)

            except Exception as e:
                return False

        for _ in range(10):
            new_customer = create_random_customer()     #create a random customer
            generate_orders_for_customer(customer_id=new_customer)      #generate 50-200 orders for this customer


    def generate_single_customer_consumption_figure(self,customer_id):
        """
        generate a bar chart to show the consumption(sum of
        order price) of 12 different months (only consider month value,
        ignore year) for the given customer
        """
        with open('data/orders.txt') as file:
            lines = file.readlines()
            orders = [eval(line) for line in lines]

        #generate a list of orders from a given customer
        customer_orders = []
        for order in orders:
            if order['user_id'] == customer_id:
                customer_orders.append(order)

        #create a dictionary to hold a sum of order price with corresponding months
        montly_consumption={}
        for order in customer_orders:
            month = order['order_time'][3:5]   #extract the month value in the order_time string
            order_price = order['order_price']
            if month in montly_consumption:
                montly_consumption[month] += order_price
            else:
                montly_consumption[month] = order_price

        #sort month in the ascending order
        sorted_monthly_consumption = sorted(montly_consumption.items(), key=lambda x: x, reverse=False)

        months = [item[0] for item in sorted_monthly_consumption]
        consumption = [item[1] for item in sorted_monthly_consumption]

        # using Bar() to plot line chart
        plt.bar(months, consumption, linewidth=1.5)

        # Add labels and title
        plt.xlabel('Month')
        plt.ylabel('Total consumption in dollar')
        plt.title('Customer monthly consumption figure')

        plt.savefig(f'data/figure/customer_{customer_id}_consumption_figure.png')
        plt.show()



    def generate_all_customers_consumption_figure(self):
        """
        a graph(any type of chart) to show the consumption(sum of
        order price) of 12 different months (only consider month value,
        ignore year) for all customers.
        """
        with open('data/orders.txt') as file:
            lines = file.readlines()
            orders = [eval(line) for line in lines]

        montly_consumption = {}
        for order in orders:
            month = order['order_time'][3:5]  # extract the month value in the order_time string
            order_price = order['order_price']
            if month in montly_consumption:
                montly_consumption[month] += order_price
            else:
                montly_consumption[month] = order_price

        # sort month in the ascending order
        sorted_monthly_consumption = sorted(montly_consumption.items(), key=lambda x: x, reverse=False)

        months = [item[0] for item in sorted_monthly_consumption]
        consumption = [item[1] for item in sorted_monthly_consumption]

        # using Bar() to plot line chart
        plt.bar(months, consumption, linewidth=1.5)

        # Add labels and title
        plt.xlabel('Month')
        plt.ylabel('Total consumption in dollar')
        plt.title('All customer monthly consumption figure')

        plt.savefig(f'data/figure/all_customer_consumption_figure.png')
        plt.show()

    def generate_all_top_10_best_sellers_figure(self):
        """
        Generate pie chart to show the top 10 best-selling products and sort
        the result in descending order.
        """
        with open('data/orders.txt') as file:
            lines = file.readlines()
            orders = [eval(line) for line in lines]

        #create a dictionary to hold counts of all products that are ordered
        product_sold = {}
        for order in orders:
            product = int(order['product_id'])
            if product in product_sold:
                product_sold[product] +=1
            else:
                product_sold[product] =1

        # Sort the dictionary items based on their values (counts) in descending order
        sorted_product_sold = sorted(product_sold.items(), key=lambda x: x[1], reverse=True)

        # Take only the top 10 product into a new dictionary, keys are product_id
        top_10_best_sellers_ids = dict(sorted_product_sold[:10])

        #create a list of set holding product id and corresponding product name
        with open('data/products.txt', 'r',encoding='utf-8') as file:
            lines = file.readlines()
            product_ids_names = {eval(line)['pro_id']: eval(line)['pro_name'] for line in lines}

        #create a top 10 best sellers dictionary with keys are product names
        top_10_best_sellers ={}
        for product_id, count in top_10_best_sellers_ids.items():
            if product_id in product_ids_names:
                product_name= product_ids_names[product_id]
                top_10_best_sellers[product_name] = count


        #sorted best sellers in descending order
        sorted_best_sellers = sorted(top_10_best_sellers.items(), key=lambda x: x[1], reverse=True)

        #extract product names and number of sold items for each product for bar chart
        product_name = [item[0] for item in sorted_best_sellers]
        numbers_sold = [item[1] for item in sorted_best_sellers]

        # using pie() to plot line chart
        plt.pie(numbers_sold, labels=product_name)

        plt.title('Top 10 best sellers')

        plt.savefig('data/figure/top_10_best_sellers_figure.png')
        plt.show()


    def delete_all_orders(self):
        """
        This method removes all the data in the data/orders.txt file.
        """
        with open('data/orders.txt', 'w') as file:
            file.truncate(0)

