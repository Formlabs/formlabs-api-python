# SLSPrinterTypes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_print_time_s** | **float** |  | [optional] 
**preprint_time_s** | **float** |  | [optional] 
**printing_time_s** | **float** |  | [optional] 
**cool_to_removal_time_s** | **float** | Time it takes to cool the build chamber to around 100°C when it can be removed from the printer. | [optional] 
**additional_cool_to_room_temp_time_s** | **float** | Time it takes to cool the build from around 100°C to nearly room temperature while inside of the printer. | [optional] 

## Example

```python
from formlabs_local_api.models.sls_printer_types import SLSPrinterTypes

# TODO update the JSON string below
json = "{}"
# create an instance of SLSPrinterTypes from a JSON string
sls_printer_types_instance = SLSPrinterTypes.from_json(json)
# print the JSON string representation of the object
print(SLSPrinterTypes.to_json())

# convert the object into a dict
sls_printer_types_dict = sls_printer_types_instance.to_dict()
# create an instance of SLSPrinterTypes from a dict
sls_printer_types_from_dict = SLSPrinterTypes.from_dict(sls_printer_types_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


