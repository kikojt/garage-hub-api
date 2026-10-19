from pydantic import BaseModel, Field

class ChangeStatusRequest(BaseModel):
    repair_status_id: int

class AssignEmployeeRequest(BaseModel):
    employee_id: int

class AddPartRequest(BaseModel):
    part_id: int
    quantity: int = Field(gt=0)
    
class UpdatePartQuantityRequest(BaseModel):
    quantity: int = Field(gt=0)
