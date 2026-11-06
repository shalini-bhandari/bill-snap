from typing import Optional, Literal
from pydantic import BaseModel, Field


class FieldConfidence(BaseModel):
    is_bill: float = Field(ge=0, le=1)
    merchant_name: float = Field(ge=0, le=1)
    bill_date: float = Field(ge=0, le=1)
    total_amount: float = Field(ge=0, le=1)
    category: float = Field(ge=0, le=1)


class BillAnalysis(BaseModel):
    is_bill: bool

    merchant_name: Optional[str] = None
    bill_date: Optional[str] = None
    total_amount: Optional[float] = None

    category: Optional[
        Literal["Food", "Utilities", "Groceries"]
    ] = None

    confidence: FieldConfidence
