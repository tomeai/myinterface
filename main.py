import uvicorn
from fastapi import FastAPI
from pymilvus import connections
from starlette import status

from db.mysql import account_database
from router import disk, account
from settings import settings

app = FastAPI(
    root_path='/opentome/api/v1'
)


@app.get(
    "/healthz",
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
def healthz():
    """
    心跳检测
    :return:
    """
    return "OK"


@app.on_event("startup")
async def startup_db():
    print("Startup event is triggered.")
    await account_database.connect()
    connections.connect(host=settings.MILVUS_HOST, port=settings.MILVUS_PORT, alias="default", db_name='opentome')
    print("Startup event is done.")


@app.on_event("shutdown")
async def shutdown_db():
    print("shutdown event is triggered.")
    await account_database.disconnect()
    connections.disconnect(alias="default")
    print("shutdown event is done.")


app.include_router(disk.router)
app.include_router(account.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
