# app/memory/permissions.py

from fastapi import HTTPException, status

def check_memory_owner(user_id: int, memory_user_id: int):
    if user_id != memory_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas autorisé à accéder à cette mémoire"
        )
