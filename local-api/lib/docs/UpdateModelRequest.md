# UpdateModelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the model used within job preparation. | [optional] 
**position** | [**ScenePositionModel**](ScenePositionModel.md) |  | [optional] 
**orientation** | [**OrientationModel**](OrientationModel.md) |  | [optional] 
**scale** | **float** | The scale factor to apply to the model | [optional] 
**units** | [**UnitsModel**](UnitsModel.md) |  | [optional] 
**lock** | [**LockModel**](LockModel.md) |  | [optional] [default to LockModel.FREE]

## Example

```python
from formlabs_local_api.models.update_model_request import UpdateModelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateModelRequest from a JSON string
update_model_request_instance = UpdateModelRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateModelRequest.to_json())

# convert the object into a dict
update_model_request_dict = update_model_request_instance.to_dict()
# create an instance of UpdateModelRequest from a dict
update_model_request_from_dict = UpdateModelRequest.from_dict(update_model_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


