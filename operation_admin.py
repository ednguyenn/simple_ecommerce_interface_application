import time
from model_admin import Admin
from operation_user import UserOps

class AdminOps:
    def __init__(self):
        pass
    def register_admin(self):
        """
        register an admin account
        """

        admin_user_name = "Admin"
        admin_password = "Admin123"
        admin_register_time = time.strftime('%Y-%m-%d %H:%M:%S')

        user_ops= UserOps()
        admin_id=user_ops.generate_unique_user_id()

        admin = Admin(user_id=admin_id,user_name=admin_user_name,user_password=admin_password,user_register_time=admin_register_time)
        admin_exist = False
        try:
            with open('data/users.txt', 'r+') as file:
                lines = file.readlines()
                for line in lines:
                    admin_obj = eval(line)
                    if admin_obj['user_role']=='admin':
                        admin_exist=True
                if admin_exist is False:
                    file.write(str(admin) + '\n')
        except Exception as e:
            return False

