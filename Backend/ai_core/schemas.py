from typing import List, Union
from pydantic import BaseModel

class TitleSlide(BaseModel):
    title: str
    subtitle: str
    content: str   # extended description
    image_description: str

class BulletSlide(BaseModel):
    title: str
    bullets: List[str]
    image_description: str

class TwoColumnSlide(BaseModel):
    title: str
    left_column: List[str]
    right_column: List[str]
    image_description: str

class ContentWithImageSlide(BaseModel):
    title: str
    content: str
    image_description: str

class SlidePreview(BaseModel):
    slide_no: int
    slide_category: str   # one of: "title_slide", "bullet_slide", "two_column_slide", "content_with_image"
    slide_content: Union[TitleSlide, BulletSlide, TwoColumnSlide, ContentWithImageSlide]
