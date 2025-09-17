
from google import genai
import json
from ai_core.schemas import SlidePreview
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.genai import types
from google.genai.errors import ServerError
from PIL import Image
from io import BytesIO
import os
from settings import GENAI_API_KEY
class GeminiAgent:
    def __init__(self):
        self.api_key = GENAI_API_KEY
        self.client = genai.Client(api_key=self.api_key, http_options={'api_version': 'v1alpha'})
        self.model = "gemini-2.0-flash-exp"
        self.config = {"response_modalities": ["TEXT"]}

    async def execute_agent(self, question, history):
        # Format history as context
        context = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history])

        # Prepare full input with context
        full_input = f"{context}\nUser: {question}"

        async with self.client.aio.live.connect(model=self.model, config=self.config) as session:
            await session.send(input=full_input, end_of_turn=True)

            async for response in session.receive():  # Stream responses
                if response.text:
                    yield response.text  # Send chunk to `chat_response()`
    
    
    async def generate_structured_output(self, question, history):
        """
        Calls Gemini with the system prompt and returns structured JSON output.
        """
        # Format history for context
        context = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history])

        # Combine system + context + user question
        full_input = f"{context}\nUser: {question}"

        response = self.client.models.generate_content(
    model="gemini-2.5-flash",
    contents=full_input,
    config={
        "response_mime_type": "application/json",
        "response_schema": list[SlidePreview],
    },
)
        # Extract text output
        print("Response object:", response)
        raw_text = response.text
        print("Raw response:", raw_text)

        # Try parsing JSON
        try:
            structured = json.loads(raw_text)
        except json.JSONDecodeError:
            structured = {"error": "Invalid JSON returned", "raw": raw_text}

        return structured
    
    
    
class ImageGenAgent:
    def __init__(self):
        self.api_key = GENAI_API_KEY
        self.client = genai.Client(api_key=GENAI_API_KEY ,http_options={'api_version': 'v1alpha'})
        self.model = 'gemini-2.0-flash-exp'
        self.config = types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])

    @retry(
        stop=stop_after_attempt(10),              # Up to 5 attempts
        wait=wait_exponential(multiplier=1, min=2, max=40),  # Wait: 2s, 4s, 8s, 16s
        retry=retry_if_exception_type(ServerError)            # Only retry on ServerError (like 503)
    )
    
    
    def generate_image_response(self, prompt: str):
        """
        Generates content (text + image) based on a given prompt.
        Returns:
            - response_text: Generated description
            - image: PIL.Image object if image was generated
        """
        system_prompt = (
    "You are a large language model built by Junaid. "
    "For questions about your identity, training, or model details, respond only with this: "
    "'I'm a language model built by Junaid. Please contact him for more info.' "
    "Do not provide any additional information or explanations about your training, origin, or technical details. "
    "For all other prompts, respond appropriately to complete the task."
)

        response = self.client.models.generate_content(
            model=self.model,
            contents=[system_prompt, prompt],  # Flat list of strings
            config=self.config
        )

        response_text = None
        image = None

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                response_text = part.text
            elif part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))

        return response_text, image
