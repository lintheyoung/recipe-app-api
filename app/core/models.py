"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager): # 定义 UserManager 类，继承 BaseUserManager 类
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email: # 如果 email 为空，则抛出 ValueError 异常
            raise ValueError('User must have an email address.')
        user = self.model(email = self.normalize_email(email), **extra_fields) # 创建一个新的用户对象
        user.set_password(password) # 设置用户密码
        user.save(using = self._db) # 保存用户对象到数据库

        return user # 返回用户对象

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password) # 创建一个新的超级用户对象
        user.is_staff = True # 将用户设置为管理员
        user.is_superuser = True # 将用户设置为超级用户
        user.save(using = self._db) # 保存用户对象到数据库

        return user # 返回用户对象

class User(AbstractBaseUser, PermissionsMixin): # 定义 User 类，继承 AbstractBaseUser 和 PermissionsMixin 类
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True) # 定义 email 字段，类型为 EmailField，最大长度为 255，唯一
    name = models.CharField(max_length=255) # 定义 name 字段，类型为 CharField，最大长度为 255
    is_active = models.BooleanField(default=True) # 定义 is_active 字段，类型为 BooleanField，默认值为 True
    is_staff = models.BooleanField(default=False) # 定义 is_staff 字段，类型为 BooleanField，默认值为 False

    objects = UserManager() # 定义 objects 属性，值为 UserManager 类的实例

    USERNAME_FIELD = 'email' # 定义 USERNAME_FIELD 属性，值为 'email'