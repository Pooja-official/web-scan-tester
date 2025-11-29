import datetime

def generate_report(vuln_results, filename="security_report.html"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    html_content = f"""
    <html>
    <head>
        <title>WebScanPro Security Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f4f4f4; color: #222; }}
            table {{ border-collapse: collapse; margin-top:20px; }}
            th, td {{ border: 1px solid #aaa; padding: 8px 12px; }}
            th {{ background: #ddd; }}
            tr:nth-child(even) {{ background: #eee; }}
        </style>
    </head>
    <body>
        <h1>WebScanPro Security Report</h1>
        <p><b>Report generated:</b> {now}</p>
        <table>
            <tr>
                <th>#</th>
                <th>Vulnerability Type</th>
                <th>Endpoint</th>
                <th>Severity</th>
                <th>Description</th>
                <th>Suggested Mitigation</th>
            </tr>
    """
    for idx, res in enumerate(vuln_results, start=1):
        html_content += f"""
            <tr>
                <td>{idx}</td>
                <td>{res['type']}</td>
                <td>{res['endpoint']}</td>
                <td>{res['severity']}</td>
                <td>{res['description']}</td>
                <td>{res['mitigation']}</td>
            </tr>
        """
    html_content += "</table></body></html>"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Report saved as {filename}")

if __name__ == "__main__":
    # Example — replace with your real scan results
    vuln_results = [
        {
            'type': 'SQL Injection',
            'endpoint': 'http://localhost/webscanpro/search.php',
            'severity': 'High',
            'description': 'SQL error message when submitting crafted input',
            'mitigation': 'Use parameterized queries/prepared statements.'
        },
        {
            'type': 'XSS',
            'endpoint': 'http://localhost/webscanpro/comments.php',
            'severity': 'Medium',
            'description': 'Reflected XSS payload in comment field',
            'mitigation': 'Properly escape user input/output.'
        }
    ]
    generate_report(vuln_results)
