from jira import JIRA
import urllib3
from helpers import authHelper, jsonHelper


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

jira_options = {
    'server': authHelper.JIRA_URL,
    'verify': False,
    'proxy': jsonHelper.credentials.get('PROXY')
}

jira = JIRA(options=jira_options, basic_auth=(authHelper.JIRA_USERNAME, authHelper.JIRA_PASSWORD))
