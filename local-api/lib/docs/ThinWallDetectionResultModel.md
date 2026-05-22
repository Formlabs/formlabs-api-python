# ThinWallDetectionResultModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**per_model_results** | [**Dict[str, ThinWallDetectionResultModelPerModelResultsValue]**](ThinWallDetectionResultModelPerModelResultsValue.md) |  | [optional] 

## Example

```python
from formlabs_local_api.models.thin_wall_detection_result_model import ThinWallDetectionResultModel

# TODO update the JSON string below
json = "{}"
# create an instance of ThinWallDetectionResultModel from a JSON string
thin_wall_detection_result_model_instance = ThinWallDetectionResultModel.from_json(json)
# print the JSON string representation of the object
print(ThinWallDetectionResultModel.to_json())

# convert the object into a dict
thin_wall_detection_result_model_dict = thin_wall_detection_result_model_instance.to_dict()
# create an instance of ThinWallDetectionResultModel from a dict
thin_wall_detection_result_model_from_dict = ThinWallDetectionResultModel.from_dict(thin_wall_detection_result_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


