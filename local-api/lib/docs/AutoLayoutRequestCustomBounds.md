# AutoLayoutRequestCustomBounds

Bounds to keep selected models inside in the layout operation (default is the maximum that will fit on the build platform)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**x_min_mm** | **float** |  | [optional] 
**x_max_mm** | **float** |  | [optional] 
**y_min_mm** | **float** |  | [optional] 
**y_max_mm** | **float** |  | [optional] 

## Example

```python
from formlabs_local_api.models.auto_layout_request_custom_bounds import AutoLayoutRequestCustomBounds

# TODO update the JSON string below
json = "{}"
# create an instance of AutoLayoutRequestCustomBounds from a JSON string
auto_layout_request_custom_bounds_instance = AutoLayoutRequestCustomBounds.from_json(json)
# print the JSON string representation of the object
print(AutoLayoutRequestCustomBounds.to_json())

# convert the object into a dict
auto_layout_request_custom_bounds_dict = auto_layout_request_custom_bounds_instance.to_dict()
# create an instance of AutoLayoutRequestCustomBounds from a dict
auto_layout_request_custom_bounds_from_dict = AutoLayoutRequestCustomBounds.from_dict(auto_layout_request_custom_bounds_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


