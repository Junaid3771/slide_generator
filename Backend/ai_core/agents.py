from ai_core.gemini_client import GeminiAgent
from ai_core.prompts import SYSTEM_PROMPT_SLIDE_PREVIEW , SYSTEM_PROMPT_SLIDE_PREVIEW_WITH_STRUCTURE


gemini_agent = GeminiAgent()


async def chat_response(prompt, history, system_prompt=SYSTEM_PROMPT_SLIDE_PREVIEW):
    if system_prompt:
        history = [{'role': 'system', 'content': system_prompt}] + history
    async for chunk in gemini_agent.execute_agent(prompt, history):
        yield chunk


async def content_generation(prompt, history):
    # Helper for API: returns full response as a string
    response = ""
    async for chunk in chat_response(prompt, history):
        response += chunk
    return response


async def structured_content_generation(prompt, history,system_prompt=SYSTEM_PROMPT_SLIDE_PREVIEW_WITH_STRUCTURE):
    if system_prompt:
        history = [{'role': 'system', 'content': system_prompt}] + history
        
    structured = await gemini_agent.generate_structured_output(prompt, history)
    return structured
        
        