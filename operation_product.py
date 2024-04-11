import os
import pandas as pd
import math
import matplotlib.pyplot as plt
class ProductOps:
    def __init__(self):
        pass
    def extract_products_from_files(self):
        """
        Extract products from csv files in data/products/* and the save them into data/products.txt
        """
        #read each files and pass the data into data/products.txt
        folder_path = 'data/product/'
        file_list= os.listdir(folder_path)

        for file in file_list:
            if file.endswith('.csv'):
                file_path=os.path.join(folder_path,file)

                df = pd.read_csv(file_path,usecols=['id', 'model', 'category', 'name',
                                                          'current_price', 'raw_price', 'discount',
                                                          'likes_count'])
                #rename the columns
                df.rename(columns={
                    'id': 'pro_id',
                    'model': 'pro_model',
                    'category': 'pro_category',
                    'name': 'pro_name',
                    'current_price': 'pro_current_price',
                    'raw_price': 'pro_raw_price',
                    'discount': 'pro_discount',
                    'likes_count': 'pro_likes_count'
                }, inplace=True)

                # Open a text file for writing in append mode with utf-8 encoding
                with open('data/products.txt', 'a',encoding='utf-8') as file:
                    # Iterate over each row in the DataFrame
                    for index, row in df.iterrows():
                        # Format the data into the desired string format
                        formatted_data = f"{row.to_dict()}\n"

                        # Write the formatted data to the text file
                        file.write(formatted_data)

    def get_product_list(self,page_number):
        """
        similar with get_customer_list() method
        This method retrieves one page of products from the database. One
        page contains a maximum of 10 items from data/products.txt file
        :return:
        """
        try:
            with open('data/products.txt', 'r') as file:
                lines = file.readlines()
                products=[]
                product_list = []

                for line in lines:
                    obj = eval(line)
                    products.append(obj)
                #this is a first index in a requested page and total pages
                starting_index = (int(page_number)-1)*10
                total_pages = math.ceil(len(products) / 10)

                #print out the list of 10 objects with a given page number
                for _ in range(10):
                    product_list.append(products[starting_index])
                    starting_index +=1
                    if starting_index == len(products):
                        return product_list, page_number, total_pages

                return product_list,page_number,total_pages
        except Exception as e:
            return False

    def delete_product(self,product_id):
        """
        This method can delete the product info from the system (i.e.,
        data/products.txt) based on the provided product_id.
        :param product_id:
        :return: True/False
        """
        with open('data/products.txt', 'r') as file:
            lines = file.readlines()

        #Iterate over lines and parsing them as dictionaries
        updated_lines=[]
        deleted=False

        for line in lines:
            obj = eval(line)
            if obj['pro_id'] == product_id:
                deleted=True
                continue
            updated_lines.append(obj)
        if not deleted:        #could not find the provided pro_id
            return False
        #rewrite the file without the one just deleted
        with open('data/products.txt', 'w') as file:
            file.writelines([str(line) + "\n" for line in updated_lines])
        return True

    def get_product_list_by_keyword(self,keyword):
        """
        This method retrieves all the products whose name contains the keyword (case insensitive).
        :param keyword:
        :return: The return result will be a list of product objects. No page limitation.
        """
        with open('data/products.txt', 'r') as file:
            lines = file.readlines()
            product_list=[]
            for line in lines:
                obj = eval(line)
                #lower all character for case insensitivity
                if keyword.lower() in obj['pro_name'].lower():
                    product_list.append(obj)
        return product_list

    def get_product_by_id(self,product_id):
        """
        This method returns one product object based on the given product_id.
        :param product_id:
        :return:A product object or None if cannot be found.
        """
        found = False
        with open('data/products.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                obj = eval(line)
                if obj['pro_id'] == product_id:
                    found = True
                    return obj
        if found == False:
            return None

    def generate_category_figure(self):
        """
        This method generates a bar chart that shows the total number of
        products for each category in descending order. The figure is saved
        into the data/figure folder.
        """

        with open('data/products.txt', 'r') as file:
            lines = file.readlines()
            products=[eval(line) for line in lines]

            #create a dictionary to hold the count occurrences of each product category
            category_counts ={}
            for product in products:
                category= product['pro_category']
                if category in category_counts:
                    category_counts[category]+=1
                else:
                    category_counts[category]=1

        # Sort the category_counts dictionary by values in descending order
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

        #extract category names and counts for the bar chart
        categories = [category[0] for category in sorted_categories]
        counts = [category[1] for category in sorted_categories]

        # using Bar() to plot line chart
        plt.bar(categories, counts, linewidth=1.5)

        # Add labels and title
        plt.xlabel('Categories')
        plt.ylabel('Number of Products')
        plt.title('Total Number of Products for Each Category')

        plt.savefig('data/figure/category_figure.png')
        plt.show()


    def generate_discount_figure(self):
        """
        This method generates a pie chart that shows the proportion of
        products that have a discount value less than 30, between 30 and 60
        inclusive, and greater than 60. The figure is saved into the data/figure
        folder.
        """
        with open('data/products.txt', 'r') as file:
            lines = file.readlines()
            products = [eval(line) for line in lines]

            #initialize a dictionary to hold occurrences for each discount group
            discount_counts ={
                "less than 30": 0,
                "between 30 to 60": 0,
                "more than 60": 0
            }
            for product in products:
                discount= product['pro_discount']
                if discount<30:
                    discount_counts["less than 30"]+=1
                elif discount>60:
                    discount_counts["more than 60"] +=1
                else:
                    discount_counts["between 30 to 60"] +=1
        #extract data for the pie chart from dictionary
        labels= list(discount_counts.keys())
        sizes=list(discount_counts.values())

        # using pie() to plot line chart
        plt.pie(sizes, labels=labels)

        plt.title("Product discount distribution")
        plt.savefig('data/figure/discount_figure.png')
        plt.show()


    def generate_likes_count_figure(self):
        """
        This method generates a bar chart of the likes count of each product
        The figure is saved into the data/figure folder.
        """
        with open('data/products.txt', 'r') as file:
            lines = file.readlines()
            products=[eval(line) for line in lines]

            #create a dictionary to hold the count occurrences of each product's like_count for each category
            category_like_counts ={}
            for product in products:
                category = product['pro_category']
                likes = product['pro_likes_count']
                if category in category_like_counts:
                    category_like_counts[category]+=likes
                else:
                    category_like_counts[category]=likes
        # Sort the category_counts dictionary by values in descending order
        sorted_categories = sorted(category_like_counts.items(), key=lambda x: x[1], reverse=False)

        # extract category names and likes_count for the bar chart
        categories = [category[0] for category in sorted_categories]
        likes_count = [category[1] for category in sorted_categories]

        # using Bar() to plot line chart
        plt.bar(categories, likes_count, linewidth=1.5)

        # Add labels and title
        plt.xlabel('Categories')
        plt.ylabel('Total of likes')
        plt.title('Total likes for Each Category')

        plt.savefig('data/figure/likes_count_figure.png')
        plt.show()

    def generate_discount_likes_count_figure(self):
        """
        This method generates a scatter chart showing the relationship
        between likes_count and discount for all products. The figure is saved
        into the data/figure folder.
        """
        with open('data/products.txt', 'r') as file:
            lines = file.readlines()
            products=[eval(line) for line in lines]

        #create 2 list of likes count and discount as x and y for scatter plot
        likes_count = [product['pro_likes_count'] for product in products]
        discount = [product['pro_discount'] for product in products]

        # using xlabel, ylabel, and title to set the labels for the chart
        plt.xlabel("Discount")
        plt.ylabel("Likes count")
        plt.title("Relationship bewteen Discounts and Likes counts")

        # using scatter() to plot scatter chart, s=5 is for easy readability
        plt.scatter(discount,likes_count , s=5)

        plt.savefig('data/figure/Discount_likes_count_figure.png')
        plt.show()

    def delete_all_products(self):
        """
        This method removes all the product data in the data/products.txt file.
        """
        with open('data/products.txt', 'w') as file:
            file.truncate(0)        #deleted everything



