from typing import List, Dict
import yaml


def get_builds_list_from_yaml(path: str):
    """
    Получить список Билдов из .YAML файла
    """
    with open(f'{path}builds.yaml') as data:
        try:
            builds_data = yaml.safe_load(data)['builds']
        except Exception:
            builds_data = None
    return builds_data


def get_tasks_list_from_yaml(path: str):
    """
    Получить список Билдов из .YAML файла
    """
    with open(f'{path}tasks.yaml') as data:
        try:
            tasks_data = yaml.safe_load(data)['tasks']
        except Exception:
            tasks_data = None
    return tasks_data


def get_build_detail(builds_data, name: str) -> Dict:
    """
    Получить информацию о конкретном Билде
    """
    try:
        build_info = [item for item in builds_data if item['name'] == name][0]
    except Exception:
        build_info = None
    return build_info


def get_task_detail(tasks_data, name: str) -> Dict:
    """
    Получить информацию о конкретном Таске
    """
    try:
        task_info = [item for item in tasks_data if item['name'] == name][0]
    except Exception:
        task_info = None
    return task_info


def get_build_dependencies(path: str, build_name: str):
    """
    Получить список зависимостей Билда. Возвращает список, в котором сначала
    выводятся зависимости, а затем — зависящие от них задачи
    """
    builds_data = get_builds_list_from_yaml(path=path)
    tasks_data = get_tasks_list_from_yaml(path=path)
    build_info = get_task_detail(builds_data, build_name)
    build_dependencies_list = find_dependencies(builds_data, tasks_data, build_name)
    build_dependencies = arrange_tasks(build_dependencies_list)
    return build_info, build_dependencies[:-1]


def get_task_dependencies(path, task_name: str):
    """
    Получить список зависимостей Таска. Возвращает список, в котором сначала
    выводятся зависимости, а затем — зависящие от них задачи
    """
    builds_data = get_builds_list_from_yaml(path=path)
    tasks_data = get_tasks_list_from_yaml(path=path)
    task_info = get_task_detail(tasks_data, task_name)
    task_dependencies_list = find_dependencies(builds_data, tasks_data, task_name)
    task_dependencies = arrange_tasks(task_dependencies_list)
    return task_info, task_dependencies[:-1]


def find_dependencies(builds_data, tasks_data, task_name: str) -> List:
    """
    Рекурсивная функция, которая возвращает список зависимостей Таска, и возвращает
    список с разными уровнями вложенности
    """
    task = get_task_detail(tasks_data, task_name)
    if not task:
        task = get_build_detail(builds_data, task_name)
    try:
        try:
            task_dependencies = task['dependencies']
        except Exception:
            task_dependencies = task['tasks']
        if not task_dependencies:
            return [task['name']]
        else:
            return [[find_dependencies(builds_data, tasks_data, task) for task in task_dependencies], task['name']]
    except Exception:
        return None


def arrange_tasks(dependencies_list: List) -> List:
    """
    Рекурсивная функция, которая 'выпрямляет' список - убирает вложенности и выводит зависимости в нужном порядке
    """
    if not dependencies_list:
        return dependencies_list
    if isinstance(dependencies_list[0], list):
        return arrange_tasks(dependencies_list[0]) + arrange_tasks(dependencies_list[1:])
    return dependencies_list[:1] + arrange_tasks(dependencies_list[1:])
