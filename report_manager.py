# report_manager.py

from datetime import datetime

class ReportManager:

    def __init__(self):
        self.steps = []

    def log(self, action, status, details="", screenshot=""):
        self.steps.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "action": action,
            "status": status,
            "details": details,
            "screenshot": screenshot
        })

report = ReportManager()