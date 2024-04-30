from fastapi import FastAPI

app = FastAPI(debug=True)
myapi = FastAPI(debug=True)


@myapi.get("/")
async def root():
    return {"message": "Hello World"}

app.mount ("/api", myapi)