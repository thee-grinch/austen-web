from fastapi import FastAPI, HTTPException, Request, APIRouter
import google.generativeai as genai  # Corrected import
from google.generativeai.types import GenerationConfig  # Added import for safety settings
import markdown

router = APIRouter()

# Replace with your actual Gemini API key
API_KEY = "YOUR_API_KEY"  # DO NOT hardcode in production! Use environment variables.
genai.configure(api_key="AIzaSyC-0ZgvH1ZHvm6vKFjB2hpdamR12QH5CvI") #moved to main app or initialized in environment variables, example : client = genai.GenerativeModel(model_name="gemini-1.0-pro", api_key=API_KEY)

@router.post("/chatbot")
async def generate_content(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required.")

    try:
        model = genai.GenerativeModel('gemini-1.0-pro') # Ensure model name is correct
        response = model.generate_content(prompt) # Pass just the prompt
        generated_text = response.candidates[0].content.parts[0].text
        html = f"<span>{markdown.markdown(generated_text)}</span>"
        print(html)        
        return {"reply": html}  # Access the generated text from the response


        # return {"result": response.text}  # Access the generated text from the response

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))


#Example how to initialize and configure safety settings
# safety_settings = [
#     {
#         "category": "HARM_CATEGORY_HARASSMENT",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE",
#     },
#     {
#         "category": "HARM_CATEGORY_HATE_SPEECH",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE",
#     },
# ]

# generation_config = GenerationConfig(temperature=0.7) # Set temperature
# model = genai.GenerativeModel(model_name="gemini-1.0-pro",
#                                 generation_config=generation_config,
#                                 safety_settings=safety_settings) # Add safety settings and temperature to model initialization