# LabelPartRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_id** | **str** | The ID of the model to label | 
**orientation** | [**OrientationModel**](OrientationModel.md) | The orientation of the label (+x left-to-right along text, +y top-to-bottom along text, +z normal to text plane). | 
**position** | [**ScenePositionModel**](ScenePositionModel.md) | The desired center point of the label | 
**label** | **str** | The label&#39;s text | 
**application_mode** | **str** |  | [optional] [default to 'EMBOSS']
**font_size_mm** | **float** | The font size of the label | 
**depth_mm** | **float** | The label&#39;s extrusion depth. This depth is a constant offset from the model&#39;s surface. | 

## Example

```python
from formlabs_local_api.models.label_part_request import LabelPartRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LabelPartRequest from a JSON string
label_part_request_instance = LabelPartRequest.from_json(json)
# print the JSON string representation of the object
print(LabelPartRequest.to_json())

# convert the object into a dict
label_part_request_dict = label_part_request_instance.to_dict()
# create an instance of LabelPartRequest from a dict
label_part_request_from_dict = LabelPartRequest.from_dict(label_part_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


