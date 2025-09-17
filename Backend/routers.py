from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse
from ai_core.agents import content_generation , structured_content_generation
from ai_core.ppt_templ import create_title_slide , create_bullet_slide , create_two_column_slide
from pptx import Presentation
import io
import json
import os
from datetime import datetime

router = APIRouter()

@router.post("/content_generation_api")
async def content_generation_api(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    history = data.get("history", [])

    response = await structured_content_generation(prompt, history)
    return JSONResponse({"content": response})



from ai_core.gemini_client import ImageGenAgent

@router.post("/generate_ppt")
async def generate_ppt(request: Request):
    data = await request.json()
    slides = data.get("slides", [])
    if isinstance(slides, str):
        slides = json.loads(slides)
    prs = Presentation()
    image_agent = ImageGenAgent()
    for idx, slide in enumerate(slides):
        category = slide.get("slide_category", "").lower()
        print(f"Processing slide {idx+1} of category: {category}")
        content = slide.get("slide_content", {})
        image = None
        if "image_description" in content and content["image_description"]:
            # Generate image from description
            _, image = image_agent.generate_image_response(content["image_description"])
            # Save image for debugging
            if image is not None:
                images_dir = os.path.join(os.path.dirname(__file__), "images")
                os.makedirs(images_dir, exist_ok=True)
                image_filename = f"slide_{idx+1}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
                image_path = os.path.join(images_dir, image_filename)
                image.save(image_path)
        if category == "title slide":
            create_title_slide(
                prs,
                content.get("title", ""),
                content.get("subtitle", ""),
                content.get("content", ""),
                image=image
            )
        # TODO: Add more slide types here
        elif category == 'bullet slide':
            print(content.get("bullets"))
            create_bullet_slide(
                prs,
                content.get("title", ""),
                content.get("bullets", []),  # list of strings
                image=image
            )
            
        elif category == 'two column slide':
            create_two_column_slide(prs, content.get("title", "") ,
                content.get("left_column", []),
                content.get("right_column", []),
                                    image=image                                   
                                    )
        elif category == 'content with image slide':
            print(content.get("content", ""))
            create_title_slide(prs, content.get("title", ""),
                               None,
                               content.get("content", ""),
                                 image=image
                                 )
    output = io.BytesIO()
    prs.save(output)
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": "attachment; filename=generated_presentation.pptx"}
    )