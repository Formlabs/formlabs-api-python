# coding: utf-8

# flake8: noqa

"""
    Formlabs Web API

     # Introduction  The Formlabs Web API provides access to Formlabs’ remote control and remote monitoring features for Internet-connected Formlabs products registered to your Dashboard account.  Some example use cases of the Dashboard Developer API: 1.  Create automated custom reports on Printer usage, material usage, and job history to gain more insights into print production 2.  More efficiently manage Printers by integrating Printer status data into existing systems (ERP/MES/custom) # Terms and Conditions -   Formlabs reserves the right to revoke or invalidate your API key at any time without warning. -   As a beta, conditions of access to the API may change in the future, access may be bundled into other future software products, etc. (we will make an effort to provide as much warning as possible) -   As a beta, the API may change at any time without warning in such a way that it may fail to support existing workflows (though we will make an effort to provide advanced notice where possible) -   You agree not to exceed the Dashboard Developer API rate limit as detailed in the \"Rate Limit\" section below. -   You will be given access to certain non-public information, software, and specifications that are confidential and proprietary to Formlabs. You will not share these outside your organization. -   By participating in this Beta you may be sharing information with Formlabs. Any information shared is governed by our Privacy Policy [https://formlabs.com/support/privacy-policy/](https://formlabs.com/support/privacy-policy/) -   The Dashboard Developer API works with Formlabs Printers that are connected to the internet and registered to Dashboard. Printers registered to Dashboard share data with Formlabs (detailed in the Data Collection section of the Privacy Policy: [https://formlabs.com/support/privacy-policy/#Data-Collection](https://formlabs.com/support/privacy-policy/#Data-Collection)). For more information about how to set up Printers and register them to Dashboard, see this link: [https://support.formlabs.com/s/article/Dashboard-Overview-and-Setup](https://support.formlabs.com/s/article/Dashboard-Overview-and-Setup)  # Technical Overview The Formlabs Dashboard Developer API is a REST HTTP API using JSON as the response data format.   Formlabs Dashboard Developer API is HTTP-based. Send a HTTP GET request to an endpoint to retrieve data from that endpoint. The integrating system should be able to make HTTP requests and process responses in JSON format.   Formlabs Dashboard Developer API uses the standard [OAuth Authentication Flow](https://tools.ietf.org/html/rfc6749#section-4.4), and all API endpoints require authentication. The access token created is valid for a day, so make sure to refresh the token regularly to maintain seamless integration with the Dashboard Developer API and ensure uninterrupted workflow.  ## Versioning  The Dashboard Developer API uses resource-based versioning, meaning API endpoints are versioned independently, rather than globally across all endpoints.  Formlabs may change the version of an endpoint to first keep in sync with product updates (could be an addition or a removal of data), in addition to any changes based on customer feedback to allow easier integrations.  Versioning can occur in the following situations:  -   The format of the response data is required to change -   The format of the response type is required to change  Any outstanding version changes or upgrades occurred on endpoints will be highlighted and documented.  ## Rate Limit  The rate of requests to the Dashboard Developer API is limited to prevent the abuse of the system. Requests from the same IP address are limited to **100 requests/second**. Requests from the same authenticated user are limited to **1500 requests/hour**. After a rate limit is exceeded, requests will return a HTTP status code of 429 with a “Retry-after” header outlining when the next request can be made.  ## Account Setup & Printer Registration  The Dashboard Developer API is only available to Formlabs.com account-holding users that are registered and have active Formlabs 3D Printer(s) associated with their accounts. If you do not have a Formlabs.com account, or you have an account but don’t have your Printers connected to it, please follow the instructions below:  1.  Sign up for a Formlabs.com account at [https://formlabs.com/dashboard/#register](https://formlabs.com/dashboard/#register) 2.  Register the Formlabs 3D Printers at [https://formlabs.com/dashboard/#setup](https://formlabs.com/dashboard/#setup). This involves connecting a Formlabs 3D Printer to the Internet and then visiting the Dashboard Registration screen on the Printer to get a registration code. Type this registration code on the Dashboard Printer registration page to complete the registration. 3.  Now the Dashboard should show your Printer’s live status, show a history of prints, etc. 4.  Visit the [Developer Tools page at](https://dashboard.formlabs.com/#developer), and create your **Application credentials** 6.  Once you have your **Client ID** and the **Client Secret**, go to the [Authentication](#tag/Authentication) section for instructions on how to get an API access token and start using the Dashboard Developer API. 

    The version of the OpenAPI document: 0.8.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


__version__ = "0.8.1"

# import apis into sdk package
from formlabs_web_api.api.authentication_api import AuthenticationApi
from formlabs_web_api.api.cartridges_api import CartridgesApi
from formlabs_web_api.api.events_api import EventsApi
from formlabs_web_api.api.printer_groups_api import PrinterGroupsApi
from formlabs_web_api.api.printers_api import PrintersApi
from formlabs_web_api.api.prints_api import PrintsApi
from formlabs_web_api.api.tanks_api import TanksApi

# import ApiClient
from formlabs_web_api.api_response import ApiResponse
from formlabs_web_api.api_client import ApiClient
from formlabs_web_api.configuration import Configuration
from formlabs_web_api.exceptions import OpenApiException
from formlabs_web_api.exceptions import ApiTypeError
from formlabs_web_api.exceptions import ApiValueError
from formlabs_web_api.exceptions import ApiKeyError
from formlabs_web_api.exceptions import ApiAttributeError
from formlabs_web_api.exceptions import ApiException

# import models into sdk package
from formlabs_web_api.models.basic_user import BasicUser
from formlabs_web_api.models.build_platform_contents_enum import BuildPlatformContentsEnum
from formlabs_web_api.models.camera_status_enum import CameraStatusEnum
from formlabs_web_api.models.cartridge import Cartridge
from formlabs_web_api.models.cartridge_read_only import CartridgeReadOnly
from formlabs_web_api.models.cartridge_slot_enum import CartridgeSlotEnum
from formlabs_web_api.models.developer_api_group_membership_create_request import DeveloperAPIGroupMembershipCreateRequest
from formlabs_web_api.models.developer_api_group_membership_update_request import DeveloperAPIGroupMembershipUpdateRequest
from formlabs_web_api.models.developer_api_groups_bulk_add_printers_request import DeveloperAPIGroupsBulkAddPrintersRequest
from formlabs_web_api.models.developer_apimy_cloud_queue_items import DeveloperAPIMyCloudQueueItems
from formlabs_web_api.models.developer_apimy_printer import DeveloperAPIMyPrinter
from formlabs_web_api.models.form_cell import FormCell
from formlabs_web_api.models.group_invitation import GroupInvitation
from formlabs_web_api.models.groups_members_destroy_request import GroupsMembersDestroyRequest
from formlabs_web_api.models.harvest_status_enum import HarvestStatusEnum
from formlabs_web_api.models.my_deep_printer_status import MyDeepPrinterStatus
from formlabs_web_api.models.my_print_run_read_only import MyPrintRunReadOnly
from formlabs_web_api.models.new_workgroup import NewWorkgroup
from formlabs_web_api.models.paginated_cartridge_list import PaginatedCartridgeList
from formlabs_web_api.models.paginated_print_run_with_fleet_control_data_list import PaginatedPrintRunWithFleetControlDataList
from formlabs_web_api.models.paginated_tank_list import PaginatedTankList
from formlabs_web_api.models.paginated_user_event_read_only_list import PaginatedUserEventReadOnlyList
from formlabs_web_api.models.partial_work_group_request import PartialWorkGroupRequest
from formlabs_web_api.models.patched_partial_work_group_request import PatchedPartialWorkGroupRequest
from formlabs_web_api.models.print_part import PrintPart
from formlabs_web_api.models.print_run_note import PrintRunNote
from formlabs_web_api.models.print_run_success import PrintRunSuccess
from formlabs_web_api.models.print_run_success_enum import PrintRunSuccessEnum
from formlabs_web_api.models.print_run_with_fleet_control_data import PrintRunWithFleetControlData
from formlabs_web_api.models.print_thumbnail_serializer_only_thumbnail import PrintThumbnailSerializerOnlyThumbnail
from formlabs_web_api.models.printer_cartridge_status import PrinterCartridgeStatus
from formlabs_web_api.models.printer_group import PrinterGroup
from formlabs_web_api.models.printer_tank_status import PrinterTankStatus
from formlabs_web_api.models.ready_to_print_enum import ReadyToPrintEnum
from formlabs_web_api.models.request_an_access_token200_response import RequestAnAccessToken200Response
from formlabs_web_api.models.request_an_access_token400_response import RequestAnAccessToken400Response
from formlabs_web_api.models.request_an_access_token401_response import RequestAnAccessToken401Response
from formlabs_web_api.models.status_enum import StatusEnum
from formlabs_web_api.models.tank import Tank
from formlabs_web_api.models.tank_mixer_state_enum import TankMixerStateEnum
from formlabs_web_api.models.tank_read_only import TankReadOnly
from formlabs_web_api.models.user_event_read_only import UserEventReadOnly
from formlabs_web_api.models.workgroup import Workgroup
from formlabs_web_api.models.workgroup_membership import WorkgroupMembership
from formlabs_web_api.models.workgroup_settings import WorkgroupSettings
