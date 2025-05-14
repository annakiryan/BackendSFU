from pydantic import BaseModel
import logging
from core.config import settings
from typing import Annotated, Protocol
from fastapi import Depends

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SMSMessage(BaseModel):
    phone: str
    message: str


class RealSMSService:
    async def send(self, sms: SMSMessage) -> None:
        logger.info(f"Sending real SMS to {sms.phone}: {sms.message}")


class TestSMSService:
    async def send(self, sms: SMSMessage) -> None:
        logger.info(f"Test SMS to {sms.phone}: {sms.message}")


class SMSService(Protocol):
    async def send(self, sms: SMSMessage) -> None:
        pass


def get_sms_service() -> SMSService:
    if settings.stage.name == "dev":
        return TestSMSService()
    return RealSMSService()


SMSServiceDep = Annotated[SMSService, Depends(get_sms_service)]
