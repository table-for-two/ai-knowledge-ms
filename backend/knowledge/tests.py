from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Role
from knowledge.models import KnowledgeBase, RoleKnowledgeBase

User = get_user_model()


class RBACLogicTest(TestCase):
    def setUp(self):
        # 1. 创建基础数据：用户、角色、知识库
        self.user = User.objects.create_user(
            username='km_specialist',
            email='km@example.com',
            password='password123'
        )
        self.role = Role.objects.create(
            name='Knowledge Manager',
            description='负责维护知识库文档的分片与索引'
        )
        self.kb = KnowledgeBase.objects.create(
            name='AI 架构指南',
            description='内部技术沉淀'
        )
    
    def test_rbac_linkage_chain(self):
        """
        验证逻辑链条：User -> Role -> KnowledgeBase
        """
        # 步骤 A: 将 User 关联到 Role
        # 假设你的 User 模型中有 roles = ManyToManyField(Role)
        self.user.roles.add(self.role)
        
        # 步骤 B: 将 Role 关联到 KnowledgeBase (通过中间表)
        # 方式 1: 直接使用关联管理器
        self.kb.roles.add(self.role)
        
        # 方式 2 (更严谨): 手动创建中间表实例，模拟复杂业务逻辑
        # RoleKnowledgeBase.objects.get_or_create(role=self.role, knowledge_base=self.kb)
        
        # 验证 1: 角色是否成功关联到知识库
        self.assertIn(self.role, self.kb.roles.all())
        
        # 验证 2: 拥有该角色的用户是否逻辑上属于该知识库
        # 我们检查：该知识库关联的所有角色中，是否包含“该用户所属的角色”
        user_roles = self.user.roles.all()
        kb_roles = self.kb.roles.all()
        
        # 取交集：判断用户角色与知识库角色是否有重合
        has_common_role = set(user_roles).intersection(set(kb_roles))
        self.assertTrue(len(has_common_role) > 0, "用户应当通过角色获得知识库访问权限")
        
        # 验证 3: 逆向查询验证
        # 检查这个特定的 User 是否出现在了 KnowledgeBase 关联的角色所涵盖的用户群中
        # 这取决于你在 User 和 Role 之间的反向引用定义
        is_user_in_kb = User.objects.filter(
            roles__knowledge_bases=self.kb,
            id=self.user.id
        ).exists()
        self.assertTrue(is_user_in_kb, "User 应该能通过 Role 链条回溯到 KnowledgeBase")
        
        print(f"✅ RBAC 链条验证通过: User({self.user.username}) -> Role({self.role.name}) -> KB({self.kb.name})")
