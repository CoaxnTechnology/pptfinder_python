from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import PPTData
from app.utils.google_search import fetch_ppt_results

router = APIRouter(prefix="", tags=["Check Keyword"])


@router.get("/check_keyword")
def check_keyword(keyword: str, db: Session = Depends(get_db)):

    # 1️⃣ Keyword validation
    if not keyword or keyword.strip() == "":
        raise HTTPException(status_code=400, detail="Keyword is required")

    keyword = keyword.strip().lower()

    # 2️⃣ Check if keyword already exists in database
    ppt_record = (
        db.query(PPTData)
        .filter(PPTData.keyword == keyword)
        .first()
    )

    if ppt_record:
        return JSONResponse(
            content={
                "exists": True,
                "object": ppt_record.object,
                "created_at": ppt_record.created_at.isoformat()
            },
            status_code=200
        )

    # 3️⃣ Fetch results from Google API
    fetched_results = fetch_ppt_results(keyword, num_results=2000)

    if not fetched_results:
        return JSONResponse(
            content={
                "exists": False,
                "keyword": keyword,
                "message": "No PPT results found on Google for this keyword."
            },
            status_code=200
        )

    # 4️⃣ Save new results into database
    new_record = PPTData(
        keyword=keyword,
        object=fetched_results,   # Cleaned: only title + link
        created_at=datetime.utcnow()
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    # 5️⃣ Return freshly fetched results
    return JSONResponse(
        content={
            "exists": True,
            "keyword": keyword,
            "saved": True,
            "total_results": len(fetched_results),
            "object": fetched_results
        },
        status_code=200
    )
