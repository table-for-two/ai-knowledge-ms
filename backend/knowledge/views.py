from rest_framework import generics, permissions
from .models import KnowledgeBase, Document
from .serializers import KnowledgeBaseSerializer, DocumentSerializer


class KnowledgeBaseViewSet(generics.ListCreateAPIView):
    """
    获取知识库列表 / 创建新知识库
    """
    serializer_class = KnowledgeBaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # 核心 RBAC 逻辑：用户只能看到自己关联角色的知识库
        # 超级用户可以看到所有
        user = self.request.user
        if user.is_superuser:
            return KnowledgeBase.objects.all()
        result = KnowledgeBase.objects.filter(roles__users=user).distinct()
        print(result)
        return result
    
    def perform_create(self, serializer):
        # 创建时可以添加额外的自动化逻辑
        serializer.save()


class DocumentViewSet(generics.CreateAPIView):
    """
    上传文档接口
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # 自动将当前登录用户设为所有者
        # 并初始化状态为 'pending'
        serializer.save(owner=self.request.user, status='pending')
        
        # TODO: 在这里触发异步任务 (Celery) 进行向量化
        # task = process_document_task.delay(serializer.instance.id)
