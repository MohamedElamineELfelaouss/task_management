from django.urls import path
from .views import TaskListCreateView, TaskDetailView, TaskStatusUpdateView,UserListCreateView,UserDetailView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/<str:status>/', TaskStatusUpdateView.as_view(), name='task-status-update'),
    
     # User Endpoints
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
