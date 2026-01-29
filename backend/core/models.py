from django.db import models
import uuid

class Project(models.Model):
    """
    Represents a user's database they want to optimize.
    Stores the DDL (CREATE TABLE statements) so the AI understands context.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    # The Schema DDL is critical for the LLM to know what indexes exist
    schema_ddl = models.TextField(help_text="Paste your schema creation SQL here")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class QueryAnalysis(models.Model):
    """
    Represents a single 'Run' of the optimization engine.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),      # In Redis Queue
        ('PROCESSING', 'Processing'), # Worker is running EXPLAIN
        ('COMPLETED', 'Completed'),   # AI has finished
        ('FAILED', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='analyses')

    # The "Bad" Query
    raw_sql = models.TextField()

    # We store the Full JSON plan to enable "Replay" capabilities later
    execution_plan = models.JSONField(null=True, blank=True)

    # Extracted metrics for the dashboard
    actual_cost = models.FloatField(null=True, blank=True)

    # The AI's output
    ai_suggestion = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - {self.status}"