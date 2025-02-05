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
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class TankReadOnly(BaseModel):
    """
    TankReadOnly
    """ # noqa: E501
    serial: StrictStr
    material: Optional[StrictStr]
    print_time_ms: Optional[StrictInt]
    layers_printed: Optional[StrictInt]
    first_fill_date: Optional[datetime]
    heatmap: Optional[StrictStr] = None
    heatmap_gif: Optional[StrictStr]
    display_name: Optional[StrictStr] = None
    layer_count: StrictInt
    inside_printer: StrictStr
    tank_type: Optional[StrictStr]
    connected_group: Optional[StrictStr]
    created_at: Optional[datetime]
    last_print_date: Optional[datetime]
    __properties: ClassVar[List[str]] = ["serial", "material", "print_time_ms", "layers_printed", "first_fill_date", "heatmap", "heatmap_gif", "display_name", "layer_count", "inside_printer", "tank_type", "connected_group", "created_at", "last_print_date"]

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
        """Create an instance of TankReadOnly from a JSON string"""
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
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "serial",
            "material",
            "print_time_ms",
            "layers_printed",
            "first_fill_date",
            "heatmap_gif",
            "layer_count",
            "inside_printer",
            "tank_type",
            "connected_group",
            "created_at",
            "last_print_date",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if material (nullable) is None
        # and model_fields_set contains the field
        if self.material is None and "material" in self.model_fields_set:
            _dict['material'] = None

        # set to None if print_time_ms (nullable) is None
        # and model_fields_set contains the field
        if self.print_time_ms is None and "print_time_ms" in self.model_fields_set:
            _dict['print_time_ms'] = None

        # set to None if layers_printed (nullable) is None
        # and model_fields_set contains the field
        if self.layers_printed is None and "layers_printed" in self.model_fields_set:
            _dict['layers_printed'] = None

        # set to None if first_fill_date (nullable) is None
        # and model_fields_set contains the field
        if self.first_fill_date is None and "first_fill_date" in self.model_fields_set:
            _dict['first_fill_date'] = None

        # set to None if heatmap_gif (nullable) is None
        # and model_fields_set contains the field
        if self.heatmap_gif is None and "heatmap_gif" in self.model_fields_set:
            _dict['heatmap_gif'] = None

        # set to None if tank_type (nullable) is None
        # and model_fields_set contains the field
        if self.tank_type is None and "tank_type" in self.model_fields_set:
            _dict['tank_type'] = None

        # set to None if connected_group (nullable) is None
        # and model_fields_set contains the field
        if self.connected_group is None and "connected_group" in self.model_fields_set:
            _dict['connected_group'] = None

        # set to None if created_at (nullable) is None
        # and model_fields_set contains the field
        if self.created_at is None and "created_at" in self.model_fields_set:
            _dict['created_at'] = None

        # set to None if last_print_date (nullable) is None
        # and model_fields_set contains the field
        if self.last_print_date is None and "last_print_date" in self.model_fields_set:
            _dict['last_print_date'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TankReadOnly from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "serial": obj.get("serial"),
            "material": obj.get("material"),
            "print_time_ms": obj.get("print_time_ms"),
            "layers_printed": obj.get("layers_printed"),
            "first_fill_date": obj.get("first_fill_date"),
            "heatmap": obj.get("heatmap"),
            "heatmap_gif": obj.get("heatmap_gif"),
            "display_name": obj.get("display_name"),
            "layer_count": obj.get("layer_count"),
            "inside_printer": obj.get("inside_printer"),
            "tank_type": obj.get("tank_type"),
            "connected_group": obj.get("connected_group"),
            "created_at": obj.get("created_at"),
            "last_print_date": obj.get("last_print_date")
        })
        return _obj


