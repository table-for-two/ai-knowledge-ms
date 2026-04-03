from rest_framework import serializers
from .models import KnowledgeBase, Document, DocumentEmbedding
from django.contrib.auth import get_user_model

User = get_user_model()


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    # 显示关联的文档数量（可选，增加前端体验）
    document_count = serializers.IntegerField(source='documents.count', read_only=True)
    
    class Meta:
        model = KnowledgeBase
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'document_count']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DocumentSerializer(serializers.ModelSerializer):
    # 返回 owner 的用户名而不是 ID
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    # 允许在序列化时看到所属的知识库 ID 列表
    kb_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=KnowledgeBase.objects.all(),
        source='knowledge_bases'
    )
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'file_path', 'owner_name', 'kb_ids',
            'is_public', 'tags', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner_name', 'status', 'created_at', 'updated_at']


class DocumentEmbeddingSerializer(serializers.ModelSerializer):
    """
    主要用于搜索结果展示。
    注意：通常不序列化巨大的 'embedding' 向量字段，只返回文本块。
    """
    
    class Meta:
        model = DocumentEmbedding
        fields = ['id', 'document', 'content_chunk', 'chunk_index', 'created_at']
