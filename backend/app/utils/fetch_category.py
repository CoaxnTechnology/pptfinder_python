# app/utils/fetch_category.py

import requests
from fastapi import HTTPException


CATEGORY_URL = "https://coaxn.com/keywords.php"


def fetch_category_data():
    """
    Fetch category data from coaxn.com/keywords.php
    Returns parsed JSON structure or raises HTTPException on failure.
    """

    try:
        # -----------------------------
        # Make API Request
        # -----------------------------
        response = requests.get(CATEGORY_URL, timeout=10)
        response.raise_for_status()

        # -----------------------------
        # Parse JSON Response
        # -----------------------------
        try:
            data = response.json()
        except ValueError:
            raise HTTPException(
                status_code=500,
                detail="Invalid JSON format returned from Category API"
            )

        # -----------------------------
        # Validate Data
        # -----------------------------
        if not isinstance(data, dict) and not isinstance(data, list):
            raise HTTPException(
                status_code=500,
                detail="Unexpected response format from Category API"
            )

        if not data:
            raise HTTPException(
                status_code=500,
                detail="Category API returned empty response"
            )

        return data

    except requests.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Category API timed out"
        )

    except requests.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Failed to connect to Category API"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch category data: {str(e)}"
        )
