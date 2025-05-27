# formlabs_local_api.GettingSceneInformationDeprecatedApi

All URIs are relative to *http://localhost:44388*

Method | HTTP request | Description
------------- | ------------- | -------------
[**estimate_print_time_deprecated**](GettingSceneInformationDeprecatedApi.md#estimate_print_time_deprecated) | **POST** /scene/estimate-print-time/ | Estimate Print Time
[**get_model_deprecated**](GettingSceneInformationDeprecatedApi.md#get_model_deprecated) | **GET** /scene/models/{id}/ | Get model
[**get_print_validation_deprecated**](GettingSceneInformationDeprecatedApi.md#get_print_validation_deprecated) | **GET** /scene/print-validation/ | Get Print Validation
[**get_scene_deprecated**](GettingSceneInformationDeprecatedApi.md#get_scene_deprecated) | **GET** /scene/ | Get Scene
[**get_scene_interferences_deprecated**](GettingSceneInformationDeprecatedApi.md#get_scene_interferences_deprecated) | **POST** /scene/interferences/ | Get Scene Interferences


# **estimate_print_time_deprecated**
> EstimatedPrintTimeModel estimate_print_time_deprecated()

Estimate Print Time

Deprecated. See [/scene/{scene_id}/estimate-print-time/](#operation/estimatePrintTime)

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.estimated_print_time_model import EstimatedPrintTimeModel
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
    api_instance = formlabs_local_api.GettingSceneInformationDeprecatedApi(api_client)

    try:
        # Estimate Print Time
        api_response = api_instance.estimate_print_time_deprecated()
        print("The response of GettingSceneInformationDeprecatedApi->estimate_print_time_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GettingSceneInformationDeprecatedApi->estimate_print_time_deprecated: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**EstimatedPrintTimeModel**](EstimatedPrintTimeModel.md)

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

# **get_model_deprecated**
> ModelProperties get_model_deprecated(id)

Get model

Deprecated. See [/scene/{scene_id}/models/{id}/](#operation/getModel)

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.model_properties import ModelProperties
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
    api_instance = formlabs_local_api.GettingSceneInformationDeprecatedApi(api_client)
    id = 'id_example' # str | The unique identifier of the model

    try:
        # Get model
        api_response = api_instance.get_model_deprecated(id)
        print("The response of GettingSceneInformationDeprecatedApi->get_model_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GettingSceneInformationDeprecatedApi->get_model_deprecated: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 

### Return type

[**ModelProperties**](ModelProperties.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Model description |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_print_validation_deprecated**
> PrintValidationResultModel get_print_validation_deprecated()

Get Print Validation

Deprecated. See [/scene/{scene_id}/print-validation/](#operation/getPrintValidation)

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.print_validation_result_model import PrintValidationResultModel
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
    api_instance = formlabs_local_api.GettingSceneInformationDeprecatedApi(api_client)

    try:
        # Get Print Validation
        api_response = api_instance.get_print_validation_deprecated()
        print("The response of GettingSceneInformationDeprecatedApi->get_print_validation_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GettingSceneInformationDeprecatedApi->get_print_validation_deprecated: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**PrintValidationResultModel**](PrintValidationResultModel.md)

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

# **get_scene_deprecated**
> SceneModel get_scene_deprecated()

Get Scene

Deprecated. See [/scene/{scene_id}/](#operation/getScene)

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.scene_model import SceneModel
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
    api_instance = formlabs_local_api.GettingSceneInformationDeprecatedApi(api_client)

    try:
        # Get Scene
        api_response = api_instance.get_scene_deprecated()
        print("The response of GettingSceneInformationDeprecatedApi->get_scene_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GettingSceneInformationDeprecatedApi->get_scene_deprecated: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**SceneModel**](SceneModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Scene description |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_scene_interferences_deprecated**
> get_scene_interferences_deprecated()

Get Scene Interferences

Deprecated. See [/scene/{scene_id}/interferences/](#operation/getSceneInterferences)

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
    api_instance = formlabs_local_api.GettingSceneInformationDeprecatedApi(api_client)

    try:
        # Get Scene Interferences
        api_instance.get_scene_interferences_deprecated()
    except Exception as e:
        print("Exception when calling GettingSceneInformationDeprecatedApi->get_scene_interferences_deprecated: %s\n" % e)
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

