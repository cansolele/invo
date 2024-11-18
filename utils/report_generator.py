# utils/report_generator.py
import os
from datetime import datetime


class HTMLReportGenerator:
    def __init__(self, use_russian=False):
        self.use_russian = use_russian
        self.translations = {
            "en": {
                "title": "Security Assessment Report",
                "target": "Target",
                "scan_time": "Scan Time",
                "scan_command": "Scan Command",
                "security_analysis": "Security Analysis",
                "headers": {
                    "EXECUTIVE SUMMARY": "Executive Summary",
                    "DETECTED SERVICES": "Detected Services",
                    "SECURITY ASSESSMENT": "Security Assessment",
                    "RECOMMENDATIONS": "Recommendations",
                },
            },
            "ru": {
                "title": "Отчет по безопасности",
                "target": "Цель",
                "scan_time": "Время сканирования",
                "scan_command": "Команда сканирования",
                "security_analysis": "Анализ безопасности",
                "headers": {
                    "КРАТКИЕ ВЫВОДЫ": "Краткие выводы",
                    "ОБНАРУЖЕННЫЕ СЕРВИСЫ": "Обнаруженные сервисы",
                    "ОЦЕНКА БЕЗОПАСНОСТИ": "Оценка безопасности",
                    "РЕКОМЕНДАЦИИ": "Рекомендации",
                },
            },
        }
        self.template = """<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8 max-w-5xl">
        <!-- Header -->
        <div class="bg-gradient-to-r from-blue-600 to-blue-800 rounded-lg p-6 mb-6">
            <h1 class="text-3xl font-bold text-white mb-2">{title}</h1>
            <p class="text-lg text-white">{target_label}: {target}</p>
            <p class="text-sm text-white opacity-80">{scan_time_label}: {scan_time}</p>
        </div>

        <!-- Command Section -->
        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h2 class="text-xl font-bold mb-3 text-blue-800">{scan_command}</h2>
            <div class="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm overflow-x-auto">
                {command}
            </div>
        </div>

        <!-- Analysis Section -->
        <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-bold mb-3 text-blue-800">{security_analysis}</h2>
            <div class="whitespace-pre-line text-gray-700">
                {analysis}
            </div>
        </div>
    </div>
</body>
</html>"""

    def generate(self, data):
        """Generate HTML report from scan data"""
        try:
            lang = "ru" if self.use_russian else "en"
            trans = self.translations[lang]

            # Format analysis text with section headers
            analysis = self._format_analysis_sections(data["analysis"], lang)

            # Create the report
            report_content = self.template.format(
                lang=lang,
                title=trans["title"],
                target_label=trans["target"],
                target=data["target"],
                scan_time_label=trans["scan_time"],
                scan_time=data["scan_time"],
                scan_command=trans["scan_command"],
                security_analysis=trans["security_analysis"],
                command=data["command"],
                analysis=analysis,
            )

            # Save the report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_dir = "reports"
            os.makedirs(report_dir, exist_ok=True)
            report_path = os.path.join(
                report_dir, f"recon_{data['target']}_{timestamp}.html"
            )

            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report_content)

            return report_path

        except Exception as e:
            print(f"Error generating report: {str(e)}")
            error_msg = (
                "Ошибка создания отчета"
                if self.use_russian
                else "Failed to generate report"
            )
            raise Exception(f"{error_msg}: {str(e)}")

    def _format_analysis_sections(self, text, lang):
        """Format the analysis text with styled section headers"""
        headers = self.translations[lang]["headers"]

        formatted_text = text
        for old_header, new_header in headers.items():
            # Add section div and styled header
            formatted_text = formatted_text.replace(
                old_header + "\n",
                f'<div class="mt-4"><h3 class="text-lg font-bold text-blue-800 mb-2">{new_header}</h3>\n',
            )

            # Find and close section div before next header
            next_header = next(
                (
                    h
                    for h in headers
                    if h in formatted_text[formatted_text.find(new_header) :]
                ),
                None,
            )
            if next_header:
                formatted_text = formatted_text.replace(
                    next_header, "</div>" + next_header
                )

        # Close the last section
        formatted_text += "</div>"
        return formatted_text
