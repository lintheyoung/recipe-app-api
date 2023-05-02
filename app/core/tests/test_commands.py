# 导入需要的模块和类
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# 使用patch装饰器模拟core.management.commands.wait_for_db.Command.check方法
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready"""
        # 设置模拟对象patched_check的返回值为True，表示数据库已准备好
        patched_check.return_value = True

        # 调用wait_for_db命令
        call_command('wait_for_db')

        # 断言patched_check方法被调用了一次，且参数为database=['default']
        patched_check.assert_called_once_with(databases=['default'])

    # 使用patch装饰器模拟time.sleep函数
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationError."""
        # 设置patched_check的side_effect属性，依次抛出两个Psycopg2Error异常、三个OperationalError异常，最后返回True
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        # 调用wait_for_db命令
        call_command('wait_for_db')

        # 断言patched_check方法被调用了6次
        self.assertEqual(patched_check.call_count, 6)

        # 断言最后一次调用patched_check方法时参数为database=['default']
        patched_check.assert_called_with(databases=['default'])
