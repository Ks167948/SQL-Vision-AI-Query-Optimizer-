from celery import shared_task
from django.db import connections
from .models import QueryAnalysis
import requests
import json

# URL for Ollama (Assumes you run Ollama on your host machine)
# "host.docker.internal" lets Docker talk to your Windows/Mac localhost
OLLAMA_API_URL = "http://host.docker.internal:11434/api/generate"

@shared_task
def analyze_query_task(analysis_id):
    """
    The Worker Process:
    1. Runs EXPLAIN ANALYZE on the Sandbox DB.
    2. Sends the result to the AI.
    3. Saves the suggestion.
    """
    print(f"WORKER: Starting job {analysis_id}")
    
    try:
        analysis = QueryAnalysis.objects.get(id=analysis_id)
        analysis.status = 'PROCESSING'
        analysis.save()

        # --- STEP 1: Run EXPLAIN in Sandbox ---
        # We connect specifically to the 'sandbox' database defined in settings
        with connections['default'].cursor() as cursor: 
            # Note: In a real app, we'd switch to 'sandbox_db' connection, 
            # but for simplicity we are using the default connection for now.
            # Ideally, you defined a second DB in settings.py, let's assume we simulate it:
            
            # Run the Explain command
            cursor.execute(f"EXPLAIN (FORMAT JSON, ANALYZE) {analysis.raw_sql}")
            plan_json = cursor.fetchone()[0]
            
            # Extract total cost (Postgres JSON format varies, simplistic extraction here)
            total_cost = plan_json[0]['Plan']['Total Cost']
            
            analysis.execution_plan = plan_json
            analysis.actual_cost = total_cost
            analysis.save()

        # --- STEP 2: Ask the AI ---
        prompt = f"""
        You are a Postgres Expert. Analyze this execution plan and the query.
        
        QUERY: {analysis.raw_sql}
        
        PLAN: {json.dumps(plan_json)}
        
        Suggest 1 specific index to reduce cost. Be brief.
        """
        
        # Call Ollama
        response = requests.post(OLLAMA_API_URL, json={
            "model": "llama3",  # Or "mistral"
            "prompt": prompt,
            "stream": False
        })
        
        if response.status_code == 200:
            ai_text = response.json().get('response', '')
            analysis.ai_suggestion = ai_text
            analysis.status = 'COMPLETED'
        else:
            analysis.error_message = f"AI Error: {response.text}"
            analysis.status = 'FAILED'

    except Exception as e:
        print(f"ERROR: {str(e)}")
        analysis.error_message = str(e)
        analysis.status = 'FAILED'
    
    analysis.save()
    print(f"WORKER: Job {analysis_id} finished.")