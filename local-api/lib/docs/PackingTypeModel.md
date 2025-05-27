# PackingTypeModel

Different ways to pack a selection of models

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**packing_type** | **str** | The optimization strategy used for packing. Minimize the height or volume of the resulting cage, or skip packing entirely | [optional] [default to 'PACK_VOLUME']

## Example

```python
from formlabs_local_api.models.packing_type_model import PackingTypeModel

# TODO update the JSON string below
json = "{}"
# create an instance of PackingTypeModel from a JSON string
packing_type_model_instance = PackingTypeModel.from_json(json)
# print the JSON string representation of the object
print(PackingTypeModel.to_json())

# convert the object into a dict
packing_type_model_dict = packing_type_model_instance.to_dict()
# create an instance of PackingTypeModel from a dict
packing_type_model_from_dict = PackingTypeModel.from_dict(packing_type_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


