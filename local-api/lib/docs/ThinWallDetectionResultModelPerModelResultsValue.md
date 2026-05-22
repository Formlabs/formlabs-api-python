# ThinWallDetectionResultModelPerModelResultsValue


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**has_thin_walls** | **bool** | Whether the model has any thin-wall regions below the threshold. | [optional] 
**thin_volume_mm3** | **float** | Total volume of thin-wall regions in cubic millimeters. Equals the sum of &#x60;thin_regions[].volume_mm3&#x60;. | [optional] 
**thin_region_count** | **int** | Number of distinct connected thin-wall regions. Equals &#x60;thin_regions.length&#x60;. | [optional] 
**thin_regions** | [**List[ThinWallDetectionResultModelPerModelResultsValueThinRegionsInner]**](ThinWallDetectionResultModelPerModelResultsValueThinRegionsInner.md) | Per-region breakdown, sorted by volume descending. A single aggregate &#x60;thin_volume_mm3&#x60; / &#x60;thin_region_count&#x60; hides whether &#x60;N&#x60; regions are &#x60;N&#x60; real features or &#x60;N&#x60; tiny artifacts; this array exposes the per-region volumes and bounding boxes so the client can inspect the distribution. Empty when &#x60;has_thin_walls&#x60; is false.  | [optional] 

## Example

```python
from formlabs_local_api.models.thin_wall_detection_result_model_per_model_results_value import ThinWallDetectionResultModelPerModelResultsValue

# TODO update the JSON string below
json = "{}"
# create an instance of ThinWallDetectionResultModelPerModelResultsValue from a JSON string
thin_wall_detection_result_model_per_model_results_value_instance = ThinWallDetectionResultModelPerModelResultsValue.from_json(json)
# print the JSON string representation of the object
print(ThinWallDetectionResultModelPerModelResultsValue.to_json())

# convert the object into a dict
thin_wall_detection_result_model_per_model_results_value_dict = thin_wall_detection_result_model_per_model_results_value_instance.to_dict()
# create an instance of ThinWallDetectionResultModelPerModelResultsValue from a dict
thin_wall_detection_result_model_per_model_results_value_from_dict = ThinWallDetectionResultModelPerModelResultsValue.from_dict(thin_wall_detection_result_model_per_model_results_value_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


