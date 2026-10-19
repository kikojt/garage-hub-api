from sqlalchemy.orm import Session

from app.repositories.customer import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate

class CustomerService:

    @staticmethod
    def get_all_customers(db: Session):
        return CustomerRepository.get_all(db)
    
    @staticmethod
    def get_customer_by_id(db: Session, customer_id: int):
        return CustomerRepository.get_by_id(db, customer_id)
    
    @staticmethod
    def create_customer(db: Session, customer: CustomerCreate):
        existing_email = CustomerRepository.get_by_email(db, customer.email)
        
        if existing_email:
            raise ValueError("Email already exists.")
        
        existing_nif = CustomerRepository.get_by_nif(db, customer.nif)
        
        if existing_nif:
            raise ValueError("NIF already exists.")

        return CustomerRepository.create(db, customer)
    
    # !!Rever!! -> Não está atualizar
    @staticmethod
    def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
        db_customer = CustomerRepository.get_by_id(db, customer_id)

        if db_customer is None:
            return None
        
        # Verifica se o email foi alterado
        if customer.email != db_customer.email:
            
            existing_email = CustomerRepository.get_by_email(db, customer.email)

            if existing_email:
                raise ValueError("Email already exists.")
            
        # Verifica se o NIF foi alterado
        if customer.nif != db_customer.nif:

            existing_nif = CustomerRepository.get_by_nif(db, customer.nif)

            if existing_nif:
                raise ValueError("NIF already exists.")

        return CustomerRepository.update(db, db_customer, customer)
    
    # !!Rever!! -> Não está a eliminar
    # Pode ser devido á base de dados ter uma relação com o Vehicle
    @staticmethod
    def delete_customer(db: Session, customer_id: int):
        db_customer = CustomerRepository.get_by_id(db, customer_id)

        if db_customer is None:
            return None
        
        CustomerRepository.delete(db, db_customer)

        return True


    @staticmethod
    def search_customers(
        db: Session,
        name: str | None = None,
        nif: str | None = None,
        phone: str | None = None
    ):
        return CustomerRepository.search(
            db,
            name,
            nif,
            phone
        )