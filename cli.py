#!/usr/bin/env python3
"""
Скрипт командной строки для генерации индивидуальных задач по теории вероятностей.
Позволяет быстро получить задачи без запуска веб-интерфейса.
"""

import argparse
import json
import os
import sys
from task_selector import TaskSelector, TOPICS

def parse_args():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description="Генерация индивидуальных задач по теории вероятностей"
    )
    
    parser.add_argument(
        "--topic", "-t",
        required=True,
        choices=TOPICS,
        help="Текущая тема обучения"
    )
    
    parser.add_argument(
        "--marks", "-m",
        required=True,
        help="Путь к JSON-файлу с оценками ученика"
    )
    
    parser.add_argument(
        "--num-tasks", "-n",
        type=int,
        default=5,
        help="Количество задач (по умолчанию: 5)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Путь для сохранения результатов в JSON (по умолчанию: вывод в консоль)"
    )
    
    return parser.parse_args()

def load_marks(marks_file):
    """Загрузка оценок из JSON-файла"""
    try:
        with open(marks_file, "r", encoding="utf-8") as f:
            marks = json.load(f)
        
        # Проверка формата оценок
        for topic in TOPICS:
            if topic not in marks:
                print(f"Предупреждение: тема '{topic}' отсутствует в файле оценок")
                marks[topic] = "ещё не изучал"
        
        return marks
    except Exception as e:
        print(f"Ошибка при загрузке оценок: {e}")
        sys.exit(1)

def main():
    """Основная функция"""
    args = parse_args()
    
    # Загрузка оценок
    marks = load_marks(args.marks)
    
    # Создание селектора задач
    selector = TaskSelector()
    
    # Создание данных ученика
    student_data = selector.create_student_data(args.topic, marks)
    
    # Получение задач
    tasks = selector.get_tasks_for_student(student_data, num_tasks=args.num_tasks)
    
    # Вывод результатов
    if args.output:
        # Сохранение в файл
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        print(f"Результаты сохранены в файл: {args.output}")
    else:
        # Вывод в консоль
        for i, task in enumerate(tasks, 1):
            print(f"\n--- Задача {i} ---")
            print(f"Условие: {task['условие']}")
            print(f"Тема: {task['тема']}")
            print(f"Сложность: {task['сложность']}")
            print(f"Тип: {task['тип']}")
            print(f"Ответ: {task['ответ']}")

if __name__ == "__main__":
    main()