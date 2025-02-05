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

In the current release, we also recommend adding the PreFormServer application the users' antivirus software exception list or explicitly whitelisting the application in the security settings of MacOS.

On MacOS, you can use the following terminal command to whitelist the PreFormServer application:
```
xattr -r -d com.apple.quarantine PreFormServer.app
```

### Starting PreFormServer
The PreFormServer application can started manually from your Operating System's command prompt or terminal,
but most integrations will start the application programatically from integration code.
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
The PreForm Server is stateful in that while it is running, it keeps a cache of the
current scene and requests will use the cached scene and possibly modify it.
For example, initially a scene may be empty and then if a load model request is made
then the cached scene will have one model loaded. Calling the load model requests
again will load another copy of the model resulting in two models in the cached scene.

## Blocking Calls & Asynchronous Requests
Unless otherwise stated, API calls are blocking: the HTTP request will not return
until the operation has completed.  Some requests like running the auto support
action on a scene with many complicated models could take over 1 minute (depending
on computer resources). The Server has a timeout of 10 minutes for all requests.

Requests made asynchronously will use the last cached state. For example, if a “get scene”
request is made during a “auto support” request that has not finished, then the
“get scene” request will return data that will not include the auto support changes.

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

- API version: 0.8.5
- Package version: 0.8.3
- Generator version: 7.11.0
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
*ExportingApi* | [**save_form_file**](docs/ExportingApi.md#save_form_file) | **POST** /scene/save-form/ | Save .form file
*ExportingApi* | [**save_fps_file**](docs/ExportingApi.md#save_fps_file) | **POST** /scene/save-fps-file/ | Save FPS file
*ExportingApi* | [**save_screenshot**](docs/ExportingApi.md#save_screenshot) | **POST** /scene/save-screenshot/ | Save screenshot file
*GettingSceneInformationApi* | [**estimate_print_time**](docs/GettingSceneInformationApi.md#estimate_print_time) | **POST** /scene/estimate-print-time/ | Estimate Print Time
*GettingSceneInformationApi* | [**get_model**](docs/GettingSceneInformationApi.md#get_model) | **GET** /scene/models/{id}/ | Get model
*GettingSceneInformationApi* | [**get_print_validation**](docs/GettingSceneInformationApi.md#get_print_validation) | **GET** /scene/print-validation/ | Get Print Validation
*GettingSceneInformationApi* | [**get_scene**](docs/GettingSceneInformationApi.md#get_scene) | **GET** /scene/ | Get Scene
*ModifyingASceneApi* | [**auto_layout**](docs/ModifyingASceneApi.md#auto_layout) | **POST** /scene/auto-layout/ | Auto Layout
*ModifyingASceneApi* | [**auto_orient**](docs/ModifyingASceneApi.md#auto_orient) | **POST** /scene/auto-orient/ | Auto Orient
*ModifyingASceneApi* | [**auto_pack**](docs/ModifyingASceneApi.md#auto_pack) | **POST** /scene/auto-pack/ | Auto Pack
*ModifyingASceneApi* | [**auto_support**](docs/ModifyingASceneApi.md#auto_support) | **POST** /scene/auto-support/ | Auto Support
*ModifyingASceneApi* | [**create_scene**](docs/ModifyingASceneApi.md#create_scene) | **POST** /scene/ | Create Scene
*ModifyingASceneApi* | [**delete_model**](docs/ModifyingASceneApi.md#delete_model) | **DELETE** /scene/models/{id}/ | Delete model
*ModifyingASceneApi* | [**duplicate_model**](docs/ModifyingASceneApi.md#duplicate_model) | **POST** /scene/models/{id}/duplicate/ | Duplicate model
*ModifyingASceneApi* | [**import_model**](docs/ModifyingASceneApi.md#import_model) | **POST** /scene/import-model/ | Import model
*ModifyingASceneApi* | [**load_form_file**](docs/ModifyingASceneApi.md#load_form_file) | **POST** /load-form/ | Load .form file
*ModifyingASceneApi* | [**replace_model**](docs/ModifyingASceneApi.md#replace_model) | **POST** /scene/models/{id}/replace/ | Replace model
*ModifyingASceneApi* | [**update_model**](docs/ModifyingASceneApi.md#update_model) | **POST** /scene/models/{id}/ | Update model
*ModifyingASceneApi* | [**update_scene**](docs/ModifyingASceneApi.md#update_scene) | **PUT** /scene/ | Update Scene
*OperationsApi* | [**call_print**](docs/OperationsApi.md#call_print) | **POST** /scene/print/ | Print
*OperationsApi* | [**get_all_operations**](docs/OperationsApi.md#get_all_operations) | **GET** /operations/ | List All Operations
*OperationsApi* | [**get_operation**](docs/OperationsApi.md#get_operation) | **GET** /operations/{id}/ | Get Operation Status
*PrintSettingsApi* | [**list_materials**](docs/PrintSettingsApi.md#list_materials) | **GET** /list-materials/ | List Materials
*PrintingApi* | [**call_print**](docs/PrintingApi.md#call_print) | **POST** /scene/print/ | Print
*RemoteAccessApi* | [**call_print**](docs/RemoteAccessApi.md#call_print) | **POST** /scene/print/ | Print
*RemoteAccessApi* | [**discover_devices**](docs/RemoteAccessApi.md#discover_devices) | **POST** /discover-devices/ | Discover Devices
*RemoteAccessApi* | [**get_device**](docs/RemoteAccessApi.md#get_device) | **GET** /devices/{id}/ | Get Device
*RemoteAccessApi* | [**get_devices**](docs/RemoteAccessApi.md#get_devices) | **GET** /devices/ | Get Devices
*RemoteAccessApi* | [**login**](docs/RemoteAccessApi.md#login) | **POST** /login/ | Login


## Documentation For Models

 - [AccessToken](docs/AccessToken.md)
 - [AutoLayoutRequest](docs/AutoLayoutRequest.md)
 - [AutoOrientRequest](docs/AutoOrientRequest.md)
 - [AutoPackRequest](docs/AutoPackRequest.md)
 - [AutoSupportRequest](docs/AutoSupportRequest.md)
 - [Default](docs/Default.md)
 - [DentalMode](docs/DentalMode.md)
 - [DeviceStatusModel](docs/DeviceStatusModel.md)
 - [DirectionVectorsModel](docs/DirectionVectorsModel.md)
 - [DiscoverDevices200Response](docs/DiscoverDevices200Response.md)
 - [DiscoverDevicesRequest](docs/DiscoverDevicesRequest.md)
 - [DuplicateModelRequest](docs/DuplicateModelRequest.md)
 - [ErrorModel](docs/ErrorModel.md)
 - [ErrorModelError](docs/ErrorModelError.md)
 - [EstimatedPrintTimeModel](docs/EstimatedPrintTimeModel.md)
 - [EulerAnglesModel](docs/EulerAnglesModel.md)
 - [FPSFile](docs/FPSFile.md)
 - [FleetControlPrinterGroup](docs/FleetControlPrinterGroup.md)
 - [Form2Printer](docs/Form2Printer.md)
 - [Form3Printer](docs/Form3Printer.md)
 - [Form4Printer](docs/Form4Printer.md)
 - [Form4PrinterCartridgeDataValue](docs/Form4PrinterCartridgeDataValue.md)
 - [Fuse11Printer](docs/Fuse11Printer.md)
 - [GenericDevice](docs/GenericDevice.md)
 - [GetAllOperations200Response](docs/GetAllOperations200Response.md)
 - [GetAllOperations200ResponseOperationsInner](docs/GetAllOperations200ResponseOperationsInner.md)
 - [GetApiVersion200Response](docs/GetApiVersion200Response.md)
 - [GetDevices200Response](docs/GetDevices200Response.md)
 - [GetOperation200Response](docs/GetOperation200Response.md)
 - [ImportModelRequest](docs/ImportModelRequest.md)
 - [ImportUnitsModel](docs/ImportUnitsModel.md)
 - [ListMaterials200Response](docs/ListMaterials200Response.md)
 - [ListMaterials200ResponsePrinterTypesInner](docs/ListMaterials200ResponsePrinterTypesInner.md)
 - [ListMaterials200ResponsePrinterTypesInnerMaterialsInner](docs/ListMaterials200ResponsePrinterTypesInnerMaterialsInner.md)
 - [ListMaterials200ResponsePrinterTypesInnerMaterialsInnerMaterialSettingsInner](docs/ListMaterials200ResponsePrinterTypesInnerMaterialsInnerMaterialSettingsInner.md)
 - [LoadFormFileRequest](docs/LoadFormFileRequest.md)
 - [LoginRequest](docs/LoginRequest.md)
 - [Manual](docs/Manual.md)
 - [ManualLayerThicknessMm](docs/ManualLayerThicknessMm.md)
 - [MaterialUsageModel](docs/MaterialUsageModel.md)
 - [ModelProperties](docs/ModelProperties.md)
 - [ModelPropertiesBoundingBox](docs/ModelPropertiesBoundingBox.md)
 - [ModelsSelectionModel](docs/ModelsSelectionModel.md)
 - [OrientationModel](docs/OrientationModel.md)
 - [Print200Response](docs/Print200Response.md)
 - [PrintRequest](docs/PrintRequest.md)
 - [PrintValidationResultModel](docs/PrintValidationResultModel.md)
 - [PrintValidationResultModelPerModelResultsValue](docs/PrintValidationResultModelPerModelResultsValue.md)
 - [RepairBehaviorModel](docs/RepairBehaviorModel.md)
 - [ReplaceModel200Response](docs/ReplaceModel200Response.md)
 - [ReplaceModelRequest](docs/ReplaceModelRequest.md)
 - [SLA](docs/SLA.md)
 - [SLS](docs/SLS.md)
 - [SaveFpsFileRequest](docs/SaveFpsFileRequest.md)
 - [SaveScreenshotRequest](docs/SaveScreenshotRequest.md)
 - [SceneModel](docs/SceneModel.md)
 - [ScenePositionModel](docs/ScenePositionModel.md)
 - [SceneTypeModel](docs/SceneTypeModel.md)
 - [TransformMatrixModel](docs/TransformMatrixModel.md)
 - [UnitsModel](docs/UnitsModel.md)
 - [UpdateModelRequest](docs/UpdateModelRequest.md)
 - [UsernameAndPassword](docs/UsernameAndPassword.md)
 - [WebAuthTokensModel](docs/WebAuthTokensModel.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization

Endpoints do not require authorization.


## Author




