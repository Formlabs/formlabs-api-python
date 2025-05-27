# coding: utf-8

# flake8: noqa

"""
    Formlabs Local API

    # Introduction The Formlabs Local API is designed for integrations that want to automate job preparation, getting local-network printer status, or sending jobs to Formlabs printers without launching the PreForm graphical user interface. A server application must be installed and run on a user's computer to use this API.  Example use cases: - Scripted job preparation that takes a folder of models, sets up a print,   and uploads it to a printer without user input. - Deep and custom integrations into 3D Modeling and Design software to   prepare print scenes beyond the scope of the PreForm Command Line Arguments.  This API uses RESTful principles. This means the API is organized around resources and collections of resources. Resources and collections are each available at their own URI. You can interact with these resources using standard HTTP Methods on the resource's URI.  Example endpoint: ``` GET http://localhost:44388/scene/ ```  Responses from the API server will be in JSON and are documented throughout the reference docs. This API is described by an [OpenAPI Specification](https://spec.openapis.org/oas/v3.1.0). This interactive documentation is automatically generated from the specification file.  # Technical Overview  ## PreFormServer Background Application All Local API integrations involve starting the PreFormServer background application to expose its HTTP API, then making local HTTP API calls in your own code. This application is like [PreForm](https://formlabs.com/software/preform/), Formlabs' regular job preparation application, but it does not open a graphical window, and interaction is done via HTTP API requests. The PreFormServer application is supported on Windows and MacOS with separate downloads for each Operating System.  ### Installing PreFormServer The PreFormServer application can be downloaded from the [Formlabs API downloads and release notes page](https://support.formlabs.com/s/article/Formlabs-API-downloads-and-release-notes). After downloading, unzip the file and move the application to the desired location on your computer. Any location can be used as the path to the application should be referenced from your integration code.  ### Starting PreFormServer The PreFormServer application can started manually from your Operating System's command prompt or terminal, but most integrations will start the application programmatically from integration code. The command line argument `--port` is required to specify the port number the HTTP Server will listen on.  The HTTP API server started by the PreFormServer application cannot immediately respond to requests. When the server is ready to accept requests, it will output `READY FOR INPUT` in the standard output.  For example, running the PreFormServer application on Windows from the command prompt: ``` PreFormServer.exe --port 44388 ``` will output something like the following: ``` starting HTTP server Listening... HTTP server listening on port 44388 READY FOR INPUT ```  ## Making API Requests The code to make HTTP API requests to a running PreFormServer can be written directly in your integration code or by using a generated library that does the API calls. The endpoints and format of the HTTP API are described on this page and in the openapi.yaml file.  Formlabs provides an example [Python library](https://github.com/Formlabs/formlabs-api-python) that handles the setup and request formatting.  ## Glossary - **Scene**: The current state of a job that can be printed on a particular printer model.   This includes both the “Scene Settings” and all of the currently loaded models and their support structures. - **Scene Settings**: Printer type and material information of scene. Describes the   build platform size, the printer capabilities, and what material and print settings   it is set up to be printed with.  ## Stateful Interactions The PreForm Server is stateful in that while it is running, it keeps a cache of scenes. By default, it caches 100 scenes in memory, with unlimited scenes stored on disk, though this may be changed with the `--scene-cache-size` parameter. Scenes are identified by their IDs, returned from the `/scene/` endpoint. `/scene/` endpoints also accept a scene ID of \"default\", which will use a single global scene. Endpoints with no scene id provided (e.g. `/scene/auto-layout/`) are deprecated. They will use the most recently created scene, and possibly modify it. All other `/scene/` requests will use the user specified scene, and possibly modify it. For example, initially a scene may be empty and then if a load model request is made then the cached scene will have one model loaded. Calling the load model endpoint again will load another copy of the model resulting in two models in the cached scene.  ## Blocking Calls & Asynchronous Requests Unless otherwise stated, API calls are blocking: the HTTP request will not return until the operation has completed.  Some requests like running the auto support action on a scene with many complicated models could take over 1 minute (depending on computer resources). The Server has a timeout of 10 minutes for all requests.  Some long-running operations can be called asynchronously by adding `?async=true` to the request. These requests will return immediately and the operation will be tracked separately. The caller can poll for completion using the `/operations/{operation_id}/` endpoint, and track the percentage progress of the outstanding operation.  Requests involving the scene will always use the scene state at the time the request was made, without any partially completed operations. For example, if a “get scene” request is made during a “auto support” request that has not finished, then the “get scene” request will return data that will not include the auto support changes.  Multiple requests editing the same scene should NOT be made in parallel. If an \"auto layout\" request is made during an \"auto support\" request that has not finished, whichever operation finishes last will \"win\": either an auto-layout of unsupported models or the original layout with supports. PreformServer currently gives no warning when this happens.  ## File Paths When saving and loading files, the local API inputs expect full operating system paths to local files on disk.  Correct file path: - `C:\\Projects\\Models\\part.stl`  Incorrect file paths: - `.\\Models\\part.stl` - `%ENV_VAR%\\part.stl` - `part.stl` - `https://filestorage.com/part.stl`  # Errors Conventional HTTP response codes are used to indicate the success or failure of an API request. In general: Codes in the 2xx range indicate success. Codes in the 4xx range indicate an error that failed given the information provided. Codes in the 5xx range indicate an error with Formlabs' servers.  # Security The HTTP Server that PreForm uses to communicate is only exposed to the local network of your computer and not to the public Internet, unless you have configured your computer to expose the port running the PreForm Server to the Internet.  Some requests require an Internet connection, require Dashboard login, and make web requests to perform their action (such as printing to a remote printer). 

    The version of the OpenAPI document: 0.9.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


__version__ = "0.9.0"

# import apis into sdk package
from formlabs_local_api.api.api_info_api import APIInfoApi
from formlabs_local_api.api.devices_api import DevicesApi
from formlabs_local_api.api.exporting_api import ExportingApi
from formlabs_local_api.api.exporting_deprecated_api import ExportingDeprecatedApi
from formlabs_local_api.api.getting_scene_information_api import GettingSceneInformationApi
from formlabs_local_api.api.getting_scene_information_deprecated_api import GettingSceneInformationDeprecatedApi
from formlabs_local_api.api.modifying_a_scene_api import ModifyingASceneApi
from formlabs_local_api.api.modifying_a_scene_deprecated_api import ModifyingASceneDeprecatedApi
from formlabs_local_api.api.operations_api import OperationsApi
from formlabs_local_api.api.operations_deprecated_api import OperationsDeprecatedApi
from formlabs_local_api.api.print_settings_api import PrintSettingsApi
from formlabs_local_api.api.printing_api import PrintingApi
from formlabs_local_api.api.printing_deprecated_api import PrintingDeprecatedApi
from formlabs_local_api.api.remote_access_api import RemoteAccessApi
from formlabs_local_api.api.remote_access_deprecated_api import RemoteAccessDeprecatedApi


# Hack added by Formlabs to have one class containing all API calls, even when openapi tags are used
class UnifiedApi(
    APIInfoApi,
    DevicesApi,
    ExportingApi,
    ExportingDeprecatedApi,
    GettingSceneInformationApi,
    GettingSceneInformationDeprecatedApi,
    ModifyingASceneApi,
    ModifyingASceneDeprecatedApi,
    OperationsApi,
    OperationsDeprecatedApi,
    PrintSettingsApi,
    PrintingApi,
    PrintingDeprecatedApi,
    RemoteAccessApi,
    RemoteAccessDeprecatedApi,
):
    def __init__(self, api_client) -> None:
        self.api_client = api_client


# import ApiClient
from formlabs_local_api.api_response import ApiResponse
from formlabs_local_api.api_client import ApiClient
from formlabs_local_api.configuration import Configuration
from formlabs_local_api.exceptions import OpenApiException
from formlabs_local_api.exceptions import ApiTypeError
from formlabs_local_api.exceptions import ApiValueError
from formlabs_local_api.exceptions import ApiKeyError
from formlabs_local_api.exceptions import ApiAttributeError
from formlabs_local_api.exceptions import ApiException

# import models into sdk package
from formlabs_local_api.models.access_token import AccessToken
from formlabs_local_api.models.add_drain_holes200_response import AddDrainHoles200Response
from formlabs_local_api.models.add_drain_holes_request import AddDrainHolesRequest
from formlabs_local_api.models.auto_layout_request import AutoLayoutRequest
from formlabs_local_api.models.auto_layout_request_custom_bounds import AutoLayoutRequestCustomBounds
from formlabs_local_api.models.auto_orient_request import AutoOrientRequest
from formlabs_local_api.models.auto_pack_request import AutoPackRequest
from formlabs_local_api.models.auto_support_request import AutoSupportRequest
from formlabs_local_api.models.base_device_status_model import BaseDeviceStatusModel
from formlabs_local_api.models.base_printing_device_status_model import BasePrintingDeviceStatusModel
from formlabs_local_api.models.default import Default
from formlabs_local_api.models.dental_mode import DentalMode
from formlabs_local_api.models.device_status_model import DeviceStatusModel
from formlabs_local_api.models.direction_vectors_model import DirectionVectorsModel
from formlabs_local_api.models.discover_devices200_response import DiscoverDevices200Response
from formlabs_local_api.models.discover_devices_request import DiscoverDevicesRequest
from formlabs_local_api.models.drain_hole_model import DrainHoleModel
from formlabs_local_api.models.drain_hole_model_depth_mm import DrainHoleModelDepthMm
from formlabs_local_api.models.duplicate_model_request import DuplicateModelRequest
from formlabs_local_api.models.error_model import ErrorModel
from formlabs_local_api.models.error_model_error import ErrorModelError
from formlabs_local_api.models.estimated_print_time_model import EstimatedPrintTimeModel
from formlabs_local_api.models.euler_angles_model import EulerAnglesModel
from formlabs_local_api.models.fps_file import FPSFile
from formlabs_local_api.models.fleet_control_printer_group_device_status_model import FleetControlPrinterGroupDeviceStatusModel
from formlabs_local_api.models.fleet_control_printer_group_device_status_model_all_of_printers import FleetControlPrinterGroupDeviceStatusModelAllOfPrinters
from formlabs_local_api.models.form2_device_status_model import Form2DeviceStatusModel
from formlabs_local_api.models.form3_family_device_status_model import Form3FamilyDeviceStatusModel
from formlabs_local_api.models.form4_family_device_status_model import Form4FamilyDeviceStatusModel
from formlabs_local_api.models.form4_family_device_status_model_all_of_cartridge_data import Form4FamilyDeviceStatusModelAllOfCartridgeData
from formlabs_local_api.models.fuse1_device_status_model import Fuse1DeviceStatusModel
from formlabs_local_api.models.generic_device_status_model import GenericDeviceStatusModel
from formlabs_local_api.models.get_all_operations200_response import GetAllOperations200Response
from formlabs_local_api.models.get_all_operations200_response_operations_inner import GetAllOperations200ResponseOperationsInner
from formlabs_local_api.models.get_all_scenes200_response import GetAllScenes200Response
from formlabs_local_api.models.get_api_version200_response import GetApiVersion200Response
from formlabs_local_api.models.get_devices200_response import GetDevices200Response
from formlabs_local_api.models.get_operation200_response import GetOperation200Response
from formlabs_local_api.models.get_scene_interferences_request import GetSceneInterferencesRequest
from formlabs_local_api.models.hollow_model200_response import HollowModel200Response
from formlabs_local_api.models.hollow_model400_response import HollowModel400Response
from formlabs_local_api.models.hollow_model_request import HollowModelRequest
from formlabs_local_api.models.import_model_request import ImportModelRequest
from formlabs_local_api.models.import_units_model import ImportUnitsModel
from formlabs_local_api.models.label_part400_response import LabelPart400Response
from formlabs_local_api.models.label_part400_response_error import LabelPart400ResponseError
from formlabs_local_api.models.label_part400_response_error_message import LabelPart400ResponseErrorMessage
from formlabs_local_api.models.label_part_request import LabelPartRequest
from formlabs_local_api.models.list_materials200_response import ListMaterials200Response
from formlabs_local_api.models.list_materials200_response_printer_types_inner import ListMaterials200ResponsePrinterTypesInner
from formlabs_local_api.models.list_materials200_response_printer_types_inner_materials_inner import ListMaterials200ResponsePrinterTypesInnerMaterialsInner
from formlabs_local_api.models.list_materials200_response_printer_types_inner_materials_inner_material_settings_inner import ListMaterials200ResponsePrinterTypesInnerMaterialsInnerMaterialSettingsInner
from formlabs_local_api.models.load_form_file_request import LoadFormFileRequest
from formlabs_local_api.models.lock_model import LockModel
from formlabs_local_api.models.login_request import LoginRequest
from formlabs_local_api.models.manual import Manual
from formlabs_local_api.models.manual_layer_thickness_mm import ManualLayerThicknessMm
from formlabs_local_api.models.material_usage_model import MaterialUsageModel
from formlabs_local_api.models.model_properties import ModelProperties
from formlabs_local_api.models.model_properties_bounding_box import ModelPropertiesBoundingBox
from formlabs_local_api.models.models_selection_model import ModelsSelectionModel
from formlabs_local_api.models.operation_accepted_model import OperationAcceptedModel
from formlabs_local_api.models.orientation_model import OrientationModel
from formlabs_local_api.models.pack_and_cage_request import PackAndCageRequest
from formlabs_local_api.models.packing_type_model import PackingTypeModel
from formlabs_local_api.models.print200_response import Print200Response
from formlabs_local_api.models.print_request import PrintRequest
from formlabs_local_api.models.print_validation_result_model import PrintValidationResultModel
from formlabs_local_api.models.print_validation_result_model_per_model_results_value import PrintValidationResultModelPerModelResultsValue
from formlabs_local_api.models.repair_behavior_model import RepairBehaviorModel
from formlabs_local_api.models.replace_model200_response import ReplaceModel200Response
from formlabs_local_api.models.replace_model_request import ReplaceModelRequest
from formlabs_local_api.models.sla import SLA
from formlabs_local_api.models.sla_printer_types import SLAPrinterTypes
from formlabs_local_api.models.sls import SLS
from formlabs_local_api.models.sls_printer_types import SLSPrinterTypes
from formlabs_local_api.models.save_fps_file_request import SaveFpsFileRequest
from formlabs_local_api.models.save_screenshot_request import SaveScreenshotRequest
from formlabs_local_api.models.save_screenshot_request_flyaround_transform import SaveScreenshotRequestFlyaroundTransform
from formlabs_local_api.models.save_screenshot_request_flyaround_transform_transform_inner import SaveScreenshotRequestFlyaroundTransformTransformInner
from formlabs_local_api.models.scan_to_model200_response import ScanToModel200Response
from formlabs_local_api.models.scan_to_model_request import ScanToModelRequest
from formlabs_local_api.models.scene_model import SceneModel
from formlabs_local_api.models.scene_position_model import ScenePositionModel
from formlabs_local_api.models.scene_type_model import SceneTypeModel
from formlabs_local_api.models.transform_matrix_model import TransformMatrixModel
from formlabs_local_api.models.units_model import UnitsModel
from formlabs_local_api.models.update_model_request import UpdateModelRequest
from formlabs_local_api.models.upload_firmware_request import UploadFirmwareRequest
from formlabs_local_api.models.user_information_model import UserInformationModel
from formlabs_local_api.models.username_and_password import UsernameAndPassword
from formlabs_local_api.models.web_auth_tokens_model import WebAuthTokensModel

# START SECTION OF CODE ADDED BY FORMLABS
from formlabs_local_api.PreFormApi import PreFormApi