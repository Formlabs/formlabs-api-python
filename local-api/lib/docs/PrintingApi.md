# formlabs_local_api.PrintingApi

All URIs are relative to *http://localhost:44388*

Method | HTTP request | Description
------------- | ------------- | -------------
[**call_print**](PrintingApi.md#call_print) | **POST** /scene/{scene_id}/print/ | Print


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
    api_instance = formlabs_local_api.PrintingApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    print_request = {"printer":"10.35.15.12","job_name":"Test Job"} # PrintRequest | 
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Print
        api_response = api_instance.call_print(scene_id, print_request, var_async=var_async)
        print("The response of PrintingApi->call_print:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PrintingApi->call_print: %s\n" % e)
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

