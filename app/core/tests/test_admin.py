"""
Tests for the Django admin modifications
"""
from django.test import TestCase  # 导入Django测试模块
from django.contrib.auth import get_user_model  # 导入获取用户模型的方法
from django.urls import reverse  # 导入反向URL解析方法
from django.test import Client  # 导入Django测试客户端

class AdminSiteTests(TestCase):  # 定义测试类

    def setUp(self):  # 定义测试前的准备工作
        """Create user and client."""
        self.client = Client()  # 创建测试客户端
        self.admin_user = get_user_model().objects.create_superuser(  # 创建超级用户
            email = "admin@example.com",  # 超级用户的邮箱
            password = 'testpass123',  # 超级用户的密码
        )

        self.client.force_login(self.admin_user)  # 强制登录超级用户
        self.user = get_user_model().objects.create_user(  # 创建普通用户
            email = 'user@example.com',  # 普通用户的邮箱
            password = 'testpass123',  # 普通用户的密码
            name = 'Test user full name'  # 普通用户的姓名
        )

    def test_users_listed(self):  # 定义测试用户列表的方法
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')  # 获取用户列表的URL
        res = self.client.get(url)  # 发送GET请求
        self.assertContains(res, self.user.name)  # 断言用户列表中包含普通用户的姓名
        self.assertContains(res, self.user.email)  # 断言用户列表中包含普通用户的邮箱

    def test_user_change_page(self):  # 定义测试用户修改页面的方法
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])  # 获取用户修改页面的URL
        res = self.client.get(url)  # 发送GET请求
        self.assertEqual(res.status_code, 200)  # 断言响应状态码为200

    def test_create_user_page(self):  # 定义测试创建用户页面的方法
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')  # 获取创建用户页面的URL
        res = self.client.get(url)  # 发送GET请求
        self.assertEqual(res.status_code, 200)  # 断言响应状态码为200