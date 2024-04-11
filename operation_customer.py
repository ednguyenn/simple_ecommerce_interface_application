import re
from operation_user import UserOps
import time
import math
from model_user import User
from model_customer import Customer

class CustomerOps:
    def __init__(self):
        pass
    def validate_email(self, user_email):
        """
        Validate the provided email address format
        An email address consists of four parts:
            ● Username: The part of the email address before the @
            symbol.
            ● @ symbol: Separates the username and domain name.
            ● Domain name: Refers to the mail server that stores or routes
            the email.
            ● Dot (.): Separates a portion of the address from the domain
            name.
        """
        #using regular expression for validaqting email format
        pattern = r'^[\w\.-]+@[\w-]+\.[\w\.]+$'

        return bool(re.match(pattern, user_email))


    def validate_mobile(self,user_mobile):
        """
        Validate the provided mobile number format
        The mobile number
        should be exactly 10 digits long, consisting only of numbers, and
        starting with either '04' or '03'
        """
        pattern = r'^(03|04)\d{8}$'
        return bool(re.match(pattern, user_mobile))

    def register_customer(self, user_name, user_password, user_email, user_mobile):
        """
        Save the information of the new customer into the data/users.txt file.
        """
        user_ops = UserOps()  # Create an instance of UserOps
        # Validate username existence, format, and password
        if not (not user_ops.check_username_exist(user_name=user_name) and
                user_ops.validate_username(user_name=user_name) and
                user_ops.validate_password(user_password=user_password)):

            return False
        # Validate email and mobile format
        if not (self.validate_email(user_email=user_email) and
                self.validate_mobile(user_mobile=user_mobile)):
            return False

        # Generate unique user ID and register time
        user_id = user_ops.generate_unique_user_id()

        #create a new customer
        try:
            user_register_time = time.strftime("%d-%m-%Y_%H:%M:%S")
            new_customer= Customer(user_id=user_id,user_name=user_name,user_password=user_password,user_register_time=user_register_time,user_role="customer",user_email=user_email,user_mobile=user_mobile)
            # Write customer information to the file
            with open('data/users.txt', 'a') as file:
                file.write(str(new_customer) + '\n')
            return True
        except Exception as e:
            return False

    def update_profile(self,attribute_name, value, customer_object):
        """
        Update the given customer object’s attribute value. According to
        different attributes, it is necessary to perform the validations to
        control the input value. If the input value is invalid, return false. If it is
        a valid input, the changes should be written into the data/users.txt
        file immediately.
        """
        userops = UserOps()  # Create an instance of UserOps
        with open('data/users.txt', 'r+') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                obj = eval(line)
                if obj['user_id'] == customer_object['user_id']:
                    if attribute_name == "user_name":
                        if not userops.check_username_exist(value) and userops.validate_username(value):
                            customer_object[attribute_name] = value
                        else:
                            return False
                    elif attribute_name == "user_password":
                        if userops.validate_password(value):
                            customer_object[attribute_name] = value
                        else:
                            return False
                    elif attribute_name == "user_email":
                        if self.validate_email(value):
                            customer_object[attribute_name] = value
                        else:
                            return False
                    elif attribute_name == "user_mobile":
                        if self.validate_mobile(value):
                            customer_object[attribute_name] = value
                        else:
                            return False
                    else:
                        return False
                    lines[i] = str(customer_object) + '\n'      #the modified object is converted to a string and updated to the same line in txt file
                    file.seek(0)                                #move to cursor to beginning of the file
                    file.writelines(lines)                      #effectively update the content
                    return True
        return False                #return False if could not find matching user_id

    def delete_customer(self,customer_id):
        """
        Delete the customer from the data/users.txt file based on the provided customer_id.
        :param customer_id: The customer id to delete
        :return: True(deleted)/False(failed)
        """
        #Read the file
        with open('data/users.txt', 'r') as file:
            lines = file.readlines()

        #Iterate over lines and parsing them as dictionaries
        updated_lines=[]
        deleted=False

        for line in lines:
            obj = eval(line)
            if obj['user_id'] == customer_id:
                deleted=True
                continue
            updated_lines.append(obj)
        if not deleted:        #could not find the provided customer ID
            return False
        #rewrite the file without the one just deleted
        with open('data/users.txt', 'w') as file:
            file.writelines([str(line) + "\n" for line in updated_lines])
        return True

    def get_customer_list(self,page_number):
        """
        Retrieve one page of customers from the data/users.txt. One page contains a maximum of 10 customers
        :param page_number:
        :return:a tuple including a list of customers objects
                and the total number of pages. For example,
                ([Customer1, Customer2,...., Customer10],
                page_number, total_page).
        """

        with open('data/users.txt', 'r') as file:
            lines = file.readlines()
            customers = []

            for line in lines:
                obj = eval(line)
                customers.append(obj)

            starting_index = (int(page_number) - 1) * 10
            total_pages = math.ceil(len(customers) / 10)
            customers_list = []

            for _ in range(10):
                if starting_index < len(customers):
                    customers_list.append(customers[starting_index])
                    starting_index += 1
                else:
                    break

        return customers_list, page_number, total_pages



    def delete_all_customers(self):
        """
        Removes all the customers from the data/users.txt file.
        :return: NA
        """
        with open('data/users.txt', 'w') as file:
            file.truncate(0)        #deleted everything





