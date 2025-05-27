# GetAllScenes200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scenes** | [**List[SceneModel]**](SceneModel.md) |  | [optional] 

## Example

```python
from formlabs_local_api.models.get_all_scenes200_response import GetAllScenes200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetAllScenes200Response from a JSON string
get_all_scenes200_response_instance = GetAllScenes200Response.from_json(json)
# print the JSON string representation of the object
print(GetAllScenes200Response.to_json())

# convert the object into a dict
get_all_scenes200_response_dict = get_all_scenes200_response_instance.to_dict()
# create an instance of GetAllScenes200Response from a dict
get_all_scenes200_response_from_dict = GetAllScenes200Response.from_dict(get_all_scenes200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


