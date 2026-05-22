# ThinWallDetectionResultModelPerModelResultsValueThinRegionsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**volume_mm3** | **float** | Volume of this connected region in mm³. | [optional] 
**bounding_box** | [**ThinWallDetectionResultModelPerModelResultsValueThinRegionsInnerBoundingBox**](ThinWallDetectionResultModelPerModelResultsValueThinRegionsInnerBoundingBox.md) |  | [optional] 

## Example

```python
from formlabs_local_api.models.thin_wall_detection_result_model_per_model_results_value_thin_regions_inner import ThinWallDetectionResultModelPerModelResultsValueThinRegionsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ThinWallDetectionResultModelPerModelResultsValueThinRegionsInner from a JSON string
thin_wall_detection_result_model_per_model_results_value_thin_regions_inner_instance = ThinWallDetectionResultModelPerModelResultsValueThinRegionsInner.from_json(json)
# print the JSON string representation of the object
print(ThinWallDetectionResultModelPerModelResultsValueThinRegionsInner.to_json())

# convert the object into a dict
thin_wall_detection_result_model_per_model_results_value_thin_regions_inner_dict = thin_wall_detection_result_model_per_model_results_value_thin_regions_inner_instance.to_dict()
# create an instance of ThinWallDetectionResultModelPerModelResultsValueThinRegionsInner from a dict
thin_wall_detection_result_model_per_model_results_value_thin_regions_inner_from_dict = ThinWallDetectionResultModelPerModelResultsValueThinRegionsInner.from_dict(thin_wall_detection_result_model_per_model_results_value_thin_regions_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


