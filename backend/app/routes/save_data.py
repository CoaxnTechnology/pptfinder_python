from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import PPTData

router = APIRouter(prefix="", tags=["Save Data"])


@router.post("/save_data")
def save_data(
    keyword: str = Form(...),
    object: str = Form(...),   # raw JSON string
    db: Session = Depends(get_db)
):

    # 1️⃣ Validate input
    if not keyword or not object:
        return JSONResponse(
            status_code=400,
            content={"error": "Keyword and object are required"}
        )

    # 2️⃣ Check if keyword already exists
    record = db.query(PPTData).filter(PPTData.keyword == keyword).first()

    if record:
        # 3️⃣ Update existing record
        record.object = object
        record.created_at = datetime.utcnow()
        db.commit()
        db.refresh(record)

        return {
            "success": True,
            "message": "Data updated successfully"
        }

    # 4️⃣ Insert new record
    new_record = PPTData(
        keyword=keyword,
        object=object,
        created_at=datetime.utcnow()
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "success": True,
        "message": "Data saved successfully"
    }
