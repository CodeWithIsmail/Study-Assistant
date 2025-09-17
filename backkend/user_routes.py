# User Authentication Routes
from fastapi import APIRouter, HTTPException, Depends, status
from datetime import timedelta
from user_models import (
    UserSignupRequest, UserLoginRequest, UserResponse, 
    TokenResponse, UserUpdateRequest, ChangePasswordRequest, MessageResponse
)
from auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from database import user_db

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignupRequest):
    """
    Sign up a new user
    """
    try:
        print(f"Attempting to create user with email: {user_data.email}")
        
        # Check if user already exists
        existing_user = await user_db.get_user_by_email(user_data.email)
        if existing_user:
            print(f"User already exists: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        print("User doesn't exist, proceeding with creation...")
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        print("Password hashed successfully")
        
        # Create user
        user_id = await user_db.create_user(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name
        )
        print(f"User created with ID: {user_id}")
        
        # Get created user
        user = await user_db.get_user_by_id(user_id)
        if not user:
            print("Failed to retrieve created user")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        
        print("User retrieved successfully")
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_id}, expires_delta=access_token_expires
        )
        print("Access token created")
        
        # Update last login
        await user_db.update_last_login(user_id)
        print("Last login updated")
        
        # Prepare user response (remove sensitive data)
        user_response = UserResponse(
            id=user["_id"],
            email=user["email"],
            full_name=user.get("full_name"),
            is_active=user["is_active"],
            created_at=user["created_at"],
            last_login=user.get("last_login")
        )
        
        print("Returning successful response")
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
        
    except ValueError as e:
        print(f"ValueError: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user account: {str(e)}"
        )

@router.post("/login", response_model=TokenResponse)
async def login(user_credentials: UserLoginRequest):
    """
    Authenticate user and return access token
    """
    try:
        # Get user by email
        user = await user_db.get_user_by_email(user_credentials.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Check if user is active
        if not user.get("is_active", False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account is deactivated"
            )
        
        # Verify password
        if not verify_password(user_credentials.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["_id"]}, expires_delta=access_token_expires
        )
        
        # Update last login
        await user_db.update_last_login(user["_id"])
        
        # Prepare user response
        user_response = UserResponse(
            id=user["_id"],
            email=user["email"],
            full_name=user.get("full_name"),
            is_active=user["is_active"],
            created_at=user["created_at"],
            last_login=user.get("last_login")
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    """
    Get current user information
    """
    return UserResponse(
        id=current_user["_id"],
        email=current_user["email"],
        full_name=current_user.get("full_name"),
        is_active=current_user["is_active"],
        created_at=current_user["created_at"],
        last_login=current_user.get("last_login")
    )

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdateRequest,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Update current user information
    """
    try:
        update_data = {}
        
        if user_update.full_name is not None:
            update_data["full_name"] = user_update.full_name
        
        if user_update.email is not None:
            # Check if new email already exists
            existing_user = await user_db.get_user_by_email(user_update.email)
            if existing_user and existing_user["_id"] != current_user["_id"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            update_data["email"] = user_update.email
        
        if update_data:
            success = await user_db.update_user(current_user["_id"], update_data)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update user"
                )
        
        # Get updated user
        updated_user = await user_db.get_user_by_id(current_user["_id"])
        
        return UserResponse(
            id=updated_user["_id"],
            email=updated_user["email"],
            full_name=updated_user.get("full_name"),
            is_active=updated_user["is_active"],
            created_at=updated_user["created_at"],
            last_login=updated_user.get("last_login")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )

@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Change user password
    """
    try:
        # Verify current password
        if not verify_password(password_data.current_password, current_user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Hash new password
        new_hashed_password = get_password_hash(password_data.new_password)
        
        # Update password
        success = await user_db.update_user(
            current_user["_id"], 
            {"hashed_password": new_hashed_password}
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update password"
            )
        
        return MessageResponse(message="Password updated successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )

@router.post("/logout", response_model=MessageResponse)
async def logout(current_user: dict = Depends(get_current_active_user)):
    """
    Logout user (in a stateless JWT system, this is mainly for frontend)
    """
    return MessageResponse(message="Logged out successfully")

# Admin routes (optional)
@router.get("/users", response_model=list[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get all users (admin only - you can add admin check later)
    """
    try:
        users = await user_db.get_all_users(skip=skip, limit=limit)
        return [
            UserResponse(
                id=user["_id"],
                email=user["email"],
                full_name=user.get("full_name"),
                is_active=user["is_active"],
                created_at=user["created_at"],
                last_login=user.get("last_login")
            )
            for user in users
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch users"
        )
