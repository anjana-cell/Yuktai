from pydantic import BaseModel, Field


class AIInvestigationResult(BaseModel):
	finding: str = Field(..., description="The primary finding from the investigation.")
	likely_cause: str = Field(..., description="The most likely cause of the finding.")
	evidence: list[str] = Field(..., description="Evidence supporting the finding.")
	recommended_action: str = Field(..., description="The recommended next action.")
	confidence: float = Field(
		...,
		ge=0.0,
		le=1.0,
		description="The AI confidence in the investigation result, from 0.0 to 1.0.",
	)
