# Проблемы, которые решает этот код

Тильда на экспорте отдает не настоящие статические сайты. Чтобы докрутить их до статического состояния, скрипт:

1) ссылки на js/ css/ images исправляются на идущие от корня;
2) страницы вида /pageXXXX.html переименовываются согласно данным из файлика в /anons/index.html (по данным htaccess)

Есть мнение, что-то где-то сломано в меню, будет починено. Но пока не понятно — кажется, достаточно переименования.

Запуск с командной строки:

`transform.py "some/folder/path"`