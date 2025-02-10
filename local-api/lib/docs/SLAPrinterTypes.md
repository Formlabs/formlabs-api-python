# SLAPrinterTypes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_print_time_s** | **float** |  | [optional] 
**preprint_time_s** | **float** |  | [optional] 
**printing_time_s** | **float** |  | [optional] 

## Example

```python
from formlabs_local_api.models.sla_printer_types import SLAPrinterTypes

# TODO update the JSON string below
json = "{}"
# create an instance of SLAPrinterTypes from a JSON string
sla_printer_types_instance = SLAPrinterTypes.from_json(json)
# print the JSON string representation of the object
print(SLAPrinterTypes.to_json())

# convert the object into a dict
sla_printer_types_dict = sla_printer_types_instance.to_dict()
# create an instance of SLAPrinterTypes from a dict
sla_printer_types_from_dict = SLAPrinterTypes.from_dict(sla_printer_types_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


