from datetime import datetime, timedelta
import hashlib
import hmac

import requests


from app.configs.constants import (
    PAYOS_API_KEY,
    PAYOS_BASE_URL,
    PAYOS_CANCEL_URL,
    PAYOS_CHECKSUM_KEY,
    PAYOS_CLIENT_ID,
    PAYOS_EXPIRE,
    PAYOS_RETURN_URL,
)
from app.schemas.payos import BillData, PayloadData, ProductData
from operator import itemgetter


class PayOSConfig:
    def __init__(self, client_id: str, api_key: str, checksum_key: str, base_url: str):
        self.checksum_key = checksum_key
        self.headers = {
            "Content-Type": "application/json",
            "x-client-id": client_id,
            "x-api-key": api_key,
        }
        self.base_url = base_url

    async def create_payment_link(self, products: list[ProductData], bill: BillData):
        expire = (datetime.now() + timedelta(seconds=PAYOS_EXPIRE)).timestamp()
        payload = PayloadData(
            **bill.model_dump(),
            items=products,
            cancelUrl=PAYOS_CANCEL_URL,
            returnUrl=PAYOS_RETURN_URL,
        )
        signature = self.__create_signature(payload)
        url = f"{self.base_url}/v2/payment-requests"
        res = requests.post(
            url,
            json={
                **payload.model_dump(),
                "signature": signature,
                "expiredAt": int(expire),
            },
            headers=self.headers,
        )
        if res.status_code == 200:
            res = res.json()
            if res["code"] == "00":
                return res["data"]
            raise Exception(res["desc"])

    def __create_signature(self, payload: PayloadData):
        amount, cancel_url, description, order_code, return_url = itemgetter(
            "amount", "cancelUrl", "description", "orderCode", "returnUrl"
        )(payload.model_dump())
        data_str = f"amount={amount}&cancelUrl={cancel_url}&description={description}&orderCode={order_code}&returnUrl={return_url}"
        data_to_signature = hmac.new(
            self.checksum_key.encode("utf-8"),
            msg=data_str.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()
        return data_to_signature


PayOSApi = PayOSConfig(
    PAYOS_CLIENT_ID, PAYOS_API_KEY, PAYOS_CHECKSUM_KEY, PAYOS_BASE_URL
)
