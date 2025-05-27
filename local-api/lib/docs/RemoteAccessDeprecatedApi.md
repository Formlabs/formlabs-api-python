# formlabs_local_api.RemoteAccessDeprecatedApi

All URIs are relative to *http://localhost:44388*

Method | HTTP request | Description
------------- | ------------- | -------------
[**print_deprecated**](RemoteAccessDeprecatedApi.md#print_deprecated) | **POST** /scene/print/ | Print


# **print_deprecated**
> Print200Response print_deprecated()

Print

Deprecated. See [/scene/{scene_id}/print/](#operation/print)

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.print200_response import Print200Response
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
    api_instance = formlabs_local_api.RemoteAccessDeprecatedApi(api_client)

    try:
        # Print
        api_response = api_instance.print_deprecated()
        print("The response of RemoteAccessDeprecatedApi->print_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RemoteAccessDeprecatedApi->print_deprecated: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Print200Response**](Print200Response.md)

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
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

