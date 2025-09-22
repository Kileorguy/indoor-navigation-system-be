from fastapi import APIRouter

router = APIRouter(
    prefix="/signal",
    tags=["signal"],
    responses={404: {"description": "Not found"}},
)

bool_val = False



@router.get("/")
async def read_bool():
    return {"bool": bool_val}

@router.post("/")
async def update_bool(new_val: bool):
    global bool_val
    bool_val = new_val
