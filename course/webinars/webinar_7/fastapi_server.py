from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
import uvicorn

PORT = 8080
STATIC_FOLDER = Path("./course/webinars/webinar_7/static/")

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_FOLDER))


@app.get("/ping")
def ping():
    return "pong"


@app.get("/index.html")
def favicon():
    return FileResponse(STATIC_FOLDER / "index.html")

@app.get("/styles.css", response_class=RedirectResponse)
def favicon():
    return f"/static/styles.css"


@app.get("/favicon.ico", response_class=RedirectResponse)
def favicon():
    return f"/static/favicon.png"


if __name__ == "__main__":
    uvicorn.run(app, port=PORT, log_level="info")