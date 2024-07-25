import ChatTTS
import torch
import torchaudio
from constants.chattts_constants import CHATTTS_WAV_PTH


class ChatTTSService:
    def __init__(self):
        self.chat = ChatTTS.Chat()
        self.chat.load(compile=True)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        pass

    def to_wav(self, texts: list):
        wavs = self.chat.infer(texts)
        for i in range(len(wavs)):
            torchaudio.save(f"{CHATTTS_WAV_PTH}/basic_output{i}.wav", torch.from_numpy(wavs[i]).unsqueeze(0), 24000)


