from fastapi import FastAPI
from sqlalchemy import text

# from app.core.database import SessionLocal

from app.routers.role import router as role_router
from app.routers.customer import router as customer_router
from app.routers.vehicle import router as vehicle_router
from app.routers.supplier import router as supplier_router
from app.routers.user import router as user_router
from app.routers.employee import router as employee_router
from app.routers.service_type import router as service_type_router
from app.routers.repair_status import router as repair_status_router
from app.routers.part import router as part_router
from app.routers.repair_part import router as repair_part_router
from app.routers.repair_order import router as repair_order_router
from app.routers.dashboard import router as dashboard_router
from app.routers.auth import router as auth_router
from app.routers.repair_workflow import router as repair_workflow_router

app = FastAPI(
    title="GarageHub API",
    description="API for vehicle repair shop management system",
    version="1.0.0",
)

app.include_router(dashboard_router)
app.include_router(role_router)
app.include_router(customer_router)
app.include_router(vehicle_router)
app.include_router(supplier_router)
app.include_router(user_router)
app.include_router(employee_router)
app.include_router(service_type_router)
app.include_router(repair_status_router)
app.include_router(part_router)
app.include_router(repair_part_router)
app.include_router(repair_order_router)
app.include_router(repair_workflow_router)
app.include_router(auth_router)
