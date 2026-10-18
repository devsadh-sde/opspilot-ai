
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag.policy_retriever import retrieve_policies


router = APIRouter(
    prefix="/policies",
    tags=["Business Policies"]
)


class PolicySearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)


@router.post("/search")
def search_policies(request: PolicySearchRequest):
    try:
        results = retrieve_policies(
            query=request.query,
            top_k=request.top_k
        )

        return {
            "query": request.query,
            "total_results": len(results),
            "policies": results
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Policy knowledge base is unavailable."
        )
