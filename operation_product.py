import math
import pandas as pd
import matplotlib.pyplot as plt


class ProductOperation:
    """Contains all the operations related to the product."""

    products_df = pd.DataFrame()

    def extract_products_from_files(self):
        """Extracts products from csv files and writes to txt file."""

        # Read csv files
        try:
            accessories_df = pd.read_csv("data/product/accessories.csv")
            bags_df = pd.read_csv("data/product/bags.csv")
            beauty_df = pd.read_csv("data/product/beauty.csv")
            house_df = pd.read_csv("data/product/house.csv")
            jewelry_df = pd.read_csv("data/product/jewelry.csv")
            kids_df = pd.read_csv("data/product/kids.csv")
            men_df = pd.read_csv("data/product/men.csv")
            shoes_df = pd.read_csv("data/product/shoes.csv")
            women_df = pd.read_csv("data/product/women.csv")
        except Exception as e:
            return e
        # Merge dataframes
        df1 = pd.merge(accessories_df, bags_df, how="outer")
        df2 = pd.merge(df1, beauty_df, how="outer")
        df3 = pd.merge(df2, house_df, how="outer")
        df4 = pd.merge(df3, jewelry_df, how="outer")
        df5 = pd.merge(df4, kids_df, how="outer")
        df6 = pd.merge(df5, men_df, how="outer")
        df7 = pd.merge(df6, shoes_df, how="outer")
        self.products_df = pd.merge(df7, women_df, how="outer")

        # Remove irrelevant columns
        columns_to_drop = ["subcategory", "is_new", "brand", "brand_url",
                           "codCountry", "variation_0_color",
                           "variation_1_color", "variation_0_thumbnail",
                           "variation_0_image", "variation_1_thumbnail",
                           "variation_1_image", "image_url", "url", "currency"]
        try:
            self.products_df = self.products_df.drop(columns=columns_to_drop)
        except KeyError:
            return KeyError
        except Exception as e:
            return e

        # Remove duplicates & reset index
        self.products_df = self.products_df.drop_duplicates()
        self.products_df = self.products_df.reset_index(drop=True)

        # Rename columns
        self.products_df = self.products_df.rename(
            columns={"id": "pro_id",
                     "model": "pro_model",
                     "category": "pro_category",
                     "name": "pro_name",
                     "current_price":
                     "pro_current_price",
                     "raw_price": "pro_raw_price",
                     "discount": "pro_discount",
                     "likes_count":
                     "pro_likes_count"})

        for product in self.products_df.index:
            # if name contains commas, remove the row from dataframe
            if "," in self.products_df['pro_name'][product]:
                self.products_df = self.products_df.drop(product)

        # Convert dataframe to list of strings
        products_list = []
        for i in self.products_df.index:
            products_list.append(f"{{'pro_id':"
                                 f"'{self.products_df['pro_id'][i]}', "
                                 f"'pro_model':"
                                 f"'{self.products_df['pro_model'][i]}', "
                                 f"'pro_category':"
                                 f"'{self.products_df['pro_category'][i]}', "
                                 f"'pro_name':"
                                 f"'{self.products_df['pro_name'][i]}', "
                                 f"'pro_current_price':"
                                 f"'{self.products_df['pro_current_price'][i]}"
                                 f"', 'pro_raw_price':"
                                 f"'{self.products_df['pro_raw_price'][i]}', "
                                 f"'pro_discount':"
                                 f"'{self.products_df['pro_discount'][i]}', "
                                 f"'pro_likes_count':"
                                 f"'{self.products_df['pro_likes_count'][i]}"
                                 f"'}}\n")

        # Write to products.txt
        try:
            file = open("data/products.txt", "w", encoding="utf-8")
            file.writelines(products_list)
        except FileNotFoundError:
            file = open("data/products.txt", "x", encoding="utf-8")
            file.writelines(products_list)
        except Exception as e:
            return e
        finally:
            file.close()

    def get_product_list(self, page_number):
        """Get a list of products within a given page range.
        Arguments: page_number.
        Return a tuple containing a list of products, current page number, and 
        total pages."""
        try:
            file = open("data/products.txt", "r", encoding="utf-8")
            product_list = file.readlines()
        except FileNotFoundError:
            file = open("data/products.txt", "w", encoding="utf-8")
            product_list = []
        except Exception as e:
            return e
        finally:
            file.close()
        # Calculate total pages
        try:
            total_page = math.ceil(len(product_list) / 10)
        except Exception as e:
            return e
        # First product on page
        low_product = (page_number * 10) - 10
        # Last product on page
        if total_page > 1:
            high_product = (page_number * 10) - 1
        else:
            high_product = len(product_list) - 1
        # Return the products on the page
        products_returned = product_list[low_product:high_product + 1]
        return (products_returned, f"Page {page_number} of {total_page}")

    def delete_product(self, pro_id):
        """Deletes the given product.
        Arguments: pro_id.
        Return True/ False to indicate whether deletion was successful."""
        try:
            file = open("data/products.txt", "r", encoding="utf-8")
            product_list = file.readlines()
        except FileNotFoundError:
            file = open("data/products.txt", "w", encoding="utf-8")
            product_list = []
        except Exception as e:
            return e
        finally:
            file.close()
        for product in product_list:
            # Check if product exists
            if str(pro_id) in product:
                product_list.remove(product)
                # Rewrite the file with the updated list
                file = open("data/products.txt", "w", encoding="utf-8")
                file.writelines(product_list)
                file.close()
                return True
        return False

    def get_product_list_by_keyword(self, keyword):
        """Get a list of products that match the given keyword.
        Arguments: keyword.
        Return a list of products."""
        try:
            file = open("data/products.txt", "r", encoding="utf-8")
            product_list = file.readlines()
        except FileNotFoundError:
            file = open("data/products.txt", "w", encoding="utf-8")
            product_list = []
        finally:
            file.close()
        # Remove products that do not match keyword
        new_product_list = []
        for product in product_list:
            if keyword.lower() in product.lower():
                new_product_list.append(product)
            else:
                continue
        if new_product_list == []:
            return []
        else:
            return new_product_list

    def get_product_by_id(self, pro_id):
        """Get a product that matches the given pro_id.
        Arguments: pro_id.
        Return a product."""
        try:
            file = open("data/products.txt", "r", encoding="utf-8")
            product_list = file.readlines()
        except FileNotFoundError:
            file = open("data/products.txt", "w", encoding="utf-8")
            product_list = []
        finally:
            file.close()
        # Remove products that do not match pro_id
        for product in product_list:
            if str(pro_id) in product:
                if str(pro_id).isdigit() and len(str(pro_id)) == 7:
                    return product
            else:
                continue
        return []

    def generate_category_figure(self):
        """Generate a bar chart showing the number of products in each. 
        category."""
        # Clear canvas
        plt.clf()
        # Get category counts.
        try:
            category_counts = self.products_df["pro_category"].value_counts()
        except KeyError:
            return KeyError
        except Exception as e:
            return e
        # Ensure full chart is shown
        plt.tight_layout()
        # Plot bar chart
        category_counts.plot.bar(color="green")
        plt.xlabel("Category")
        # Rotate x-axis labels
        plt.xticks(rotation=22)
        plt.ylabel("Number of Products")
        plt.title("Number of Products in Each Category")
        # Save figure
        try:
            plt.savefig("data/figure/category_figure.png")
        except Exception as e:
            return e

    def generate_discount_figure(self):
        """Generate a pie chart showing the number of products in each 
        discount range."""
        # Clear canvas
        plt.clf()
        # Get discount counts
        try:
            discount_counts = self.products_df["pro_discount"].value_counts(
                bins=[0, 30, 60, 100])
        except KeyError:
            return KeyError
        except Exception as e:
            return e
        # Ensure full chart is shown
        plt.tight_layout()
        # Plot pie chart
        discount_counts.plot.pie(autopct="%.2f%%",
                                 colors=["blue", "green", "red"],
                                 labels=["30-60%", "60-100%", "0-30%"])
        plt.ylabel("")
        plt.title("Number of Products in Each Discount Range")
        # Save figure
        try:
            plt.savefig("data/figure/discount_figure.png")
        except Exception as e:
            return e

    def generate_likes_count_figure(self):
        """Generate a horizontal bar chart showing the number of likes for each 
        category."""

        # Clear canvas
        plt.clf()

        # Group by category & calculate the sum of likes for each
        try:
            category_likes_sum = self.products_df.groupby(
                'pro_category')['pro_likes_count'].sum().reset_index()

            # Sort in ascending order by the sum of likes
            category_likes_sum_sorted = category_likes_sum.sort_values(
                by='pro_likes_count')
        except KeyError:
            return KeyError
        except Exception as e:
            return e

        # Create the chart
        plt.tight_layout()
        plt.barh(category_likes_sum_sorted['pro_category'],
                 category_likes_sum_sorted['pro_likes_count'],
                 color='cornflowerblue')
        plt.xlabel('Count of Likes')
        plt.yticks(rotation=45)
        plt.ylabel('Category')
        plt.title('Count of Likes by Category')

        # Save the figure to the "data/figure" folder
        try:
            plt.savefig('data/figure/likes_count_figure.png')
        except Exception as e:
            return e

    def generate_discount_likes_count_figure(self):
        """Generate a scatter chart showing relationship between discount and 
        likes."""

        # Clear canvas
        plt.clf()

        # Create the chart
        plt.tight_layout()
        plt.scatter(self.products_df['pro_discount'],
                    self.products_df['pro_likes_count'],
                    color='cornflowerblue')
        plt.xlabel('Discount')
        plt.ylabel('Count of Likes')
        plt.title('Relationship between Discount and Likes')

        # Save the figure to the "data/figure" folder
        try:
            plt.savefig('data/figure/discount_likes_count_figure.png')
        except Exception as e:
            return e

    def delete_all_products(self):
        """Deletes all products on file."""
        try:
            file = open("data/products.txt", "w", encoding="utf-8")
            file.write("")
        except FileNotFoundError:
            file = open("data/products.txt", "x", encoding="utf-8")
            file.write("")
        except Exception as e:
            return e
        finally:
            file.close()
