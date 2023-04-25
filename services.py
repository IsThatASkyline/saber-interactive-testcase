from typing import List, Dict
import yaml


def get_builds_list_from_yaml(path: str) -> List:
    """
    Получить список Билдов из .YAML файла
    """
    with open(f'{path}builds.yaml') as data:
        try:
            builds_data = yaml.safe_load(data)['builds']
        except Exception:
            builds_data = None
    return builds_data


def get_tasks_list_from_yaml(path: str) -> List:
    """
    Получить список Тасков из .YAML файла
    """
    with open(f'{path}tasks.yaml') as data:
        try:
            tasks_data = yaml.safe_load(data)['tasks']
        except Exception:
            tasks_data = None
    return tasks_data


def get_build_detail_from_yaml(path: str, name: str) -> Dict:
    """
    Получить информацию о конкретном Билде
    """
    builds_data = get_builds_list_from_yaml(path)
    try:
        build_info = [item for item in builds_data if item['name'] == name][0]
    except Exception:
        build_info = None
    return build_info


def get_task_detail_from_yaml(path: str, name: str) -> Dict:
    """
    Получить информацию о конкретном Таске
    """
    tasks_data = get_tasks_list_from_yaml(path)
    try:
        task_info = [item for item in tasks_data if item['name'] == name][0]
    except Exception:
        task_info = None
    return task_info


def get_build_dependencies(path: str, build_name: str) -> List:
    """
    Получить список зависимостей Билда. Возвращает список, в котором сначала
    выводятся зависимости, а затем — зависящие от них задачи
    """
    build = get_build_detail_from_yaml(path, build_name)
    build_tasks = []
    for task_name in build['tasks']:
        r = find_dependencies(path, task_name)
        build_tasks.append(r)
    build_dependencies = arrange_tasks(build_tasks)
    return build_dependencies


def get_task_dependencies(path: str, task_name: str) -> List:
    """
    Получить список зависимостей Таска. Возвращает список, в котором сначала
    выводятся зависимости, а затем — зависящие от них задачи
    """
    task = get_task_detail_from_yaml(path, task_name)
    task_dependencies_list = []
    for task_name in task['dependencies']:
        r = find_dependencies(path, task_name)
        if r:
            task_dependencies_list.append(r)
    task_dependencies = arrange_tasks(task_dependencies_list)
    return task_dependencies


def find_dependencies(path: str, task_name: str) -> List:
    """
    Рекурсивная функция, которая возвращает список зависимостей Таска, и возвращает
    список с разными уровнями вложенности
    """
    task = get_task_detail_from_yaml(path, task_name)
    try:
        if not task['dependencies']:
            return task['name']
        else:
            return [[find_dependencies(path, task) for task in task['dependencies']], task['name']]
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
