# coding: utf-8

"""
    Formlabs Local API

    # Introduction The Formlabs Local API is designed for integrations that want to automate job preparation, getting local-network printer status, or sending jobs to Formlabs printers without launching the PreForm graphical user interface. A server application must be installed and run on a user's computer to use this API.  Example use cases: - Scripted job preparation that takes a folder of models, sets up a print,   and uploads it to a printer without user input. - Deep and custom integrations into 3D Modeling and Design software to   prepare print scenes beyond the scope of the PreForm Command Line Arguments.  This API uses RESTful principles. This means the API is organized around resources and collections of resources. Resources and collections are each available at their own URI. You can interact with these resources using standard HTTP Methods on the resource's URI.  Example endpoint: ``` GET http://localhost:44388/scene/ ```  Responses from the API server will be in JSON and are documented throughout the reference docs. This API is described by an [OpenAPI Specification](https://spec.openapis.org/oas/v3.1.0). This interactive documentation is automatically generated from the specification file.  # Technical Overview  ## PreFormServer Background Application All Local API integrations involve starting the PreFormServer background application to expose its HTTP API, then making local HTTP API calls in your own code. This application is like [PreForm](https://formlabs.com/software/preform/), Formlabs' regular job preparation application, but it does not open a graphical window, and interaction is done via HTTP API requests. The PreFormServer application is supported on Windows and MacOS with separate downloads for each Operating System.  ### Installing PreFormServer The PreFormServer application can be downloaded from the [Formlabs API downloads and release notes page](https://support.formlabs.com/s/article/Formlabs-API-downloads-and-release-notes). After downloading, unzip the file and move the application to the desired location on your computer. Any location can be used as the path to the application should be referenced from your integration code.  In the current release, we also recommend adding the PreFormServer application the users' antivirus software exception list or explicitly whitelisting the application in the security settings of MacOS.  On MacOS, you can use the following terminal command to whitelist the PreFormServer application: ``` xattr -r -d com.apple.quarantine PreFormServer.app ```  ### Starting PreFormServer The PreFormServer application can started manually from your Operating System's command prompt or terminal, but most integrations will start the application programatically from integration code. The command line argument `--port` is required to specify the port number the HTTP Server will listen on.  The HTTP API server started by the PreFormServer application cannot immediately respond to requests. When the server is ready to accept requests, it will output `READY FOR INPUT` in the standard output.  For example, running the PreFormServer application on Windows from the command prompt: ``` PreFormServer.exe --port 44388 ``` will output something like the following: ``` starting HTTP server Listening... HTTP server listening on port 44388 READY FOR INPUT ```  ## Making API Requests The code to make HTTP API requests to a running PreFormServer can be written directly in your integration code or by using a generated library that does the API calls. The endpoints and format of the HTTP API are described on this page and in the openapi.yaml file.  Formlabs provides an example [Python library](https://github.com/Formlabs/formlabs-api-python) that handles the setup and request formatting.  ## Glossary - **Scene**: The current state of a job that can be printed on a particular printer model.   This includes both the “Scene Settings” and all of the currently loaded models and their support structures. - **Scene Settings**: Printer type and material information of scene. Describes the   build platform size, the printer capabilities, and what material and print settings   it is set up to be printed with.  ## Stateful Interactions The PreForm Server is stateful in that while it is running, it keeps a cache of the current scene and requests will use the cached scene and possibly modify it. For example, initially a scene may be empty and then if a load model request is made then the cached scene will have one model loaded. Calling the load model requests again will load another copy of the model resulting in two models in the cached scene.  ## Blocking Calls & Asynchronous Requests Unless otherwise stated, API calls are blocking: the HTTP request will not return until the operation has completed.  Some requests like running the auto support action on a scene with many complicated models could take over 1 minute (depending on computer resources). The Server has a timeout of 10 minutes for all requests.  Requests made asynchronously will use the last cached state. For example, if a “get scene” request is made during a “auto support” request that has not finished, then the “get scene” request will return data that will not include the auto support changes.  ## File Paths When saving and loading files, the local API inputs expect full operating system paths to local files on disk.  Correct file path: - `C:\\Projects\\Models\\part.stl`  Incorrect file paths: - `.\\Models\\part.stl` - `%ENV_VAR%\\part.stl` - `part.stl` - `https://filestorage.com/part.stl`  # Errors Conventional HTTP response codes are used to indicate the success or failure of an API request. In general: Codes in the 2xx range indicate success. Codes in the 4xx range indicate an error that failed given the information provided. Codes in the 5xx range indicate an error with Formlabs' servers.  # Security The HTTP Server that PreForm uses to communicate is only exposed to the local network of your computer and not to the public Internet, unless you have configured your computer to expose the port running the PreForm Server to the Internet.  Some requests require an Internet connection, require Dashboard login, and make web requests to perform their action (such as printing to a remote printer). 

    The version of the OpenAPI document: 0.8.3
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from formlabs_local_api.models.fleet_control_printer_group import FleetControlPrinterGroup
from formlabs_local_api.models.form2_printer import Form2Printer
from formlabs_local_api.models.form3_printer import Form3Printer
from formlabs_local_api.models.form4_printer import Form4Printer
from formlabs_local_api.models.fuse11_printer import Fuse11Printer
from formlabs_local_api.models.generic_device import GenericDevice
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

DEVICESTATUSMODEL_ONE_OF_SCHEMAS = ["FleetControlPrinterGroup", "Form2Printer", "Form3Printer", "Form4Printer", "Fuse11Printer", "GenericDevice"]

class DeviceStatusModel(BaseModel):
    """
    DeviceStatusModel
    """
    # data type: GenericDevice
    oneof_schema_1_validator: Optional[GenericDevice] = None
    # data type: FleetControlPrinterGroup
    oneof_schema_2_validator: Optional[FleetControlPrinterGroup] = None
    # data type: Form4Printer
    oneof_schema_3_validator: Optional[Form4Printer] = None
    # data type: Form3Printer
    oneof_schema_4_validator: Optional[Form3Printer] = None
    # data type: Fuse11Printer
    oneof_schema_5_validator: Optional[Fuse11Printer] = None
    # data type: Form2Printer
    oneof_schema_6_validator: Optional[Form2Printer] = None
    actual_instance: Optional[Union[FleetControlPrinterGroup, Form2Printer, Form3Printer, Form4Printer, Fuse11Printer, GenericDevice]] = None
    one_of_schemas: Set[str] = { "FleetControlPrinterGroup", "Form2Printer", "Form3Printer", "Form4Printer", "Fuse11Printer", "GenericDevice" }

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = DeviceStatusModel.model_construct()
        error_messages = []
        match = 0
        # validate data type: GenericDevice
        if not isinstance(v, GenericDevice):
            error_messages.append(f"Error! Input type `{type(v)}` is not `GenericDevice`")
        else:
            match += 1
        # validate data type: FleetControlPrinterGroup
        if not isinstance(v, FleetControlPrinterGroup):
            error_messages.append(f"Error! Input type `{type(v)}` is not `FleetControlPrinterGroup`")
        else:
            match += 1
        # validate data type: Form4Printer
        if not isinstance(v, Form4Printer):
            error_messages.append(f"Error! Input type `{type(v)}` is not `Form4Printer`")
        else:
            match += 1
        # validate data type: Form3Printer
        if not isinstance(v, Form3Printer):
            error_messages.append(f"Error! Input type `{type(v)}` is not `Form3Printer`")
        else:
            match += 1
        # validate data type: Fuse11Printer
        if not isinstance(v, Fuse11Printer):
            error_messages.append(f"Error! Input type `{type(v)}` is not `Fuse11Printer`")
        else:
            match += 1
        # validate data type: Form2Printer
        if not isinstance(v, Form2Printer):
            error_messages.append(f"Error! Input type `{type(v)}` is not `Form2Printer`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in DeviceStatusModel with oneOf schemas: FleetControlPrinterGroup, Form2Printer, Form3Printer, Form4Printer, Fuse11Printer, GenericDevice. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in DeviceStatusModel with oneOf schemas: FleetControlPrinterGroup, Form2Printer, Form3Printer, Form4Printer, Fuse11Printer, GenericDevice. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # deserialize data into GenericDevice
        try:
            instance.actual_instance = GenericDevice.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into FleetControlPrinterGroup
        try:
            instance.actual_instance = FleetControlPrinterGroup.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into Form4Printer
        try:
            instance.actual_instance = Form4Printer.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into Form3Printer
        try:
            instance.actual_instance = Form3Printer.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into Fuse11Printer
        try:
            instance.actual_instance = Fuse11Printer.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into Form2Printer
        try:
            instance.actual_instance = Form2Printer.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into DeviceStatusModel with oneOf schemas: FleetControlPrinterGroup, Form2Printer, Form3Printer, Form4Printer, Fuse11Printer, GenericDevice. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into DeviceStatusModel with oneOf schemas: FleetControlPrinterGroup, Form2Printer, Form3Printer, Form4Printer, Fuse11Printer, GenericDevice. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], FleetControlPrinterGroup, Form2Printer, Form3Printer, Form4Printer, Fuse11Printer, GenericDevice]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


