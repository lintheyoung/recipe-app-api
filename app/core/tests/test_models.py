from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def create_user(email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'  # 设置测试用的邮箱
        password = 'testpass123'  # 设置测试用的密码
        user = get_user_model().objects.create_user(
            email=email,  # 使用上面设置的邮箱
            password=password,  # 使用上面设置的密码
        )

        self.assertEqual(user.email, email)  # 断言邮箱是否正确
        self.assertTrue(user.check_password(password))  # 断言密码是否正确

    def test_new_user_email_normailized(self):
        """Test email is normailized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],  # 测试大小写混合的邮箱
            ['Test2@Example.com', 'Test2@example.com'],  # 测试大小写混合的邮箱
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],  # 测试大小写混合的邮箱
            ['test4@example.COM', 'test4@example.com'],  # 测试大小写混合的邮箱
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')  # 创建用户
            self.assertEqual(user.email,expected)  # 断言邮箱是否正确

    def test_new_user_without_email_raise_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):  # 断言是否抛出 ValueError 异常
            get_user_model().objects.create_user('', 'test123')  # 创建用户

    def test_create_superuser(self):
        """Test creating a new superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',  # 设置测试用的邮箱
            'testpass123'  # 设置测试用的密码
        )

        self.assertTrue(user.is_superuser)  # 断言用户是否是超级用户
        self.assertTrue(user.is_staff)  # 断言用户是否是员工

    def test_create_recipe(self):
        """Test creating a new recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title = 'Sample recipe name',
            time_minutes = 5,
            price = Decimal('10.00'),
            description = 'Sample recipe description',
        )

        self.assertEqual(str(recipe), recipe.title)  # 断言 recipe 的字符串是否是 recipe 的 title))

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)