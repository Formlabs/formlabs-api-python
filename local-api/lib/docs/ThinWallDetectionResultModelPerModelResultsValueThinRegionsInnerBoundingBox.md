# ThinWallDetectionResultModelPerModelResultsValueThinRegionsInnerBoundingBox

Axis-aligned bounding box of the region in the model's physical-mm coordinates (mesh coordinates pre-multiplied by the model's mm-scale). 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**min_corner** | [**ThinWallDetectionResultModelPerModelResultsValueThinRegionsInnerBoundingBoxMinCorner**](ThinWallDetectionResultModelPerModelResultsValueThinRegionsInnerBoundingBoxMinCorner.md) |  | [optional] 
**max_corner** | [**ThinWallDetectionResultModelPerModelResultsValueThinRegionsInnerBoundingBoxMinCorner**](ThinWallDetectionResultModelPerModelResultsValueThinRegionsInnerBoundingBoxMinCorner.md) |  | [optional] 

## Example

```python
from formlabs_local_api.models.thin_wall_detection_result_model_per_model_results_value_thin_regions_inner_bounding_box import ThinWallDetectionResultModelPerModelResultsValueThinRegionsInnerBoundingBox

# TODO update the JSON string below
json = "{}"
# create an instance of ThinWallDetectionResultModelPerModelResultsValueThinRegionsInnerBoundingBox from a JSON string
thin_wall_detection_result_model_per_model_results_value_thin_regions_inner_bounding_box_instance = ThinWallDetectionResultModelPerModelResultsValueThinRegionsInnerBoundingBox.from_json(json)
# print the JSON string representation of the object
print(ThinWallDetectionResultModelPerModelResultsValueThinRegionsInnerBoundingBox.to_json())

# convert the object into a dict
thin_wall_detection_result_model_per_model_results_value_thin_regions_inner_bounding_box_dict = thin_wall_detection_result_model_per_model_results_value_thin_regions_inner_bounding_box_instance.to_dict()
# create an instance of ThinWallDetectionResultModelPerModelResultsValueThinRegionsInnerBoundingBox from a dict
thin_wall_detection_result_model_per_model_results_value_thin_regions_inner_bounding_box_from_dict = ThinWallDetectionResultModelPerModelResultsValueThinRegionsInnerBoundingBox.from_dict(thin_wall_detection_result_model_per_model_results_value_thin_regions_inner_bounding_box_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


