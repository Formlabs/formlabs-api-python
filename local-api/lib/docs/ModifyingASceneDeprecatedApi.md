# formlabs_local_api.ModifyingASceneDeprecatedApi

All URIs are relative to *http://localhost:44388*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_drain_holes_deprecated**](ModifyingASceneDeprecatedApi.md#add_drain_holes_deprecated) | **POST** /scene/add-drain-holes/ | Add Drain Holes
[**auto_layout_deprecated**](ModifyingASceneDeprecatedApi.md#auto_layout_deprecated) | **POST** /scene/auto-layout/ | Auto Layout
[**auto_orient_deprecated**](ModifyingASceneDeprecatedApi.md#auto_orient_deprecated) | **POST** /scene/auto-orient/ | Auto Orient
[**auto_pack_deprecated**](ModifyingASceneDeprecatedApi.md#auto_pack_deprecated) | **POST** /scene/auto-pack/ | Auto Pack
[**auto_support_deprecated**](ModifyingASceneDeprecatedApi.md#auto_support_deprecated) | **POST** /scene/auto-support/ | Auto Support
[**delete_model_deprecated**](ModifyingASceneDeprecatedApi.md#delete_model_deprecated) | **DELETE** /scene/models/{id}/ | Delete model
[**duplicate_model_deprecated**](ModifyingASceneDeprecatedApi.md#duplicate_model_deprecated) | **POST** /scene/models/{id}/duplicate/ | Duplicate model
[**hollow_model_deprecated**](ModifyingASceneDeprecatedApi.md#hollow_model_deprecated) | **POST** /scene/hollow/ | Hollow Model
[**import_model_deprecated**](ModifyingASceneDeprecatedApi.md#import_model_deprecated) | **POST** /scene/import-model/ | Import model
[**label_part_deprecated**](ModifyingASceneDeprecatedApi.md#label_part_deprecated) | **POST** /scene/label/ | Label Part
[**replace_model_deprecated**](ModifyingASceneDeprecatedApi.md#replace_model_deprecated) | **POST** /scene/models/{id}/replace/ | Replace model
[**scan_to_model_deprecated**](ModifyingASceneDeprecatedApi.md#scan_to_model_deprecated) | **POST** /scene/scan-to-model/ | Scan to model
[**update_model_deprecated**](ModifyingASceneDeprecatedApi.md#update_model_deprecated) | **POST** /scene/models/{id}/ | Update model
[**update_scene_deprecated**](ModifyingASceneDeprecatedApi.md#update_scene_deprecated) | **PUT** /scene/ | Update Scene


# **add_drain_holes_deprecated**
> AddDrainHoles200Response add_drain_holes_deprecated()

Add Drain Holes

Deprecated. See [/scene/{scene_id}/add-drain-holes/](#operation/addDrainHoles)

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.add_drain_holes200_response import AddDrainHoles200Response
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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)

    try:
        # Add Drain Holes
        api_response = api_instance.add_drain_holes_deprecated()
        print("The response of ModifyingASceneDeprecatedApi->add_drain_holes_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->add_drain_holes_deprecated: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**AddDrainHoles200Response**](AddDrainHoles200Response.md)

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

# **auto_layout_deprecated**
> SceneModel auto_layout_deprecated()

Auto Layout

Deprecated. See [/scene/{scene_id}/auto-layout/](#operation/autoLayout)

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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)

    try:
        # Auto Layout
        api_response = api_instance.auto_layout_deprecated()
        print("The response of ModifyingASceneDeprecatedApi->auto_layout_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->auto_layout_deprecated: %s\n" % e)
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
**200** | Success |  -  |
**400** | ## Bad Request  The scene will not be modified if any error occurs. The response will contain an error message.  |  -  |
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auto_orient_deprecated**
> auto_orient_deprecated()

Auto Orient

Deprecated. See [/scene/{scene_id}/auto-orient/](#operation/autoOrient)

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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)

    try:
        # Auto Orient
        api_instance.auto_orient_deprecated()
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->auto_orient_deprecated: %s\n" % e)
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

# **auto_pack_deprecated**
> SceneModel auto_pack_deprecated()

Auto Pack

Deprecated. See [/scene/{scene_id}/auto-pack/](#operation/autoPack)

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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)

    try:
        # Auto Pack
        api_response = api_instance.auto_pack_deprecated()
        print("The response of ModifyingASceneDeprecatedApi->auto_pack_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->auto_pack_deprecated: %s\n" % e)
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
**200** | Success |  -  |
**400** | ## Bad Request  The scene will not be modified if any error occurs. The response will contain an error message.  |  -  |
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auto_support_deprecated**
> auto_support_deprecated()

Auto Support

Deprecated. See [/scene/{scene_id}/auto-support/](#operation/autoSupport)

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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)

    try:
        # Auto Support
        api_instance.auto_support_deprecated()
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->auto_support_deprecated: %s\n" % e)
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

# **delete_model_deprecated**
> delete_model_deprecated(id)

Delete model

Deprecated. See [/scene/{scene_id}/models/{id}/](#operation/deleteModel)

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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)
    id = 'id_example' # str | The unique identifier of the model

    try:
        # Delete model
        api_instance.delete_model_deprecated(id)
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->delete_model_deprecated: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 

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

# **duplicate_model_deprecated**
> SceneModel duplicate_model_deprecated(id)

Duplicate model

Deprecated. See [/scene/{scene_id}/models/{id}/duplicate/](#operation/duplicateModel)

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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)
    id = 'id_example' # str | The unique identifier of the model

    try:
        # Duplicate model
        api_response = api_instance.duplicate_model_deprecated(id)
        print("The response of ModifyingASceneDeprecatedApi->duplicate_model_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->duplicate_model_deprecated: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 

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
**200** | Success |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **hollow_model_deprecated**
> HollowModel200Response hollow_model_deprecated()

Hollow Model

Deprecated. See [/scene/{scene_id}/hollow/](#operation/hollowModel)

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.hollow_model200_response import HollowModel200Response
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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)

    try:
        # Hollow Model
        api_response = api_instance.hollow_model_deprecated()
        print("The response of ModifyingASceneDeprecatedApi->hollow_model_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->hollow_model_deprecated: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**HollowModel200Response**](HollowModel200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**202** | Async operation accepted |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **import_model_deprecated**
> ModelProperties import_model_deprecated()

Import model

Deprecated. See [/scene/{scene_id}/import-model/](#operation/importModel)

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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)

    try:
        # Import model
        api_response = api_instance.import_model_deprecated()
        print("The response of ModifyingASceneDeprecatedApi->import_model_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->import_model_deprecated: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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
**200** | Success |  -  |
**400** | Bad Request |  -  |
**202** | Async operation accepted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **label_part_deprecated**
> HollowModel200Response label_part_deprecated()

Label Part

Deprecated. See [/scene/{scene_id}/label/](#operation/labelPart)

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.hollow_model200_response import HollowModel200Response
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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)

    try:
        # Label Part
        api_response = api_instance.label_part_deprecated()
        print("The response of ModifyingASceneDeprecatedApi->label_part_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->label_part_deprecated: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**HollowModel200Response**](HollowModel200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**202** | Async operation accepted |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_model_deprecated**
> ReplaceModel200Response replace_model_deprecated(id)

Replace model

Deprecated. See [/scene/{scene_id}/models/{id}/replace/](#operation/replaceModel)

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.replace_model200_response import ReplaceModel200Response
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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)
    id = 'id_example' # str | The unique identifier of the model

    try:
        # Replace model
        api_response = api_instance.replace_model_deprecated(id)
        print("The response of ModifyingASceneDeprecatedApi->replace_model_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->replace_model_deprecated: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 

### Return type

[**ReplaceModel200Response**](ReplaceModel200Response.md)

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

# **scan_to_model_deprecated**
> ScanToModel200Response scan_to_model_deprecated()

Scan to model

Deprecated. See [/scene/{scene_id}/scan-to-model/](#operation/scanToModel)

### Example


```python
import formlabs_local_api
from formlabs_local_api.models.scan_to_model200_response import ScanToModel200Response
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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)

    try:
        # Scan to model
        api_response = api_instance.scan_to_model_deprecated()
        print("The response of ModifyingASceneDeprecatedApi->scan_to_model_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->scan_to_model_deprecated: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ScanToModel200Response**](ScanToModel200Response.md)

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

# **update_model_deprecated**
> update_model_deprecated(id)

Update model

Deprecated. See [/scene/{scene_id}/models/{id}/](#operation/updateModel)

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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)
    id = 'id_example' # str | The unique identifier of the model

    try:
        # Update model
        api_instance.update_model_deprecated(id)
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->update_model_deprecated: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The unique identifier of the model | 

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

# **update_scene_deprecated**
> SceneModel update_scene_deprecated()

Update Scene

Deprecated. See [/scene/{scene_id}/](#operation/updateScene)

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
    api_instance = formlabs_local_api.ModifyingASceneDeprecatedApi(api_client)

    try:
        # Update Scene
        api_response = api_instance.update_scene_deprecated()
        print("The response of ModifyingASceneDeprecatedApi->update_scene_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModifyingASceneDeprecatedApi->update_scene_deprecated: %s\n" % e)
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
**200** | Success |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

