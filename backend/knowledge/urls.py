from django.urls import path
from .views import KnowledgeBaseViewSet, DocumentViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('knowledge-bases/', KnowledgeBaseViewSet.as_view(), name='kb-list-create'),
    path('documents/upload/', DocumentViewSet.as_view(), name='document-upload'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
