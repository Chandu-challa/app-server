from sqlalchemy import Column, String, Float, Date, TIMESTAMP
from database import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    date_of_birth = Column(Date)
    account_balance = Column(Float)
    created_at = Column(TIMESTAMP)