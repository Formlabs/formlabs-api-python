# formlabs_web_api.PrintsApi

All URIs are relative to *https://api.formlabs.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**printers_prints_list**](PrintsApi.md#printers_prints_list) | **GET** /developer/v1/printers/{printer_serial}/prints/ | 
[**prints_list**](PrintsApi.md#prints_list) | **GET** /developer/v1/prints/ | 


# **printers_prints_list**
> PaginatedPrintRunWithFleetControlDataList printers_prints_list(printer_serial, var_date=var_date, date__gt=date__gt, date__lt=date__lt, machine_type_id=machine_type_id, material=material, name=name, page=page, per_page=per_page, printer=printer, status=status)



List of all prints associated with my account

### Example

* Bearer Authentication (bearerAuth):

```python
import formlabs_web_api
from formlabs_web_api.models.paginated_print_run_with_fleet_control_data_list import PaginatedPrintRunWithFleetControlDataList
from formlabs_web_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.formlabs.com
# See configuration.py for a list of all supported configuration parameters.
configuration = formlabs_web_api.Configuration(
    host = "https://api.formlabs.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = formlabs_web_api.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with formlabs_web_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = formlabs_web_api.PrintsApi(api_client)
    printer_serial = 'printer_serial_example' # str | 
    var_date = '2013-10-20T19:20:30+01:00' # datetime | Filter by date time (ISO 8601 Format)  (optional)
    date__gt = '2013-10-20T19:20:30+01:00' # datetime | Filter by date time greater than date time specified (ISO 8601 Format) (optional)
    date__lt = '2013-10-20T19:20:30+01:00' # datetime | Filter by date time less than date time specified (ISO 8601 Format) (optional)
    machine_type_id = ['machine_type_id_example'] # List[str] | Filter by machine type id. (optional)
    material = 'material_example' # str |  (optional)
    name = 'name_example' # str | Filter by name of the print (Substring Match) (optional)
    page = 56 # int | A page number within the paginated result set. (optional)
    per_page = 56 # int | Number of results to return per page. (optional)
    printer = 'printer_example' # str | Filter by printer serial (optional)
    status = 'status_example' # str | Filter by status of the print. Possible values are:           * `QUEUED` - Queued           * `PREPRINT` - Preprint           * `PRINTING` - Printing           * `PAUSING` - Pausing           * `PAUSED` - Paused           * `FINISHED` - Finished           * `ABORTING` - Aborting           * `ABORTED` - Aborted           * `ERROR` - Error           * `WAITING_FOR_RESOLUTION` - Waiting for Resolution           * `PREHEAT` - Preheat           * `PRECOAT` - Precoat           * `POSTCOAT` - Postcoat (optional)

    try:
        api_response = api_instance.printers_prints_list(printer_serial, var_date=var_date, date__gt=date__gt, date__lt=date__lt, machine_type_id=machine_type_id, material=material, name=name, page=page, per_page=per_page, printer=printer, status=status)
        print("The response of PrintsApi->printers_prints_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PrintsApi->printers_prints_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **printer_serial** | **str**|  | 
 **var_date** | **datetime**| Filter by date time (ISO 8601 Format)  | [optional] 
 **date__gt** | **datetime**| Filter by date time greater than date time specified (ISO 8601 Format) | [optional] 
 **date__lt** | **datetime**| Filter by date time less than date time specified (ISO 8601 Format) | [optional] 
 **machine_type_id** | [**List[str]**](str.md)| Filter by machine type id. | [optional] 
 **material** | **str**|  | [optional] 
 **name** | **str**| Filter by name of the print (Substring Match) | [optional] 
 **page** | **int**| A page number within the paginated result set. | [optional] 
 **per_page** | **int**| Number of results to return per page. | [optional] 
 **printer** | **str**| Filter by printer serial | [optional] 
 **status** | **str**| Filter by status of the print. Possible values are:           * &#x60;QUEUED&#x60; - Queued           * &#x60;PREPRINT&#x60; - Preprint           * &#x60;PRINTING&#x60; - Printing           * &#x60;PAUSING&#x60; - Pausing           * &#x60;PAUSED&#x60; - Paused           * &#x60;FINISHED&#x60; - Finished           * &#x60;ABORTING&#x60; - Aborting           * &#x60;ABORTED&#x60; - Aborted           * &#x60;ERROR&#x60; - Error           * &#x60;WAITING_FOR_RESOLUTION&#x60; - Waiting for Resolution           * &#x60;PREHEAT&#x60; - Preheat           * &#x60;PRECOAT&#x60; - Precoat           * &#x60;POSTCOAT&#x60; - Postcoat | [optional] 

### Return type

[**PaginatedPrintRunWithFleetControlDataList**](PaginatedPrintRunWithFleetControlDataList.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **prints_list**
> PaginatedPrintRunWithFleetControlDataList prints_list(var_date=var_date, date__gt=date__gt, date__lt=date__lt, machine_type_id=machine_type_id, material=material, name=name, page=page, per_page=per_page, printer=printer, status=status)



List of all prints associated with my account

### Example

* Bearer Authentication (bearerAuth):

```python
import formlabs_web_api
from formlabs_web_api.models.paginated_print_run_with_fleet_control_data_list import PaginatedPrintRunWithFleetControlDataList
from formlabs_web_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.formlabs.com
# See configuration.py for a list of all supported configuration parameters.
configuration = formlabs_web_api.Configuration(
    host = "https://api.formlabs.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = formlabs_web_api.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with formlabs_web_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = formlabs_web_api.PrintsApi(api_client)
    var_date = '2013-10-20T19:20:30+01:00' # datetime | Filter by date time (ISO 8601 Format)  (optional)
    date__gt = '2013-10-20T19:20:30+01:00' # datetime | Filter by date time greater than date time specified (ISO 8601 Format) (optional)
    date__lt = '2013-10-20T19:20:30+01:00' # datetime | Filter by date time less than date time specified (ISO 8601 Format) (optional)
    machine_type_id = ['machine_type_id_example'] # List[str] | Filter by machine type id. (optional)
    material = 'material_example' # str |  (optional)
    name = 'name_example' # str | Filter by name of the print (Substring Match) (optional)
    page = 56 # int | A page number within the paginated result set. (optional)
    per_page = 56 # int | Number of results to return per page. (optional)
    printer = 'printer_example' # str | Filter by printer serial (optional)
    status = 'status_example' # str | Filter by status of the print. Possible values are:           * `QUEUED` - Queued           * `PREPRINT` - Preprint           * `PRINTING` - Printing           * `PAUSING` - Pausing           * `PAUSED` - Paused           * `FINISHED` - Finished           * `ABORTING` - Aborting           * `ABORTED` - Aborted           * `ERROR` - Error           * `WAITING_FOR_RESOLUTION` - Waiting for Resolution           * `PREHEAT` - Preheat           * `PRECOAT` - Precoat           * `POSTCOAT` - Postcoat (optional)

    try:
        api_response = api_instance.prints_list(var_date=var_date, date__gt=date__gt, date__lt=date__lt, machine_type_id=machine_type_id, material=material, name=name, page=page, per_page=per_page, printer=printer, status=status)
        print("The response of PrintsApi->prints_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PrintsApi->prints_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **var_date** | **datetime**| Filter by date time (ISO 8601 Format)  | [optional] 
 **date__gt** | **datetime**| Filter by date time greater than date time specified (ISO 8601 Format) | [optional] 
 **date__lt** | **datetime**| Filter by date time less than date time specified (ISO 8601 Format) | [optional] 
 **machine_type_id** | [**List[str]**](str.md)| Filter by machine type id. | [optional] 
 **material** | **str**|  | [optional] 
 **name** | **str**| Filter by name of the print (Substring Match) | [optional] 
 **page** | **int**| A page number within the paginated result set. | [optional] 
 **per_page** | **int**| Number of results to return per page. | [optional] 
 **printer** | **str**| Filter by printer serial | [optional] 
 **status** | **str**| Filter by status of the print. Possible values are:           * &#x60;QUEUED&#x60; - Queued           * &#x60;PREPRINT&#x60; - Preprint           * &#x60;PRINTING&#x60; - Printing           * &#x60;PAUSING&#x60; - Pausing           * &#x60;PAUSED&#x60; - Paused           * &#x60;FINISHED&#x60; - Finished           * &#x60;ABORTING&#x60; - Aborting           * &#x60;ABORTED&#x60; - Aborted           * &#x60;ERROR&#x60; - Error           * &#x60;WAITING_FOR_RESOLUTION&#x60; - Waiting for Resolution           * &#x60;PREHEAT&#x60; - Preheat           * &#x60;PRECOAT&#x60; - Precoat           * &#x60;POSTCOAT&#x60; - Postcoat | [optional] 

### Return type

[**PaginatedPrintRunWithFleetControlDataList**](PaginatedPrintRunWithFleetControlDataList.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

