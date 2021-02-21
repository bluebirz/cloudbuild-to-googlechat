import base64
import json
from httplib2 import Http
from dateutil.parser import isoparse
from datetime import datetime, timezone
import pytz
import os

GGCHAT_URL = os.environ.get('_URL', 'Environment variable does not exist')
    
def send_ggchat(payload):
    time_pattern = "%Y-%m-%d %H:%M:%S"
    time_timezone = pytz.timezone("Asia/Bangkok")
    time_start = isoparse(payload['timing']['FETCHSOURCE']['startTime']).astimezone(time_timezone)
    time_end = isoparse(payload['timing']['BUILD']['endTime']).astimezone(time_timezone)

    message =  """{{ "cards": [{{
        "header": {{
            "title": "Build Notification for Backend Core",
            "subtitle": "Build {build_id} is {status}"
        }},
        "sections": [{{
            "widgets": [
                {{"keyValue": {{"topLabel": "Repo", "content": "{repo}"}} }},
                {{"keyValue": {{"topLabel": "Branch", "content": "{branch}"}} }},
                {{"keyValue": {{"topLabel": "Commit", "content": "{commit}"}} }},
                {{"keyValue": {{"topLabel": "Created", "content": "{created_time}"}} }},
                {{"keyValue": {{"topLabel": "Status", "content": "{status}"}} }},
                {{"keyValue": {{"topLabel": "Duration (sec)", "content": "{duration}"}} }},
                {{"buttons": [{{
                    "textButton": {{
                        "text": "{build_id} log Link",
                        "onClick": {{"openLink": {{"url": "{log_url}"}} }}
                    }} 
                }} ] }}
            ]
        }} ]
    }} ] }} """.format(
                    build_id=payload['id'].split("-")[0],
                    status=payload['status'],
                    repo=payload['substitutions']['REPO_NAME'],
                    branch=payload['substitutions']['BRANCH_NAME'],
                    commit=payload['substitutions']['SHORT_SHA'],
                    created_time=time_start.strftime(time_pattern),
                    duration=(time_end - time_start).total_seconds(),
                    log_url=payload['logUrl'],
                    )

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()
    response = http_obj.request(
        uri=GGCHAT_URL,
        method='POST',
        headers=message_headers,
        body=json.dumps(json.loads(message))
    )
    print(response)


def cloudbuild_notifications(event, context):
    message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    send_ggchat(message)