

class IOInterface:
    def __init__(self):
        pass
    def get_user_input(self, message, num_of_args):
        """
        accept user input
        :param message:
        :param num_of_args:
        :return: result is [“arg1”, “arg2”, “arg3”]
        """
        user_inputs = input(f"{message}: ").split()

        if 'exit' in user_inputs:
            raise SystemExit("Exiting program.")

        accepted_inputs = user_inputs[:num_of_args]

        #Pad the list with empty strings if the length is less than num_of_args
        accepted_inputs += [''] * (num_of_args - len(accepted_inputs))

        return accepted_inputs

    def main_menu(self):
        """
        Display login menu
        """
        print("""
                    ----------------------------------------------------------
                    |                                                        |
                    |       Welcome to AMAMONASH ONLINE SHOPPING Interface ! |   
                    |                                                        |
                    |                You have the following options:         |
                    |                                                        |
                    |             (1). Login to AMAMONASH                    |
                    |             (2). Register a new account                |
                    |             (3). Quit !                                |
                    |                                                        |
                    ----------------------------------------------------------
        """)

    def admin_menu(self):
        """
        Display admin menu
        """
        print("""
                    ----------------------------------------------------------
                    |                                                        |
                    |                Welcome to the Interface                |
                    |                   Hello Admin!                         |
                    |                                                        |
                    |        You have access to powerful tools and           |
                    |        functionalities to manage your customer         |
                    |                                                        |
                    ----------------------------------------------------------
                    Choose the following options:
                    (1). Show products
                    (2). Add customers
                    (3). Show customers
                    (4). Show orders
                    (5). Generate test data
                    (6). Generate all statistical figures
                    (7). Delete all data
                    (8). Logout
        """)

    def customer_menu(self):
        """
        Display customer menu
        """
        print("""
                ----------------------------------------------------------
                |                                                        |
                |                Welcome to the Interface                |
                |                   Hello Customer!                         |
                |                                                        |
                |        You have access to powerful tools and           |
                |        functionalities to manage your customer         |
                |                                                        |
                ----------------------------------------------------------
                Choose the following options:
                (1). Show profile
                (2). Update profile
                (3). Show products (user input could be “3 keyword” or “3”)
                (4). Show history orders
                (5). Generate all consumption figures
                (6). Logout                
                """)
    def show_list(self,user_role,list_type,object_list):
        """
        Prints out the different types of list
        :param user_role:
        :param list_type:
        :param object_list:
        :return:
        """

        def print_list():
            """ This function prints out the lists of objects """
            print(f"List Type: {list_type}")
            print("Row Number | Data")
            for i, item in enumerate(object_list[0], start=1):
                print(i)
                self.print_object(item)
            print(f"Page Number: {object_list[1]}")
            print(f"Total Page Number: {object_list[2]}")

        if user_role == "customer":
            if list_type == "Product" or list_type == "Order":
                print_list()
            elif list_type == "Customer":
                self.print_error_message(error_source="io_interface.showlist", error_message="Sorry ! You do not have access to Customer List!")
            else:
                self.print_error_message(error_source="io_interface.showlist",error_message="List type does not exist")
        elif user_role == "admin":
            if list_type in ["Customer", "Product", "Order"]:
                print_list()
            else:
                self.print_error_message(error_source="io_interface.showlist",error_message="List type does not exist")
        else:
            self.print_error_message(error_source="io_interface.showlist", error_message="Wrong user role !")


    def print_error_message(self,error_source,error_message):
        """
        Prints out an error message and shows where the error occurred
        :param error_source:
        :param error_message:
        """
        print(f"Error in {error_source}: {error_message}")

    def print_message(self,message):
        """
        Print out the given message
        :param message:
        """
        print(message)
    def print_object(self, target_object):
        """
        Print out the object using the str() function.
        :param target_object:
        :return:
        """
        print(str(target_object))

