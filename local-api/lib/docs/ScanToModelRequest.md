# ScanToModelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file** | **str** | Full path to the file to load | 
**units** | [**ImportUnitsModel**](ImportUnitsModel.md) |  | [optional] [default to ImportUnitsModel.DETECTED]
**cutoff_height_mm** | **float** | Remove all scan data below this height (in mm) from the model, replace with extrude from the bottom of the model. | 
**extrude_distance_mm** | **float** | Extrude this distance (in mm) from the removed bottom of the model. Default is 0mm. | [optional] 
**hollow** | **bool** | Whether to hollow the model and fill in with a honeycomb infill. | [optional] 
**cutoff_below_gumline_mm** | **float** | Remove all scan data below this height (in mm) from the model, relative to the gumline, replace with extrude from the bottom of the model. | [optional] 
**shell_thickness_mm** | **float** | The thickness of the outer shell of the model, in mm. Requires hollow&#x3D;true. | [optional] 
**wall_thickness_mm** | **float** | The thickness of the honeycomb infill of the model, in mm. Requires hollow&#x3D;true. | [optional] 
**drain_hole_radius_mm** | **float** | The radius of drain holes in the model, in mm. Requires hollow&#x3D;true. | [optional] [default to 1.5]
**drain_hole_height_ratio** | **float** | The ratio of the height of the drain hole to the width of the drain hole. Requires hollow&#x3D;true. | [optional] [default to 1]

## Example

```python
from formlabs_local_api.models.scan_to_model_request import ScanToModelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ScanToModelRequest from a JSON string
scan_to_model_request_instance = ScanToModelRequest.from_json(json)
# print the JSON string representation of the object
print(ScanToModelRequest.to_json())

# convert the object into a dict
scan_to_model_request_dict = scan_to_model_request_instance.to_dict()
# create an instance of ScanToModelRequest from a dict
scan_to_model_request_from_dict = ScanToModelRequest.from_dict(scan_to_model_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


