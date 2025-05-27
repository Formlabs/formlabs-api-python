# SceneModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**models** | [**List[ModelProperties]**](ModelProperties.md) |  | [optional] 
**scene_settings** | [**SceneTypeModel**](SceneTypeModel.md) |  | [optional] 
**material_usage** | [**MaterialUsageModel**](MaterialUsageModel.md) |  | [optional] 
**layer_count** | **int** | The number of layers in the scene | [optional] 
**id** | **str** | The ID of the created scene | [optional] 

## Example

```python
from formlabs_local_api.models.scene_model import SceneModel

# TODO update the JSON string below
json = "{}"
# create an instance of SceneModel from a JSON string
scene_model_instance = SceneModel.from_json(json)
# print the JSON string representation of the object
print(SceneModel.to_json())

# convert the object into a dict
scene_model_dict = scene_model_instance.to_dict()
# create an instance of SceneModel from a dict
scene_model_from_dict = SceneModel.from_dict(scene_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


