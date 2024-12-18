import formlabs_local_api_minimal as formlabs
import requests

pathToPreformServer = "/workspace/PreFormServer/PreFormServer.exe"
with formlabs.PreFormApi.start_preform_server(pathToPreformServer=pathToPreformServer, command_prefix="/usr/bin/wine"):
    payload = {
        "machine_type": "FORM-4-0",
        "material_code": "FLRG1011",
        "layer_thickness_mm": 0.1,
        "print_setting": "DEFAULT"
    }
    response = requests.request("POST", "http://localhost:44388/scene/", json=payload)
    response.raise_for_status()
    print(response.json())
    print("Scene created, exiting")
