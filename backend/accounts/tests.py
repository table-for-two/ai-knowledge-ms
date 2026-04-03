from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()  # 始终使用这个方法获取自定义 User


class UserPermissionTest(TestCase):
    def setUp(self):
        # 创建一个测试用的超级用户
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='123'
        )
        # 创建一个普通用户
        self.normal_user = User.objects.create_user(
            username='worker',
            email='worker@example.com',
            password='123'
        )
    
    def test_admin_is_staff(self):
        """测试超级用户是否拥有后台管理权限"""
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)
    
    def test_normal_user_permissions(self):
        """测试普通用户默认不具备管理权限"""
        self.assertFalse(self.normal_user.is_staff)
        self.assertFalse(self.normal_user.has_perm('accounts.add_user'))
    
    def test_rbac_role_assignment(self):
        """测试你的自定义 Role 是否能正确关联到 User (这是你 RBAC 的核心)"""
        # 假设你定义了 Role 模型并建立了关联
        # 这里的逻辑取决于你在 models.py 中如何定义 User 和 Role 的关系
        pass

# class UserPermissionTest(TestCase):
#     pass
