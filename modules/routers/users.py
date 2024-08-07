from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from modules.database.models import user_farm_models
from modules.database.schemas import user_farm_schemas
from modules.utilities import auth
from modules.utilities.auth import get_db_session

router = APIRouter(tags=["Users"])


@router.post("/register", response_model=user_farm_schemas.UserInDB)
def register_user(user: user_farm_schemas.UserCreate, db: Session = Depends(get_db_session)):  # noqa: B008
    db_user = (
        db.query(user_farm_models.User).filter(user_farm_models.User.username == user.username).first()
    )  # noqa: 950
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = user_farm_models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )  # noqa: 950
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token", response_model=user_farm_schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)  # noqa: B008
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=user_farm_schemas.UserInDB)
async def read_users_me(current_user: user_farm_models.User = Depends(auth.get_current_user)):  # noqa: B008
    return current_user


@router.post("/logout")
async def logout(current_user: user_farm_models.User = Depends(auth.get_current_user)):  # noqa: B008
    # In a stateless JWT system, we don't actually invalidate the token on the server.
    # Instead, we rely on the client to remove the token.
    # Here, we'll just return a success message.
    return {"detail": "Successfully logged out"}


# # Protected route example
# @router.get("/protected-route")
# async def protected_route(current_user: user_farm_models.User = Depends(auth.get_current_user)):  # noqa: B008
#     return {"message": f"Hello, {current_user.username}! This is a protected route."}
