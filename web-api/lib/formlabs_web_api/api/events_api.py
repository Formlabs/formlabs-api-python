# coding: utf-8

"""
    Formlabs Web API

     # Introduction  The Formlabs Web API provides access to Formlabs’ remote control and remote monitoring features for Internet-connected Formlabs products registered to your Dashboard account.  Some example use cases of the Dashboard Developer API: 1.  Create automated custom reports on Printer usage, material usage, and job history to gain more insights into print production 2.  More efficiently manage Printers by integrating Printer status data into existing systems (ERP/MES/custom) # Terms and Conditions -   Formlabs reserves the right to revoke or invalidate your API key at any time without warning. -   As a beta, conditions of access to the API may change in the future, access may be bundled into other future software products, etc. (we will make an effort to provide as much warning as possible) -   As a beta, the API may change at any time without warning in such a way that it may fail to support existing workflows (though we will make an effort to provide advanced notice where possible) -   You agree not to exceed the Dashboard Developer API rate limit as detailed in the \"Rate Limit\" section below. -   You will be given access to certain non-public information, software, and specifications that are confidential and proprietary to Formlabs. You will not share these outside your organization. -   By participating in this Beta you may be sharing information with Formlabs. Any information shared is governed by our Privacy Policy [https://formlabs.com/support/privacy-policy/](https://formlabs.com/support/privacy-policy/) -   The Dashboard Developer API works with Formlabs Printers that are connected to the internet and registered to Dashboard. Printers registered to Dashboard share data with Formlabs (detailed in the Data Collection section of the Privacy Policy: [https://formlabs.com/support/privacy-policy/#Data-Collection](https://formlabs.com/support/privacy-policy/#Data-Collection)). For more information about how to set up Printers and register them to Dashboard, see this link: [https://support.formlabs.com/s/article/Dashboard-Overview-and-Setup](https://support.formlabs.com/s/article/Dashboard-Overview-and-Setup)  # Technical Overview The Formlabs Dashboard Developer API is a REST HTTP API using JSON as the response data format.   Formlabs Dashboard Developer API is HTTP-based. Send a HTTP GET request to an endpoint to retrieve data from that endpoint. The integrating system should be able to make HTTP requests and process responses in JSON format.   Formlabs Dashboard Developer API uses the standard [OAuth Authentication Flow](https://tools.ietf.org/html/rfc6749#section-4.4), and all API endpoints require authentication. The access token created is valid for a day, so make sure to refresh the token regularly to maintain seamless integration with the Dashboard Developer API and ensure uninterrupted workflow.  ## Versioning  The Dashboard Developer API uses resource-based versioning, meaning API endpoints are versioned independently, rather than globally across all endpoints.  Formlabs may change the version of an endpoint to first keep in sync with product updates (could be an addition or a removal of data), in addition to any changes based on customer feedback to allow easier integrations.  Versioning can occur in the following situations:  -   The format of the response data is required to change -   The format of the response type is required to change  Any outstanding version changes or upgrades occurred on endpoints will be highlighted and documented.  ## Rate Limit  The rate of requests to the Dashboard Developer API is limited to prevent the abuse of the system. Requests from the same IP address are limited to **100 requests/second**. Requests from the same authenticated user are limited to **1500 requests/hour**. After a rate limit is exceeded, requests will return a HTTP status code of 429 with a “Retry-after” header outlining when the next request can be made.  ## Account Setup & Printer Registration  The Dashboard Developer API is only available to Formlabs.com account-holding users that are registered and have active Formlabs 3D Printer(s) associated with their accounts. If you do not have a Formlabs.com account, or you have an account but don’t have your Printers connected to it, please follow the instructions below:  1.  Sign up for a Formlabs.com account at [https://formlabs.com/dashboard/#register](https://formlabs.com/dashboard/#register) 2.  Register the Formlabs 3D Printers at [https://formlabs.com/dashboard/#setup](https://formlabs.com/dashboard/#setup). This involves connecting a Formlabs 3D Printer to the Internet and then visiting the Dashboard Registration screen on the Printer to get a registration code. Type this registration code on the Dashboard Printer registration page to complete the registration. 3.  Now the Dashboard should show your Printer’s live status, show a history of prints, etc. 4.  Visit the [Developer Tools page at](https://dashboard.formlabs.com/#developer), and create your **Application credentials** 6.  Once you have your **Client ID** and the **Client Secret**, go to the [Authentication](#tag/Authentication) section for instructions on how to get an API access token and start using the Dashboard Developer API. 

    The version of the OpenAPI document: 0.8.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

import warnings
from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated

from datetime import datetime
from pydantic import Field, StrictInt, StrictStr
from typing import Optional
from typing_extensions import Annotated
from formlabs_web_api.models.paginated_user_event_read_only_list import PaginatedUserEventReadOnlyList

from formlabs_web_api.api_client import ApiClient, RequestSerialized
from formlabs_web_api.api_response import ApiResponse
from formlabs_web_api.rest import RESTResponseType


class EventsApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def events_list(
        self,
        cartridge: Annotated[Optional[StrictStr], Field(description="Filter by resin cartridge serial")] = None,
        date__gt: Annotated[Optional[datetime], Field(description="Filter by date greater than date specified (ISO 8601 Format)")] = None,
        date__lt: Annotated[Optional[datetime], Field(description="Filter by date less than date specified (ISO 8601 Format)")] = None,
        page: Annotated[Optional[StrictInt], Field(description="A page number within the paginated result set.")] = None,
        per_page: Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None,
        print_run: Annotated[Optional[StrictStr], Field(description="Filter by print id")] = None,
        printer: Annotated[Optional[StrictStr], Field(description="Filter by printer serial")] = None,
        tank: Annotated[Optional[StrictStr], Field(description="Filter by resin tank serial")] = None,
        type: Annotated[Optional[StrictStr], Field(description="Filter by Event Type")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> PaginatedUserEventReadOnlyList:
        """events_list

        List of all events associated with my account

        :param cartridge: Filter by resin cartridge serial
        :type cartridge: str
        :param date__gt: Filter by date greater than date specified (ISO 8601 Format)
        :type date__gt: datetime
        :param date__lt: Filter by date less than date specified (ISO 8601 Format)
        :type date__lt: datetime
        :param page: A page number within the paginated result set.
        :type page: int
        :param per_page: Number of results to return per page.
        :type per_page: int
        :param print_run: Filter by print id
        :type print_run: str
        :param printer: Filter by printer serial
        :type printer: str
        :param tank: Filter by resin tank serial
        :type tank: str
        :param type: Filter by Event Type
        :type type: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._events_list_serialize(
            cartridge=cartridge,
            date__gt=date__gt,
            date__lt=date__lt,
            page=page,
            per_page=per_page,
            print_run=print_run,
            printer=printer,
            tank=tank,
            type=type,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "PaginatedUserEventReadOnlyList",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data


    @validate_call
    def events_list_with_http_info(
        self,
        cartridge: Annotated[Optional[StrictStr], Field(description="Filter by resin cartridge serial")] = None,
        date__gt: Annotated[Optional[datetime], Field(description="Filter by date greater than date specified (ISO 8601 Format)")] = None,
        date__lt: Annotated[Optional[datetime], Field(description="Filter by date less than date specified (ISO 8601 Format)")] = None,
        page: Annotated[Optional[StrictInt], Field(description="A page number within the paginated result set.")] = None,
        per_page: Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None,
        print_run: Annotated[Optional[StrictStr], Field(description="Filter by print id")] = None,
        printer: Annotated[Optional[StrictStr], Field(description="Filter by printer serial")] = None,
        tank: Annotated[Optional[StrictStr], Field(description="Filter by resin tank serial")] = None,
        type: Annotated[Optional[StrictStr], Field(description="Filter by Event Type")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[PaginatedUserEventReadOnlyList]:
        """events_list

        List of all events associated with my account

        :param cartridge: Filter by resin cartridge serial
        :type cartridge: str
        :param date__gt: Filter by date greater than date specified (ISO 8601 Format)
        :type date__gt: datetime
        :param date__lt: Filter by date less than date specified (ISO 8601 Format)
        :type date__lt: datetime
        :param page: A page number within the paginated result set.
        :type page: int
        :param per_page: Number of results to return per page.
        :type per_page: int
        :param print_run: Filter by print id
        :type print_run: str
        :param printer: Filter by printer serial
        :type printer: str
        :param tank: Filter by resin tank serial
        :type tank: str
        :param type: Filter by Event Type
        :type type: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._events_list_serialize(
            cartridge=cartridge,
            date__gt=date__gt,
            date__lt=date__lt,
            page=page,
            per_page=per_page,
            print_run=print_run,
            printer=printer,
            tank=tank,
            type=type,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "PaginatedUserEventReadOnlyList",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )


    @validate_call
    def events_list_without_preload_content(
        self,
        cartridge: Annotated[Optional[StrictStr], Field(description="Filter by resin cartridge serial")] = None,
        date__gt: Annotated[Optional[datetime], Field(description="Filter by date greater than date specified (ISO 8601 Format)")] = None,
        date__lt: Annotated[Optional[datetime], Field(description="Filter by date less than date specified (ISO 8601 Format)")] = None,
        page: Annotated[Optional[StrictInt], Field(description="A page number within the paginated result set.")] = None,
        per_page: Annotated[Optional[StrictInt], Field(description="Number of results to return per page.")] = None,
        print_run: Annotated[Optional[StrictStr], Field(description="Filter by print id")] = None,
        printer: Annotated[Optional[StrictStr], Field(description="Filter by printer serial")] = None,
        tank: Annotated[Optional[StrictStr], Field(description="Filter by resin tank serial")] = None,
        type: Annotated[Optional[StrictStr], Field(description="Filter by Event Type")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """events_list

        List of all events associated with my account

        :param cartridge: Filter by resin cartridge serial
        :type cartridge: str
        :param date__gt: Filter by date greater than date specified (ISO 8601 Format)
        :type date__gt: datetime
        :param date__lt: Filter by date less than date specified (ISO 8601 Format)
        :type date__lt: datetime
        :param page: A page number within the paginated result set.
        :type page: int
        :param per_page: Number of results to return per page.
        :type per_page: int
        :param print_run: Filter by print id
        :type print_run: str
        :param printer: Filter by printer serial
        :type printer: str
        :param tank: Filter by resin tank serial
        :type tank: str
        :param type: Filter by Event Type
        :type type: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._events_list_serialize(
            cartridge=cartridge,
            date__gt=date__gt,
            date__lt=date__lt,
            page=page,
            per_page=per_page,
            print_run=print_run,
            printer=printer,
            tank=tank,
            type=type,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "PaginatedUserEventReadOnlyList",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _events_list_serialize(
        self,
        cartridge,
        date__gt,
        date__lt,
        page,
        per_page,
        print_run,
        printer,
        tank,
        type,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[
            str, Union[str, bytes, List[str], List[bytes], List[Tuple[str, bytes]]]
        ] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        if cartridge is not None:
            
            _query_params.append(('cartridge', cartridge))
            
        if date__gt is not None:
            if isinstance(date__gt, datetime):
                _query_params.append(
                    (
                        'date__gt',
                        date__gt.strftime(
                            self.api_client.configuration.datetime_format
                        )
                    )
                )
            else:
                _query_params.append(('date__gt', date__gt))
            
        if date__lt is not None:
            if isinstance(date__lt, datetime):
                _query_params.append(
                    (
                        'date__lt',
                        date__lt.strftime(
                            self.api_client.configuration.datetime_format
                        )
                    )
                )
            else:
                _query_params.append(('date__lt', date__lt))
            
        if page is not None:
            
            _query_params.append(('page', page))
            
        if per_page is not None:
            
            _query_params.append(('per_page', per_page))
            
        if print_run is not None:
            
            _query_params.append(('print_run', print_run))
            
        if printer is not None:
            
            _query_params.append(('printer', printer))
            
        if tank is not None:
            
            _query_params.append(('tank', tank))
            
        if type is not None:
            
            _query_params.append(('type', type))
            
        # process the header parameters
        # process the form parameters
        # process the body parameter


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )


        # authentication setting
        _auth_settings: List[str] = [
            'bearerAuth'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/developer/v1/events/',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )


