from operation_customer import CustomerOps
from operation_order import OrderOps
from operation_product import ProductOps
from operation_admin import AdminOps
from io_interface import IOInterface
from operation_user import UserOps

#create multiple operation instances for the system
adminops = AdminOps()
userops = UserOps()
customerops = CustomerOps()
orderops = OrderOps()
productops = ProductOps()
ioops = IOInterface()
def login_control():
    while True:
        ioops.print_message(message="Log in to your account")
        username = ioops.get_user_input(message="Username: ",
                                        num_of_args=1)[0]
        password = ioops.get_user_input(message="Password: ",
                                        num_of_args=1)[0]

        user_data = userops.login(username, password)
        if user_data:
            ioops.print_message(message="Login successful")
            if user_data['user_role'] == "customer":
                customer_control(user_data=user_data)
            elif user_data['user_role'] == "admin":
                admin_control(user_data=user_data)
            else:
                ioops.print_error_message(error_source="operation_user.login",
                                          error_message="User does not have access to the system")
                continue
        else:
            ioops.print_error_message(error_source="operation_user.login",
                                      error_message="Invalid username or password")
            continue
def customer_control(user_data):
    while True:
        ioops.customer_menu()
        action = ioops.get_user_input(message="Enter your action: ",
                                      num_of_args=1)[0]

        #show profile
        if action == '1':
            ioops.print_message(message="Below is your user details \n")
            ioops.print_object(user_data)
        #update profile
        elif action=='2':
            ioops.print_message(message="Update your details: \n")
            while True:
                #get attribute_name
                attribute_name=ioops.get_user_input(message="Which filed would you like to change ('user_name', 'user_password', 'user_email' or 'user_mobile')?: ",
                                                    num_of_args=1)[0]
                #validate attribute name
                if attribute_name not in  ['user_name', 'user_password', 'user_email' ,'user_mobile']:
                    ioops.print_error_message(error_source="main.customer_control",
                                              error_message="Invalid attribute name")
                    continue
                #get new value for entered attribute
                value = ioops.get_user_input(message="New value: ",num_of_args=1)[0]
                if customerops.update_profile(attribute_name=attribute_name, value=value, customer_object=user_data) == True:
                    ioops.print_message(message="Updated customer details")
                    break
                else:
                    ioops.print_error_message(error_source="operation_customer.update_profile",
                                              error_message="invalid value")
                    continue
        #show product list
        elif action =='3':

            while True:
                product_list = productops.get_product_list(1)
                ioops.print_message(message=f"The product list has {product_list[2]} pages")
                ioops.print_message(message=
                                    """
                                    You have the following options:
                                    (1). Enter a page number to view list
                                    (2). Find a list of product by keyword
                                    (3). Find a product by product_id
                                    """)
                s_action = ioops.get_user_input(message="Enter your action: ",
                                                  num_of_args=1)[0]
                if s_action.lower() == 'back':
                    break
                #get_product_list
                if s_action =='1':
                    #enter the page to view the product list
                    while True:
                        page_number = ioops.get_user_input(message="Enter the page number to view (type 'back' to go back): ",
                                                               num_of_args=1)[0]
                        if page_number.lower() =='back':
                            ioops.print_message(message="Exiting product search.")
                            break

                        if int(page_number) >product_list[2]:
                            ioops.print_error_message(error_source="main.customer_control",
                                                      error_message="Page you entered is out of range")
                            continue
                        else:
                            ioops.show_list(user_role="customer",
                                            list_type="Product",
                                            object_list=productops.get_product_list(page_number=int(page_number)))
                            continue

                #get product list by keyword
                elif s_action=='2':
                    while True:
                        keyword = ioops.get_user_input(message="Enter the keyword (type 'back' to go back): ",
                                                       num_of_args=1)[0]

                        # Check if the user wants to exit
                        if keyword.lower() == 'back':
                            ioops.print_message(message="Exiting product search.")
                            break

                        product_keyword_list = productops.get_product_list_by_keyword(keyword=keyword)

                        if not product_keyword_list:
                            ioops.print_message(message=f"No products found for keyword '{keyword}'.\n")
                        else:
                            ioops.print_message(message=f"Here is your product list by keyword '{keyword}' : \n")
                            for product in product_keyword_list:
                                ioops.print_object(product)
                                ioops.print_message(message="\n")
                #get product by id
                elif s_action=='3':
                    while True:
                        try:
                            product_id=ioops.get_user_input(message="Enter the product_id (type 'back' to go back): ",
                                                            num_of_args=1)[0]
                            if product_id.lower() == 'back':
                                ioops.print_message(message="Exiting product search")
                                break

                            if productops.get_product_by_id(product_id=int(product_id)) is not None:
                                found_product=productops.get_product_by_id(int(product_id))
                                ioops.print_object(found_product)

                            else:
                                ioops.print_message("No product_id found")
                        except ValueError:
                            ioops.print_message("Invalid input! Please enter a valid integer for product_id.")

                else:
                    ioops.print_error_message(error_source="main.customer_control",
                                              error_message="Invalid action")
                    continue


        # show history orders
        elif action=='4':
            order_list = orderops.get_order_list(customer_id=user_data['user_id'],page_number=1)
            #show order list
            ioops.show_list(user_role="customer",
                            list_type="Order",
                            object_list=order_list)
            while True:
                page_number = ioops.get_user_input(message="Enter the page number to view (type 'back' to go back): ",
                                                       num_of_args=1)[0]
                if page_number.lower() == 'back':
                    ioops.print_message(message="Exiting order search.")
                    break

                if int(page_number) > order_list[2]:
                    ioops.print_error_message(error_source="main.customer_control",
                                              error_message="Page you entered is out of range")
                    continue
                else:
                    ioops.show_list(user_role="customer",
                                    list_type="Order",
                                    object_list=orderops.get_order_list(customer_id=user_data['user_id'],
                                                                        page_number=int(page_number)))
                    continue

        #Generate all consumption figures
        elif action=='5':
            ioops.print_message("A figure for your consumption in this account was generated \n ")
            #generate this customer consumption figure
            orderops.generate_single_customer_consumption_figure(customer_id=user_data['user_id'])

            ioops.print_message(message="A figure for current top 10 best sellers was generated \n ")
            #generate all top 10 best sellers figures
            orderops.generate_all_top_10_best_sellers_figure()

        elif action =='6':
            ioops.print_message(message="Logged out successfully")
            login_control()
        else:
            ioops.print_error_message(error_source="main.customer_control",
                                      error_message="Invalid action")
            return True



def admin_control(user_data):

    while True:
        ioops.admin_menu()
        action = ioops.get_user_input(message="Enter your action: ", num_of_args=1)[0]
        if action.lower() == 'back':
            break
        if action == '1':
            #show products
            while True:
                product_list = productops.get_product_list(1)
                ioops.print_message(message=f"The product list has {product_list[2]} pages")
                ioops.print_message(message=
                                    """
                                    You have the following options:
                                    (1). Enter a page number to view list
                                    (2). Find a list of product by keyword
                                    (3). Find a product by product_id
                                    (4). Delete a product
                                    """)

                s_action = ioops.get_user_input(message="Enter your action: ",
                                              num_of_args=1)[0]
                if s_action.lower() == 'back':
                    break
                # get_product_list
                if s_action == '1':
                    # enter the page to view the product list
                    while True:
                        page_number = ioops.get_user_input(message="Enter the page number to view (type 'back' to go back): ",
                                             num_of_args=1)[0]
                        if page_number.lower() == 'back':
                            ioops.print_message(message="Exiting product search.")
                            break

                        if int(page_number) > product_list[2]:
                            ioops.print_error_message(error_source="main.admin_control",
                                                      error_message="Page you entered is out of range")
                            continue
                        else:
                            ioops.show_list(user_role="admin",
                                            list_type="Product",
                                            object_list=productops.get_product_list(page_number=int(page_number)))
                            continue

                # get product list by keyword
                elif s_action == '2':
                    while True:
                        keyword = ioops.get_user_input(message="Enter the keyword (type 'back' to go back): ",
                                                       num_of_args=1)[0]

                        # Check if the user wants to exit
                        if keyword.lower() == 'back':
                            ioops.print_message(message="Exiting product search.")
                            break

                        product_keyword_list = productops.get_product_list_by_keyword(keyword=keyword)

                        if not product_keyword_list:
                            ioops.print_message(message=f"No products found for keyword '{keyword}'.\n")
                        else:
                            ioops.print_message(message=f"Here is your product list by keyword '{keyword}' : \n")
                            for product in product_keyword_list:
                                ioops.print_object(product)
                                ioops.print_message(message="\n")
                # get product by id
                elif s_action == '3':
                    while True:
                        try:
                            product_id = ioops.get_user_input(message="Enter the product_id (type 'back' to go back): ",
                                                              num_of_args=1)[0]
                            if product_id.lower() == 'back':
                                ioops.print_message(message="Exiting product search")
                                break

                            if productops.get_product_by_id(product_id=int(product_id)) is not None:
                                found_product = productops.get_product_by_id(int(product_id))
                                ioops.print_object(found_product)

                            else:
                                ioops.print_message("No product_id found")
                        except ValueError:
                            ioops.print_message("Invalid input! Please enter a valid integer for product_id.")
                elif s_action == '4':
                    while True:
                        product_id = ioops.get_user_input(message="Enter the product_id you want to delete: (type 'back' to go back) ",
                                                          num_of_args=1)[0]
                        if product_id.lower() == 'back':
                            break
                        if productops.delete_product(product_id=int(product_id)) is True:
                            ioops.print_message("Product has been deleted")
                        else:
                            ioops.print_error_message(error_source="operation_product.delete_product", error_message="Could not delete product")

                else:
                    ioops.print_error_message(error_source="main.admin_control",
                                              error_message="Invalid action")
                    continue
        #add a customer into the system
        elif action=='2':

            ioops.print_message(message="Add a customer account below: ")

            while True:
                # Get username and validate
                user_name = ioops.get_user_input(message="username: ", num_of_args=1)[0]
                if not userops.validate_username(user_name):
                    ioops.print_error_message(error_source="operation_user.validate_username",
                                              error_message="The name should only contain letters or underscores, and its length should be at least 5 characters.")
                    continue

                if userops.check_username_exist(user_name):
                    ioops.print_error_message(error_source="operation_user.check_username_exist",
                                              error_message="username already exists")
                    continue
                else:
                    ioops.print_message(message="username available")

                    # Get password and validate
                    while True:
                        user_password = ioops.get_user_input(message="password: ", num_of_args=1)[0]
                        if not userops.validate_password(user_password):
                            ioops.print_error_message(error_source="operation_user.validate_password",
                                                      error_message="The password should contain at least one letter and one number. The length of the password must be greater than or equal to 5 characters.")
                            continue
                        else:
                            ioops.print_message(message="valid password")
                            break  # Exit password loop if password is valid

                    # Get email and mobile number
                    while True:
                        user_email = ioops.get_user_input(message="Enter your email address: ", num_of_args=1)[0]
                        if not customerops.validate_email(user_email):
                            ioops.print_error_message(error_source="operation_customer.validate_email",
                                                      error_message="Invalid email")
                            continue

                        user_mobile = ioops.get_user_input(message="Enter your mobile number: ", num_of_args=1)[0]
                        if not customerops.validate_mobile(user_mobile):
                            ioops.print_error_message(error_source="operation_customer.validate_mobile",
                                                      error_message="Invalid mobile number")
                            continue

                        # Register customer
                        if not customerops.register_customer(user_name=user_name, user_password=user_password,
                                                             user_mobile=user_mobile, user_email=user_email):
                            ioops.print_error_message(error_source="operation_customer.register_customer",
                                                      error_message="Could not register customer account")
                        else:
                            ioops.print_message(message="Successfully registered")
                            admin_control(user_data)
                            break  # Exit registration loop
        #show customer list
        elif action=='3':
            customer_list = customerops.get_customer_list(page_number=1)
            # show customer list
            ioops.show_list(user_role="admin",
                            list_type="Customer",
                            object_list=customer_list)
            while True:
                page_number = ioops.get_user_input(message="""
                Enter the page number to view customer page
                (type 'delete' to delete customer by customer id)
                (type 'back' to go back): 
                """,
                num_of_args=1)[0]
                if page_number.lower() == 'back':
                    break
                #delete a customer
                if page_number.lower() == 'delete':
                    while True:
                        customer_id = ioops.get_user_input(message="Enter the customer_id you want to delete: (type 'back' to go back) ",
                                                          num_of_args=1)[0]
                        if customer_id.lower() == 'back':
                            break
                        if customerops.delete_customer(customer_id=customer_id) is True:
                            ioops.print_message("Customer has been deleted")
                        else:
                            ioops.print_error_message(error_source="operation_customer.delete_customer", error_message="Could not delete customer")
                    break

                try:
                    page_number = int(page_number)
                    if page_number > customer_list[2]:
                        ioops.print_error_message(error_source="main.admin_control",
                                                  error_message="Page you entered is out of range")
                        continue
                    else:
                        customer_list = customerops.get_customer_list(page_number=page_number)
                        #show the list with the enter page number
                        ioops.show_list(user_role="admin",
                                        list_type="Customer",
                                        object_list=customer_list)
                        continue
                except ValueError:
                    ioops.print_error_message(error_source="main.admin_control",
                                              error_message="Invalid page number. Please enter a valid page number.")
                    continue
        #show orderes
        elif action=='4':
            ioops.print_message("To get orders list, please enter the customer_id below !")
            while True:
                customer_id = ioops.get_user_input(message="Enter the customer_id (type 'back' to go back) ",
                                                   num_of_args=1)[0]
                while True:
                    order_list = orderops.get_order_list(page_number=1,customer_id=customer_id)
                    ioops.print_message(message=f"The order list for customer {customer_id} has {order_list[2]} pages")


                    page_number = ioops.get_user_input(message="""
                    Enter the page number to view order page
                    (type 'delete' to delete order by order_id)
                    (type 'back' to go back): 
                    """,
                    num_of_args=1)[0]
                    if page_number.lower() == 'back':
                        break
                    # delete an order
                    if page_number.lower() == 'delete':
                        while True:
                            order_id = ioops.get_user_input(
                                message="Enter the order_id you want to delete: (type 'back' to go back) ",
                                num_of_args=1)[0]
                            if order_id.lower() == 'back':
                                break
                            if orderops.delete_order(order_id=order_id) is True:
                                ioops.print_message("Order has been deleted")
                            else:
                                ioops.print_error_message(error_source="operation_order.delete_order",
                                                          error_message="Could not delete order")
                        break

                    if int(page_number) > order_list[2]:
                        ioops.print_error_message(error_source="main.admin_control",
                                                  error_message="Page you entered is out of range")
                        continue
                    else:
                        ioops.show_list(user_role="admin",
                                        list_type="Order",
                                        object_list=orderops.get_order_list(customer_id=customer_id,
                                                                            page_number=int(page_number)))
                        continue

        # generate test data
        elif action=='5':
            ioops.print_message(message="Generating test data... please wait ...")

            #extract the product data before generate_test_order_data
            productops.extract_products_from_files()

            if orderops.generate_test_order_data() == False:
                ioops.print_error_message(error_source="operation_order.generate_test_order_data", error_message="Could not generate test order data.")
            else:
                ioops.print_message(message="Test data generated")

        # generate all statistical figures
        elif action=='6':
            ioops.print_message(message="Generating all statistical figures ... ")

            #generate catgory figure
            productops.generate_category_figure()

            #generate discount figure
            productops.generate_discount_figure()

            #generate likes count figure
            productops.generate_likes_count_figure()

            #generate discount likes count figure
            productops.generate_discount_likes_count_figure()

            #generate all customers consumption figure
            orderops.generate_all_customers_consumption_figure()

            ioops.print_message(message="All 5 figures generated")


        # delete all data: products.txt, users.txt, orders.txt
        elif action=='7':
            orderops.delete_all_orders()
            productops.delete_all_products()
            customerops.delete_all_customers()

            ioops.print_message(message="Delete all orders, products and customers data")

        elif action=='8':
            ioops.print_message(message="Logged out successfully")
            login_control()
        else:
            ioops.print_error_message(error_source="main.admin_control", error_message="Invalid action")
            return True

def main():


    #manually register an Admin everytime the system is called
    adminops.register_admin()

    #Print login page
    ioops.main_menu()
    while True:
        main_menu_action = ioops.get_user_input(message="Enter your action: ",num_of_args=1)[0]
        if main_menu_action== '1':
            login_control()
        elif main_menu_action== '2':
            #register a customer
            ioops.print_message(message="Become a member today - register your account !")

            while True:
                # Get username and validate
                user_name = ioops.get_user_input(message="username: ", num_of_args=1)[0]
                if not userops.validate_username(user_name):
                    ioops.print_error_message(error_source="operation_user.validate_username",
                                              error_message="The name should only contain letters or underscores, and its length should be at least 5 characters.")
                    continue

                if userops.check_username_exist(user_name):
                    ioops.print_error_message(error_source="operation_user.check_username_exist",
                                              error_message="username already exists")
                    continue
                else:
                    ioops.print_message(message="username available")

                    # Get password and validate
                    while True:
                        user_password = ioops.get_user_input(message="password: ", num_of_args=1)[0]
                        if not userops.validate_password(user_password):
                            ioops.print_error_message(error_source="operation_user.validate_password",
                                                      error_message="The password should contain at least one letter and one number. The length of the password must be greater than or equal to 5 characters.")
                            continue
                        else:
                            ioops.print_message(message="valid password")
                            break  # Exit password loop if password is valid

                    # Get email and mobile number
                    while True:
                        user_email = ioops.get_user_input(message="Enter your email address: ", num_of_args=1)[0]
                        if not customerops.validate_email(user_email):
                            ioops.print_error_message(error_source="operation_customer.validate_email",
                                                      error_message="Invalid email")
                            continue

                        user_mobile = ioops.get_user_input(message="Enter your mobile number: ", num_of_args=1)[0]
                        if not customerops.validate_mobile(user_mobile):
                            ioops.print_error_message(error_source="operation_customer.validate_mobile",
                                                      error_message="Invalid mobile number")
                            continue

                        # Register customer
                        if not customerops.register_customer(user_name=user_name, user_password=user_password,
                                                             user_mobile=user_mobile, user_email=user_email):
                            ioops.print_error_message(error_source="operation_customer.register_customer",
                                                      error_message="Could not register customer account")
                        else:
                            ioops.print_message(message="Successfully registered")
                            login_control()
                            break  # Exit registration loop

        #quit the program
        elif main_menu_action== '3':
            ioops.print_message(message="Quit the program ! See you next time")
            break
        else:
            ioops.print_error_message(error_source="main.main", error_message="Invalid option")
            continue    #ask for another input
if __name__ == "__main__":
    main()