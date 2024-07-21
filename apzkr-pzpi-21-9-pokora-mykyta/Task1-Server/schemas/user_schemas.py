from typing import Optional
from pydantic import BaseModel, EmailStr, constr, field_validator, Field
import re


class BaseUserRequest(BaseModel):
    email: EmailStr = Field(..., description="Електронна пошта користувача")
    password: constr(min_length=8) = Field(..., description="Пароль користувача")

    @field_validator('password')
    def validate_password(cls, v):
        if not re.search(r'\d', v):
            raise ValueError('Пароль повинен містити щонайменше одну цифру')
        if not re.search(r'[a-zA-Z]', v):
            raise ValueError('Пароль повинен містити щонайменше одну літеру')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Пароль повинен містити щонайменше один спеціальний символ')
        return v


class UserRegisterRequest(BaseUserRequest):
    display_name: Optional[str] = Field(None, description="Ім'я користувача для відображення")

    @field_validator('display_name')
    def validate_display_name(cls, v):
        if v and len(v) < 2:
            raise ValueError("Ім''я користувача повинно містити щонайменше 2 символи")
        return v


class UserUpdateRequest(BaseModel):
    display_name: Optional[str] = Field(None, description="Ім'я користувача для відображення")
    email: Optional[EmailStr] = Field(None, description="Електронна пошта користувача")
    phone_number: Optional[str] = Field(None, description="Номер телефону користувача")

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if v:
            cleaned_number = re.sub(r'\D', '', v)
            if 10 <= len(cleaned_number) <= 15:
                return '+' + cleaned_number if not v.startswith('+') else '+' + cleaned_number
            else:
                raise ValueError('Номер телефону повинен містити від 10 до 15 цифр')
        return v

    class Config:
        from_attributes = True
