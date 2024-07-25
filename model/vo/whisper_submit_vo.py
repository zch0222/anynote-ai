from pydantic import BaseModel

class WhisperSubmitVO(BaseModel):

    task_id: str

    def to_dict(self):
        return {
            "taskId": self.task_id,
        }
