# coding: utf-8

"""
    Formlabs Developer API

    The Formlabs Dashboard Developer API provides resources to integrate Formlabs products into customer’s workflow and existing systems

    The version of the OpenAPI document: 0.1.0
    Contact: api-inquiry@formlabs.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from typing import Optional, Set
from typing_extensions import Self

class PrintPart(BaseModel):
    """
    PrintPart
    """ # noqa: E501
    id: StrictInt
    guid: StrictStr
    display_name: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    end_layer: Optional[Annotated[int, Field(le=2147483647, strict=True, ge=-2147483648)]] = None
    name: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    raw_mesh_hash: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    start_layer: Optional[Annotated[int, Field(le=2147483647, strict=True, ge=-2147483648)]] = None
    volume_ml: Optional[Union[StrictFloat, StrictInt]] = None
    prepared_scene: StrictStr
    __properties: ClassVar[List[str]] = ["id", "guid", "display_name", "end_layer", "name", "raw_mesh_hash", "start_layer", "volume_ml", "prepared_scene"]

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
        """Create an instance of PrintPart from a JSON string"""
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
        """
        excluded_fields: Set[str] = set([
            "id",
            "guid",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if raw_mesh_hash (nullable) is None
        # and model_fields_set contains the field
        if self.raw_mesh_hash is None and "raw_mesh_hash" in self.model_fields_set:
            _dict['raw_mesh_hash'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PrintPart from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "guid": obj.get("guid"),
            "display_name": obj.get("display_name"),
            "end_layer": obj.get("end_layer"),
            "name": obj.get("name"),
            "raw_mesh_hash": obj.get("raw_mesh_hash"),
            "start_layer": obj.get("start_layer"),
            "volume_ml": obj.get("volume_ml"),
            "prepared_scene": obj.get("prepared_scene")
        })
        return _obj


