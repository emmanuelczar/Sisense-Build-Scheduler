import requests
from datetime import datetime
import time


HOST_V1 = 'http://sisense.********.com:0000/api/v1'
HOST_V09= 'http://sisense.********.com:0000/api'

GET_ELASTICUBE_ENDPOINT = f'{HOST_V1}/elasticubes/getElasticubes'

ACCESS_TOKEN = "your token here preceded by keyword 'Bearer' "

headers = {
    "authorization": ACCESS_TOKEN
}

response = requests.get(url=GET_ELASTICUBE_ENDPOINT, headers=headers)
response.raise_for_status()
print(response.json())

elasticubes = response.json()


elasticube_dict = {elasticubes[i]['title']: elasticubes[i]["_id"] for i in range(0, len(elasticubes))}
print(elasticube_dict)


SERVER_ADDRESS = "localhost"


def build_elasticube(cube_name, build_type):
    """ Full Build -> use 'entire' or 'full'
    Accumulative Build -> use 'accumulate or 'fullupdateexisting
    Changes Only Build -> use 'schemachanges' or 'delta'. """
    parameters = {
        "type": f'{build_type}'
    }
    elasticube_response = requests.post(url=f'{HOST_V09}/elasticubes/localhost/{cube_name}/startBuild',
                                        params=parameters, headers=headers)
    elasticube_response.raise_for_status()
    print(elasticube_response.text)


scheduler_is_on = True

while scheduler_is_on:
    today = datetime.now().astimezone()
    date_today_string = today.strftime('%m%d%Y')
    time_now_string = today.strftime('%H:%M')
    if time_now_string == "13:00" or time_now_string == "17:00":
        build_elasticube(cube_name="cube_1", build_type="full")
    if time_now_string == "11:00" or time_now_string == "16:00":
        build_elasticube(cube_name="cube_2", build_type="full")
    else:
        print("no scheduled build")

    time.sleep(60)


























