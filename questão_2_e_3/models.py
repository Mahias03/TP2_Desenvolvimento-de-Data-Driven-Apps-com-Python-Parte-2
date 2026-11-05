from pydantic import BaseModel

class TextEn(BaseModel):
    text: str

class TextAl(BaseModel):
    text_al: str