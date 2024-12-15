from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()  # Make a copy of the request data
        data["user"] = request.user.id  # Automatically assign the logged-in user

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Save the task with the user
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
