from fastapi import FastAPI

app = FastAPI(
    title="My FastAPI App",
    description="My FastAPI App",
    version="0.0.1",
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    return {"stats": "ok"}
