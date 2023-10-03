import model_user
import model_customer
import model_admin
import model_product
import model_order
import operation_user
import operation_customer
import operation_admin
import operation_product
import operation_order

# model_user test
model_user1 = model_user.User()
model_user2 = model_user.User("u_0000000001", "user_", "a0001",
                              "01-01-2001_01:01:01", "customer")
# print(model_user1)
# print(model_user2)

# model_customer test
model_customer1 = model_customer.Customer()
model_customer2 = model_customer.Customer("u_0000000001", "user_", "a0001",
                                          "sam@mail.com", "0000000001",
                                          "00-00-0000_00:00:01", "customer")
# print(model_customer1)
# print(model_customer2)

# model_admin test
model_admin1 = model_admin.Admin()
model_admin2 = model_admin.Admin("u_0000000001", "user_", "a0001",
                                 "00-00-0000_00:00:01", "admin")
# print(model_admin1)
# print(model_admin2)

# model_product test
model_product1 = model_product.Product()
model_product2 = model_product.Product("0000001", "SKUF00001", "cat_1",
                                       "ukulele", "$10", "$9.99", "10%", "100")
# print(model_product1)
# print(model_product2)

# model_order test
model_order1 = model_order.Order()
model_order2 = model_order.Order("o_00001", "u_0000000001", "0000001",
                                 "00-00-0000_00:00:01")
# print(model_order1)
# print(model_order2)

# operation_user test
operation_user1 = operation_user.UserOperation()
# print(operation_user1.generate_unique_user_id())
# encrypted_password = operation_user1.encrypt_password("a0000")
# print(operation_user1.decrypt_password(encrypted_password))
# print(operation_user1.check_username_exist("sam_h"))
# print(operation_user1.validate_username("sam_h"))
# print(operation_user1.validate_password("a0000"))
# print(operation_user1.login("sam_h", "a0008"))
# print(operation_user1.login("stan_", "a0009"))


# operation_customer test
op_cust = operation_customer.CustomerOperation()
# print(op_cust.validate_email("sam@mail.com.au"))
# print(op_cust.validate_mobile("0400000000"))
# op_cust.register_customer("sam_h", "a0000", "sam@mail.com", "0400000000")
cust_object = model_customer.Customer("u_7170689932", "stanley", "a0000",
                                      "02-10-2023_20:24:45", "customer",
                                      "demo@mail.com", "0400000000")
# op_cust.update_profile("user_name", "the_don", cust_object)
# op_cust.delete_customer("u_8920372347")
# print(op_cust.get_customer_list(1))
# op_cust.delete_all_customers()

op_admin = operation_admin.AdminOperation()
# op_admin.register_admin(user_name="_admin_", user_password="xxxx0")

op_product = operation_product.ProductOperation()
op_product.extract_products_from_files()
# print(op_product.get_product_list(7452))
# op_product.delete_product("1671872")
# print(op_product.get_product_list_by_keyword("festival"))
# print(op_product.get_product_by_id("1674377"))
# op_product.generate_category_figure()
# op_product.generate_discount_figure()
# op_product.generate_likes_count_figure()
# op_product.generate_discount_likes_count_figure()
# op_product.delete_all_products()

op_order = operation_order.OrderOperation()
# print(op_order.generate_unique_order_id())
# print(op_order.create_an_order("u_1111111111", "0000000"))
# op_order.delete_order("0_93152")
# print(op_order.get_order_list("u_0000000000", 1))
op_order.generate_test_order_data()
