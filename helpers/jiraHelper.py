from helpers import authHelper

from jira import JIRA

# Авторизация в Jira
jira_options = {'server': authHelper.JIRA_URL}
jira = JIRA(options=jira_options, basic_auth=(authHelper.JIRA_USERNAME, authHelper.JIRA_PASSWORD))

