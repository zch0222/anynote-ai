from pydantic import BaseModel


class WhisperRunVO(BaseModel):
    text: str
    srt: str
    txt: str

    def to_dict(self):
        return {
            "text": self.text,
            "srt": self.srt,
            "txt": self.txt
        }
