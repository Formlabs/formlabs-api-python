# MaterialUsageModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**volume_ml** | **float** | The total volume of models and supports in the scene | 
**unsupported_volume_ml** | **float** | The total volume of all models in the scene, not including their supports | 
**total_powder_ml** | **float** |  | 
**total_powder_kg** | **float** |  | 
**total_sintered_powder_ml** | **float** |  | 
**total_sintered_powder_kg** | **float** |  | 
**mass_packing_density** | **float** |  | 

## Example

```python
from formlabs_local_api.models.material_usage_model import MaterialUsageModel

# TODO update the JSON string below
json = "{}"
# create an instance of MaterialUsageModel from a JSON string
material_usage_model_instance = MaterialUsageModel.from_json(json)
# print the JSON string representation of the object
print(MaterialUsageModel.to_json())

# convert the object into a dict
material_usage_model_dict = material_usage_model_instance.to_dict()
# create an instance of MaterialUsageModel from a dict
material_usage_model_from_dict = MaterialUsageModel.from_dict(material_usage_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


