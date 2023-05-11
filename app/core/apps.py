from django.apps import AppConfig

# 这段代码定义了一个名为CoreConfig的Django应用程序配置类，它位于app\core\apps.py文件中。该类指定了默认的自动字段类型为django.db.models.BigAutoField，并将应用程序命名为core。这个类可以用来配置应用程序的一些行为，例如在应用程序启动时执行某些操作。

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
