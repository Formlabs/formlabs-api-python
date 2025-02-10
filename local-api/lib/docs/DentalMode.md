# DentalMode


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**models** | [**ModelsSelectionModel**](ModelsSelectionModel.md) |  | 
**mode** | **str** | DENTAL mode applies algorithms used in PreForm&#39;s Dental Workspace | 
**tilt** | **int** | Degrees of tilt. Only applies to the DENTAL mode | [optional] 

## Example

```python
from formlabs_local_api.models.dental_mode import DentalMode

# TODO update the JSON string below
json = "{}"
# create an instance of DentalMode from a JSON string
dental_mode_instance = DentalMode.from_json(json)
# print the JSON string representation of the object
print(DentalMode.to_json())

# convert the object into a dict
dental_mode_dict = dental_mode_instance.to_dict()
# create an instance of DentalMode from a dict
dental_mode_from_dict = DentalMode.from_dict(dental_mode_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


