# AutoLayoutRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**models** | [**ModelsSelectionModel**](ModelsSelectionModel.md) |  | [optional] 
**mode** | **str** | &#x60;\&quot;DENTAL\&quot;&#x60; mode applies algorithms used in PreForm&#39;s Dental Workspace. Leave mode unset to use algorithms from the Standard Workspace. | [optional] 
**model_spacing_mm** | **float** | Minimum (non-zero) distance between models in the scene. | [optional] 
**allow_overlapping_supports** | **bool** | Whether to allow rafts to overlap. | [optional] 
**lock_rotation** | **bool** | Whether to keep model rotation about Z fixed during layout. | [optional] 
**build_platform_2_optimized** | **bool** | Whether to optimize the build platform for two models. | [optional] 
**custom_bounds** | [**AutoLayoutRequestCustomBounds**](AutoLayoutRequestCustomBounds.md) |  | [optional] 

## Example

```python
from formlabs_local_api.models.auto_layout_request import AutoLayoutRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AutoLayoutRequest from a JSON string
auto_layout_request_instance = AutoLayoutRequest.from_json(json)
# print the JSON string representation of the object
print(AutoLayoutRequest.to_json())

# convert the object into a dict
auto_layout_request_dict = auto_layout_request_instance.to_dict()
# create an instance of AutoLayoutRequest from a dict
auto_layout_request_from_dict = AutoLayoutRequest.from_dict(auto_layout_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


