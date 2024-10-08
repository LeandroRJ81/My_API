from fastapi import APIRouter, HTTPException, status
import pymongo.errors
from schemas.user_schema import UserAuth, UserDetail
from services.user_service import UserService
import pymongo

user_router = APIRouter()

@user_router.post('/adiciona', summary='Adiciona Usuário', response_model=UserDetail)
async def adiciona_usuario(data: UserAuth):
    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username ou e-mail deste usuário já existe'
        )

@user_router.delete('/exclui', summary='Exclui Usuário')
async def exclui_usuario(username: str, password: str):
    try:
        # Verifica se o usuário existe e a senha está correta
        user = await UserService.delete_user(username=username, password=password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Usuário não encontrado ou senha incorreta'
            )
        
        return {"detail": "Usuário excluído com sucesso"}
    
    except pymongo.errors.PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Erro no banco de dados'
        )