from models import (Base, session,
                    Product, engine)
import csv, datetime, time


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



def add_csv():
    with open('inventory.csv') as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            print(row)
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



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
