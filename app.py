from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True))

@app.get("/")
async def index():
    return FileResponse("./static/index.html", media_type="text/html")