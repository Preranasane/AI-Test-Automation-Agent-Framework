from report_manager import report

def generate_html_report():

    html = """
    <html>
    <head>
        <title>AI Agent Report</title>
    </head>
    <body>

    <h2>Execution Report</h2>

    <table border="1">
        <tr>
            <th>Time</th>
            <th>Action</th>
            <th>Status</th>
            <th>Details</th>
            <th>Screenshot</th>
        </tr>
    """

    for step in report.steps:
        html += f"""
        <tr>
            <td>{step['time']}</td>
            <td>{step['action']}</td>
            <td>{step['status']}</td>
            <td>{step['details']}</td>
            <td><a href="{step['screenshot']}">View</a></td>
        </tr>
        """

    html += """
    </table>
    </body>
    </html>
    """

    with open("reports/report.html", "w", encoding="utf-8") as f:
        f.write(html)