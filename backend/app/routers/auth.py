from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, UserLogin, Token, UserUpdate
from app.utils import verify_password, get_password_hash, create_access_token
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/register", response_model=UserResponse, summary="用户注册")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """用户注册接口"""
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 检查学号是否已存在
    if user.student_id:
        existing_student = db.query(User).filter(User.student_id == user.student_id).first()
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="学号已存在"
            )

    # 创建新用户
    password_hash = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        password_hash=password_hash,
        real_name=user.real_name,
        student_id=user.student_id,
        email=user.email,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login", response_model=Token, summary="用户登录")
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """用户登录接口"""
    # 查找用户
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 验证密码
    if not verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 生成访问令牌
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user


@router.put("/me", response_model=UserResponse, summary="更新当前用户信息")
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新当前用户信息"""
    if user_update.real_name is not None:
        current_user.real_name = user_update.real_name
    if user_update.student_id is not None:
        # 检查学号是否被其他用户使用
        existing = db.query(User).filter(
            User.student_id == user_update.student_id,
            User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="学号已被使用"
            )
        current_user.student_id = user_update.student_id
    if user_update.email is not None:
        current_user.email = user_update.email
    
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/users", summary="获取用户列表")
async def get_users(
    skip: int = 0,
    limit: int = 20,
    role: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户列表（仅管理员）"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    
    users = query.offset(skip).limit(limit).all()
    return users
