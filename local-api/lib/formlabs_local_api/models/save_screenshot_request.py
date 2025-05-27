# coding: utf-8

"""
    Formlabs Local API

    # Introduction The Formlabs Local API is designed for integrations that want to automate job preparation, getting local-network printer status, or sending jobs to Formlabs printers without launching the PreForm graphical user interface. A server application must be installed and run on a user's computer to use this API.  Example use cases: - Scripted job preparation that takes a folder of models, sets up a print,   and uploads it to a printer without user input. - Deep and custom integrations into 3D Modeling and Design software to   prepare print scenes beyond the scope of the PreForm Command Line Arguments.  This API uses RESTful principles. This means the API is organized around resources and collections of resources. Resources and collections are each available at their own URI. You can interact with these resources using standard HTTP Methods on the resource's URI.  Example endpoint: ``` GET http://localhost:44388/scene/ ```  Responses from the API server will be in JSON and are documented throughout the reference docs. This API is described by an [OpenAPI Specification](https://spec.openapis.org/oas/v3.1.0). This interactive documentation is automatically generated from the specification file.  # Technical Overview  ## PreFormServer Background Application All Local API integrations involve starting the PreFormServer background application to expose its HTTP API, then making local HTTP API calls in your own code. This application is like [PreForm](https://formlabs.com/software/preform/), Formlabs' regular job preparation application, but it does not open a graphical window, and interaction is done via HTTP API requests. The PreFormServer application is supported on Windows and MacOS with separate downloads for each Operating System.  ### Installing PreFormServer The PreFormServer application can be downloaded from the [Formlabs API downloads and release notes page](https://support.formlabs.com/s/article/Formlabs-API-downloads-and-release-notes). After downloading, unzip the file and move the application to the desired location on your computer. Any location can be used as the path to the application should be referenced from your integration code.  ### Starting PreFormServer The PreFormServer application can started manually from your Operating System's command prompt or terminal, but most integrations will start the application programmatically from integration code. The command line argument `--port` is required to specify the port number the HTTP Server will listen on.  The HTTP API server started by the PreFormServer application cannot immediately respond to requests. When the server is ready to accept requests, it will output `READY FOR INPUT` in the standard output.  For example, running the PreFormServer application on Windows from the command prompt: ``` PreFormServer.exe --port 44388 ``` will output something like the following: ``` starting HTTP server Listening... HTTP server listening on port 44388 READY FOR INPUT ```  ## Making API Requests The code to make HTTP API requests to a running PreFormServer can be written directly in your integration code or by using a generated library that does the API calls. The endpoints and format of the HTTP API are described on this page and in the openapi.yaml file.  Formlabs provides an example [Python library](https://github.com/Formlabs/formlabs-api-python) that handles the setup and request formatting.  ## Glossary - **Scene**: The current state of a job that can be printed on a particular printer model.   This includes both the “Scene Settings” and all of the currently loaded models and their support structures. - **Scene Settings**: Printer type and material information of scene. Describes the   build platform size, the printer capabilities, and what material and print settings   it is set up to be printed with.  ## Stateful Interactions The PreForm Server is stateful in that while it is running, it keeps a cache of scenes. By default, it caches 100 scenes in memory, with unlimited scenes stored on disk, though this may be changed with the `--scene-cache-size` parameter. Scenes are identified by their IDs, returned from the `/scene/` endpoint. `/scene/` endpoints also accept a scene ID of \"default\", which will use a single global scene. Endpoints with no scene id provided (e.g. `/scene/auto-layout/`) are deprecated. They will use the most recently created scene, and possibly modify it. All other `/scene/` requests will use the user specified scene, and possibly modify it. For example, initially a scene may be empty and then if a load model request is made then the cached scene will have one model loaded. Calling the load model endpoint again will load another copy of the model resulting in two models in the cached scene.  ## Blocking Calls & Asynchronous Requests Unless otherwise stated, API calls are blocking: the HTTP request will not return until the operation has completed.  Some requests like running the auto support action on a scene with many complicated models could take over 1 minute (depending on computer resources). The Server has a timeout of 10 minutes for all requests.  Some long-running operations can be called asynchronously by adding `?async=true` to the request. These requests will return immediately and the operation will be tracked separately. The caller can poll for completion using the `/operations/{operation_id}/` endpoint, and track the percentage progress of the outstanding operation.  Requests involving the scene will always use the scene state at the time the request was made, without any partially completed operations. For example, if a “get scene” request is made during a “auto support” request that has not finished, then the “get scene” request will return data that will not include the auto support changes.  Multiple requests editing the same scene should NOT be made in parallel. If an \"auto layout\" request is made during an \"auto support\" request that has not finished, whichever operation finishes last will \"win\": either an auto-layout of unsupported models or the original layout with supports. PreformServer currently gives no warning when this happens.  ## File Paths When saving and loading files, the local API inputs expect full operating system paths to local files on disk.  Correct file path: - `C:\\Projects\\Models\\part.stl`  Incorrect file paths: - `.\\Models\\part.stl` - `%ENV_VAR%\\part.stl` - `part.stl` - `https://filestorage.com/part.stl`  # Errors Conventional HTTP response codes are used to indicate the success or failure of an API request. In general: Codes in the 2xx range indicate success. Codes in the 4xx range indicate an error that failed given the information provided. Codes in the 5xx range indicate an error with Formlabs' servers.  # Security The HTTP Server that PreForm uses to communicate is only exposed to the local network of your computer and not to the public Internet, unless you have configured your computer to expose the port running the PreForm Server to the Internet.  Some requests require an Internet connection, require Dashboard login, and make web requests to perform their action (such as printing to a remote printer). 

    The version of the OpenAPI document: 0.9.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from formlabs_local_api.models.models_selection_model import ModelsSelectionModel
from formlabs_local_api.models.save_screenshot_request_flyaround_transform import SaveScreenshotRequestFlyaroundTransform
from typing import Optional, Set
from typing_extensions import Self

class SaveScreenshotRequest(BaseModel):
    """
    SaveScreenshotRequest
    """ # noqa: E501
    file: Annotated[str, Field(strict=True)] = Field(description="The file path to save the .png/.webp screenshot or .webp flyaround to")
    view_type: Optional[StrictStr] = Field(default='ZOOM_ON_MODELS', description="The type of view to use when taking the screenshot")
    yaw: Optional[Union[StrictFloat, StrictInt]] = Field(default=45.0, description="Yaw rotation in degrees for the camera's view, where 0º looks down the negative X-axis")
    pitch: Optional[Union[StrictFloat, StrictInt]] = Field(default=35.264, description="Pitch rotation in degrees for the camera's view, where 0º looks flat from the horizon and positive angles look down on models (in SLA scenes, toward the build platform)")
    image_size_px: Optional[StrictInt] = Field(default=820, description="Size of the largest dimension of the exported image in pixels.")
    crop_to_models: Optional[StrictBool] = Field(default=True, description="If the screenshot view should be sized and cropped so the models take up most of the frame. If false, the zooming will be the same for all viewing angles.")
    models: Optional[ModelsSelectionModel] = None
    flyaround_transform: Optional[SaveScreenshotRequestFlyaroundTransform] = None
    __properties: ClassVar[List[str]] = ["file", "view_type", "yaw", "pitch", "image_size_px", "crop_to_models", "models", "flyaround_transform"]

    @field_validator('file')
    def file_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^.*\.(png|webp)$", value):
            raise ValueError(r"must validate the regular expression /^.*\.(png|webp)$/")
        return value

    @field_validator('view_type')
    def view_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['ZOOM_ON_MODELS', 'FULL_BUILD_VOLUME', 'FULL_PLATFORM_WIDTH']):
            raise ValueError("must be one of enum values ('ZOOM_ON_MODELS', 'FULL_BUILD_VOLUME', 'FULL_PLATFORM_WIDTH')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of SaveScreenshotRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of models
        if self.models:
            _dict['models'] = self.models.to_dict()
        # override the default output from pydantic by calling `to_dict()` of flyaround_transform
        if self.flyaround_transform:
            _dict['flyaround_transform'] = self.flyaround_transform.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SaveScreenshotRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "file": obj.get("file"),
            "view_type": obj.get("view_type") if obj.get("view_type") is not None else 'ZOOM_ON_MODELS',
            "yaw": obj.get("yaw") if obj.get("yaw") is not None else 45.0,
            "pitch": obj.get("pitch") if obj.get("pitch") is not None else 35.264,
            "image_size_px": obj.get("image_size_px") if obj.get("image_size_px") is not None else 820,
            "crop_to_models": obj.get("crop_to_models") if obj.get("crop_to_models") is not None else True,
            "models": ModelsSelectionModel.from_dict(obj["models"]) if obj.get("models") is not None else None,
            "flyaround_transform": SaveScreenshotRequestFlyaroundTransform.from_dict(obj["flyaround_transform"]) if obj.get("flyaround_transform") is not None else None
        })
        return _obj


