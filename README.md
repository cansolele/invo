# INVO - AI-Powered Penetration Testing Tool

INVO - это инструмент для автоматизированного тестирования на проникновение, использующий искусственный интеллект для анализа результатов сканирования и выработки рекомендаций по безопасности.

## Быстрый старт

```bash
# Установка
git clone https://github.com/cansolele/invo.git
cd invo
chmod +x setup.sh
./setup.sh

# Использование
./invo example.com -r        # Базовая разведка
./invo example.com -r -Ru    # Разведка с отчетом на русском
./invo --help               # Справка
```

## Режимы и инструменты

### Разведка (Reconnaissance) [-r]

- **nmap** - сетевое сканирование и обнаружение сервисов
- **sudomy** - автоматизированная разведка поддоменов (в разработке)
- _Список будет дополняться_

## Требования

### Системные требования

- Kali Linux (Или другой дистрибутив с установленными необходимыми утилитами)
- Python 3.10+
- Git

### AI компоненты

```bash
# Установка Ollama
curl -fsSL https://ollama.com/install.sh | sh
systemctl start ollama

# Загрузка модели (qwen 2.5 - как пример, можете выбрать свою модель)
ollama pull qwen2.5:32b
```

## Использование

### Основные опции

```bash
./invo <домен> [опции]

Опции:
  -r        Режим разведки
  -Ru       Использовать русский язык
  -v        Подробный вывод
```

### Примеры использования

```bash
# Базовая разведка домена
./invo example.com -r

# Разведка с отчетом на русском языке
./invo example.com -r -Ru

# Разведка с подробным выводом
./invo example.com -r -v
```

### Структура отчетов

```
reports/
└── example.com_20241118_152847/    # Домен и временная метка
    └── reconnaissance/             # Режим сканирования
        └── nmap/                  # Используемый инструмент
            ├── nmap_output.txt    # Сырой вывод
            └── nmap_ai.html       # AI анализ
```

## Конфигурация

Настройки в `config/config.yml`:

```yaml
ai:
  model: "qwen2.5:32b"
  host: "http://localhost:11434"
  temperature: 0.1
  timeout: 300
  num_ctx: 8192 # Контекст для больших выводов

logging:
  level: INFO
  file: logs/invo.log

nmap:
  timeout: 300
  max_retries: 2
```

## Структура проекта

```
invo/
├── config/             # Конфигурация
├── modules/           # Модули режимов
├── utils/            # Вспомогательные функции
├── reports/          # Отчеты
├── logs/            # Логи
├── invo.py         # Основной код
├── invo            # Скрипт запуска
└── setup.sh        # Установщик
```
