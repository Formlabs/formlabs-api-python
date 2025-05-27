# formlabs_local_api.ExportingDeprecatedApi

All URIs are relative to *http://localhost:44388*

Method | HTTP request | Description
------------- | ------------- | -------------
[**save_form_file_deprecated**](ExportingDeprecatedApi.md#save_form_file_deprecated) | **POST** /scene/save-form/ | Save .form file
[**save_fps_file_deprecated**](ExportingDeprecatedApi.md#save_fps_file_deprecated) | **POST** /scene/save-fps-file/ | Save FPS file
[**save_screenshot_deprecated**](ExportingDeprecatedApi.md#save_screenshot_deprecated) | **POST** /scene/save-screenshot/ | Save screenshot file


# **save_form_file_deprecated**
> save_form_file_deprecated()

Save .form file

Deprecated. See [/scene/{scene_id}/save-form/](#operation/saveFormFile)

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
    api_instance = formlabs_local_api.ExportingDeprecatedApi(api_client)

    try:
        # Save .form file
        api_instance.save_form_file_deprecated()
    except Exception as e:
        print("Exception when calling ExportingDeprecatedApi->save_form_file_deprecated: %s\n" % e)
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
**200** | OK |  -  |
**400** | Bad Request |  -  |
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_fps_file_deprecated**
> save_fps_file_deprecated()

Save FPS file

Deprecated. See [/scene/{scene_id}/save-fps-file/](#operation/saveFpsFile)

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
    api_instance = formlabs_local_api.ExportingDeprecatedApi(api_client)

    try:
        # Save FPS file
        api_instance.save_fps_file_deprecated()
    except Exception as e:
        print("Exception when calling ExportingDeprecatedApi->save_fps_file_deprecated: %s\n" % e)
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

# **save_screenshot_deprecated**
> save_screenshot_deprecated()

Save screenshot file

Deprecated. See [/scene/{scene_id}/save-screenshot/](#operation/saveScreenshot)

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
    api_instance = formlabs_local_api.ExportingDeprecatedApi(api_client)

    try:
        # Save screenshot file
        api_instance.save_screenshot_deprecated()
    except Exception as e:
        print("Exception when calling ExportingDeprecatedApi->save_screenshot_deprecated: %s\n" % e)
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
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

