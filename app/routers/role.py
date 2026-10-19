from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.services.role import RoleService

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


@router.get("/", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return RoleService.get_all_roles(db)

@router.post("/", response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return RoleService.create_role(db, role)

@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = RoleService.get_role_by_id(db, role_id)

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )
    return role

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    update_role = RoleService.update_role(db, role_id, role)

    if update_role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )
    
    return update_role


@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    delete_role = RoleService.delete_role(db, role_id)

    if delete_role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )
    
    return {
        "message": "Role deleted successfully"
    }