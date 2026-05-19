from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String, unique=True)
    amount = Column(Integer)
    date = Column(DateTime)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship("Customer", back_populates="invoices")

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    invoices = relationship("Invoice", back_populates="customer")

def sync_invoice_data(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Fetch latest invoice data from external source
    latest_invoices = fetch_latest_invoices()  # Assume this function exists
    
    for invoice_data in latest_invoices:
        existing_invoice = session.query(Invoice).filter_by(invoice_number=invoice_data['invoice_number']).first()
        
        if existing_invoice:
            # Update existing invoice record
            existing_invoice.amount = invoice_data['amount']
            existing_invoice.date = invoice_data['date']
        else:
            # Create new invoice record
            new_invoice = Invoice(
                invoice_number=invoice_data['invoice_number'],
                amount=invoice_data['amount'],
                date=datetime.datetime.strptime(invoice_data['date'], '%Y-%m-%d'),
                customer_id=invoice_data['customer_id']
            )
            session.add(new_invoice)
    
    session.commit()

def fetch_latest_invoices():
    # Placeholder function to fetch latest invoices from an external source
    return [
        {'invoice_number': 'INV001', 'amount': 100, 'date': '2023-01-01', 'customer_id': 1},
        {'invoice_number': 'INV002', 'amount': 200, 'date': '2023-01-02', 'customer_id': 2}
    ]

if __name__ == "__main__":
    engine = create_engine('sqlite:///surrogate.db')
    Base.metadata.create_all(engine)
    sync_invoice_data(engine)