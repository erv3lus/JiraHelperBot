import json

# Чтение данных из JSON-файла
def read_credentials_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        default_config = {
            "JIRA_URL": "",
            "JIRA_USERNAME": "",
            "JIRA_PASSWORD": "",
            "TELEGRAM_BOT_TOKEN": "",
            "TELEGRAM_CHAT_ID": ""
        }
        with open(file_path, 'w') as file:
            json.dump(default_config, file, ensure_ascii=False, indent=4)
        data = default_config

    return data

credentials_file = 'credentials.json'
credentials = read_credentials_json(credentials_file)

def read_config_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        default_config = {
            "TASK_PATH": "",
            "": ""
        }
        with open(file_path, 'w') as file:
            json.dump(default_config, file, ensure_ascii=False, indent=4)
        data = default_config

    return data

config_file = 'config.json'
config = read_credentials_json(config_file)
