from fastapi import APIRouter

router = APIRouter(
    prefix="/signal",
    tags=["signal"],
    responses={404: {"description": "Not found"}},
)

bool_val = False

# ini buat rest API

@router.get("/")
async def read_bool():
    return {"bool": bool_val}

@router.post("/")
async def toggle_bool():
    global bool_val
    if bool_val: bool_val = False
    else: bool_val = True
    return {"bool": bool_val}
