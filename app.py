from models import (Base, session,
                    Product, engine)
import csv, datetime, time, sqlite3
from datetime import date


def menu():
    while True:
        print('''
              \nSTORE INVENTORY APP
              \r
              \n--- MAIN MENU ---
              \rEnter 'v' to search product database
              \rEnter 'l' to view a list of all products
              \rEnter 'a' to add a product
              \rEnter 'b' to export a csv
              \rEnter 'x' to exit
              \r''')
        menu_selection = input('Selection:  ')
        if menu_selection in ['a', 'b', 'l', 'v', 'x']:
            return menu_selection
        else:
            print(f'Not a valid option. Please select from the menu.')
            time.sleep(1)

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
                  \n----- ID ERROR -----
                  \rThis id number does not exist in the inventory.
                  \rThe id should be a numerical value that corresponds with a product in the inventory.
                  \rPress enter to try again.
                  \r''')


def clean_quantity(quantity_str):
    try:
        quantity_str = int(quantity_str)
    except ValueError:
        input('''
            \n--- QUANTITY ERROR ---
            \rThe quantity should be an integer value.
            \rPress enter to try again.
            \r''')
    else:
        return quantity_str


def add_csv():
    with open('inventory.csv') as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            new_product_name = row[0]
            item_in_inventory = session.query(Product).filter(Product.product_name==new_product_name).one_or_none()
            product_name = row[0]
            product_price = clean_price(row[1])
            product_quantity = clean_quantity(row[2])
            date_updated = clean_date(row[3])

            new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated)
            
            if item_in_inventory:
                if item_in_inventory.date_updated < new_product.date_updated:
                    item_in_inventory.product_price = new_product.product_price
                    item_in_inventory.product_quantity = new_product.product_quantity
                    item_in_inventory.date_updated = new_product.date_updated
                    
            elif item_in_inventory == None:
                session.add(new_product)

        session.commit()




def export_csv():
    database_file = 'inventory.db'
    table_name = 'inventory'
    csv_file_path = 'inventory_backup.csv'

    column_names = ['product_name', 'product_price', 'product_quantity', 'date_updated']

    product_list = session.query(Product).all()

    

    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(column_names)

        for product in product_list:
            csv_writer.writerow([
                product.product_name,
                f'${product.product_price / 100}',
                product.product_quantity,
                product.date_updated.strftime('%m/%d/%Y')
            ])

    time.sleep(1.5)
    print('\n---> Database export complete.')


def app():
    app_running = True
    while app_running:
        choice = menu()

        if choice.lower() == 'v':
            # VIEW INDIVIDUAL PRODUCTS
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
            input('\nPress enter to return to the main menu')

        elif choice.lower() == 'l':
            # VIEW THE WHOLE INVENTORY
            for product in session.query(Product):
                print(f'''\n{product.product_id}. {product.product_name} | ${product.product_price/100} | x{product.product_quantity}
                     \rLast Updated: {product.date_updated}''')
            input('\nPress enter to return to the main menu')

        
        elif choice.lower() == 'a':
            # ADD PRODUCT TO INVENTORY
            print('Add a product - ')
            product_name = input('Product Name:  ')
            
            price_error = True
            while price_error:
                product_price = input('Product Price:  ')
                product_price = clean_price(f'${product_price}')
                if type(product_price) == int:
                    price_error = False
            
            quantity_error = True
            while quantity_error:
                product_quantity = input('Quantity:  ')
                product_quantity = clean_quantity(product_quantity)
                if type(product_quantity) == int:
                    quantity_error = False

            new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date.today())
            
            item_in_inventory = session.query(Product).filter(Product.product_name==new_product.product_name).one_or_none()
            if item_in_inventory == None:
                session.add(new_product)
                session.commit()
                print('The product has been added.')
                time.sleep(1.5)
                input('\nPress enter to return to the main menu')
            
            else:
                print('This product already exists in the inventory.')
                print(item_in_inventory)
                edit_choice = input('Would you like to update the existing product? (y/n)  ')
                
                if edit_choice.lower() == 'y':
                    item_in_inventory.product_price = new_product.product_price
                    item_in_inventory.product_quantity = new_product.product_quantity
                    item_in_inventory.date_updated = new_product.date_updated
                    session.commit()
                    print('The product has been update')
                    time.sleep(1.5)
                    input('Press enter to return to the main menu')

                else:
                    input(f'\nNo updates were made. Press enter to return to the main menu\n')


        elif choice.lower() == 'b':
            export_csv()

        
        else:
            # EXIT THE APP
            print("\nGoodbye\n")
            app_running = False



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
    