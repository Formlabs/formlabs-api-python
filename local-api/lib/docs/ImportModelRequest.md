# ImportModelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file** | **str** | Full path to the file to load | 
**repair_behavior** | [**RepairBehaviorModel**](RepairBehaviorModel.md) |  | [optional] [default to RepairBehaviorModel.ERROR]
**name** | **str** | The name of the model used within job preparation. | [optional] 
**position** | [**ScenePositionModel**](ScenePositionModel.md) |  | [optional] 
**orientation** | [**OrientationModel**](OrientationModel.md) |  | [optional] 
**scale** | **float** | The scale factor to apply to the model | [optional] [default to 1]
**units** | [**ImportUnitsModel**](ImportUnitsModel.md) |  | [optional] [default to ImportUnitsModel.DETECTED]
**lock** | [**LockModel**](LockModel.md) |  | [optional] [default to LockModel.FREE]

## Example

```python
from formlabs_local_api.models.import_model_request import ImportModelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ImportModelRequest from a JSON string
import_model_request_instance = ImportModelRequest.from_json(json)
# print the JSON string representation of the object
print(ImportModelRequest.to_json())

# convert the object into a dict
import_model_request_dict = import_model_request_instance.to_dict()
# create an instance of ImportModelRequest from a dict
import_model_request_from_dict = ImportModelRequest.from_dict(import_model_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


