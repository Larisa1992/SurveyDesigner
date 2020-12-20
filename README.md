# SurveyDesigner
Финальный проект курса Full-stack веб-разработчик на Python: конструктор создания опросов


Приложение развернуто Heroku по адресу
https://rocky-tundra-10357.herokuapp.com/

Можно запустить в Docker контейнере.
Для этого нужно отредактировать настройки проекта:
    -в файле SurveyDesigner/settings.py изменить значение константы HEROKU на False:
    HEROKU=False

Загрузить фикстуры
1) приложения users
python manage.py loaddata users_data.xml

2) основного приложения polls
python manage.py loaddata polls_data.xml

Документация проекта оформлена в формате HTML.
Чтобы ее просмотреть, в скаченном репозитории откройте файл SurveyDesigner\docs\build\html\index.html в браузере.