
from fastapi import APIRouter

from app.routers import user_router, auth_router, customer_router, supplier_router, furnace_router, product_router, hardness_router, inoculant_router
from app.routers import fesi_granule_router
from app.routers import packing_router
from app.routers import element_router
from app.routers import iron_type_router
from app.routers import raw_material_router
from app.routers import wire_router
from app.routers import element_stock_router
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
api_router.include_router(product_router.router)
api_router.include_router(hardness_router.router)
api_router.include_router(inoculant_router.router)
api_router.include_router(fesi_granule_router.router)
api_router.include_router(packing_router.router)
api_router.include_router(element_router.router)
api_router.include_router(iron_type_router.router)
api_router.include_router(raw_material_router.router)
api_router.include_router(wire_router.router)
api_router.include_router(element_stock_router.router)