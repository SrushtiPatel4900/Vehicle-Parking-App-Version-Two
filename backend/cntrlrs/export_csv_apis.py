from flask_restful import Resource
from flask import request, send_file

from celery.result import AsyncResult
import os

class ExportCSVAPI(Resource):
    # Trigger CSV export
    def get(self):
        from tasks.export_csv_task import export_user_csv
        user_id = request.args.get("user_id")
        if not user_id:
            return {"status": "error", "message": "user_id required"}, 400

        task = export_user_csv.delay(int(user_id))
        return {"status": "started", "task_id": task.id}

# Check task status and download CSV
class DownloadCSVAPI(Resource):
    def get(self):
        task_id = request.args.get("task_id")
        if not task_id:
            return {"status": "error", "message": "task_id required"}, 400

        task = AsyncResult(task_id)
        if task.state == "PENDING":
            return {"status": "pending"}
        elif task.state == "FAILURE":
            return {"status": "failed", "message": str(task.result)}
        elif task.state == "SUCCESS":
            data = task.result
            file_path = data["file_path"]
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)
            else:
                return {"status": "error", "message": "File not found"}
