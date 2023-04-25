# Тестовое задание на позицию Junior Python Developer в Saber Interactive

## Задание
[Saber_Interactive_Junior_Python_Developer.docx](https://github.com/artklk12/saber-interactive-testcase/files/11322437/Saber_Interactive_Junior_Python_Developer.docx)

## Установка
```
git clone https://github.com/artklk12/saber-interactive-testcase.git
pip install -r requirements.txt
```

## Использование
```
python app.py [команда] [аргументы] [флаги]
```

### Примеры
Структура проекта для примера
* app.py
* services.py
* tasks.yaml
* builds.yaml
* old_data
  * tasks.yaml
  * builds.yaml
  
1) Вывести список всех Билдов
```
python app.py list builds
```
```
List of available builds:
* approach_important
* audience_stand
* time_alone
```

2) Вывести информацию о Таске design_black_centaurs, из файла, находящегося в директории old_data
```
python app.py get design_black_centaurs -p 'old_data/'
```
```
Task info:
* name: design_black_centaurs
* dependencies: bring_black_leprechauns, write_aqua_leprechauns
```

**Как и сказано в задании, сначала выводятся зависимости, а затем — зависящие от них задачи**

## Тестирование
Тесты находятся в директории tests, также там находятся тестовые данные, tasks.yaml и builds.yaml

Для запуска тестов выполните
```
coverage run -m pytest -v
```

Чтобы узнать процент покрытия кода тестами, выполните
```
coverage report
```
```
Name                Stmts   Miss  Cover
---------------------------------------
app.py                 60     13    78%
services.py            61     10    84%
tests\__init__.py       0      0   100%
tests\test_app.py      36      0   100%
---------------------------------------
TOTAL                 157     23    85%
```

 
