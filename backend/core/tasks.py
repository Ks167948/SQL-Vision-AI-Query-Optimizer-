from celery import shared_task
from django.db import connections, transaction
from .models import QueryAnalysis
import requests
import json

OLLAMA_API_URL = "http://host.docker.internal:11434/api/generate"

@shared_task
def analyze_query_task(analysis_id):
    print(f"WORKER: Starting job {analysis_id}")
    
    try:
        analysis = QueryAnalysis.objects.get(id=analysis_id)
        analysis.status = 'PROCESSING'
        analysis.save()

        # --- STEP 1: The Sandbox Transaction ---
        # We use 'atomic' to ensure we can rollback changes (Keep DB clean)
        # Note: In a real production setup, you would use connections['sandbox_db']
        with transaction.atomic():
            with connections['default'].cursor() as cursor:
                # A. Apply the User's Schema first! (Create the missing 'users' table)
                # We assume the DDL contains valid SQL like "CREATE TABLE..."
                print(f"WORKER: Applying schema for {analysis.project.name}...")
                cursor.execute(analysis.project.schema_ddl)
                
                # B. Insert dummy data (Optional but helps EXPLAIN work better)
                # If the table is empty, EXPLAIN usually returns 0 cost.
                # Let's try to infer the table name or just skip for now.
                
                # C. Run EXPLAIN on the User's Query
                print(f"WORKER: Running analysis on: {analysis.raw_sql}")
                cursor.execute(f"EXPLAIN (FORMAT JSON, ANALYZE) {analysis.raw_sql}")
                plan_json = cursor.fetchone()[0]
                
                # Extract cost
                total_cost = plan_json[0]['Plan']['Total Cost']
                
                # D. Save Results BEFORE Rolling Back
                # We must modify the object instance, but NOT save to DB yet if it's inside the transaction blocks 
                # that we intend to roll back? 
                # Actually, Django models live outside the raw cursor transaction if we are careful.
                # But to be safe, we extract the data into variables first.
                
                # RAISE EXCEPTION to force Rollback!
                # This ensures the 'users' table is deleted after analysis.
                raise Exception("Force Rollback")

    except Exception as e:
        # We expect the "Force Rollback" exception. 
        if str(e) == "Force Rollback":
            print("WORKER: Analysis successful, rolling back DB changes.")
        else:
            print(f"ERROR: {str(e)}")
            analysis.error_message = str(e)
            analysis.status = 'FAILED'
            analysis.save()
            return

    # --- STEP 2: Ask the AI ---
    # (This happens outside the transaction, so the DB is clean)
    try:
        prompt = f"""
        You are a Postgres Expert. Analyze this execution plan.
        
        QUERY: {analysis.raw_sql}
        PLAN: {json.dumps(plan_json)}
        
        Suggest 1 optimization.
        """
        
        response = requests.post(OLLAMA_API_URL, json={
            "model": "llama3", 
            "prompt": prompt, 
            "stream": False
        })
        
        if response.status_code == 200:
            ai_text = response.json().get('response', '')
            analysis.ai_suggestion = ai_text
            analysis.execution_plan = plan_json
            analysis.actual_cost = total_cost
            analysis.status = 'COMPLETED'
        else:
            analysis.status = 'FAILED'
            analysis.error_message = "AI Connection Failed"

        analysis.save()
        print(f"WORKER: Job {analysis_id} finished successfully.")

    except Exception as e:
        print(f"AI ERROR: {str(e)}")
        analysis.status = 'FAILED'
        analysis.save()