# utils/console_logger.py
class ConsoleLogger:
    def __init__(self, use_russian=False, verbose=False):
        self.use_russian = use_russian
        self.verbose = verbose
        self.tool_names = {
            "nmap": {"ru": "Сетевой сканер (Nmap)", "en": "Network Mapper (Nmap)"},
            "sudomy": {
                "ru": "Инструмент перечисления поддоменов (Sudomy)",
                "en": "Subdomain Enumeration Tool (Sudomy)",
            },
        }

        self.messages = {
            "start_scan": {
                "en": "🚀 Starting {} scan for: {}",
                "ru": "🚀 Запуск сканирования {} для: {}",
            },
            "generating_command": {
                "en": "⚙️  Generating {} command...",
                "ru": "⚙️  Генерация команды {}...",
            },
            "command_generated": {
                "en": "✓ {} command generated: {}",
                "ru": "✓ Команда {} сгенерирована: {}",
            },
            "starting_tool": {
                "en": "▶️  Starting {} scan...",
                "ru": "▶️  Запуск сканирования {}...",
            },
            "scan_complete": {
                "en": "✓ {} scan completed successfully",
                "ru": "✓ Сканирование {} успешно завершено",
            },
            "analyzing_results": {
                "en": "🔍 Analyzing {} results...",
                "ru": "🔍 Анализ результатов {}...",
            },
            "analysis_complete": {
                "en": "✓ {} analysis completed",
                "ru": "✓ Анализ {} завершен",
            },
            "generating_report": {
                "en": "📝 Generating {} report...",
                "ru": "📝 Генерация отчета {}...",
            },
            "report_complete": {
                "en": "✓ {} report generated successfully at: {}",
                "ru": "✓ Отчет {} успешно сгенерирован: {}",
            },
            "creating_directory": {
                "en": "📁 Creating directory structure...",
                "ru": "📁 Создание структуры директорий...",
            },
            "tool_output": {"en": "\nOutput from {}:\n{}\n", "ru": "\nВывод {}:\n{}\n"},
            "error": {"en": "❌ Error in {}: {}", "ru": "❌ Ошибка в {}: {}"},
        }

    def log(self, message_key, tool="", **kwargs):
        """Log message with optional tool name and parameters"""
        try:
            lang = "ru" if self.use_russian else "en"
            tool_name = (
                self.tool_names.get(tool, {}).get(lang, tool.upper()) if tool else ""
            )

            message = self.messages[message_key][lang]
            if tool:
                formatted_message = message.format(tool_name, *kwargs.values())
            else:
                formatted_message = message.format(*kwargs.values())

            print(formatted_message)

        except Exception as e:
            print(f"Logging error: {str(e)}")

    def log_tool_output(self, tool, output):
        """Log tool output only in verbose mode"""
        if self.verbose and output:
            lang = "ru" if self.use_russian else "en"
            tool_name = self.tool_names.get(tool, {}).get(lang, tool.upper())
            separator = "═" * 80
            print(f"\n{separator}")
            print(self.messages["tool_output"][lang].format(tool_name, output))
            print(f"{separator}\n")

    def log_error(self, tool, error):
        """Log error message"""
        lang = "ru" if self.use_russian else "en"
        tool_name = self.tool_names.get(tool, {}).get(lang, tool.upper())
        print(f"\n{self.messages['error'][lang].format(tool_name, error)}\n")
