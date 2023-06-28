
import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProductDTO:
    id: uuid.UUID
    name: str
    description: str
    price: float
    stock: int
    createdAt: datetime
    updatedAt: datetime
    photo: str