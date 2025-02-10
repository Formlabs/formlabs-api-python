# AutoOrientRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**models** | [**ModelsSelectionModel**](ModelsSelectionModel.md) |  | 
**mode** | **str** | DENTAL mode applies algorithms used in PreForm&#39;s Dental Workspace | 
**tilt** | **int** | Degrees of tilt. Only applies to the DENTAL mode | [optional] 

## Example

```python
from formlabs_local_api.models.auto_orient_request import AutoOrientRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AutoOrientRequest from a JSON string
auto_orient_request_instance = AutoOrientRequest.from_json(json)
# print the JSON string representation of the object
print(AutoOrientRequest.to_json())

# convert the object into a dict
auto_orient_request_dict = auto_orient_request_instance.to_dict()
# create an instance of AutoOrientRequest from a dict
auto_orient_request_from_dict = AutoOrientRequest.from_dict(auto_orient_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


