# ThinWallDetectionRequestModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**models** | [**ThinWallDetectionRequestModelModels**](ThinWallDetectionRequestModelModels.md) |  | [optional] 
**threshold_mm** | **float** | Wall thickness threshold in millimeters. Regions thinner than this are flagged. Effective detection resolution is internally clamped at a floor of 0.05 mm; thresholds requesting a finer voxel grid (&#x60;threshold_mm &lt; ~0.2&#x60;) coarsen rather than blow up memory, so features thinner than 0.05 mm cannot be detected regardless of threshold.  | 

## Example

```python
from formlabs_local_api.models.thin_wall_detection_request_model import ThinWallDetectionRequestModel

# TODO update the JSON string below
json = "{}"
# create an instance of ThinWallDetectionRequestModel from a JSON string
thin_wall_detection_request_model_instance = ThinWallDetectionRequestModel.from_json(json)
# print the JSON string representation of the object
print(ThinWallDetectionRequestModel.to_json())

# convert the object into a dict
thin_wall_detection_request_model_dict = thin_wall_detection_request_model_instance.to_dict()
# create an instance of ThinWallDetectionRequestModel from a dict
thin_wall_detection_request_model_from_dict = ThinWallDetectionRequestModel.from_dict(thin_wall_detection_request_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


