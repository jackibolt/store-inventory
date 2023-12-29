from models import (Base, session,
                    Product, engine)
import csv, datetime, time


def menu():
    while True:
        print('''
              \nSTORE INVENTORY
              \r
              \rEnter 'v' to view products
              \rEnter 'x' to view all products
              \rEnter 'a' to add a product
              \rEnter 'b' to export a csv
              \r''')
        return input('Selection:  ')
        
        


def clean_price(price_str):
    price_split = price_str.split('$')
    price_float = float(price_split[1])
    price_cents = price_float *100
    return int(price_cents)


def clean_quantity(quantity_str):
    quantity_str = int(quantity_str)
    return quantity_str


def clean_date(date_str):
    split_date = date_str.split('/')
    month = int(split_date[0])
    day = int(split_date[1])
    year = int(split_date[2])
    return datetime.date(year, month, day)


def clean_selected_id(id_str, options):
    try:
        id_str = int(id_str)
        options_list = []
        for item in options:
            option_num = item.split('.')
            option_num = int(option_num[0])
            options_list.append(option_num)
    except ValueError:
        input('''
              \n ----- ID ERROR -----
              \rThe id should be a numerical value.
              \rPress enter to try again.
              \r''')
    else:
        if id_str in options_list:
            return id_str
        else:
            input('''
                  \n ----- ID ERROR -----
                  \rThe id should be a numerical value that corresponds with a product in the inventory.
                  \rPress enter to try again.
                  \r''')



def add_csv():
    with open('inventory.csv') as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            # print(row)
            item_in_inventory = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if item_in_inventory == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = clean_quantity(row[2])
                date_updated = clean_date(row[3])

                new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated)
                session.add(new_product)
        session.new
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice.lower() == 'v':
            #view
            product_list = []
            for product in session.query(Product):
                product_list.append(f'{product.product_id}. {product.product_name}')
            print('\nProduct List: ')
            for item in product_list:
                print(f'\r{item}')

            id_error = True
            while id_error:
                selected_id = input('Select product id:  ')
                selected_id = clean_selected_id(selected_id, product_list)
                if type(selected_id) == int:
                    id_error = False
            selected_product = session.query(Product).filter(Product.product_id == selected_id).first()
            print(selected_product)


        elif choice.lower() == 'x':
            for product in session.query(Product):
                print(f'''\n{product.product_id}. {product.product_name} | ${product.product_price/100} | x{product.product_quantity}
                     \rLast Updated: {product.date_updated}''')
            input('\nPress enter to return to the main menu')
        elif choice.lower() == 'a':
            #add
            pass
        elif choice.lower() == 'b':
            #export csv
            pass
        else:
            print("Goodbye")
            app_running = False



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
    