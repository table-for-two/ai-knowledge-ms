from pgvector.django import VectorField, HnswIndex
from django.db import models
from accounts.models import User, Role


class KnowledgeBase(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    roles = models.ManyToManyField(Role, through='RoleKnowledgeBase', related_name='knowledge_bases')
    
    class Meta:
        db_table = 'knowledge_bases'


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='docs/%Y/%m/%d/',
        verbose_name="物理文件",
        default=''
    )
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    knowledge_bases = models.ManyToManyField(
        KnowledgeBase,
        through='KnowledgeBaseDocument',
        related_name='documents'
    )
    is_public = models.BooleanField(default=False)
    tags = models.JSONField(default=dict)  # 对应 SQL 的 JSONB
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 记录文档处理状态：上传中、分片中、已索引、失败
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '待处理'),
            ('processing', '处理中'),
            ('completed', '已完成'),
            ('failed', '失败')
        ],
        default='pending'
    )
    
    class Meta:
        db_table = 'documents'
        indexes = [
            models.Index(fields=['owner'], name='idx_docs_owner'),
        ]


class DocumentEmbedding(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='embeddings')
    # OpenAI text-embedding-3-small 维度为 1536
    embedding = VectorField(dimensions=1536)
    content_chunk = models.TextField()
    chunk_index = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'document_embeddings'
        indexes = [
            # 特殊索引（如 HNSW）必须在模型中显式声明，以便 Django 识别
            HnswIndex(
                name='idx_doc_vector',
                fields=['embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops']
            )
        ]


class KnowledgeBaseDocument(models.Model):
    knowledge_base = models.ForeignKey(KnowledgeBase, on_delete=models.CASCADE, related_name='kb_document_links')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='doc_kb_links')
    
    added_at = models.DateTimeField(auto_now_add=True)  # 特有的元数据
    # 状态可以放在这里，实现“一文多库”的独立进度控制
    status = models.CharField(max_length=20, default='pending')
    
    class Meta:
        db_table = 'knowledge_base_documents'
        unique_together = ('knowledge_base', 'document')


class RoleKnowledgeBase(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_kb_links')
    knowledge_base = models.ForeignKey(KnowledgeBase, on_delete=models.CASCADE, related_name='kb_role_links')
    
    class Meta:
        db_table = 'role_knowledge_bases'
        unique_together = ('role', 'knowledge_base')
