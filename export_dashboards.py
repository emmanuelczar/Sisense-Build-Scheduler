import requests
import shutil
from datetime import datetime

today = datetime.now()
date_today = today.strftime('%m%d%Y')


HOST = 'http://sisense.********.com:0000/api/v1'
DASHBOARDS_ENDPOINT_EXPORT = f'{HOST}/dashboards/export'
DASHBOARDS_ENDPOINT = f'{HOST}/dashboards'
ACCESS_TOKEN = "your token here preceded by keyword 'Bearer' "

    # TODO 1: Get list of all dashboards
headers = {
    "authorization": ACCESS_TOKEN
}

dashboard_parameters = {
    "fields": "parentFolder,title,oid"
}

dashboards = requests.get(url=DASHBOARDS_ENDPOINT, headers=headers, params=dashboard_parameters)
dashboards.raise_for_status()
dashboard_list = dashboards.json()
print(dashboard_list)
print(type(dashboard_list))
print(len(dashboard_list))


    # TODO 2: Get parent folder list of all the dashboards
folder_list = [dashboard['parentFolder'] for dashboard in dashboard_list if 'parentFolder' in dashboard]
print(set(folder_list))

    # TODO 3: Make a dictionary of Folder:[dashboards]

folder_dict = {i: [] for i in folder_list}
print(folder_dict)


for folder in folder_dict:
    for i in dashboard_list:
        try :
            if i["parentFolder"] == folder:
                folder_dict[folder].append(i['oid'])
        except KeyError:
            print(i)


print(folder_dict)

filename_dict = {
    "dashboard_ID here1": "folder name",
    "dashboard_ID here2": "folder name",

}


for folder in folder_dict:
    dashboard_ids = {
        "dashboardIds": f"{','.join(folder_dict[folder])}"
    }
    dashboard_exports = requests.get(url=DASHBOARDS_ENDPOINT_EXPORT, params=dashboard_ids, headers=headers, stream=True)
    dashboard_exports.raise_for_status()

    try:
        with open(f'{filename_dict[folder]}_{date_today}.dash', 'wb') as out_file:
            shutil.copyfileobj(dashboard_exports.raw, out_file)
    except KeyError:
        with open(f'{folder}_{date_today}.dash', 'wb') as out_file:
            shutil.copyfileobj(dashboard_exports.raw, out_file)






