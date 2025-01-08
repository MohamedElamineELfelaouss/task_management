from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer, UserSerializer,TaskStatusUpdateSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
)


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve a list of tasks",
        description=(
            "Returns a list of tasks for the authenticated user. "
            "You can filter the tasks using the following query parameters:\n\n"
            "- `status`: Filter by task status (e.g., `Pending`, `Completed`).\n"
            "- `priority`: Filter by task priority (e.g., `Low`, `Medium`, `High`).\n\n"
            "You can also order tasks using the `ordering` parameter:\n\n"
            "- `ordering=priority` to order by priority.\n"
            "- `ordering=due_date` to order by due date.\n"
            "- `ordering=status` to order by status."
        ),
        parameters=[
            OpenApiParameter(
                name="status",
                description="Filter tasks by their status (Pending or Completed).",
                required=False,
                type=str,
                examples=[
                    OpenApiExample("Pending", value="Pending"),
                    OpenApiExample("Completed", value="Completed"),
                ],
            ),
            OpenApiParameter(
                name="priority",
                description="Filter tasks by their priority (Low, Medium, High).",
                required=False,
                type=str,
                examples=[
                    OpenApiExample("Low", value="Low"),
                    OpenApiExample("Medium", value="Medium"),
                    OpenApiExample("High", value="High"),
                ],
            ),
            OpenApiParameter(
                name="ordering",
                description=(
                    "Order the results by a field. Supported fields are:\n"
                    "- `priority`\n"
                    "- `due_date`\n"
                    "- `status`"
                ),
                required=False,
                type=str,
                examples=[
                    OpenApiExample("Order by priority", value="priority"),
                    OpenApiExample("Order by due date", value="due_date"),
                    OpenApiExample("Order by status", value="status"),
                ],
            ),
        ],
    ),
    post=extend_schema(
        summary="Create a new task",
        description="Creates a new task for the authenticated user.",
        request=TaskSerializer,
        responses=TaskSerializer,
    ),
)
class TaskListCreateView(generics.ListCreateAPIView):
    """
    List tasks for the authenticated user or create a new task.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "priority"]
    ordering_fields = ["priority", "due_date", "status"]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve a specific task",
        description="Retrieves a task by ID for the authenticated user.",
    ),
    put=extend_schema(
        summary="Update a task",
        description="Fully updates a task for the authenticated user.",
    ),
    delete=extend_schema(
        summary="Delete a task",
        description="Deletes a task for the authenticated user.",
    ),
    patch=extend_schema(
        operation_id="update_task_details",  # Unique operation ID
        description="Partially updates a task's details.",
    ),
)
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific task.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TaskStatusUpdateView(APIView):
    """
    Update the status of a task (mark as complete or incomplete).
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Update task status",
        description="Updates the status of a task (mark as complete or incomplete).",
        request=TaskStatusUpdateSerializer,
        responses={200: TaskStatusUpdateSerializer},
        operation_id="update_task_status",  # Unique operation ID
    )
    def patch(self, request, pk, status):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
            if status == "complete":
                task.status = "Completed"
                task.completed_at = timezone.now()
            elif status == "incomplete":
                task.status = "Pending"
                task.completed_at = None
            else:
                return Response({"error": "Invalid status"}, status=400)
            task.save()
            return Response(
                TaskSerializer(task).data, status=200
            )  # Return full task details
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)


@extend_schema_view(
    get=extend_schema(
        summary="List all users",
        description="Returns a list of all users (admin only).",
    ),
    post=extend_schema(
        summary="Create a user",
        description="Creates a new user account.",
        request=UserSerializer,
        responses=UserSerializer,
    ),
)
class UserListCreateView(generics.ListCreateAPIView):
    """
    List all users (admin only) or create a new user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve user details",
        description="Retrieve the details of the authenticated user or an admin.",
    ),
    patch=extend_schema(
        summary="Update user details",
        description="Partially updates user details (admin or self).",
    ),
    delete=extend_schema(
        summary="Delete a user",
        description="Deletes a user (admin only).",
    ),
)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete user details.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Allow admins to access any profile. Non-admin users can access only their own profile.
        """
        obj = super().get_object()
        if self.request.user.is_staff or obj.id == self.request.user.id:
            return obj
        raise PermissionDenied(
            "You do not have permission to access this user's profile."
        )

    def update(self, request, *args, **kwargs):
        """
        Partial updates for user details.
        """
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
