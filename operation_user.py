import random
import string


class UserOps:
    def __init__(self):
        pass

    def generate_unique_user_id(self):          #2.6.1
        """
        This method is used to generate and return a 10-digit unique user id starting with ‘u_’ every time when a new user is registered.
        """

        with open('data/users.txt', 'r') as file:
            lines = file.readlines()
            users = [eval(line) for line in lines]
            while True:
                ten_digits_number = ''.join(str(random.randint(0, 9)) for _ in range(10))
                unique_user_id = 'u_' + ten_digits_number
                if unique_user_id not in [user['user_id'] for user in users]:
                    return unique_user_id

    def encrypt_password(self, user_password):      #2.6.2
        """ Encode a user-provided password """

        #use string library to create a list of characters to perform random choice
        characters= string.ascii_letters + string.digits
        random_string= ''.join(random.choice(characters) for _ in range(len(user_password)*2))

        #encrypted the user pass word by combining it random_string follow a required pattern
        encrypted_password= '^^' + ''.join([random_string[index*2]+random_string[index*2+1]+user_password[index] for index in range(len(user_password))]) +'$$'

        return encrypted_password

    def decrypt_password(self, encrypted_password):         #2.6.3
        """
        Decode the encrypted password with a similar rule as the encryption method
        """

        #remove ^^ and $$ characters
        user_password= encrypted_password[2:-2]

        #decrypted the password by selecting the correct character out of the given string
        user_provided_password= ''.join([user_password[index] if (index+1)%3==0 else '' for index in range(len(user_password))])
        return user_provided_password

    def check_username_exist(self,user_name):              #2.6.4
        """
        Verify whether a user is already registered or exists in the system.
        """

        users_file_path = 'data/users.txt'
        with open(users_file_path, 'r') as file:
            for line in file:
                user_data = eval(line)
                if user_data['user_name'] == user_name:
                    return True
        return False

    def validate_username(self, user_name):         #2.6.5
        """
        Validate the user's name. The name should only contain letters or underscores, and its length should be at least 5 characters
        """
        length= len(user_name)
        characters= string.ascii_letters +'_'

        if len(user_name) >=5 and all((character in characters for character in user_name)):
            return True
        else:
            return False


    def validate_password(self,user_password):              #2.6.6
        """
        Validate the user's password. The password should contain at least
        one letter (this letter can be either uppercase or lowercase) and one
        number. The length of the password must be greater than or equal to
        5 characters.
        """
        length= len(user_password)
        letters= string.ascii_letters
        digits= string.digits
        if len(user_password) >= 5 and any(character in letters for character in user_password) and any(character in digits for character in user_password):
            return True
        else:
            return False



    def login(self,user_name,user_password):
        """
        Verify the provided user’s name and password combination against
        stored user data to determine the authorization status for accessing
        the system

        """
        users_file_path = 'data/users.txt'
        with open(users_file_path, 'r') as file:
            for line in file:
                user_data = eval(line)
                if user_data['user_name'] == user_name and user_data['user_password'] == user_password:
                    return user_data
        return False







