from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def root():
    return {"message": "Loan Workflow API"}