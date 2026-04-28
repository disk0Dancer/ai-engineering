# Intro AI Agents — Customer Support Agent

Курс-практикум по базовым паттернам AI agents на примере customer support assistant для игровой платёжной платформы GamePay. Репозиторий ведёт студента от первого запуска до понимания, как связаны LLM, tools, memory, routing, context engineering и agent loop.

## Что вы соберёте

После онбординга у вас будет рабочий support agent, который умеет:

- принимать сообщение пользователя;
- выбирать specialist-а через multi-agent router;
- вызывать tools для invoice lookup, customer lookup, subscription lookup, FAQ search и refund request;
- сохранять user-scoped memory;
- собирать контекст из system prompt, memory и tool observations;
- возвращать проверяемый ответ с фактами из tools.

Проект запускается без API-ключей: по умолчанию используется deterministic `EchoLLM`. Это позволяет сначала разобрать архитектуру агента, а затем заменить LLM adapter на OpenAI, Anthropic, Ollama или другой провайдер.

## Темы курса

| Тема | Где смотреть |
| --- | --- |
| LLM boundaries | `support_agent/interfaces.py`, `support_agent/llm.py` |
| Tools and MCP contract | `support_agent/tools.py`, `support_agent/data/*.json` |
| Memory | `support_agent/memory.py` |
| Multi-agent patterns | `support_agent/multi_agent.py` |
| Context engineering | `support_agent/context.py` |
| Customer support agent loop | `support_agent/agent.py` |

## Быстрый старт: локально

```bash
git clone git@github.com:disk0Dancer/ai-engineering.git
cd ai-engineering
make install
make demo
make test
```

`make install` создаёт `.venv`, ставит пакет в editable-режиме и выполняет smoke-check агента.

Если SSH clone недоступен, используйте HTTPS:

```bash
git clone https://github.com/disk0Dancer/ai-engineering.git
cd ai-engineering
make install
```

## Быстрый старт: Google Colab

В новой Colab notebook выполните одну ячейку:

```python
!git clone https://github.com/disk0Dancer/ai-engineering.git
%cd ai-engineering
!make install
!make demo
!make test
```

После этого можно менять код прямо в Colab и повторно запускать:

```python
!make demo
!make test
```

## Проверка установки

Команда:

```bash
make demo
```

ожидаемо печатает примерно такой сценарий:

```text
> How do refunds work?
[refund-agent] I checked the available support data and summarized the safe next step below.
Refunds are usually available within 14 days if the purchase was not consumed.

> Please refund INV-1001 for alex@example.com
[refund-agent] I checked the available support data and summarized the safe next step below.
Customer Alex Chen (alex@example.com): tier=gold, risk=low.
Invoice INV-1001: paid, 9.99 USD for Dragon Quest Online; delivery=delivered.
Refund review ticket created: RF-INV-1001.
```

## Структура проекта

```text
support_agent/
  interfaces.py     # Protocol boundaries: LLM, Tool, Memory
  llm.py            # EchoLLM adapter for deterministic runs
  tools.py          # support tools with MCP-shaped inputs/outputs
  data/*.json       # invoices, customers, subscriptions and FAQ demo data
  memory.py         # user-scoped memory
  context.py        # prompt and context assembly
  agent.py          # customer support agent loop
  multi_agent.py    # router and specialist handoff pattern
  cli.py            # command-line entry point

scripts/
  demo.py           # runs several realistic support messages

docs/
  ARCHITECTURE.md   # component map and execution flow
  EXERCISES.md      # extension tasks for students

tests/
  test_agent.py     # behaviour checks for tools, memory, router and agent
```

## Demo data

Для показа агента добавлены небольшие JSON-таблицы:

- `support_agent/data/invoices.json` — платежи и delivery status;
- `support_agent/data/customers.json` — профиль клиента, tier и risk level;
- `support_agent/data/subscriptions.json` — подписки и renewal dates;
- `support_agent/data/faq.json` — короткая support knowledge base.

Попробуйте менять эти файлы и снова запускать `make demo`: tools читают данные из JSON, а агент строит ответ на основе tool observations.

## Как читать код

Рекомендуемый порядок:

1. `support_agent/schema.py` — какие данные передаются между частями системы.
2. `support_agent/interfaces.py` — какие контракты держат архитектуру заменяемой.
3. `support_agent/tools.py` — как выглядят tool calls и JSON-like observations.
4. `support_agent/memory.py` — где хранится память пользователя.
5. `support_agent/context.py` — что попадает в prompt перед вызовом LLM.
6. `support_agent/agent.py` — основной agent loop.
7. `support_agent/multi_agent.py` — routing и handoff specialist-ам.
8. `tests/test_agent.py` — какие свойства поведения считаются важными.

## Основные команды

```bash
make install   # create .venv, install package + dev tools, run smoke-check
make demo      # run scripted customer support conversation examples
make test      # run pytest
make lint      # run ruff check
make fmt       # run ruff format
make clean     # remove caches and build artifacts
```

## Следующий шаг

После первого запуска переходите к [`docs/EXERCISES.md`](docs/EXERCISES.md): там задания на новый tool, memory summary, нового specialist-а, улучшение context builder и вынос tools в настоящий MCP server.
