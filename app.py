from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from router.message import MessageRouter

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True))

@app.get("/")
async def index():
    return FileResponse("./static/index.html", media_type="text/html")

app.include_router(MessageRouter)