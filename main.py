from fastapi import FastAPI

from routers import signal_router
app = FastAPI()

app.include_router(signal_router.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}

