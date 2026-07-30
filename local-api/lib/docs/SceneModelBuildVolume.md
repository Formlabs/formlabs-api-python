# SceneModelBuildVolume

The build volume geometry for this scene's printer and material.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimensions_mm** | [**SceneModelBuildVolumeDimensionsMm**](SceneModelBuildVolumeDimensionsMm.md) |  | 
**fillet_radius_mm** | **float** | Corner fillet radius of the build volume in millimeters. Non-zero for SLS printers with a rounded build volume. | 

## Example

```python
from formlabs_local_api.models.scene_model_build_volume import SceneModelBuildVolume

# TODO update the JSON string below
json = "{}"
# create an instance of SceneModelBuildVolume from a JSON string
scene_model_build_volume_instance = SceneModelBuildVolume.from_json(json)
# print the JSON string representation of the object
print(SceneModelBuildVolume.to_json())

# convert the object into a dict
scene_model_build_volume_dict = scene_model_build_volume_instance.to_dict()
# create an instance of SceneModelBuildVolume from a dict
scene_model_build_volume_from_dict = SceneModelBuildVolume.from_dict(scene_model_build_volume_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


