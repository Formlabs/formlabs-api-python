# SaveScreenshotRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file** | **str** | The file path to save the .png screenshot to | 
**view_type** | **str** | The type of view to use when taking the screenshot | [optional] [default to 'ZOOM_ON_MODELS']
**yaw** | **float** | Yaw rotation in degrees for the camera&#39;s view, where 0º looks down the negative X-axis | [optional] [default to 45.0]
**pitch** | **float** | Pitch rotation in degrees for the camera&#39;s view, where 0º looks flat from the horizon and positive angles look down on models (in SLA scenes, toward the build platform) | [optional] [default to 35.264]
**image_size_px** | **int** | Size of the largest dimension of the exported image in pixels. | [optional] [default to 820]
**crop_to_models** | **bool** | If the screenshot view should be sized and cropped so the models take up most of the frame. If false, the zooming will be the same for all viewing angles. | [optional] [default to True]
**models** | [**ModelsSelectionModel**](ModelsSelectionModel.md) |  | [optional] 

## Example

```python
from formlabs_local_api.models.save_screenshot_request import SaveScreenshotRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SaveScreenshotRequest from a JSON string
save_screenshot_request_instance = SaveScreenshotRequest.from_json(json)
# print the JSON string representation of the object
print(SaveScreenshotRequest.to_json())

# convert the object into a dict
save_screenshot_request_dict = save_screenshot_request_instance.to_dict()
# create an instance of SaveScreenshotRequest from a dict
save_screenshot_request_from_dict = SaveScreenshotRequest.from_dict(save_screenshot_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


