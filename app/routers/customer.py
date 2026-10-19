from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services.customer import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.get("/", response_model=list[CustomerResponse])
def get_all_customers(db: Session = Depends(get_db)):
    return CustomerService.get_all_customers(db)

@router.get("/search", response_model=list[CustomerResponse])
def search_customers(
    name: str | None = None,
    nif: str | None = None,
    phone: str | None = None,
    db: Session = Depends(get_db)
):
    return CustomerService.search_customers(
        db,
        name,
        nif,
        phone
    )

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = CustomerService.get_customer_by_id(db, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )
    return customer

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        return CustomerService.create_customer(db, customer)
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    try:
        update_customer = CustomerService.get_customer_by_id(db, customer_id)

        if update_customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found."
            )
        
        return update_customer
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    delete_customer = CustomerService.get_customer_by_id(db, customer_id)

    if delete_customer is None:
        raise HTTPException(
                status_code=404,
                detail="Customer not found."
            )
        
    return {
        "message": "Customer deleted successfully."
    }