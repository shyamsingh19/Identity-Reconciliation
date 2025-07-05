from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.services.identify_logic import identify_contact
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter()


class IdentifyRequest(BaseModel):
    email: str | None
    phoneNumber: str | None


@router.post("/identify")
async def identify(request: IdentifyRequest):
    try:
        logger.debug(f"Received request: {request}")
        if not request.email and not request.phoneNumber:
            raise HTTPException(
                status_code=400, detail="Either email or phoneNumber is required."
            )

        return await identify_contact(
            email=request.email, phoneNumber=request.phoneNumber
        )
    except Exception as e:
        logger.error(f"Error identifying contact: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
