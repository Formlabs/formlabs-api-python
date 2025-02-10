# SLA


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**volume_ml** | **float** | The total volume of models and supports in the scene | 
**unsupported_volume_ml** | **float** | The total volume of all models in the scene, not including their supports | 

## Example

```python
from formlabs_local_api.models.sla import SLA

# TODO update the JSON string below
json = "{}"
# create an instance of SLA from a JSON string
sla_instance = SLA.from_json(json)
# print the JSON string representation of the object
print(SLA.to_json())

# convert the object into a dict
sla_dict = sla_instance.to_dict()
# create an instance of SLA from a dict
sla_from_dict = SLA.from_dict(sla_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


