from sqlalchemy import (create_engine, Column, 
                        Integer, String, Date)
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Product(Base):

    __tablename__ = 'inventory'

    product_id = Column(Integer, primary_key=True)
    product_name = Column('Product Name', String)
    product_quantity = Column('Quantity', Integer)
    product_price = Column('Price', Integer)
    date_updated = Column('Last Update', Date)

    def __repr__(self):
        return f'''
                \n{self.product_id}. {self.product_name} - ${self.product_price}
                \rQuantity: {self.product_quantity}
                \rLast Update: {self.date_updated}
                '''