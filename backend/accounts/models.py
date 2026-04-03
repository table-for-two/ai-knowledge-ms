from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
        自定义用户模型。
        继承自 AbstractUser，已包含：
        - username (str): 用户名
        - password (str): 加密哈希
        - is_active (bool): 激活状态
        - is_staff (bool): 是否可进入后台
    """
    email = models.EmailField(max_length=255, unique=True, verbose_name="邮箱")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    last_login_at = models.DateTimeField(null=True, blank=True, verbose_name="最后登录时间")
    
    roles = models.ManyToManyField(
        'Role',
        through='UserRole',
        related_name='users',
        verbose_name="用户角色"
    )
    
    class Meta:
        db_table = 'users'
    
    def get_custom_permissions(self):
        """
        递归获取用户及其角色树的所有权限 code。
        这是后续 AI 知识库进行权限过滤的核心逻辑。
        """
        permission_codes = set()
        for role in self.roles.all():
            # 这里可以编写递归逻辑查找父角色权限
            # 或者简单地获取当前所有角色的权限
            codes = role.permissions.values_list('code', flat=True)
            permission_codes.update(codes)
        return list(permission_codes)


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="角色名称")
    description = models.TextField(null=True, blank=True, verbose_name="描述")
    
    # 自引用外键：指向自身 ID
    # null=True, blank=True 因为顶级角色（如 Admin）没有父级
    # on_delete=models.SET_NULL 对应你 SQL 中的 ON DELETE SET NULL
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',  # 方便通过父级找子级：role.children.all()
        verbose_name="父角色"
    )
    
    permissions = models.ManyToManyField(
        'Permission',
        through='RolePermission',
        verbose_name="角色权限"
    )
    
    class Meta:
        db_table = 'roles'
    
    def __str__(self):
        return self.name


class Permission(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'permissions'


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'role_permissions'
        unique_together = ('role', 'permission')


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'user_roles'
        unique_together = ('user', 'role')
