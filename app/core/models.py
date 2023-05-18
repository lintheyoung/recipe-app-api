"""
Database models.
"""
import uuid
import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)

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

class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, # 定义 user 字段，类型为 ForeignKey，值为 settings.AUTH_USER_MODEL
        on_delete=models.CASCADE, # 定义 on_delete 属性，值为 models.CASCADE，在删除这个人的时候，也顺便一起删除
    )
    title = models.CharField(max_length=255) # 定义 title 字段，类型为 CharField，最大长度为 255
    description = models.TextField(blank=True) # 定义 description 字段，类型为 TextField
    time_minutes = models.IntegerField() # 定义 time_minutes 字段，类型为 IntegerField
    price = models.DecimalField(max_digits=5, decimal_places=2) # 定义 price 字段，类型为 DecimalField
    link = models.CharField(max_length=255, blank=True) # 定义 link 字段，类型为 CharField，最大长度为 255
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')

    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title # 返回 title 字段的值
    
class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
    
class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name