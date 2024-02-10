from helpers import authHelper, dbHelper, jiraHelper, logHelper, mdHelper

from dateutil import parser
import datetime
import pytz


#Стартовое сообщение
def send_welcome(message):
    authHelper.bot.reply_to(message,
                      f'Привет, Кирилл\n'
                      'Я создан для того, чтобы:\n'
                      '1. Уведомлять тебя о новых задачах в Jira /tasks\n'
                      '2. Уведомлять тебя о новых комментариях к задачам\n'
                      '3. Создавать в твоем Obsidian заметки по задачам\n')

#Вывод задач в работе
def get_tasks(message):
    jql_query = f'assignee = {authHelper.JIRA_USERNAME} AND statusCategory != Done'
    issues = jiraHelper.jira.search_issues(jql_query)

    if issues:
        response = "Задачи на тебе:\n" + "\n".join([f"{issue.key}: {issue.fields.summary}" for issue in issues])
    else:
        response = "Ты свободен как птица в полёте :)"

    authHelper.bot.reply_to(message, response)

#Загрузка сохраненных комментариев из базы данных
def load_checked_comments():
    raw_comments = dbHelper.load_checked_comments()
    checked_comments = {}
    for issue_key, comment_time_str in raw_comments.items():
        comment_time = parser.parse(comment_time_str)
        checked_comments[issue_key] = comment_time
    return checked_comments

checked_comments = load_checked_comments()

#Уведомления о новых комментариях
def update_comments():
    jql_query = f'(assignee = {authHelper.JIRA_USERNAME} OR watcher = {authHelper.JIRA_USERNAME})'
    issues = jiraHelper.jira.search_issues(jql_query)

    new_comments_found = False  # Флаг для отслеживания наличия новых комментариев

    for issue in issues:
        issue_key = issue.key
        comments = jiraHelper.jira.comments(issue)
        if issue_key not in checked_comments:
            # Установка минимального значения datetime с учетом временной зоны
            checked_comments[issue_key] = datetime.datetime.min.replace(tzinfo=pytz.UTC)

        for comment in comments:
            comment_created_str = comment.created
            # Использование dateutil для преобразования строки в datetime
            comment_created = parser.parse(comment_created_str)
            if comment_created > checked_comments[issue_key]:
                message = f"Новый комментарий в задаче {issue_key} от {comment.author.displayName}:\n{comment.body}"
                authHelper.bot.send_message(authHelper.TELEGRAM_CHAT_ID, message)
                checked_comments[issue_key] = comment_created
                new_comments_found = True

    if new_comments_found:
        dbHelper.save_checked_comments(checked_comments)
    else:
        logHelper.logger.info("Новых комментариев нет")

    logHelper.logger.info('Проверка новых комментариев завершена')

    # Запуск следующей проверки через 60 секунд
    #threading.Timer(60, update_comments()).start()

#Уведомления о смене статусов
def update_status():
    checked_statuses = dbHelper.load_checked_statuses()
    jql_query = f'(assignee = {authHelper.JIRA_USERNAME})'
    issues = jiraHelper.jira.search_issues(jql_query)

    for issue in issues:
        issue_key = issue.key
        current_status = issue.fields.status.name

        if issue_key in checked_statuses:
            previous_status = checked_statuses[issue_key]
        else:
            checked_statuses[issue_key] = current_status
            previous_status = current_status

        if current_status != previous_status:
            message = f"Статус задачи {issue_key} изменился на '{current_status}'."
            authHelper.bot.send_message(authHelper.TELEGRAM_CHAT_ID, message)

        checked_statuses[issue_key] = current_status

        mdHelper.update_status_in_md_file(issue_key, current_status)  # Передача только кода задачи и статуса

        dbHelper.update_checked_statuses(issue_key, current_status)

    dbHelper.save_checked_statuses(checked_statuses)

    logHelper.logger.info('Проверка статусов задач завершена')

    # Запуск следующей проверки через 60 секунд
    #threading.Timer(60, update_status).start()


# Уведомления о новых задачах
def update_tasks():
    jql_query = f'assignee = {authHelper.JIRA_USERNAME} AND created >= -1d'
    issues = jiraHelper.jira.search_issues(jql_query)

    checked_assigned_tasks = dbHelper.load_checked_assigned_tasks()

    new_tasks = []
    for issue in issues:
        issue_key = issue.key
        if issue_key not in checked_assigned_tasks:
            new_tasks.append(issue)
            checked_assigned_tasks[issue_key] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        mdHelper.create_task_md(issue_key, issue.fields.description)

    dbHelper.save_checked_assigned_tasks(checked_assigned_tasks)

    if new_tasks:
        response = "Новые задачи назначены вам:\n" + "\n".join(
            [f"{issue.key}: {issue.fields.summary}" for issue in new_tasks])
        authHelper.bot.send_message(authHelper.TELEGRAM_CHAT_ID, response)

    logHelper.logger.info('Проверка новых задач завершена')

    # Запуск следующей проверки через 60 секунд
    #threading.Timer(60, update_tasks).start()



