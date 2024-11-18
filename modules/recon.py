# modules/recon.py
import os
from datetime import datetime
from utils.report_generator import HTMLReportGenerator


class Recon:
    def __init__(self, ai_handler, command_executor, use_russian=False):
        """Initialize Recon module"""
        self.ai_handler = ai_handler
        self.command_executor = command_executor
        self.report_generator = HTMLReportGenerator(use_russian)
        self.use_russian = use_russian

    def perform_recon(self, domain):
        """Perform reconnaissance on target domain"""
        # Create timestamp for this scan session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create directory structure for reports
        base_dir = os.path.join("reports", f"{domain}_{timestamp}")
        recon_dir = os.path.join(base_dir, "reconnaissance")
        nmap_dir = os.path.join(recon_dir, "nmap")

        # Create directories
        os.makedirs(nmap_dir, exist_ok=True)

        # Perform nmap scan and analysis
        scan_data = self._run_nmap_scan(domain)

        # Save raw nmap output
        raw_output_path = os.path.join(nmap_dir, "nmap_output.txt")
        with open(raw_output_path, "w", encoding="utf-8") as f:
            f.write(scan_data["raw_output"])

        # Generate AI analysis report
        scan_data["report_dir"] = nmap_dir
        self.report_generator.generate(
            scan_data, os.path.join(nmap_dir, "nmap_ai.html")
        )

        return scan_data

    def _run_nmap_scan(self, domain):
        """Execute nmap scan and analyze results"""
        command_prompt = f"""Generate efficient nmap command for scanning {domain}.
Requirements:
- Fast but thorough scan
- Version detection (-sV)
- Common scripts (-sC)
- Fast timing (use -T4)
Return ONLY the command itself."""

        try:
            recon_command = self.ai_handler.get_command(command_prompt).strip()
            scan_output = self.command_executor.execute(recon_command)

            if self.use_russian:
                analysis_prompt = f"""### Инструкция ###
Вы - эксперт по безопасности. Проанализируйте ПОЛНЫЙ вывод сканирования nmap.
Используйте ТОЛЬКО русский язык.
Обработайте ВСЕ найденные сервисы и уязвимости.

Строго следуйте этой структуре:

КРАТКИЕ ВЫВОДЫ
[Краткое описание всех ключевых находок]

ОБНАРУЖЕННЫЕ СЕРВИСЫ
[Полный анализ КАЖДОГО найденного сервиса и порта]

ОЦЕНКА БЕЗОПАСНОСТИ
[Общий анализ уровня безопасности]

РЕКОМЕНДАЦИИ
[Конкретные рекомендации по защите]

### Данные сканирования ###
{scan_output}"""
            else:
                analysis_prompt = f"""### Instruction ###
You are a security expert. Analyze the COMPLETE nmap scan output.
Process ALL discovered services and vulnerabilities.

Strictly follow this structure:

EXECUTIVE SUMMARY
[Brief overview of key findings]

DETECTED SERVICES
[Full analysis of EACH found service and port]

SECURITY ASSESSMENT
[Overall security analysis]

RECOMMENDATIONS
[Specific security recommendations]

### Scan Data ###
{scan_output}"""

            analysis = self.ai_handler.analyze_output(analysis_prompt)
            analysis = self._clean_analysis_text(analysis)

            return {
                "target": domain,
                "command": recon_command,
                "raw_output": scan_output,
                "analysis": analysis,
                "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "scan_type": "nmap",
                "language": "ru" if self.use_russian else "en",
            }

        except Exception as e:
            error_msg = (
                "Ошибка сканирования Nmap" if self.use_russian else "Nmap scan failed"
            )
            raise Exception(f"{error_msg}: {str(e)}")

    def _clean_analysis_text(self, text):
        """Remove any markup or special formatting from text"""
        try:
            text = text.replace("```", "").replace("`", "")
            text = text.replace("**", "").replace("__", "")
            text = text.replace("*", "").replace("_", "")
            text = text.replace("#", "")
            text = text.replace("<", "&lt;").replace(">", "&gt;")
            text = "\n".join(line.strip() for line in text.split("\n"))
            text = text.replace("\\n", "\n").replace("\\t", "  ")
            return text.strip()
        except Exception as e:
            return text
