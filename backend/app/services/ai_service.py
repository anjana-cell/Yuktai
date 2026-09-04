import json
import os

from dotenv import load_dotenv
from google import genai

from app.schemas.ai import AIInvestigationResult


load_dotenv()


def investigate_exception(exception_data):
	api_key = os.getenv("GEMINI_API_KEY")
	if not api_key:
		raise ValueError("GEMINI_API_KEY is not set")

	prompt = f"""
The deterministic reconciliation engine has already detected an exception.
Investigate and explain the supplied exception data only:

{json.dumps(exception_data, default=str)}

Do not override the reconciliation result.
Do not invent transactions or evidence.
Do not make authoritative financial decisions.
Explain the exception and recommend what a human reviewer should investigate.
Return only the requested structured fields.
"""

	try:
		client = genai.Client(api_key=api_key)
		response = client.interactions.create(
			model="gemini-3.6-flash",
			input=prompt,
			response_format={
				"type": "text",
				"mime_type": "application/json",
				"schema": AIInvestigationResult.model_json_schema(),
			},
		)

		result_data = json.loads(response.output_text)
		expected_fields = set(AIInvestigationResult.model_fields)
		if set(result_data) != expected_fields:
			raise ValueError("Gemini response did not contain the required fields")
		return AIInvestigationResult.model_validate(result_data)
	except Exception as error:
		raise RuntimeError(f"Gemini investigation request failed: {error}") from error
