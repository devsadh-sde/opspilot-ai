
from fastapi import FastAPI

from app.api.order_proposals import router as order_proposals_router
from app.api.inventory import router as inventory_router
from app.api.suppliers import router as supplier_router
from app.api.pricing import router as pricing_router
from app.api.requests import router as request_router
from app.api.fulfillment import router as fulfillment_router
from app.api.policies import router as policies_router


app = FastAPI(title="OpsPilot AI")

# Register our API routers
app.include_router(inventory_router)
app.include_router(fulfillment_router)
app.include_router(request_router)
app.include_router(supplier_router)
app.include_router(pricing_router)
app.include_router(order_proposals_router)
app.include_router(policies_router)


@app.get("/")
def home():
    return {"message": "Welcome to OpsPilot AI!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
