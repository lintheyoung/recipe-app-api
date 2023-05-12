from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id'] # 按照id排序
    list_display = ['email', 'name'] # 在admin页面中显示email和name
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _("Permissions"), # 权限
            {
                'fields':(
                    'is_active', # 是否激活
                    'is_staff', # 是否员工
                    'is_superuser', # 是否超级用户
                )
            }
        ),
        (_("Important dates"), {'fields': ('last_login',)}), # 最后登录时间
    )
    readonly_fields = ['last_login',] # 只读字段
    # 这个是用在创建一个新的用户的时候需要显示什么内容
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 
                       'password1',
                       'password2',
                       'name',
                       'is_active',
                       'is_staff',
                       'is_superuser',
                       )
        }),
    )

admin.site.register(models.User, UserAdmin) # 注册User模型和UserAdmin类到admin页面
admin.site.register(models.Recipe) # 注册Recipe模型到admin页面
admin.site.register(models.Tag)