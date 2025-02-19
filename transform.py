import logging
import os
import shutil
import sys
import re

from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_txt(filename):
    with open(filename, encoding='utf-8') as txt_file:
        return txt_file.read()

def save_txt(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

def fix_js_css_images(all_projects_pages: list, folders_to_fix: list = ('/js', '/css', '/images')) -> None:
    """
    Исправляем путь для каталогов js/css/images на идущий из корня.

    :param all_projects_pages: Список всех страниц проекта, в которых требуется проверить необходимость исправления.
    :param folders_to_fix: Список папок, для которых будет проверяться наличие проблемных путей, в формате /folder_name.
    :return:
    """
    # Регулярка для поиска http/https ссылок в кавычках
    dynamic_part = "|".join(re.escape(folder) for folder in folders_to_fix)
    pattern = rf'["\'](https?://[^"\']*({dynamic_part})[^"\']*)["\']'
    for page in all_projects_pages:
        page_code = read_txt(page)
        if any(folder in page_code for folder in folders_to_fix):
            matches = re.findall(pattern, page_code)
            for match in matches:
                # Оставим только очевидно внутренние ссылки
                if 'tilda' in match[0]:
                    clean_url = match[1] + match[0].split(match[1], 1)[1]
                    save_txt(page, page_code.replace(match[0], clean_url))
                    logging.info(f'Сохранена новая версия файла {page}')


def fix_menu(work_dir_path: str) -> None:
    #menu = read_txt(Path(work_dir_path, 'headhtml').resolve())
    pass


def rename_pages(work_dir_path: str) -> None:
    """
    Переименовывает все страницы по данным htaccess
    :param work_dir_path: Рабочий каталог с экспортированными файлами.
    :return:
    """
    with open(Path(work_dir_path, 'htaccess').resolve(), 'r', encoding='utf-8') as file:
        rules = file.readlines()
    for rule in rules:
        match = re.match(r'^RewriteRule\s+(\S+)(?!/)\s+(\S+)', rule)
        if match:
            new_folder, old_name = match.groups()
            old_path = Path(os.path.join(wor_dir_path, old_name))
            if (new_folder[-2:] == '/$')|('.html' not in old_name):
                continue
            else:
                new_folder = new_folder[1:-1]
            new_path = Path(os.path.join(wor_dir_path, new_folder))
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            if os.path.exists(old_path):
                os.rename(old_path, Path(os.path.join(wor_dir_path, 'index.html')))
                shutil.move(Path(os.path.join(wor_dir_path, 'index.html')), new_path)
                logging.info(f"Переименовываем и перемещаем {old_name} → {new_folder}")
            else:
                logging.error(f"Файл {old_name} не найден, переименование невозможно")


def fix_tilda(work_dir_path: str = None) -> None:
    """
    Последовательно применяет функции, исправляющие экспорт из тильды.

    :param work_dir_path: Рабочий каталог с экспортированными файлами.
    :return:
    """
    if not work_dir_path:
        logging.error("Отсутствует путь к каталогу с экспортом сайта")
        return
    all_projects_pages = []
    for path, subdirs, files in os.walk(work_dir_path):
        if '\images' not in path:
            for name in files:
                all_projects_pages.append(Path(os.path.join(path, name)).resolve())
    fix_js_css_images(all_projects_pages)
    rename_pages(work_dir_path)
    #fix_menu(work_dir_path)


if __name__ == "__main__":
    wor_dir_path = sys.argv[1] if len(sys.argv) == 2 else None
    fix_tilda(wor_dir_path)



