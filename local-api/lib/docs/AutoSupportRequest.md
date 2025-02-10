# AutoSupportRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**models** | [**ModelsSelectionModel**](ModelsSelectionModel.md) |  | 
**density** | **float** | Unitless factor to adjust the density of supports (default is 1.0) | [optional] 
**slope_multiplier** | **float** | Unitless factor to increase or decrease support density on steep slopes (default is 1.0) | [optional] 
**only_minima** | **bool** | Whether to only generate touchpoints on local minima, skipping all other supports. Default is false. | [optional] 
**raft_type** | **str** | The type of raft to apply to the models | [optional] 
**raft_label_enabled** | **bool** | Whether to enable raft labeling | [optional] 
**breakaway_structure_enabled** | **bool** | Whether to enable breakaway structure | [optional] 
**touchpoint_size_mm** | **float** | The size of the touchpoints | [optional] 
**internal_supports_enabled** | **bool** | Whether to enable internal supports | [optional] 
**raft_thickness_mm** | **float** | The thickness of the raft | [optional] 
**height_above_raft_mm** | **float** |  | [optional] 
**z_compression_correction_mm** | **float** |  | [optional] 
**early_layer_merge_mm** | **float** |  | [optional] 

## Example

```python
from formlabs_local_api.models.auto_support_request import AutoSupportRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AutoSupportRequest from a JSON string
auto_support_request_instance = AutoSupportRequest.from_json(json)
# print the JSON string representation of the object
print(AutoSupportRequest.to_json())

# convert the object into a dict
auto_support_request_dict = auto_support_request_instance.to_dict()
# create an instance of AutoSupportRequest from a dict
auto_support_request_from_dict = AutoSupportRequest.from_dict(auto_support_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


