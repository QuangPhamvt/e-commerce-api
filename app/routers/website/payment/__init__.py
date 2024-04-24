from fastapi import APIRouter, Depends
from app.configs.constants import PAYMENT, PAYMENT_PATH, PAYMENT_PREFIX
from app.dependencies.get_db import get_db
from app.dependencies.verify_access_token import get_me
from app.schemas.bill import CreateBillBody
from app.schemas.responses import Res201Resquest
from fastapi import status

from app.services.payment import PaymentService

"""
Payment API
"""

CHECKOUT = PAYMENT_PATH["CHECKOUT"]
PAYMENT_SUCCESS = PAYMENT_PATH["PAYMENT_SUCCESS"]
PAYMENT_FAIL = PAYMENT_PATH["PAYMENT_FAIL"]
GET_BILL_DETAIL = PAYMENT_PATH["GET_BILL_DETAIL"]


router = APIRouter(prefix=PAYMENT_PREFIX, tags=[PAYMENT])


@router.post(
    CHECKOUT,
    description="This endpoint is used to checkout a cart",
    status_code=status.HTTP_201_CREATED,
    responses={201: {"description": "Checkout cart succeed!", "model": Res201Resquest}},
)
async def checkout(body: CreateBillBody, user_id=Depends(get_me), db=Depends(get_db)):
    return await PaymentService(db).checkout(body, user_id)


@router.get(
    PAYMENT_SUCCESS,
    description="This endpoint is used to update a bill when payment success",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Bill was paid!"}},
)
async def payment_success(orderCode: int, db=Depends(get_db)):
    return await PaymentService(db).payment_success(orderCode)


@router.get(
    PAYMENT_FAIL,
    description="This endpoint is used to update a bill when payment fail",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Bill was canceled!"}},
)
async def payment_fail(orderCode: int, db=Depends(get_db)):
    return await PaymentService(db).payment_fail(orderCode)
