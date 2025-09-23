# HollowModelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**models** | [**ModelsSelectionModel**](ModelsSelectionModel.md) | A list of models to hollow | [optional] 
**wall_thickness_mm** | **float** | The desired wall thickness of the hollowed models | [optional] 
**feature_size_mm** | **float** | The size of features to keep on hollowed geometry. Higher values will produce a smoother, simpler inner hollowed surface with a less accurate thickness wall thickness around features smaller than this value. | [optional] [default to 1]
**accuracy** | **float** | The accuracy of the hollowing operation. Higher values are slower but more accurate. | [optional] [default to 0.5]

## Example

```python
from formlabs_local_api.models.hollow_model_request import HollowModelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of HollowModelRequest from a JSON string
hollow_model_request_instance = HollowModelRequest.from_json(json)
# print the JSON string representation of the object
print(HollowModelRequest.to_json())

# convert the object into a dict
hollow_model_request_dict = hollow_model_request_instance.to_dict()
# create an instance of HollowModelRequest from a dict
hollow_model_request_from_dict = HollowModelRequest.from_dict(hollow_model_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


