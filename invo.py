# invo.py
#!/usr/bin/env python3

import argparse
import sys
import os
from modules.recon import Recon
from modules.ai_handler import AIHandler
from modules.command_executor import CommandExecutor
from config.config_loader import ConfigLoader
from utils.logger import setup_logger


class InvoPentest:
    """Main class for AI-powered penetration testing tool"""

    def __init__(self, use_russian=False):
        """Initialize the penetration testing tool"""
        try:
            self.config = ConfigLoader().config
            self.logger = setup_logger()
            self.ai_handler = AIHandler(self.config)
            self.command_executor = CommandExecutor()
            self.use_russian = use_russian
        except Exception as e:
            error_msg = (
                "Ошибка инициализации" if use_russian else "Initialization error"
            )
            print(f"{error_msg}: {str(e)}")
            sys.exit(1)

    def validate_domain(self, domain):
        """Validate domain format"""
        if not domain or "." not in domain:
            msg = (
                "Неверный формат домена"
                if self.use_russian
                else "Invalid domain format"
            )
            raise ValueError(msg)
        return domain

    def run_reconnaissance(self, domain, verbose=False):
        """Run reconnaissance mode"""
        recon = Recon(self.ai_handler, self.command_executor, self.use_russian)
        return recon.perform_recon(domain)

    def run(self, domain, mode, verbose=False):
        """Main execution method"""
        try:
            # Validate domain
            domain = self.validate_domain(domain)
            start_msg = f"{'Начало сканирования' if self.use_russian else 'Starting scan'}: {domain}"
            self.logger.info(start_msg)

            # Execute selected mode
            if mode == "reconnaissance":
                results = self.run_reconnaissance(domain, verbose)
            else:
                error_msg = (
                    "Неподдерживаемый режим" if self.use_russian else "Unsupported mode"
                )
                raise ValueError(f"{error_msg}: {mode}")

            # Log completion
            complete_msg = (
                "Сканирование завершено успешно"
                if self.use_russian
                else "Scan completed successfully"
            )
            self.logger.info(complete_msg)

        except Exception as e:
            error_msg = "Ошибка выполнения" if self.use_russian else "Execution error"
            self.logger.error(f"{error_msg}: {str(e)}")
            raise


def main():
    """Main entry point"""
    # Prepare help messages
    description = {
        "tool": {
            "en": """AI-Powered Penetration Testing Tool

Available modes:
  -r, --recon    Reconnaissance mode - gather information about target
                 Currently supports: nmap scanning
                 
Example usage:
  Basic reconnaissance:    ./run.sh example.com -r
  Russian language:       ./run.sh example.com -r -Ru
  Verbose output:        ./run.sh example.com -r -v""",
            "ru": """Инструмент тестирования на проникновение с ИИ

Доступные режимы:
  -r, --recon    Режим разведки - сбор информации о цели
                 Поддерживает: сканирование nmap
                 
Примеры использования:
  Базовая разведка:      ./run.sh example.com -r
  На русском языке:      ./run.sh example.com -r -Ru
  Подробный вывод:       ./run.sh example.com -r -v""",
        }
    }

    # Initialize argument parser
    is_russian = "-Ru" in sys.argv or "--russian" in sys.argv
    parser = argparse.ArgumentParser(
        description=description["tool"]["ru" if is_russian else "en"],
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Add arguments
    parser.add_argument(
        "domain", help="Целевой домен" if is_russian else "Target domain"
    )

    parser.add_argument(
        "-r",
        "--recon",
        action="store_true",
        help="Режим разведки" if is_russian else "Reconnaissance mode",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Подробный вывод" if is_russian else "Verbose output",
    )

    parser.add_argument(
        "-Ru",
        "--russian",
        action="store_true",
        help="Использовать русский язык" if is_russian else "Use Russian language",
    )

    # Parse arguments
    args = parser.parse_args()

    # Validate mode selection
    if not args.recon:
        parser.error(
            "Необходимо выбрать режим (-r для разведки)"
            if is_russian
            else "Mode must be selected (-r for reconnaissance)"
        )

    try:
        # Initialize and run
        app = InvoPentest(use_russian=args.russian)
        mode = "reconnaissance" if args.recon else None
        app.run(args.domain, mode, args.verbose)

    except KeyboardInterrupt:
        print(
            "\n"
            + (
                "Сканирование прервано пользователем"
                if args.russian
                else "Scan interrupted by user"
            )
        )
        sys.exit(0)
    except Exception as e:
        print(f"{'Критическая ошибка' if args.russian else 'Critical error'}: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
