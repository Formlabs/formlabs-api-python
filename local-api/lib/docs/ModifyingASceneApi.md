# formlabs_local_api.ModifyingASceneApi

All URIs are relative to *http://localhost:44388*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_drain_holes**](ModifyingASceneApi.md#add_drain_holes) | **POST** /scene/{scene_id}/add-drain-holes/ | Add Drain Holes
[**auto_layout**](ModifyingASceneApi.md#auto_layout) | **POST** /scene/{scene_id}/auto-layout/ | Auto Layout
[**auto_orient**](ModifyingASceneApi.md#auto_orient) | **POST** /scene/{scene_id}/auto-orient/ | Auto Orient
[**auto_pack**](ModifyingASceneApi.md#auto_pack) | **POST** /scene/{scene_id}/auto-pack/ | Auto Pack
[**auto_support**](ModifyingASceneApi.md#auto_support) | **POST** /scene/{scene_id}/auto-support/ | Auto Support
[**create_default_scene**](ModifyingASceneApi.md#create_default_scene) | **POST** /scene/default/ | Create Default Scene
[**create_scene**](ModifyingASceneApi.md#create_scene) | **POST** /scene/ | Create Scene
[**delete_model**](ModifyingASceneApi.md#delete_model) | **DELETE** /scene/{scene_id}/models/{id}/ | Delete model
[**duplicate_model**](ModifyingASceneApi.md#duplicate_model) | **POST** /scene/{scene_id}/models/{id}/duplicate/ | Duplicate model
[**hollow_model**](ModifyingASceneApi.md#hollow_model) | **POST** /scene/{scene_id}/hollow/ | Hollow Model
[**import_model**](ModifyingASceneApi.md#import_model) | **POST** /scene/{scene_id}/import-model/ | Import model
[**label_part**](ModifyingASceneApi.md#label_part) | **POST** /scene/{scene_id}/label/ | Label Part
[**load_form_file**](ModifyingASceneApi.md#load_form_file) | **POST** /load-form/ | Load .form file
[**pack_and_cage**](ModifyingASceneApi.md#pack_and_cage) | **POST** /scene/pack-and-cage/ | Pack and Cage
[**replace_model**](ModifyingASceneApi.md#replace_model) | **POST** /scene/{scene_id}/models/{id}/replace/ | Replace model
[**scan_to_model**](ModifyingASceneApi.md#scan_to_model) | **POST** /scene/{scene_id}/scan-to-model/ | Scan to model
[**update_model**](ModifyingASceneApi.md#update_model) | **POST** /scene/{scene_id}/models/{id}/ | Update model
[**update_scene**](ModifyingASceneApi.md#update_scene) | **PUT** /scene/{scene_id}/ | Update Scene


# **add_drain_holes**
> AddDrainHoles200Response add_drain_holes(scene_id, add_drain_holes_request, var_async=var_async)

Add Drain Holes

Add specified drain holes to specified model

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.add_drain_holes200_response import AddDrainHoles200Response
from formlabs_local_api.models.add_drain_holes_request import AddDrainHolesRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    add_drain_holes_request = formlabs_local_api.AddDrainHolesRequest() # AddDrainHolesRequest | Drain hole parameters
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Add Drain Holes
        api_response = api_instance.add_drain_holes(scene_id, add_drain_holes_request, var_async=var_async)
        print("The response of ModifyingASceneApi->add_drain_holes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->add_drain_holes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **add_drain_holes_request** | [**AddDrainHolesRequest**](AddDrainHolesRequest.md)| Drain hole parameters | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

### Return type

[**AddDrainHoles200Response**](AddDrainHoles200Response.md)

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

# **auto_layout**
> SceneModel auto_layout(scene_id, auto_layout_request, var_async=var_async)

Auto Layout

Automatically arrange models on the build platform. Only applies to SLA-type scenes like the Form 4 (use /scene/auto-pack/ for SLS-type scenes like the Fuse 1+)

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.auto_layout_request import AutoLayoutRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    auto_layout_request = {"models":"ALL","model_spacing_mm":1.0,"allow_overlapping_supports":false,"lock_rotation":false,"build_platform_2_optimized":false} # AutoLayoutRequest | Models to run the auto layout operation on
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Auto Layout
        api_response = api_instance.auto_layout(scene_id, auto_layout_request, var_async=var_async)
        print("The response of ModifyingASceneApi->auto_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->auto_layout: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **auto_layout_request** | [**AutoLayoutRequest**](AutoLayoutRequest.md)| Models to run the auto layout operation on | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

### Return type

[**SceneModel**](SceneModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | ## Bad Request  The scene will not be modified if any error occurs. The response will contain an error message.  |  -  |
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auto_orient**
> auto_orient(scene_id, auto_orient_request, var_async=var_async)

Auto Orient

Automatically choose model orientation for printing

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.auto_orient_request import AutoOrientRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    auto_orient_request = {"models":"ALL"} # AutoOrientRequest | Models to run the auto orient operation on
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Auto Orient
        api_instance.auto_orient(scene_id, auto_orient_request, var_async=var_async)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->auto_orient: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **auto_orient_request** | [**AutoOrientRequest**](AutoOrientRequest.md)| Models to run the auto orient operation on | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

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
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auto_pack**
> SceneModel auto_pack(scene_id, auto_pack_request, var_async=var_async)

Auto Pack

Automatically arrange models in the build volume. Only applies to SLS-type scenes like the Fuse 1+ (use /scene/auto-layout/ for SLA-type scenes like the Form 4)

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.auto_pack_request import AutoPackRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    auto_pack_request = formlabs_local_api.AutoPackRequest() # AutoPackRequest | Auto pack parameters
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Auto Pack
        api_response = api_instance.auto_pack(scene_id, auto_pack_request, var_async=var_async)
        print("The response of ModifyingASceneApi->auto_pack:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->auto_pack: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **auto_pack_request** | [**AutoPackRequest**](AutoPackRequest.md)| Auto pack parameters | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

### Return type

[**SceneModel**](SceneModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | ## Bad Request  The scene will not be modified if any error occurs. The response will contain an error message.  |  -  |
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auto_support**
> auto_support(scene_id, auto_support_request, var_async=var_async)

Auto Support

Generate support structures on models

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.auto_support_request import AutoSupportRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    auto_support_request = {"models":"ALL"} # AutoSupportRequest | Models to run the auto support operation on
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Auto Support
        api_instance.auto_support(scene_id, auto_support_request, var_async=var_async)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->auto_support: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **auto_support_request** | [**AutoSupportRequest**](AutoSupportRequest.md)| Models to run the auto support operation on | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

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
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_default_scene**
> SceneModel create_default_scene(scene_type_model)

Create Default Scene

Create a default scene

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.scene_model import SceneModel
from formlabs_local_api.models.scene_type_model import SceneTypeModel
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_type_model = {"machine_type":"FORM-4-0","material_code":"FLGPBK05","print_setting":"DEFAULT","layer_thickness_mm":0.025} # SceneTypeModel | Create a default scene with a given printing setup. For a full list of possible settings, call the GET /list-materials/ endpoint 

    try:
        # Create Default Scene
        api_response = api_instance.create_default_scene(scene_type_model)
        print("The response of ModifyingASceneApi->create_default_scene:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->create_default_scene: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_type_model** | [**SceneTypeModel**](SceneTypeModel.md)| Create a default scene with a given printing setup. For a full list of possible settings, call the GET /list-materials/ endpoint  | 

### Return type

[**SceneModel**](SceneModel.md)

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

# **create_scene**
> SceneModel create_scene(scene_type_model)

Create Scene

Create a new scene

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.scene_model import SceneModel
from formlabs_local_api.models.scene_type_model import SceneTypeModel
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_type_model = {"machine_type":"FORM-4-0","material_code":"FLGPBK05","print_setting":"DEFAULT","layer_thickness_mm":0.025} # SceneTypeModel | Create a scene with a given printing setup. For a full list of possible settings, call the GET /list-materials/ endpoint 

    try:
        # Create Scene
        api_response = api_instance.create_scene(scene_type_model)
        print("The response of ModifyingASceneApi->create_scene:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->create_scene: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_type_model** | [**SceneTypeModel**](SceneTypeModel.md)| Create a scene with a given printing setup. For a full list of possible settings, call the GET /list-materials/ endpoint  | 

### Return type

[**SceneModel**](SceneModel.md)

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

# **delete_model**
> delete_model(id, scene_id)

Delete model

Delete a model from the current scene

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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    id = 'id_example' # str | The unique identifier of the model
    scene_id = 'scene_id_example' # str | The unique identifier of the scene

    try:
        # Delete model
        api_instance.delete_model(id, scene_id)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->delete_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 
 **scene_id** | **str**| The unique identifier of the scene | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **duplicate_model**
> SceneModel duplicate_model(id, scene_id, duplicate_model_request)

Duplicate model

Duplicate a model

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.duplicate_model_request import DuplicateModelRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    id = 'id_example' # str | The unique identifier of the model
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    duplicate_model_request = formlabs_local_api.DuplicateModelRequest() # DuplicateModelRequest | 

    try:
        # Duplicate model
        api_response = api_instance.duplicate_model(id, scene_id, duplicate_model_request)
        print("The response of ModifyingASceneApi->duplicate_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->duplicate_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 
 **scene_id** | **str**| The unique identifier of the scene | 
 **duplicate_model_request** | [**DuplicateModelRequest**](DuplicateModelRequest.md)|  | 

### Return type

[**SceneModel**](SceneModel.md)

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

# **hollow_model**
> HollowModel200Response hollow_model(scene_id, hollow_model_request, var_async=var_async)

Hollow Model

Hollows the specified models

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.hollow_model200_response import HollowModel200Response
from formlabs_local_api.models.hollow_model_request import HollowModelRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    hollow_model_request = formlabs_local_api.HollowModelRequest() # HollowModelRequest | 
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Hollow Model
        api_response = api_instance.hollow_model(scene_id, hollow_model_request, var_async=var_async)
        print("The response of ModifyingASceneApi->hollow_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->hollow_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **hollow_model_request** | [**HollowModelRequest**](HollowModelRequest.md)|  | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

### Return type

[**HollowModel200Response**](HollowModel200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**202** | Async operation accepted |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **import_model**
> ModelProperties import_model(scene_id, import_model_request, var_async=var_async)

Import model

Import a model into the current scene

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.import_model_request import ImportModelRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    import_model_request = {"file":"C:\\Users\\user\\Desktop\\test.stl"} # ImportModelRequest | 
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Import model
        api_response = api_instance.import_model(scene_id, import_model_request, var_async=var_async)
        print("The response of ModifyingASceneApi->import_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->import_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **import_model_request** | [**ImportModelRequest**](ImportModelRequest.md)|  | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

### Return type

[**ModelProperties**](ModelProperties.md)

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
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **label_part**
> HollowModel200Response label_part(scene_id, label_part_request, var_async=var_async)

Label Part

Labels the specified model. Labels wrap around a model's surface.

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.hollow_model200_response import HollowModel200Response
from formlabs_local_api.models.label_part_request import LabelPartRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    label_part_request = formlabs_local_api.LabelPartRequest() # LabelPartRequest | 
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Label Part
        api_response = api_instance.label_part(scene_id, label_part_request, var_async=var_async)
        print("The response of ModifyingASceneApi->label_part:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->label_part: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **label_part_request** | [**LabelPartRequest**](LabelPartRequest.md)|  | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

### Return type

[**HollowModel200Response**](HollowModel200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**202** | Async operation accepted |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **load_form_file**
> SceneModel load_form_file(load_form_file_request, var_async=var_async)

Load .form file

Load a .form file and create a new scene from it

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.load_form_file_request import LoadFormFileRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    load_form_file_request = {"file":"C:\\Users\\user\\Desktop\\test.form"} # LoadFormFileRequest | Full path to the .form file to load
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Load .form file
        api_response = api_instance.load_form_file(load_form_file_request, var_async=var_async)
        print("The response of ModifyingASceneApi->load_form_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->load_form_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **load_form_file_request** | [**LoadFormFileRequest**](LoadFormFileRequest.md)| Full path to the .form file to load | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

### Return type

[**SceneModel**](SceneModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Scene description |  -  |
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pack_and_cage**
> SceneModel pack_and_cage(pack_and_cage_request)

Pack and Cage

Automatically arrange models in the build volume and create a cage around them. Only applies to SLS-type scenes like the Fuse 1+.

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.pack_and_cage_request import PackAndCageRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    pack_and_cage_request = formlabs_local_api.PackAndCageRequest() # PackAndCageRequest | Auto pack parameters

    try:
        # Pack and Cage
        api_response = api_instance.pack_and_cage(pack_and_cage_request)
        print("The response of ModifyingASceneApi->pack_and_cage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->pack_and_cage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pack_and_cage_request** | [**PackAndCageRequest**](PackAndCageRequest.md)| Auto pack parameters | 

### Return type

[**SceneModel**](SceneModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | ## Bad Request  The scene will not be modified if any error occurs. The response will contain an error message.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_model**
> ReplaceModel200Response replace_model(id, scene_id, replace_model_request)

Replace model

Replace a model currently in the scene with a new model, copying the existing models setup and supports

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.replace_model200_response import ReplaceModel200Response
from formlabs_local_api.models.replace_model_request import ReplaceModelRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    id = 'id_example' # str | The unique identifier of the model
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    replace_model_request = formlabs_local_api.ReplaceModelRequest() # ReplaceModelRequest | 

    try:
        # Replace model
        api_response = api_instance.replace_model(id, scene_id, replace_model_request)
        print("The response of ModifyingASceneApi->replace_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->replace_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 
 **scene_id** | **str**| The unique identifier of the scene | 
 **replace_model_request** | [**ReplaceModelRequest**](ReplaceModelRequest.md)|  | 

### Return type

[**ReplaceModel200Response**](ReplaceModel200Response.md)

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

# **scan_to_model**
> ScanToModel200Response scan_to_model(scene_id, scan_to_model_request, var_async=var_async)

Scan to model

Convert an STL scan of teeth to a solid, printable model in an SLA scene

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.scan_to_model200_response import ScanToModel200Response
from formlabs_local_api.models.scan_to_model_request import ScanToModelRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    scan_to_model_request = formlabs_local_api.ScanToModelRequest() # ScanToModelRequest | 
    var_async = True # bool | Whether to run the operation asynchronously (optional)

    try:
        # Scan to model
        api_response = api_instance.scan_to_model(scene_id, scan_to_model_request, var_async=var_async)
        print("The response of ModifyingASceneApi->scan_to_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->scan_to_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **scan_to_model_request** | [**ScanToModelRequest**](ScanToModelRequest.md)|  | 
 **var_async** | **bool**| Whether to run the operation asynchronously | [optional] 

### Return type

[**ScanToModel200Response**](ScanToModel200Response.md)

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
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_model**
> update_model(id, scene_id, update_model_request)

Update model

Update a model's properties

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.update_model_request import UpdateModelRequest
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    id = 'id_example' # str | The unique identifier of the model
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    update_model_request = {"position":{"x":10,"y":1,"z":2}} # UpdateModelRequest | Model properties to update

    try:
        # Update model
        api_instance.update_model(id, scene_id, update_model_request)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->update_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 
 **scene_id** | **str**| The unique identifier of the scene | 
 **update_model_request** | [**UpdateModelRequest**](UpdateModelRequest.md)| Model properties to update | 

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

# **update_scene**
> SceneModel update_scene(scene_id, scene_type_model)

Update Scene

Update the scene's properties

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.scene_model import SceneModel
from formlabs_local_api.models.scene_type_model import SceneTypeModel
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
    api_instance = formlabs_local_api.ModifyingASceneApi(api_client)
    scene_id = 'scene_id_example' # str | The unique identifier of the scene
    scene_type_model = {"machine_type":"FORM-4-0","material_code":"FLGPBK05","print_setting":"DEFAULT","layer_thickness_mm":0.025} # SceneTypeModel | 

    try:
        # Update Scene
        api_response = api_instance.update_scene(scene_id, scene_type_model)
        print("The response of ModifyingASceneApi->update_scene:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneApi->update_scene: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scene_id** | **str**| The unique identifier of the scene | 
 **scene_type_model** | [**SceneTypeModel**](SceneTypeModel.md)|  | 

### Return type

[**SceneModel**](SceneModel.md)

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

