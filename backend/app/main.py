from fastapi import FastAPI

app = FastAPI(title="OpsPilot AI")

@app.get("/")
def home():
    return {"message": "Welcome to OpsPilot AI!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
