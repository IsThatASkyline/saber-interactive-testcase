from click.testing import CliRunner
from app import main

"""
Тесты для CLI-утилиты

Для тестов я использую специальные builds.yaml и tasks.yaml, которые находятся в директории tests.
Чтобы указать путь к ним, я использую флаг -p

Запустить тесты - coverage run -m pytest -v
Проверить % покрытия кода тестами - coverage report
"""


def test_get_tasks_list():
    runner = CliRunner()
    result = runner.invoke(main, ['list', 'tasks', '-p', 'tests/'])

    assert result.output == 'List of available tasks:\n* task1\n* sub_task1\n* sub_task2\n'


def test_get_builds_list():
    runner = CliRunner()
    result = runner.invoke(main, ['list', 'builds', '-p', 'tests/'])

    assert result.output == 'List of available builds:\n* build1\n* build2\n'


def test_get_build_detail():
    runner = CliRunner()
    result1 = runner.invoke(main, ['get', 'build', 'build1', '-p', 'tests/'])
    result2 = runner.invoke(main, ['get', 'build', 'build2', '-p', 'tests/'])

    assert result1.output == 'Build info:\n* name: build1\n* tasks: sub_task1, sub_task2\n'
    assert result2.output == 'Build info:\n* name: build2\n* tasks: sub_task1, sub_task2, task1\n'


def test_get_task_detail():
    runner = CliRunner()
    result1 = runner.invoke(main, ['get', 'task', 'sub_task1', '-p', 'tests/'])
    result2 = runner.invoke(main, ['get', 'task', 'task1', '-p', 'tests/'])

    assert result1.output == 'Task info:\n* name: sub_task1\n* dependencies: []\n'
    assert result2.output == 'Task info:\n* name: task1\n* dependencies: sub_task1, sub_task2\n'


def test_wrong_commands_and_args():
    runner = CliRunner()
    path = 'wrong/path/'
    arg = 'wrong_arg'
    command = 'wrong_command'
    path_err = runner.invoke(main, ['list', 'tasks', '-p', path])
    arg_err1 = runner.invoke(main, ['get', arg, 'sub_task1', '-p', 'tests/'])
    arg_err2 = runner.invoke(main, ['list', arg])
    command_err = runner.invoke(main, [command])

    assert path_err.output == f'Не найдены файлы builds.yaml и tasks.yaml по пути: {path}\n'
    assert arg_err1.output == f'Неверный аргумент: {arg}\nДоступные аргументы: build, task\n'
    assert arg_err2.output == f'Неверный аргумент: {arg}\nДоступные аргументы: builds, tasks\n'
    assert f"Error: No such command '{command}'.\n" in command_err.output
