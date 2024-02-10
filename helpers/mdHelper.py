from helpers import jsonHelper

import os

path = jsonHelper.config.get('TASK_PATH')

status_mapping = {key: value for key, value in jsonHelper.config.items() if key != "TASK_PATH"}

def create_task_md(issue_key, issue_description):
    filename = os.path.join(path + f'{issue_key}.md')
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"---\n"
                   f"Статус: \n"
                   f"Приоритет: \n"
                   f"Тип: \n"
                   f"ЕИС: \n"
                   f"Jira: JIRA:{issue_key}\n"
                   f"Доработка: \n"
                   f"Связано: \n"
                   f"Комментарий:\n"
                   f"---\n"
                   f"### <font color=\"#1f497d\">Информация по задаче:</font>\n"
                   f"```jira-search\n"
                   f"query: issue = \"{issue_key}\"\n"
                   f"columns: KEY, REPORTER, CREATED, UPDATED, PRIORITY\n"
                   f"```\n"
                   f"### <font color=\"#1f497d\">Связанные задачи:</font>\n"
                   f"```jira-search\n"
                   f"issueLinkType in (\"Зависит от\", \"Склонирован от\", Связано, \"Клон\", "
                   f"\"Дублирует\", \"Основной (дублирован)\", \"Блокирует\", \"Противоречит\", "
                   f"\"Имеет баги\", \"Баг к\") AND issue in linkedIssues(\"{issue_key}\")\n"
                   f"```\n"
                   f"---\n"
                   f"# <font color=\"#c00000\">Что нужно сделать:</font>\n"
                   f"#### Описание задачи: \n"
                   f"{issue_description}\n\n"
                   f"---\n"
                   f"# <font color=\"#c00000\">Анализ:</font>\n\n\n"
                   f"---\n# <font color=\"#c00000\">Комментарии:</font>\n\n\n---\n")

def update_status_in_md_file(issue_key, jira_status):
    md_status = status_mapping.get(jira_status, "")

    with open(path + f'{issue_key}.md', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(path + f'{issue_key}.md', 'w', encoding='utf-8') as file:
        for line in lines:
            if line.startswith("Статус:"):
                file.write(f"Статус: {md_status}\n")
            else:
                file.write(line)

