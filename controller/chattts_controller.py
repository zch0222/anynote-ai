from fastapi import APIRouter, Depends, Request
from service.chattts_service import ChatTTSService
from model.dto import ChatttsToWavDTO

chattts_router = APIRouter()

@chattts_router.post('/api/chattts/toWav')
def chattts(data: ChatttsToWavDTO, service: ChatTTSService = Depends()):
    return service.to_wav(data.texts)


