from rest_framework import serializers
from .models import Project, QueryAnalysis

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'schema_ddl', 'created_at']

class QueryAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryAnalysis
        fields = ['id', 'project', 'raw_sql', 'status', 'actual_cost', 'ai_suggestion', 'created_at']
        read_only_fields = ['status', 'actual_cost', 'ai_suggestion'] 
        # User only sends 'project' ID and 'raw_sql'. The rest is calculated by our system.