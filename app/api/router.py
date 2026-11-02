
from fastapi import APIRouter

from app.routers import user_router, auth_router, customer_router, supplier_router, furnace_router

api_router = APIRouter()

api_router.include_router(
    user_router.router,
    prefix="/users",
    tags=["User Management"],
)


api_router.include_router(
    auth_router.router,
    prefix="/auth",
    tags=["Authentication"],
)

api_router.include_router(customer_router.router)
api_router.include_router(supplier_router.router)
api_router.include_router(furnace_router.router)
