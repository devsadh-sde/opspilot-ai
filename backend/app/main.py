
from fastapi import FastAPI

from app.api.inventory import router as inventory_router
from app.api.suppliers import router as supplier_router
from app.api.pricing import router as pricing_router


app = FastAPI(title="OpsPilot AI")

# Register our API routers
app.include_router(inventory_router)
app.include_router(supplier_router)
app.include_router(pricing_router)


@app.get("/")
def home():
    return {"message": "Welcome to OpsPilot AI!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
