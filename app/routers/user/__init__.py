from fastapi import APIRouter


router = APIRouter()


@router.get("/detail")
async def read_user():
    return {"detail": "Hello World from user api"}
