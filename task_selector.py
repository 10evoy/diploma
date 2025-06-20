import os
import json
import random
import openai
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

# Список всех тем
TOPICS = [
    "Геометрическая вероятность: выбор точки из фигуры на плоскости и из числового отрезка",
    "Примеры случайных величин",
    "Распределение вероятностей",
    "Биномиальное распределение",
    "Практическая работа: построение биномиального распределения",
    "Математическое ожидание и его свойства",
    "Рассеивание значений, дисперсия, стандартное отклонение",
    "Свойства дисперсии",
    "Математическое ожидание числа успехов в серии испытаний Бернулли",
    "Дисперсия числа успехов",
    "Практическая работа: математическое ожидание, дисперсия и стандартное отклонение",
    "Измерения вероятностей, точность приближения",
    "Практическая работа: проверка близости частоты и вероятности",
    "Социологические обследования",
    "Закон больших чисел",
    "Число сочетаний",
    "Формула бинома Ньютона",
    "Свойства биномиальных коэффициентов",
    "Треугольник Паскаля",
    "Практическая работа: треугольник Паскаля и свойства биномиальных коэффициентов"
]

# Связи между темами
RELATED_TOPICS_DICT = {
    "Геометрическая вероятность: выбор точки из фигуры на плоскости и из числового отрезка": [
        "Распределение вероятностей", "Измерения вероятностей, точность приближения", "Биномиальное распределение"
    ],
    "Примеры случайных величин": [
        "Распределение вероятностей", "Биномиальное распределение", "Математическое ожидание и его свойства"
    ],
    "Распределение вероятностей": [
        "Биномиальное распределение", "Математическое ожидание и его свойства", "Примеры случайных величин"
    ],
    "Биномиальное распределение": [
        "Число сочетаний", "Формула бинома Ньютона", "Математическое ожидание числа успехов в серии испытаний Бернулли"
    ],
    "Практическая работа: построение биномиального распределения": [
        "Биномиальное распределение", "Число сочетаний", "Формула бинома Ньютона"
    ],
    "Математическое ожидание и его свойства": [
        "Рассеивание значений, дисперсия, стандартное отклонение", "Свойства дисперсии", "Математическое ожидание числа успехов в серии испытаний Бернулли"
    ],
    "Рассеивание значений, дисперсия, стандартное отклонение": [
        "Математическое ожидание и его свойства", "Свойства дисперсии", "Дисперсия числа успехов"
    ],
    "Свойства дисперсии": [
        "Рассеивание значений, дисперсия, стандартное отклонение", "Математическое ожидание и его свойства", "Дисперсия числа успехов"
    ],
    "Математическое ожидание числа успехов в серии испытаний Бернулли": [
        "Биномиальное распределение", "Математическое ожидание и его свойства", "Дисперсия числа успехов"
    ],
    "Дисперсия числа успехов": [
        "Математическое ожидание числа успехов в серии испытаний Бернулли", "Свойства дисперсии", "Рассеивание значений, дисперсия, стандартное отклонение"
    ],
    "Практическая работа: математическое ожидание, дисперсия и стандартное отклонение": [
        "Математическое ожидание и его свойства", "Рассеивание значений, дисперсия, стандартное отклонение", "Свойства дисперсии"
    ],
    "Измерения вероятностей, точность приближения": [
        "Закон больших чисел", "Практическая работа: проверка близости частоты и вероятности", "Социологические обследования"
    ],
    "Практическая работа: проверка близости частоты и вероятности": [
        "Измерения вероятностей, точность приближения", "Закон больших чисел", "Социологические обследования"
    ],
    "Социологические обследования": [
        "Измерения вероятностей, точность приближения", "Закон больших чисел", "Практическая работа: проверка близости частоты и вероятности"
    ],
    "Закон больших чисел": [
        "Измерения вероятностей, точность приближения", "Социологические обследования", "Практическая работа: проверка близости частоты и вероятности"
    ],
    "Число сочетаний": [
        "Формула бинома Ньютона", "Свойства биномиальных коэффициентов", "Треугольник Паскаля"
    ],
    "Формула бинома Ньютона": [
        "Число сочетаний", "Свойства биномиальных коэффициентов", "Треугольник Паскаля"
    ],
    "Свойства биномиальных коэффициентов": [
        "Число сочетаний", "Формула бинома Ньютона", "Треугольник Паскаля"
    ],
    "Треугольник Паскаля": [
        "Число сочетаний", "Формула бинома Ньютона", "Свойства биномиальных коэффициентов"
    ],
    "Практическая работа: треугольник Паскаля и свойства биномиальных коэффициентов": [
        "Треугольник Паскаля", "Свойства биномиальных коэффициентов", "Формула бинома Ньютона"
    ]
}

# Промпты для ИИ
SYSTEM_PROMPT = """
Ты — учебный ассистент, составляешь индивидуальные задачи по теории вероятностей.
Входные данные: текущая тема, связанные темы, оценки ученика.
Сгенерируй 3-5 задач в формате JSON:
[{"тема": "...", "сложность": "...", "тип": "..."}]

Правила:
- Обязательно включи задачу по текущей теме
- Сложность: 2-3/неизучено → "базовый", 4 → "средний", 5 → "повышенный"
- Типы: "построение", "вычисление", "доказательство", "прикладная"
"""

USER_PROMPT_TEMPLATE = "Вот данные об ученике:\n{data}"

class TaskSelector:
    def __init__(self, tasks_file="generated_probability_tasks.json"):
        """
        Инициализация селектора задач
        
        Args:
            tasks_file (str): Путь к файлу с задачами
        """
        self.tasks_file = tasks_file
        self.tasks = self._load_tasks()
        
    def _load_tasks(self):
        """Загрузка задач из файла"""
        try:
            with open(self.tasks_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка при загрузке задач: {e}")
            return []
    
    def get_tasks_for_student(self, student_data, num_tasks=5):
        """
        Получение задач для ученика на основе его данных
        
        Args:
            student_data (dict): Данные ученика (текущая тема, связанные темы, оценки)
            num_tasks (int): Количество задач для выбора
            
        Returns:
            list: Список выбранных задач
        """
        # Получение рекомендаций от LLM
        task_recommendations = self._get_llm_recommendations(student_data)
        
        if not task_recommendations:
            # Если не удалось получить рекомендации, используем текущую тему и базовую сложность
            task_recommendations = [
                {"тема": student_data["current_topic"], "сложность": "базовый", "тип": "вычисление"}
            ]
        
        # Выбор задач на основе рекомендаций
        selected_tasks = self._select_tasks_by_recommendations(task_recommendations, num_tasks)
        
        return selected_tasks
    
    def _get_llm_recommendations(self, student_data):
        """
        Получение рекомендаций от LLM
        
        Args:
            student_data (dict): Данные ученика
            
        Returns:
            list: Список рекомендаций в формате [{"тема": "...", "сложность": "...", "тип": "..."}]
        """
        try:
            client = openai.OpenAI(api_key=API_KEY, base_url="https://llm.api.cloud.yandex.net/v1")
            
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT_TEMPLATE.format(data=json.dumps(student_data, ensure_ascii=False))}
            ]
            
            completion = client.chat.completions.create(
                model=f"gpt://{FOLDER_ID}/yandexgpt/latest",
                messages=messages
            )
            
            reply = completion.choices[0].message.content
            
            # Извлечение JSON из ответа
            start = reply.find('[')
            end = reply.rfind(']')
            
            if start != -1 and end != -1:
                reply = reply[start:end+1]
                
            recommendations = json.loads(reply)
            
            # Проверка валидности рекомендаций
            if not self._validate_recommendations(recommendations):
                return None
                
            return recommendations
            
        except Exception as e:
            print(f"Ошибка при получении рекомендаций от LLM: {e}")
            return None
    
    def _validate_recommendations(self, recommendations):
        """
        Проверка валидности рекомендаций
        
        Args:
            recommendations (list): Список рекомендаций
            
        Returns:
            bool: True, если рекомендации валидны, иначе False
        """
        if not isinstance(recommendations, list):
            return False
            
        for rec in recommendations:
            if not all(key in rec for key in ["тема", "сложность", "тип"]):
                return False
                
        return True
    
    def _select_tasks_by_recommendations(self, recommendations, num_tasks):
        """
        Выбор задач на основе рекомендаций
        
        Args:
            recommendations (list): Список рекомендаций
            num_tasks (int): Количество задач для выбора
            
        Returns:
            list: Список выбранных задач
        """
        selected_tasks = []
        
        # Группировка задач по рекомендациям
        for rec in recommendations:
            # Фильтрация задач по теме, сложности и типу
            matching_tasks = [
                task for task in self.tasks 
                if task["тема"] == rec["тема"] and 
                   task["сложность"] == rec["сложность"] and 
                   task["тип"] == rec["тип"]
            ]
            
            # Если нет точных совпадений, ищем по теме и сложности
            if not matching_tasks:
                matching_tasks = [
                    task for task in self.tasks 
                    if task["тема"] == rec["тема"] and 
                       task["сложность"] == rec["сложность"]
                ]
            
            # Если все еще нет совпадений, ищем только по теме
            if not matching_tasks:
                matching_tasks = [
                    task for task in self.tasks 
                    if task["тема"] == rec["тема"]
                ]
            
            # Если есть подходящие задачи, выбираем случайную
            if matching_tasks:
                selected_task = random.choice(matching_tasks)
                
                # Проверяем, что задача еще не выбрана
                if selected_task not in selected_tasks:
                    selected_tasks.append(selected_task)
                
                # Если достигли нужного количества задач, завершаем
                if len(selected_tasks) >= num_tasks:
                    break
        
        # Если выбрано меньше задач, чем требуется, добавляем случайные задачи
        if len(selected_tasks) < num_tasks:
            remaining_tasks = [task for task in self.tasks if task not in selected_tasks]
            
            # Если есть оставшиеся задачи, выбираем случайные
            if remaining_tasks:
                additional_tasks = random.sample(
                    remaining_tasks, 
                    min(num_tasks - len(selected_tasks), len(remaining_tasks))
                )
                selected_tasks.extend(additional_tasks)
        
        return selected_tasks

    def create_student_data(self, current_topic, marks):
        """
        Создание данных ученика
        
        Args:
            current_topic (str): Текущая тема
            marks (dict): Оценки ученика по темам
            
        Returns:
            dict: Данные ученика
        """
        # Получение связанных тем
        related_topics = RELATED_TOPICS_DICT.get(current_topic, [])
        
        # Создание данных ученика
        student_data = {
            "current_topic": current_topic,
            "related_topics": related_topics,
            "marks": marks
        }
        
        return student_data

# Пример использования
if __name__ == "__main__":
    # Создание селектора задач
    selector = TaskSelector()
    
    # Пример данных ученика
    current_topic = "Биномиальное распределение"
    marks = {
        "Геометрическая вероятность: выбор точки из фигуры на плоскости и из числового отрезка": "ещё не изучал",
        "Примеры случайных величин": 2,
        "Распределение вероятностей": "ещё не изучал",
        "Биномиальное распределение": "ещё не изучал",
        "Практическая работа: построение биномиального распределения": 5,
        "Математическое ожидание и его свойства": 2,
        "Рассеивание значений, дисперсия, стандартное отклонение": 4,
        "Свойства дисперсии": 4,
        "Математическое ожидание числа успехов в серии испытаний Бернулли": 4,
        "Дисперсия числа успехов": "ещё не изучал",
        "Практическая работа: математическое ожидание, дисперсия и стандартное отклонение": 4,
        "Измерения вероятностей, точность приближения": 3,
        "Практическая работа: проверка близости частоты и вероятности": 3,
        "Социологические обследования": 4,
        "Закон больших чисел": "ещё не изучал",
        "Число сочетаний": "ещё не изучал",
        "Формула бинома Ньютона": 2,
        "Свойства биномиальных коэффициентов": 5,
        "Треугольник Паскаля": 2,
        "Практическая работа: треугольник Паскаля и свойства биномиальных коэффициентов": "ещё не изучал"
    }
    
    # Создание данных ученика
    student_data = selector.create_student_data(current_topic, marks)
    
    # Получение задач для ученика
    tasks = selector.get_tasks_for_student(student_data, num_tasks=3)
    
    # Вывод задач
    for i, task in enumerate(tasks, 1):
        print(f"Задача {i}:")
        print(f"Условие: {task['условие']}")
        print(f"Тема: {task['тема']}")
        print(f"Сложность: {task['сложность']}")
        print(f"Тип: {task['тип']}")
        print()