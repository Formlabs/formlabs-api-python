# coding: utf-8

"""
    Formlabs Web API

     # Introduction  The Formlabs Web API provides access to Formlabs’ remote control and remote monitoring features for Internet-connected Formlabs products registered to your Dashboard account.  Some example use cases of the Dashboard Developer API: 1.  Create automated custom reports on Printer usage, material usage, and job history to gain more insights into print production 2.  More efficiently manage Printers by integrating Printer status data into existing systems (ERP/MES/custom) # Terms and Conditions -   Formlabs reserves the right to revoke or invalidate your API key at any time without warning. -   As a beta, conditions of access to the API may change in the future, access may be bundled into other future software products, etc. (we will make an effort to provide as much warning as possible) -   As a beta, the API may change at any time without warning in such a way that it may fail to support existing workflows (though we will make an effort to provide advanced notice where possible) -   You agree not to exceed the Dashboard Developer API rate limit as detailed in the \"Rate Limit\" section below. -   You will be given access to certain non-public information, software, and specifications that are confidential and proprietary to Formlabs. You will not share these outside your organization. -   By participating in this Beta you may be sharing information with Formlabs. Any information shared is governed by our Privacy Policy [https://formlabs.com/support/privacy-policy/](https://formlabs.com/support/privacy-policy/) -   The Dashboard Developer API works with Formlabs Printers that are connected to the internet and registered to Dashboard. Printers registered to Dashboard share data with Formlabs (detailed in the Data Collection section of the Privacy Policy: [https://formlabs.com/support/privacy-policy/#Data-Collection](https://formlabs.com/support/privacy-policy/#Data-Collection)). For more information about how to set up Printers and register them to Dashboard, see this link: [https://support.formlabs.com/s/article/Dashboard-Overview-and-Setup](https://support.formlabs.com/s/article/Dashboard-Overview-and-Setup)  # Technical Overview The Formlabs Dashboard Developer API is a REST HTTP API using JSON as the response data format.   Formlabs Dashboard Developer API is HTTP-based. Send a HTTP GET request to an endpoint to retrieve data from that endpoint. The integrating system should be able to make HTTP requests and process responses in JSON format.   Formlabs Dashboard Developer API uses the standard [OAuth Authentication Flow](https://tools.ietf.org/html/rfc6749#section-4.4), and all API endpoints require authentication. The access token created is valid for a day, so make sure to refresh the token regularly to maintain seamless integration with the Dashboard Developer API and ensure uninterrupted workflow.  ## Versioning  The Dashboard Developer API uses resource-based versioning, meaning API endpoints are versioned independently, rather than globally across all endpoints.  Formlabs may change the version of an endpoint to first keep in sync with product updates (could be an addition or a removal of data), in addition to any changes based on customer feedback to allow easier integrations.  Versioning can occur in the following situations:  -   The format of the response data is required to change -   The format of the response type is required to change  Any outstanding version changes or upgrades occurred on endpoints will be highlighted and documented.  ## Rate Limit  The rate of requests to the Dashboard Developer API is limited to prevent the abuse of the system. Requests from the same IP address are limited to **100 requests/second**. Requests from the same authenticated user are limited to **1500 requests/hour**. After a rate limit is exceeded, requests will return a HTTP status code of 429 with a “Retry-after” header outlining when the next request can be made.  ## Account Setup & Printer Registration  The Dashboard Developer API is only available to Formlabs.com account-holding users that are registered and have active Formlabs 3D Printer(s) associated with their accounts. If you do not have a Formlabs.com account, or you have an account but don’t have your Printers connected to it, please follow the instructions below:  1.  Sign up for a Formlabs.com account at [https://formlabs.com/dashboard/#register](https://formlabs.com/dashboard/#register) 2.  Register the Formlabs 3D Printers at [https://formlabs.com/dashboard/#setup](https://formlabs.com/dashboard/#setup). This involves connecting a Formlabs 3D Printer to the Internet and then visiting the Dashboard Registration screen on the Printer to get a registration code. Type this registration code on the Dashboard Printer registration page to complete the registration. 3.  Now the Dashboard should show your Printer’s live status, show a history of prints, etc. 4.  Visit the [Developer Tools page at](https://dashboard.formlabs.com/#developer), and create your **Application credentials** 6.  Once you have your **Client ID** and the **Client Secret**, go to the [Authentication](#tag/Authentication) section for instructions on how to get an API access token and start using the Dashboard Developer API. 

    The version of the OpenAPI document: 0.8.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from formlabs_web_api.models.build_platform_contents_enum import BuildPlatformContentsEnum
from formlabs_web_api.models.camera_status_enum import CameraStatusEnum
from formlabs_web_api.models.form_cell import FormCell
from formlabs_web_api.models.my_print_run_read_only import MyPrintRunReadOnly
from formlabs_web_api.models.ready_to_print_enum import ReadyToPrintEnum
from formlabs_web_api.models.tank_mixer_state_enum import TankMixerStateEnum
from typing import Optional, Set
from typing_extensions import Self

class MyDeepPrinterStatus(BaseModel):
    """
    MyDeepPrinterStatus
    """ # noqa: E501
    status: StrictStr
    last_pinged_at: Optional[datetime] = None
    hopper_level: Optional[Annotated[int, Field(le=2147483647, strict=True, ge=-2147483648)]] = None
    material_credit: Optional[Union[StrictFloat, StrictInt]] = None
    hopper_material: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    last_modified: datetime
    current_temperature: Optional[Union[StrictFloat, StrictInt]] = None
    current_print_run: MyPrintRunReadOnly
    form_cell: FormCell
    last_printer_cooldown_started: Optional[datetime] = None
    outer_boundary_offset_corrections: Optional[Any] = None
    build_platform_contents: Optional[BuildPlatformContentsEnum] = None
    tank_mixer_state: Optional[TankMixerStateEnum] = None
    ready_to_print: Optional[ReadyToPrintEnum] = None
    printer_capabilities: Optional[List[Annotated[str, Field(strict=True, max_length=100)]]] = None
    printernet_capabilities: Optional[List[Annotated[str, Field(strict=True, max_length=100)]]] = None
    camera_status: Optional[CameraStatusEnum] = None
    __properties: ClassVar[List[str]] = ["status", "last_pinged_at", "hopper_level", "material_credit", "hopper_material", "last_modified", "current_temperature", "current_print_run", "form_cell", "last_printer_cooldown_started", "outer_boundary_offset_corrections", "build_platform_contents", "tank_mixer_state", "ready_to_print", "printer_capabilities", "printernet_capabilities", "camera_status"]

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
        """Create an instance of MyDeepPrinterStatus from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "status",
            "last_modified",
            "current_print_run",
            "form_cell",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of current_print_run
        if self.current_print_run:
            _dict['current_print_run'] = self.current_print_run.to_dict()
        # override the default output from pydantic by calling `to_dict()` of form_cell
        if self.form_cell:
            _dict['form_cell'] = self.form_cell.to_dict()
        # set to None if last_pinged_at (nullable) is None
        # and model_fields_set contains the field
        if self.last_pinged_at is None and "last_pinged_at" in self.model_fields_set:
            _dict['last_pinged_at'] = None

        # set to None if hopper_level (nullable) is None
        # and model_fields_set contains the field
        if self.hopper_level is None and "hopper_level" in self.model_fields_set:
            _dict['hopper_level'] = None

        # set to None if material_credit (nullable) is None
        # and model_fields_set contains the field
        if self.material_credit is None and "material_credit" in self.model_fields_set:
            _dict['material_credit'] = None

        # set to None if current_temperature (nullable) is None
        # and model_fields_set contains the field
        if self.current_temperature is None and "current_temperature" in self.model_fields_set:
            _dict['current_temperature'] = None

        # set to None if last_printer_cooldown_started (nullable) is None
        # and model_fields_set contains the field
        if self.last_printer_cooldown_started is None and "last_printer_cooldown_started" in self.model_fields_set:
            _dict['last_printer_cooldown_started'] = None

        # set to None if outer_boundary_offset_corrections (nullable) is None
        # and model_fields_set contains the field
        if self.outer_boundary_offset_corrections is None and "outer_boundary_offset_corrections" in self.model_fields_set:
            _dict['outer_boundary_offset_corrections'] = None

        # set to None if printernet_capabilities (nullable) is None
        # and model_fields_set contains the field
        if self.printernet_capabilities is None and "printernet_capabilities" in self.model_fields_set:
            _dict['printernet_capabilities'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of MyDeepPrinterStatus from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "status": obj.get("status"),
            "last_pinged_at": obj.get("last_pinged_at"),
            "hopper_level": obj.get("hopper_level"),
            "material_credit": obj.get("material_credit"),
            "hopper_material": obj.get("hopper_material"),
            "last_modified": obj.get("last_modified"),
            "current_temperature": obj.get("current_temperature"),
            "current_print_run": MyPrintRunReadOnly.from_dict(obj["current_print_run"]) if obj.get("current_print_run") is not None else None,
            "form_cell": FormCell.from_dict(obj["form_cell"]) if obj.get("form_cell") is not None else None,
            "last_printer_cooldown_started": obj.get("last_printer_cooldown_started"),
            "outer_boundary_offset_corrections": obj.get("outer_boundary_offset_corrections"),
            "build_platform_contents": obj.get("build_platform_contents"),
            "tank_mixer_state": obj.get("tank_mixer_state"),
            "ready_to_print": obj.get("ready_to_print"),
            "printer_capabilities": obj.get("printer_capabilities"),
            "printernet_capabilities": obj.get("printernet_capabilities"),
            "camera_status": obj.get("camera_status")
        })
        return _obj


