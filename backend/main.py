from fastapi import FastAPI

app = FastAPI(title="Erp System")

@app.get("/")
def root():
    return {"message" : "Erp System is runnimg"}