# formlabs_local_api.GettingSceneInformationApi

All URIs are relative to *http://localhost:44388*

Method | HTTP request | Description
------------- | ------------- | -------------
[**estimate_print_time**](GettingSceneInformationApi.md#estimate_print_time) | **POST** /scene/{scene_id}/estimate-print-time/ | Estimate Print Time
[**get_all_scenes**](GettingSceneInformationApi.md#get_all_scenes) | **GET** /scenes/ | Get All Scenes
[**get_model**](GettingSceneInformationApi.md#get_model) | **GET** /scene/{scene_id}/models/{id}/ | Get model
[**get_print_validation**](GettingSceneInformationApi.md#get_print_validation) | **GET** /scene/{scene_id}/print-validation/ | Get Print Validation
[**get_scene**](GettingSceneInformationApi.md#get_scene) | **GET** /scene/{scene_id}/ | Get Scene
[**get_scene_interferences**](GettingSceneInformationApi.md#get_scene_interferences) | **POST** /scene/{scene_id}/interferences/ | Get Scene Interferences


# **estimate_print_time**
> EstimatedPrintTimeModel estimate_print_time(scene_id, var_async=var_async)

Estimate Print Time

Calculate the estimated print time for the current scene

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
    api_instance = formlabs_local_api.GettingSceneInformationApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Estimate Print Time
        api_response = api_instance.estimate_print_time(scene_id, var_async=var_async)
        print("The response of GettingSceneInformationApi->estimate_print_time:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GettingSceneInformationApi->estimate_print_time: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

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

# **get_all_scenes**
> GetAllScenes200Response get_all_scenes()

Get All Scenes

Get data about all scenes

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.get_all_scenes200_response import GetAllScenes200Response
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
    api_instance = formlabs_local_api.GettingSceneInformationApi(api_client)

    try:
        # Get All Scenes
        api_response = api_instance.get_all_scenes()
        print("The response of GettingSceneInformationApi->get_all_scenes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GettingSceneInformationApi->get_all_scenes: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetAllScenes200Response**](GetAllScenes200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Descriptions of all scenes |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_model**
> ModelProperties get_model(id, scene_id)

Get model

Get a model's properties

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
    api_instance = formlabs_local_api.GettingSceneInformationApi(api_client)
    id = 'id_example' # str | The unique identifier of the model
    scene_id = 'scene_id_example' # str | The unique identifier of the scene

    try:
        # Get model
        api_response = api_instance.get_model(id, scene_id)
        print("The response of GettingSceneInformationApi->get_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GettingSceneInformationApi->get_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 
 **scene_id** | **str**| The unique identifier of the scene | 

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

# **get_print_validation**
> PrintValidationResultModel get_print_validation(scene_id, var_async=var_async)

Get Print Validation

Calculate the print validation for the current scene

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
    api_instance = formlabs_local_api.GettingSceneInformationApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Get Print Validation
        api_response = api_instance.get_print_validation(scene_id, var_async=var_async)
        print("The response of GettingSceneInformationApi->get_print_validation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GettingSceneInformationApi->get_print_validation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

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

# **get_scene**
> SceneModel get_scene(scene_id)

Get Scene

Get data about the scene with the given ID, or the most recently created scene if no ID is provided

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
    api_instance = formlabs_local_api.GettingSceneInformationApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene

    try:
        # Get Scene
        api_response = api_instance.get_scene(scene_id)
        print("The response of GettingSceneInformationApi->get_scene:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GettingSceneInformationApi->get_scene: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 

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

# **get_scene_interferences**
> get_scene_interferences(scene_id, get_scene_interferences_request=get_scene_interferences_request)

Get Scene Interferences

Returns a list of pairs of IDs of interfering models.

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.get_scene_interferences_request import GetSceneInterferencesRequest
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
    api_instance = formlabs_local_api.GettingSceneInformationApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    get_scene_interferences_request = formlabs_local_api.GetSceneInterferencesRequest() # GetSceneInterferencesRequest | Interferences parameters (optional)

    try:
        # Get Scene Interferences
        api_instance.get_scene_interferences(scene_id, get_scene_interferences_request=get_scene_interferences_request)
    except Exception as e:
        print("Exception when calling GettingSceneInformationApi->get_scene_interferences: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **get_scene_interferences_request** | [**GetSceneInterferencesRequest**](GetSceneInterferencesRequest.md)| Interferences parameters | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

