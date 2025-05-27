# formlabs_local_api.RemoteAccessApi

All URIs are relative to *http://localhost:44388*

Method | HTTP request | Description
------------- | ------------- | -------------
[**call_print**](RemoteAccessApi.md#call_print) | **POST** /scene/{scene_id}/print/ | Print
[**discover_devices**](RemoteAccessApi.md#discover_devices) | **POST** /discover-devices/ | Discover Devices
[**get_device**](RemoteAccessApi.md#get_device) | **GET** /devices/{id}/ | Get Device
[**get_devices**](RemoteAccessApi.md#get_devices) | **GET** /devices/ | Get Devices
[**get_user**](RemoteAccessApi.md#get_user) | **GET** /user/ | Get logged in user information
[**login**](RemoteAccessApi.md#login) | **POST** /login/ | Login
[**logout**](RemoteAccessApi.md#logout) | **POST** /logout/ | Log out


# **call_print**
> Print200Response call_print(scene_id, print_request, var_async=var_async)

Print

Upload the current scene to a printer or Fleet Control.

By default, only locally discovered printer names or local IP addresses are supported.
To upload prints remotely to your Fleet Control queue or printers registered to your
Dashboard account, you must be logged in and have an Internet connection.
Use the Login endpoint to authenticate with Formlabs Web Services.


### Example


```python
import formlabs_local_api
from formlabs_local_api.models.print200_response import Print200Response
from formlabs_local_api.models.print_request import PrintRequest
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
    api_instance = formlabs_local_api.RemoteAccessApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    print_request = {"printer":"10.35.15.12","job_name":"Test Job"} # PrintRequest | 
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Print
        api_response = api_instance.call_print(scene_id, print_request, var_async=var_async)
        print("The response of RemoteAccessApi->call_print:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RemoteAccessApi->call_print: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **print_request** | [**PrintRequest**](PrintRequest.md)|  | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

### Return type

[**Print200Response**](Print200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **discover_devices**
> DiscoverDevices200Response discover_devices(discover_devices_request, var_async=var_async)

Discover Devices

Discover new devices on the network

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.discover_devices200_response import DiscoverDevices200Response
from formlabs_local_api.models.discover_devices_request import DiscoverDevicesRequest
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
    api_instance = formlabs_local_api.RemoteAccessApi(api_client)
    discover_devices_request = {"timeout_seconds":10} # DiscoverDevicesRequest | 
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Discover Devices
        api_response = api_instance.discover_devices(discover_devices_request, var_async=var_async)
        print("The response of RemoteAccessApi->discover_devices:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RemoteAccessApi->discover_devices: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **discover_devices_request** | [**DiscoverDevicesRequest**](DiscoverDevicesRequest.md)|  | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

### Return type

[**DiscoverDevices200Response**](DiscoverDevices200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_device**
> DeviceStatusModel get_device(id)

Get Device

Get a previously discovered device's status

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.device_status_model import DeviceStatusModel
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
    api_instance = formlabs_local_api.RemoteAccessApi(api_client)
    id = 'id_example' # str | The unique identifier of the printer

    try:
        # Get Device
        api_response = api_instance.get_device(id)
        print("The response of RemoteAccessApi->get_device:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RemoteAccessApi->get_device: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the printer | 

### Return type

[**DeviceStatusModel**](DeviceStatusModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_devices**
> GetDevices200Response get_devices(can_print=can_print)

Get Devices

List of previously discovered device statuses

By default, only locally discovered printer names are returned.
To include your Fleet Control queues or printers registered to your
Dashboard account, you must be logged in and have an Internet connection.
Use the Login endpoint to authenticate with Formlabs Web Services.


### Example


```python
import formlabs_local_api
from formlabs_local_api.models.get_devices200_response import GetDevices200Response
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
    api_instance = formlabs_local_api.RemoteAccessApi(api_client)
    can_print = True # bool | If true, only devices that can receive prints will be returned. (optional)

    try:
        # Get Devices
        api_response = api_instance.get_devices(can_print=can_print)
        print("The response of RemoteAccessApi->get_devices:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RemoteAccessApi->get_devices: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **can_print** | **bool**| If true, only devices that can receive prints will be returned. | [optional] 

### Return type

[**GetDevices200Response**](GetDevices200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user**
> UserInformationModel get_user()

Get logged in user information

Get the logged in user's account information

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.user_information_model import UserInformationModel
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
    api_instance = formlabs_local_api.RemoteAccessApi(api_client)

    try:
        # Get logged in user information
        api_response = api_instance.get_user()
        print("The response of RemoteAccessApi->get_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RemoteAccessApi->get_user: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UserInformationModel**](UserInformationModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**404** | No user is logged in |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **login**
> WebAuthTokensModel login(login_request)

Login

Log in to Formlabs Web Services using an existing formlabs.com account.

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.login_request import LoginRequest
from formlabs_local_api.models.web_auth_tokens_model import WebAuthTokensModel
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
    api_instance = formlabs_local_api.RemoteAccessApi(api_client)
    login_request = {"username":"username","password":"password"} # LoginRequest | User credentials

    try:
        # Login
        api_response = api_instance.login(login_request)
        print("The response of RemoteAccessApi->login:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RemoteAccessApi->login: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **login_request** | [**LoginRequest**](LoginRequest.md)| User credentials | 

### Return type

[**WebAuthTokensModel**](WebAuthTokensModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **logout**
> logout()

Log out

Log out of Formlabs Web Services

### Example


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
    api_instance = formlabs_local_api.RemoteAccessApi(api_client)

    try:
        # Log out
        api_instance.logout()
    except Exception as e:
        print("Exception when calling RemoteAccessApi->logout: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

