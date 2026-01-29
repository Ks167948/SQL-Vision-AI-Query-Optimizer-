from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Project, QueryAnalysis
from .serializers import ProjectSerializer, QueryAnalysisSerializer

# --- THIS WAS LIKELY MISSING ---
from .tasks import analyze_query_task
# -------------------------------

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Projects (schemas) to be viewed or created.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class QueryAnalysisViewSet(viewsets.ModelViewSet):
    """
    API endpoint to submit SQL queries for analysis.
    """
    queryset = QueryAnalysis.objects.all()
    serializer_class = QueryAnalysisSerializer

    def create(self, request, *args, **kwargs):
        # 1. Save the request to the main database
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        analysis_job = serializer.save()

        # 2. Trigger the Worker
        # Now this will work because we imported it above!
        analyze_query_task.delay(analysis_job.id)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)