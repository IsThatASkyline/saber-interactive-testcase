import click
import services


# создаем группу команд `cli`
@click.group()
def main():
    pass


# присоединяем команду `list`
@main.command()
@click.option('-p', '--path', default='', help='Path to .yaml file')
@click.argument('inst')
def list(path, inst):
    """
    Вывести все Билды/Таски

    -p, --path: Используйте для переопределения пути к .yaml файлам.
                По умолчанию, путем до файлов считается текущая рабочая директория
    """
    try:
        if inst == 'builds':
            builds_data = services.get_builds_list_from_yaml(path)
            click.echo('List of available builds:')
            if builds_data:
                for item in builds_data:
                    click.echo(f"* {item['name']}")
            else:
                click.echo("  No builds available")

        elif inst == 'tasks':
            tasks_data = services.get_tasks_list_from_yaml(path)
            click.echo('List of available tasks:')
            if tasks_data:
                for item in tasks_data:
                    click.echo(f"* {item['name']}")
            else:
                click.echo("  No tasks available")

        else:
            click.echo(f'Неверный аргумент: {inst}\nДоступные аргументы: builds, tasks')
    except FileNotFoundError:
        click.echo(f'Не найдены файлы builds.yaml и tasks.yaml по пути: {path}')


# присоединяем команду `get`
@main.command()
@click.option('-p', '--path', default='', help='Path to .yaml file')
@click.argument('inst')
@click.argument('name')
def get(path, inst, name):
    """
    Получить подробную информацию о Билде/Таске

    -p, --path: Используйте для переопределения пути к .yaml файлам.
                По умолчанию, путем до файлов считается текущая рабочая директория
    """
    try:
        if inst == 'build':
            try:
                build_info, build_dependencies = services.get_build_dependencies(path, name)
                click.echo('Build info:')
                click.echo(f"* name: {build_info['name']}")
                click.echo(f"* tasks: {', '.join(build_dependencies) if build_dependencies else []}")
            except TypeError:
                click.echo(f'Билд с именем {name} не найден')
            except KeyError:
                click.echo(f'Зависимости билда {name} не определены')

        elif inst == 'task':
            try:
                task_info, task_dependencies = services.get_task_dependencies(path, name)
                click.echo('Task info:')
                click.echo(f"* name: {task_info['name']}")
                click.echo(f"* dependencies: {', '.join(task_dependencies) if task_dependencies else []}")
            except TypeError:
                click.echo(f'Таск с именем {name} не найден')
            except KeyError:
                click.echo(f'Зависимости задачи {name} не определены')

        else:
            click.echo(f'Неверный аргумент: {inst}\nДоступные аргументы: build, task')
    except FileNotFoundError:
        click.echo(f'Не найдены файлы builds.yaml и tasks.yaml по пути: {path}')


if __name__ == '__main__':
    main()
