from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

class CustomerRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Customer).all()
    
    @staticmethod
    def get_by_id(db: Session, customer_id: int):
        return db.query(Customer).filter(Customer.id == customer_id).first()
    
    @staticmethod
    def get_by_nif(db: Session, nif: str):
        return db.query(Customer).filter(Customer.nif == nif).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(Customer).filter(Customer.email == email).first()
    
    @staticmethod
    def create(db: Session, customer: CustomerCreate):
        db_customer = Customer(
            first_name = customer.first_name,
            last_name = customer.last_name,
            nif = customer.nif,
            phone = customer.phone,
            email = customer.email,
            address = customer.address,
            city = customer.city,
            postal_code = customer.postal_code
        )

        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)

        return db_customer
    
    @staticmethod
    def update(db: Session, db_customer: Customer, customer: CustomerUpdate):
        db_customer.first_name = customer.first_name
        db_customer.last_name = customer.last_name
        db_customer.nif = customer.nif
        db_customer.phone = customer.phone
        db_customer.email = customer.email
        db_customer.address = customer.address
        db_customer.city = customer.city
        db_customer.postal_code = customer.postal_code

        db.commit()
        db.refresh(db_customer)

        return db_customer
    
    @staticmethod
    def delete(db: Session, db_customer: Customer):
        db.delete(db_customer)
        db.commit()


    @staticmethod
    def search(
        db: Session,
        name: str | None = None,
        nif: str | None = None,
        phone: str | None = None
    ):

        query = db.query(Customer)

        if name:
            query = query.filter(
                Customer.first_name.ilike(f"%{name}%") | Customer.last_name.ilike(f"%{name}%")
            )

        if nif:
            query = query.filter(
                Customer.nif == nif
            )

        if phone:
            query = query.filter(
                Customer.phone.ilike(f"%{phone}%")
            )

        return query.all()