# formlabs_web_api

# Introduction

The Formlabs Web API provides access to Formlabs’ remote control and remote monitoring features for Internet-connected Formlabs products registered to your Dashboard account.

Some example use cases of the Dashboard Developer API:
1.  Create automated custom reports on Printer usage, material usage, and job history to gain more insights into print production
2.  More efficiently manage Printers by integrating Printer status data into existing systems (ERP/MES/custom)
# Terms and Conditions
-   Formlabs reserves the right to revoke or invalidate your API key at any time without warning.
-   As a beta, conditions of access to the API may change in the future, access may be bundled into other future software products, etc.
(we will make an effort to provide as much warning as possible)
-   As a beta, the API may change at any time without warning in such a way that it may fail to support existing workflows
(though we will make an effort to provide advanced notice where possible)
-   You agree not to exceed the Dashboard Developer API rate limit as detailed in the \"Rate Limit\" section below.
-   You will be given access to certain non-public information, software, and specifications that are confidential and proprietary to Formlabs.
You will not share these outside your organization.
-   By participating in this Beta you may be sharing information with Formlabs. Any information shared is governed by our Privacy Policy
[https://formlabs.com/support/privacy-policy/](https://formlabs.com/support/privacy-policy/)
-   The Dashboard Developer API works with Formlabs Printers that are connected to the internet and registered to Dashboard.
Printers registered to Dashboard share data with Formlabs (detailed in the Data Collection section of the Privacy Policy:
[https://formlabs.com/support/privacy-policy/#Data-Collection](https://formlabs.com/support/privacy-policy/#Data-Collection)).
For more information about how to set up Printers and register them to Dashboard, see this link:
[https://support.formlabs.com/s/article/Dashboard-Overview-and-Setup](https://support.formlabs.com/s/article/Dashboard-Overview-and-Setup)

# Technical Overview
The Formlabs Dashboard Developer API is a REST HTTP API using JSON as the response data format. 

Formlabs Dashboard Developer API is HTTP-based. Send a HTTP GET request to an endpoint to retrieve data from that endpoint.
The integrating system should be able to make HTTP requests and process responses in JSON format. 

Formlabs Dashboard Developer API uses the standard [OAuth Authentication Flow](https://tools.ietf.org/html/rfc6749#section-4.4),
and all API endpoints require authentication.
The access token created is valid for a day, so make sure to refresh the token regularly to maintain seamless integration with the Dashboard Developer API and ensure uninterrupted workflow.

## Versioning

The Dashboard Developer API uses resource-based versioning, meaning API endpoints are versioned independently, rather than globally across all endpoints.

Formlabs may change the version of an endpoint to first keep in sync with product updates (could be an addition or a removal of data), in addition to any changes based on customer feedback to allow easier integrations.

Versioning can occur in the following situations:

-   The format of the response data is required to change
-   The format of the response type is required to change

Any outstanding version changes or upgrades occurred on endpoints will be highlighted and documented.

## Rate Limit

The rate of requests to the Dashboard Developer API is limited to prevent the abuse of the system.
Requests from the same IP address are limited to **100 requests/second**.
Requests from the same authenticated user are limited to **1500 requests/hour**.
After a rate limit is exceeded, requests will return a HTTP status code of 429
with a “Retry-after” header outlining when the next request can be made.

## Account Setup & Printer Registration

The Dashboard Developer API is only available to Formlabs.com account-holding users that are registered and have active Formlabs 3D Printer(s) associated with their accounts. If you do not have a Formlabs.com account, or you have an account but don’t have your Printers connected to it, please follow the instructions below:

1.  Sign up for a Formlabs.com account at [https://formlabs.com/dashboard/#register](https://formlabs.com/dashboard/#register)
2.  Register the Formlabs 3D Printers at [https://formlabs.com/dashboard/#setup](https://formlabs.com/dashboard/#setup). This involves connecting a Formlabs 3D Printer to the Internet and then visiting the Dashboard Registration screen on the Printer to get a registration code. Type this registration code on the Dashboard Printer registration page to complete the registration.
3.  Now the Dashboard should show your Printer’s live status, show a history of prints, etc.
4.  Visit the [Developer Tools page at](https://dashboard.formlabs.com/#developer), and create your **Application credentials**
6.  Once you have your **Client ID** and the **Client Secret**, go to the [Authentication](#tag/Authentication) section for instructions on how to get an API access token and start using the Dashboard Developer API.


This Python package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 0.8.1
- Package version: 0.8.0
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
import formlabs_web_api
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import formlabs_web_api
```

### Tests

Execute `pytest` to run the tests.

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import formlabs_web_api
from formlabs_web_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.formlabs.com
# See configuration.py for a list of all supported configuration parameters.
configuration = formlabs_web_api.Configuration(
    host = "https://api.formlabs.com"
)



# Enter a context with an instance of the API client
with formlabs_web_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = formlabs_web_api.AuthenticationApi(api_client)
    grant_type = 'grant_type_example' # str | The type of grant being used. Currently only `client_credentials` is supported
    client_id = 'client_id_example' # str | Your Client ID.
    client_secret = 'client_secret_example' # str | Your Client Secret.

    try:
        api_response = api_instance.request_an_access_token(grant_type, client_id, client_secret)
        print("The response of AuthenticationApi->request_an_access_token:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AuthenticationApi->request_an_access_token: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://api.formlabs.com*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AuthenticationApi* | [**request_an_access_token**](docs/AuthenticationApi.md#request_an_access_token) | **POST** /developer/v1/o/token/ | 
*AuthenticationApi* | [**revoke_an_access_token**](docs/AuthenticationApi.md#revoke_an_access_token) | **POST** /developer/v1/o/revoke_token/ | 
*CartridgesApi* | [**cartridges_list**](docs/CartridgesApi.md#cartridges_list) | **GET** /developer/v1/cartridges/ | 
*EventsApi* | [**events_list**](docs/EventsApi.md#events_list) | **GET** /developer/v1/events/ | 
*PrinterGroupsApi* | [**groups_bulk_add_printers_create**](docs/PrinterGroupsApi.md#groups_bulk_add_printers_create) | **POST** /developer/v1/groups/bulk-add-printers/ | 
*PrinterGroupsApi* | [**groups_create**](docs/PrinterGroupsApi.md#groups_create) | **POST** /developer/v1/groups/ | 
*PrinterGroupsApi* | [**groups_destroy**](docs/PrinterGroupsApi.md#groups_destroy) | **DELETE** /developer/v1/groups/{group_id}/ | 
*PrinterGroupsApi* | [**groups_list**](docs/PrinterGroupsApi.md#groups_list) | **GET** /developer/v1/groups/ | 
*PrinterGroupsApi* | [**groups_members_create**](docs/PrinterGroupsApi.md#groups_members_create) | **POST** /developer/v1/groups/{group_id}/members/ | 
*PrinterGroupsApi* | [**groups_members_destroy**](docs/PrinterGroupsApi.md#groups_members_destroy) | **DELETE** /developer/v1/groups/{group_id}/members/ | 
*PrinterGroupsApi* | [**groups_members_update**](docs/PrinterGroupsApi.md#groups_members_update) | **PUT** /developer/v1/groups/{group_id}/members/ | 
*PrinterGroupsApi* | [**groups_partial_update**](docs/PrinterGroupsApi.md#groups_partial_update) | **PATCH** /developer/v1/groups/{group_id}/ | 
*PrinterGroupsApi* | [**groups_queue_list**](docs/PrinterGroupsApi.md#groups_queue_list) | **GET** /developer/v1/groups/{group_id}/queue/ | 
*PrintersApi* | [**printers_list**](docs/PrintersApi.md#printers_list) | **GET** /developer/v1/printers/ | 
*PrintersApi* | [**printers_retrieve**](docs/PrintersApi.md#printers_retrieve) | **GET** /developer/v1/printers/{printer_serial}/ | 
*PrintsApi* | [**printers_prints_list**](docs/PrintsApi.md#printers_prints_list) | **GET** /developer/v1/printers/{printer_serial}/prints/ | 
*PrintsApi* | [**prints_list**](docs/PrintsApi.md#prints_list) | **GET** /developer/v1/prints/ | 
*TanksApi* | [**tanks_list**](docs/TanksApi.md#tanks_list) | **GET** /developer/v1/tanks/ | 


## Documentation For Models

 - [BasicUser](docs/BasicUser.md)
 - [BuildPlatformContentsEnum](docs/BuildPlatformContentsEnum.md)
 - [CameraStatusEnum](docs/CameraStatusEnum.md)
 - [Cartridge](docs/Cartridge.md)
 - [CartridgeReadOnly](docs/CartridgeReadOnly.md)
 - [CartridgeSlotEnum](docs/CartridgeSlotEnum.md)
 - [DeveloperAPIGroupMembershipCreateRequest](docs/DeveloperAPIGroupMembershipCreateRequest.md)
 - [DeveloperAPIGroupMembershipUpdateRequest](docs/DeveloperAPIGroupMembershipUpdateRequest.md)
 - [DeveloperAPIGroupsBulkAddPrintersRequest](docs/DeveloperAPIGroupsBulkAddPrintersRequest.md)
 - [DeveloperAPIMyCloudQueueItems](docs/DeveloperAPIMyCloudQueueItems.md)
 - [DeveloperAPIMyPrinter](docs/DeveloperAPIMyPrinter.md)
 - [FormCell](docs/FormCell.md)
 - [GroupInvitation](docs/GroupInvitation.md)
 - [GroupsMembersDestroyRequest](docs/GroupsMembersDestroyRequest.md)
 - [HarvestStatusEnum](docs/HarvestStatusEnum.md)
 - [MyDeepPrinterStatus](docs/MyDeepPrinterStatus.md)
 - [MyPrintRunReadOnly](docs/MyPrintRunReadOnly.md)
 - [NewWorkgroup](docs/NewWorkgroup.md)
 - [PaginatedCartridgeList](docs/PaginatedCartridgeList.md)
 - [PaginatedPrintRunWithFleetControlDataList](docs/PaginatedPrintRunWithFleetControlDataList.md)
 - [PaginatedTankList](docs/PaginatedTankList.md)
 - [PaginatedUserEventReadOnlyList](docs/PaginatedUserEventReadOnlyList.md)
 - [PartialWorkGroupRequest](docs/PartialWorkGroupRequest.md)
 - [PatchedPartialWorkGroupRequest](docs/PatchedPartialWorkGroupRequest.md)
 - [PrintPart](docs/PrintPart.md)
 - [PrintRunNote](docs/PrintRunNote.md)
 - [PrintRunSuccess](docs/PrintRunSuccess.md)
 - [PrintRunSuccessEnum](docs/PrintRunSuccessEnum.md)
 - [PrintRunWithFleetControlData](docs/PrintRunWithFleetControlData.md)
 - [PrintThumbnailSerializerOnlyThumbnail](docs/PrintThumbnailSerializerOnlyThumbnail.md)
 - [PrinterCartridgeStatus](docs/PrinterCartridgeStatus.md)
 - [PrinterGroup](docs/PrinterGroup.md)
 - [PrinterTankStatus](docs/PrinterTankStatus.md)
 - [ReadyToPrintEnum](docs/ReadyToPrintEnum.md)
 - [RequestAnAccessToken200Response](docs/RequestAnAccessToken200Response.md)
 - [RequestAnAccessToken400Response](docs/RequestAnAccessToken400Response.md)
 - [RequestAnAccessToken401Response](docs/RequestAnAccessToken401Response.md)
 - [StatusEnum](docs/StatusEnum.md)
 - [Tank](docs/Tank.md)
 - [TankMixerStateEnum](docs/TankMixerStateEnum.md)
 - [TankReadOnly](docs/TankReadOnly.md)
 - [UserEventReadOnly](docs/UserEventReadOnly.md)
 - [Workgroup](docs/Workgroup.md)
 - [WorkgroupMembership](docs/WorkgroupMembership.md)
 - [WorkgroupSettings](docs/WorkgroupSettings.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization


Authentication schemes defined for the API:
<a id="bearerAuth"></a>
### bearerAuth

- **Type**: Bearer authentication


## Author




