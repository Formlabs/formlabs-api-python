# formlabs_local_api
# Introduction
The Formlabs Local API is designed for integrations that want to automate
job preparation, getting local-network printer status, or sending jobs to Formlabs printers
without launching the PreForm graphical user interface. A server application
must be installed and run on a user's computer to use this API.

Example use cases:
- Scripted job preparation that takes a folder of models, sets up a print,
  and uploads it to a printer without user input.
- Deep and custom integrations into 3D Modeling and Design software to
  prepare print scenes beyond the scope of the PreForm Command Line Arguments.

This API uses RESTful principles. This means the API is organized around
resources and collections of resources. Resources and collections are each
available at their own URI. You can interact with these resources using
standard HTTP Methods on the resource's URI.

Example endpoint:
```
GET http://localhost:44388/scene/
```

Responses from the API server will be in JSON and are documented throughout
the reference docs. This API is described by an [OpenAPI Specification](https://spec.openapis.org/oas/v3.1.0).
This interactive documentation is automatically generated from the specification file.

# Technical Overview

## PreFormServer Background Application
All Local API integrations involve starting the PreFormServer background
application to expose its HTTP API, then making local HTTP API calls in your own code.
This application is like [PreForm](https://formlabs.com/software/preform/), Formlabs' regular job preparation application,
but it does not open a graphical window, and interaction is done via HTTP API requests.
The PreFormServer application is supported on Windows and MacOS with separate
downloads for each Operating System.

### Installing PreFormServer
The PreFormServer application can be downloaded from the [Formlabs API downloads and release notes page](https://support.formlabs.com/s/article/Formlabs-API-downloads-and-release-notes).
After downloading, unzip the file and move the application to the desired location on your computer.
Any location can be used as the path to the application should be referenced from your integration code.

### Starting PreFormServer
The PreFormServer application can started manually from your Operating System's command prompt or terminal,
but most integrations will start the application programmatically from integration code.
The command line argument `--port` is required to specify the port number the HTTP Server will listen on.

The HTTP API server started by the PreFormServer application cannot immediately respond to requests.
When the server is ready to accept requests, it will output `READY FOR INPUT` in the standard output.

For example, running the PreFormServer application on Windows from the command prompt:
```
PreFormServer.exe --port 44388
```
will output something like the following:
```
starting HTTP server
Listening...
HTTP server listening on port 44388
READY FOR INPUT
```

## Making API Requests
The code to make HTTP API requests to a running PreFormServer can be written
directly in your integration code or by using a generated library that does
the API calls. The endpoints and format of the HTTP API are described on this
page and in the openapi.yaml file.  Formlabs provides an example [Python library](https://github.com/Formlabs/formlabs-api-python)
that handles the setup and request formatting.

## Glossary
- **Scene**: The current state of a job that can be printed on a particular printer model.
  This includes both the “Scene Settings” and all of the currently loaded models and their support structures.
- **Scene Settings**: Printer type and material information of scene. Describes the
  build platform size, the printer capabilities, and what material and print settings
  it is set up to be printed with.

## Stateful Interactions
The PreForm Server is stateful in that while it is running, it keeps a cache of scenes.
By default, it caches 100 scenes in memory, with unlimited scenes stored on disk, though this
may be changed with the `--scene-cache-size` parameter. Scenes are identified by their
IDs, returned from the `/scene/` endpoint. `/scene/` endpoints also accept a scene ID of
\"default\", which will use a single global scene. Endpoints with no scene id provided
(e.g. `/scene/auto-layout/`) are deprecated. They will use the most recently created scene,
and possibly modify it. All other `/scene/` requests will use the user specified scene, and possibly
modify it. For example, initially a scene may be empty and then if a load model request
is made then the cached scene will have one model loaded. Calling the load model endpoint
again will load another copy of the model resulting in two models in the cached scene.

## Blocking Calls & Asynchronous Requests
Unless otherwise stated, API calls are blocking: the HTTP request will not return
until the operation has completed.  Some requests like running the auto support
action on a scene with many complicated models could take over 1 minute (depending
on computer resources). The Server has a timeout of 10 minutes for all requests.

Some long-running operations can be called asynchronously by adding `?async=true` to the
request. These requests will return immediately and the operation will be tracked
separately. The caller can poll for completion using the `/operations/{operation_id}/`
endpoint, and track the percentage progress of the outstanding operation.

Requests involving the scene will always use the scene state at the time the request
was made, without any partially completed operations. For example, if a “get scene”
request is made during a “auto support” request that has not finished, then the
“get scene” request will return data that will not include the auto support changes.

Multiple requests editing the same scene should NOT be made in parallel. If an \"auto
layout\" request is made during an \"auto support\" request that has not finished,
whichever operation finishes last will \"win\": either an auto-layout of unsupported
models or the original layout with supports. PreformServer currently gives no warning
when this happens.

## File Paths
When saving and loading files, the local API inputs expect full operating system paths
to local files on disk.

Correct file path:
- `C:\\Projects\\Models\\part.stl`

Incorrect file paths:
- `.\\Models\\part.stl`
- `%ENV_VAR%\\part.stl`
- `part.stl`
- `https://filestorage.com/part.stl`

# Errors
Conventional HTTP response codes are used to indicate the success or failure of
an API request. In general: Codes in the 2xx range indicate success. Codes in
the 4xx range indicate an error that failed given the information provided.
Codes in the 5xx range indicate an error with Formlabs' servers.

# Security
The HTTP Server that PreForm uses to communicate is only exposed to the local
network of your computer and not to the public Internet, unless you have
configured your computer to expose the port running the PreForm Server to the Internet.

Some requests require an Internet connection, require Dashboard login, and
make web requests to perform their action (such as printing to a remote printer).


This Python package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 0.9.0
- Package version: 0.9.0
- Generator version: 7.12.0
- Build package: org.openapitools.codegen.languages.PythonClientCodegen
For more information, please visit [https://support.formlabs.com/](https://support.formlabs.com/)

## Requirements.

Python 3.8+

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import formlabs_local_api
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import formlabs_local_api
```

### Tests

Execute `pytest` to run the tests.

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import formlabs_local_api
from formlabs_local_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:44388
# See configuration.py for a list of all supported configuration parameters.
configuration = formlabs_local_api.Configuration(
    host = "http://localhost:44388"
)



# Enter a context with an instance of the API client
with formlabs_local_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = formlabs_local_api.APIInfoApi(api_client)

    try:
        # Get API Version
        api_response = api_instance.get_api_version()
        print("The response of APIInfoApi->get_api_version:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling APIInfoApi->get_api_version: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://localhost:44388*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*APIInfoApi* | [**get_api_version**](docs/APIInfoApi.md#get_api_version) | **GET** / | Get API Version
*DevicesApi* | [**discover_devices**](docs/DevicesApi.md#discover_devices) | **POST** /discover-devices/ | Discover Devices
*DevicesApi* | [**get_device**](docs/DevicesApi.md#get_device) | **GET** /devices/{id}/ | Get Device
*DevicesApi* | [**get_devices**](docs/DevicesApi.md#get_devices) | **GET** /devices/ | Get Devices
*DevicesApi* | [**upload_firmware**](docs/DevicesApi.md#upload_firmware) | **POST** /upload-firmware/ | Upload Firmware
*ExportingApi* | [**save_form_file**](docs/ExportingApi.md#save_form_file) | **POST** /scene/{scene_id}/save-form/ | Save .form file
*ExportingApi* | [**save_fps_file**](docs/ExportingApi.md#save_fps_file) | **POST** /scene/{scene_id}/save-fps-file/ | Save FPS file
*ExportingApi* | [**save_screenshot**](docs/ExportingApi.md#save_screenshot) | **POST** /scene/{scene_id}/save-screenshot/ | Save screenshot file
*ExportingDeprecatedApi* | [**save_form_file_deprecated**](docs/ExportingDeprecatedApi.md#save_form_file_deprecated) | **POST** /scene/save-form/ | Save .form file
*ExportingDeprecatedApi* | [**save_fps_file_deprecated**](docs/ExportingDeprecatedApi.md#save_fps_file_deprecated) | **POST** /scene/save-fps-file/ | Save FPS file
*ExportingDeprecatedApi* | [**save_screenshot_deprecated**](docs/ExportingDeprecatedApi.md#save_screenshot_deprecated) | **POST** /scene/save-screenshot/ | Save screenshot file
*GettingSceneInformationApi* | [**estimate_print_time**](docs/GettingSceneInformationApi.md#estimate_print_time) | **POST** /scene/{scene_id}/estimate-print-time/ | Estimate Print Time
*GettingSceneInformationApi* | [**get_all_scenes**](docs/GettingSceneInformationApi.md#get_all_scenes) | **GET** /scenes/ | Get All Scenes
*GettingSceneInformationApi* | [**get_model**](docs/GettingSceneInformationApi.md#get_model) | **GET** /scene/{scene_id}/models/{id}/ | Get model
*GettingSceneInformationApi* | [**get_print_validation**](docs/GettingSceneInformationApi.md#get_print_validation) | **GET** /scene/{scene_id}/print-validation/ | Get Print Validation
*GettingSceneInformationApi* | [**get_scene**](docs/GettingSceneInformationApi.md#get_scene) | **GET** /scene/{scene_id}/ | Get Scene
*GettingSceneInformationApi* | [**get_scene_interferences**](docs/GettingSceneInformationApi.md#get_scene_interferences) | **POST** /scene/{scene_id}/interferences/ | Get Scene Interferences
*GettingSceneInformationDeprecatedApi* | [**estimate_print_time_deprecated**](docs/GettingSceneInformationDeprecatedApi.md#estimate_print_time_deprecated) | **POST** /scene/estimate-print-time/ | Estimate Print Time
*GettingSceneInformationDeprecatedApi* | [**get_model_deprecated**](docs/GettingSceneInformationDeprecatedApi.md#get_model_deprecated) | **GET** /scene/models/{id}/ | Get model
*GettingSceneInformationDeprecatedApi* | [**get_print_validation_deprecated**](docs/GettingSceneInformationDeprecatedApi.md#get_print_validation_deprecated) | **GET** /scene/print-validation/ | Get Print Validation
*GettingSceneInformationDeprecatedApi* | [**get_scene_deprecated**](docs/GettingSceneInformationDeprecatedApi.md#get_scene_deprecated) | **GET** /scene/ | Get Scene
*GettingSceneInformationDeprecatedApi* | [**get_scene_interferences_deprecated**](docs/GettingSceneInformationDeprecatedApi.md#get_scene_interferences_deprecated) | **POST** /scene/interferences/ | Get Scene Interferences
*ModifyingASceneApi* | [**add_drain_holes**](docs/ModifyingASceneApi.md#add_drain_holes) | **POST** /scene/{scene_id}/add-drain-holes/ | Add Drain Holes
*ModifyingASceneApi* | [**auto_layout**](docs/ModifyingASceneApi.md#auto_layout) | **POST** /scene/{scene_id}/auto-layout/ | Auto Layout
*ModifyingASceneApi* | [**auto_orient**](docs/ModifyingASceneApi.md#auto_orient) | **POST** /scene/{scene_id}/auto-orient/ | Auto Orient
*ModifyingASceneApi* | [**auto_pack**](docs/ModifyingASceneApi.md#auto_pack) | **POST** /scene/{scene_id}/auto-pack/ | Auto Pack
*ModifyingASceneApi* | [**auto_support**](docs/ModifyingASceneApi.md#auto_support) | **POST** /scene/{scene_id}/auto-support/ | Auto Support
*ModifyingASceneApi* | [**create_default_scene**](docs/ModifyingASceneApi.md#create_default_scene) | **POST** /scene/default/ | Create Default Scene
*ModifyingASceneApi* | [**create_scene**](docs/ModifyingASceneApi.md#create_scene) | **POST** /scene/ | Create Scene
*ModifyingASceneApi* | [**delete_model**](docs/ModifyingASceneApi.md#delete_model) | **DELETE** /scene/{scene_id}/models/{id}/ | Delete model
*ModifyingASceneApi* | [**duplicate_model**](docs/ModifyingASceneApi.md#duplicate_model) | **POST** /scene/{scene_id}/models/{id}/duplicate/ | Duplicate model
*ModifyingASceneApi* | [**hollow_model**](docs/ModifyingASceneApi.md#hollow_model) | **POST** /scene/{scene_id}/hollow/ | Hollow Model
*ModifyingASceneApi* | [**import_model**](docs/ModifyingASceneApi.md#import_model) | **POST** /scene/{scene_id}/import-model/ | Import model
*ModifyingASceneApi* | [**label_part**](docs/ModifyingASceneApi.md#label_part) | **POST** /scene/{scene_id}/label/ | Label Part
*ModifyingASceneApi* | [**load_form_file**](docs/ModifyingASceneApi.md#load_form_file) | **POST** /load-form/ | Load .form file
*ModifyingASceneApi* | [**pack_and_cage**](docs/ModifyingASceneApi.md#pack_and_cage) | **POST** /scene/pack-and-cage/ | Pack and Cage
*ModifyingASceneApi* | [**replace_model**](docs/ModifyingASceneApi.md#replace_model) | **POST** /scene/{scene_id}/models/{id}/replace/ | Replace model
*ModifyingASceneApi* | [**scan_to_model**](docs/ModifyingASceneApi.md#scan_to_model) | **POST** /scene/{scene_id}/scan-to-model/ | Scan to model
*ModifyingASceneApi* | [**update_model**](docs/ModifyingASceneApi.md#update_model) | **POST** /scene/{scene_id}/models/{id}/ | Update model
*ModifyingASceneApi* | [**update_scene**](docs/ModifyingASceneApi.md#update_scene) | **PUT** /scene/{scene_id}/ | Update Scene
*ModifyingASceneDeprecatedApi* | [**add_drain_holes_deprecated**](docs/ModifyingASceneDeprecatedApi.md#add_drain_holes_deprecated) | **POST** /scene/add-drain-holes/ | Add Drain Holes
*ModifyingASceneDeprecatedApi* | [**auto_layout_deprecated**](docs/ModifyingASceneDeprecatedApi.md#auto_layout_deprecated) | **POST** /scene/auto-layout/ | Auto Layout
*ModifyingASceneDeprecatedApi* | [**auto_orient_deprecated**](docs/ModifyingASceneDeprecatedApi.md#auto_orient_deprecated) | **POST** /scene/auto-orient/ | Auto Orient
*ModifyingASceneDeprecatedApi* | [**auto_pack_deprecated**](docs/ModifyingASceneDeprecatedApi.md#auto_pack_deprecated) | **POST** /scene/auto-pack/ | Auto Pack
*ModifyingASceneDeprecatedApi* | [**auto_support_deprecated**](docs/ModifyingASceneDeprecatedApi.md#auto_support_deprecated) | **POST** /scene/auto-support/ | Auto Support
*ModifyingASceneDeprecatedApi* | [**delete_model_deprecated**](docs/ModifyingASceneDeprecatedApi.md#delete_model_deprecated) | **DELETE** /scene/models/{id}/ | Delete model
*ModifyingASceneDeprecatedApi* | [**duplicate_model_deprecated**](docs/ModifyingASceneDeprecatedApi.md#duplicate_model_deprecated) | **POST** /scene/models/{id}/duplicate/ | Duplicate model
*ModifyingASceneDeprecatedApi* | [**hollow_model_deprecated**](docs/ModifyingASceneDeprecatedApi.md#hollow_model_deprecated) | **POST** /scene/hollow/ | Hollow Model
*ModifyingASceneDeprecatedApi* | [**import_model_deprecated**](docs/ModifyingASceneDeprecatedApi.md#import_model_deprecated) | **POST** /scene/import-model/ | Import model
*ModifyingASceneDeprecatedApi* | [**label_part_deprecated**](docs/ModifyingASceneDeprecatedApi.md#label_part_deprecated) | **POST** /scene/label/ | Label Part
*ModifyingASceneDeprecatedApi* | [**replace_model_deprecated**](docs/ModifyingASceneDeprecatedApi.md#replace_model_deprecated) | **POST** /scene/models/{id}/replace/ | Replace model
*ModifyingASceneDeprecatedApi* | [**scan_to_model_deprecated**](docs/ModifyingASceneDeprecatedApi.md#scan_to_model_deprecated) | **POST** /scene/scan-to-model/ | Scan to model
*ModifyingASceneDeprecatedApi* | [**update_model_deprecated**](docs/ModifyingASceneDeprecatedApi.md#update_model_deprecated) | **POST** /scene/models/{id}/ | Update model
*ModifyingASceneDeprecatedApi* | [**update_scene_deprecated**](docs/ModifyingASceneDeprecatedApi.md#update_scene_deprecated) | **PUT** /scene/ | Update Scene
*OperationsApi* | [**call_print**](docs/OperationsApi.md#call_print) | **POST** /scene/{scene_id}/print/ | Print
*OperationsApi* | [**get_all_operations**](docs/OperationsApi.md#get_all_operations) | **GET** /operations/ | List All Operations
*OperationsApi* | [**get_operation**](docs/OperationsApi.md#get_operation) | **GET** /operations/{id}/ | Get Operation Status
*OperationsDeprecatedApi* | [**print_deprecated**](docs/OperationsDeprecatedApi.md#print_deprecated) | **POST** /scene/print/ | Print
*PrintSettingsApi* | [**list_materials**](docs/PrintSettingsApi.md#list_materials) | **GET** /list-materials/ | List Materials
*PrintingApi* | [**call_print**](docs/PrintingApi.md#call_print) | **POST** /scene/{scene_id}/print/ | Print
*PrintingDeprecatedApi* | [**print_deprecated**](docs/PrintingDeprecatedApi.md#print_deprecated) | **POST** /scene/print/ | Print
*RemoteAccessApi* | [**call_print**](docs/RemoteAccessApi.md#call_print) | **POST** /scene/{scene_id}/print/ | Print
*RemoteAccessApi* | [**discover_devices**](docs/RemoteAccessApi.md#discover_devices) | **POST** /discover-devices/ | Discover Devices
*RemoteAccessApi* | [**get_device**](docs/RemoteAccessApi.md#get_device) | **GET** /devices/{id}/ | Get Device
*RemoteAccessApi* | [**get_devices**](docs/RemoteAccessApi.md#get_devices) | **GET** /devices/ | Get Devices
*RemoteAccessApi* | [**get_user**](docs/RemoteAccessApi.md#get_user) | **GET** /user/ | Get logged in user information
*RemoteAccessApi* | [**login**](docs/RemoteAccessApi.md#login) | **POST** /login/ | Login
*RemoteAccessApi* | [**logout**](docs/RemoteAccessApi.md#logout) | **POST** /logout/ | Log out
*RemoteAccessDeprecatedApi* | [**print_deprecated**](docs/RemoteAccessDeprecatedApi.md#print_deprecated) | **POST** /scene/print/ | Print


## Documentation For Models

 - [AccessToken](docs/AccessToken.md)
 - [AddDrainHoles200Response](docs/AddDrainHoles200Response.md)
 - [AddDrainHolesRequest](docs/AddDrainHolesRequest.md)
 - [AutoLayoutRequest](docs/AutoLayoutRequest.md)
 - [AutoLayoutRequestCustomBounds](docs/AutoLayoutRequestCustomBounds.md)
 - [AutoOrientRequest](docs/AutoOrientRequest.md)
 - [AutoPackRequest](docs/AutoPackRequest.md)
 - [AutoSupportRequest](docs/AutoSupportRequest.md)
 - [BaseDeviceStatusModel](docs/BaseDeviceStatusModel.md)
 - [BasePrintingDeviceStatusModel](docs/BasePrintingDeviceStatusModel.md)
 - [Default](docs/Default.md)
 - [DentalMode](docs/DentalMode.md)
 - [DeviceStatusModel](docs/DeviceStatusModel.md)
 - [DirectionVectorsModel](docs/DirectionVectorsModel.md)
 - [DiscoverDevices200Response](docs/DiscoverDevices200Response.md)
 - [DiscoverDevicesRequest](docs/DiscoverDevicesRequest.md)
 - [DrainHoleModel](docs/DrainHoleModel.md)
 - [DrainHoleModelDepthMm](docs/DrainHoleModelDepthMm.md)
 - [DuplicateModelRequest](docs/DuplicateModelRequest.md)
 - [ErrorModel](docs/ErrorModel.md)
 - [ErrorModelError](docs/ErrorModelError.md)
 - [EstimatedPrintTimeModel](docs/EstimatedPrintTimeModel.md)
 - [EulerAnglesModel](docs/EulerAnglesModel.md)
 - [FPSFile](docs/FPSFile.md)
 - [FleetControlPrinterGroupDeviceStatusModel](docs/FleetControlPrinterGroupDeviceStatusModel.md)
 - [FleetControlPrinterGroupDeviceStatusModelAllOfPrinters](docs/FleetControlPrinterGroupDeviceStatusModelAllOfPrinters.md)
 - [Form2DeviceStatusModel](docs/Form2DeviceStatusModel.md)
 - [Form3FamilyDeviceStatusModel](docs/Form3FamilyDeviceStatusModel.md)
 - [Form4FamilyDeviceStatusModel](docs/Form4FamilyDeviceStatusModel.md)
 - [Form4FamilyDeviceStatusModelAllOfCartridgeData](docs/Form4FamilyDeviceStatusModelAllOfCartridgeData.md)
 - [Fuse1DeviceStatusModel](docs/Fuse1DeviceStatusModel.md)
 - [GenericDeviceStatusModel](docs/GenericDeviceStatusModel.md)
 - [GetAllOperations200Response](docs/GetAllOperations200Response.md)
 - [GetAllOperations200ResponseOperationsInner](docs/GetAllOperations200ResponseOperationsInner.md)
 - [GetAllScenes200Response](docs/GetAllScenes200Response.md)
 - [GetApiVersion200Response](docs/GetApiVersion200Response.md)
 - [GetDevices200Response](docs/GetDevices200Response.md)
 - [GetOperation200Response](docs/GetOperation200Response.md)
 - [GetSceneInterferencesRequest](docs/GetSceneInterferencesRequest.md)
 - [HollowModel200Response](docs/HollowModel200Response.md)
 - [HollowModel400Response](docs/HollowModel400Response.md)
 - [HollowModelRequest](docs/HollowModelRequest.md)
 - [ImportModelRequest](docs/ImportModelRequest.md)
 - [ImportUnitsModel](docs/ImportUnitsModel.md)
 - [LabelPart400Response](docs/LabelPart400Response.md)
 - [LabelPart400ResponseError](docs/LabelPart400ResponseError.md)
 - [LabelPart400ResponseErrorMessage](docs/LabelPart400ResponseErrorMessage.md)
 - [LabelPartRequest](docs/LabelPartRequest.md)
 - [ListMaterials200Response](docs/ListMaterials200Response.md)
 - [ListMaterials200ResponsePrinterTypesInner](docs/ListMaterials200ResponsePrinterTypesInner.md)
 - [ListMaterials200ResponsePrinterTypesInnerMaterialsInner](docs/ListMaterials200ResponsePrinterTypesInnerMaterialsInner.md)
 - [ListMaterials200ResponsePrinterTypesInnerMaterialsInnerMaterialSettingsInner](docs/ListMaterials200ResponsePrinterTypesInnerMaterialsInnerMaterialSettingsInner.md)
 - [LoadFormFileRequest](docs/LoadFormFileRequest.md)
 - [LockModel](docs/LockModel.md)
 - [LoginRequest](docs/LoginRequest.md)
 - [Manual](docs/Manual.md)
 - [ManualLayerThicknessMm](docs/ManualLayerThicknessMm.md)
 - [MaterialUsageModel](docs/MaterialUsageModel.md)
 - [ModelProperties](docs/ModelProperties.md)
 - [ModelPropertiesBoundingBox](docs/ModelPropertiesBoundingBox.md)
 - [ModelsSelectionModel](docs/ModelsSelectionModel.md)
 - [OperationAcceptedModel](docs/OperationAcceptedModel.md)
 - [OrientationModel](docs/OrientationModel.md)
 - [PackAndCageRequest](docs/PackAndCageRequest.md)
 - [PackingTypeModel](docs/PackingTypeModel.md)
 - [Print200Response](docs/Print200Response.md)
 - [PrintRequest](docs/PrintRequest.md)
 - [PrintValidationResultModel](docs/PrintValidationResultModel.md)
 - [PrintValidationResultModelPerModelResultsValue](docs/PrintValidationResultModelPerModelResultsValue.md)
 - [RepairBehaviorModel](docs/RepairBehaviorModel.md)
 - [ReplaceModel200Response](docs/ReplaceModel200Response.md)
 - [ReplaceModelRequest](docs/ReplaceModelRequest.md)
 - [SLA](docs/SLA.md)
 - [SLAPrinterTypes](docs/SLAPrinterTypes.md)
 - [SLS](docs/SLS.md)
 - [SLSPrinterTypes](docs/SLSPrinterTypes.md)
 - [SaveFpsFileRequest](docs/SaveFpsFileRequest.md)
 - [SaveScreenshotRequest](docs/SaveScreenshotRequest.md)
 - [SaveScreenshotRequestFlyaroundTransform](docs/SaveScreenshotRequestFlyaroundTransform.md)
 - [SaveScreenshotRequestFlyaroundTransformTransformInner](docs/SaveScreenshotRequestFlyaroundTransformTransformInner.md)
 - [ScanToModel200Response](docs/ScanToModel200Response.md)
 - [ScanToModelRequest](docs/ScanToModelRequest.md)
 - [SceneModel](docs/SceneModel.md)
 - [ScenePositionModel](docs/ScenePositionModel.md)
 - [SceneTypeModel](docs/SceneTypeModel.md)
 - [TransformMatrixModel](docs/TransformMatrixModel.md)
 - [UnitsModel](docs/UnitsModel.md)
 - [UpdateModelRequest](docs/UpdateModelRequest.md)
 - [UploadFirmwareRequest](docs/UploadFirmwareRequest.md)
 - [UserInformationModel](docs/UserInformationModel.md)
 - [UsernameAndPassword](docs/UsernameAndPassword.md)
 - [WebAuthTokensModel](docs/WebAuthTokensModel.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization

Endpoints do not require authorization.


## Author




