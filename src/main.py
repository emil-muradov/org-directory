from fastapi import FastAPI
from fastapi.responses import Response
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from api.v1.routes import router as v1_router
from infrastructure.di.container import Container


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

container = Container()
container.wire(modules=["api.v1.routes"])

app.include_router(v1_router)


@app.get("/")
def health():
    return Response(status_code=200, content="OK")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3001, reload=True)
