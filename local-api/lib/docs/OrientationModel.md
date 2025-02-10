# OrientationModel

The orientation of the model in the scene. It can be specified using one of the following: Euler angles, a transform matrix, or direction vectors. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**x** | **float** | Rotation in degrees around the x axis (applied second) | 
**y** | **float** | Rotation in degrees around the y axis (applied last) | 
**z** | **float** | Rotation in degrees around the z axis (applied first) | 
**linear** | **List[List[float]]** |  | 
**z_direction** | **List[float]** | 3D unit vector in model space saying which piece of the model will point \&quot;up\&quot; in scene space.  | 
**x_direction** | **List[float]** | 3D unit vector in model space, perpendicular to Z direction, saying which piece of the model will point \&quot;right\&quot; in scene space.  | 

## Example

```python
from formlabs_local_api.models.orientation_model import OrientationModel

# TODO update the JSON string below
json = "{}"
# create an instance of OrientationModel from a JSON string
orientation_model_instance = OrientationModel.from_json(json)
# print the JSON string representation of the object
print(OrientationModel.to_json())

# convert the object into a dict
orientation_model_dict = orientation_model_instance.to_dict()
# create an instance of OrientationModel from a dict
orientation_model_from_dict = OrientationModel.from_dict(orientation_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


