# PackAndCageRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**models** | [**ModelsSelectionModel**](ModelsSelectionModel.md) |  | 
**packing_type** | [**PackingTypeModel**](PackingTypeModel.md) |  | [optional] 
**cage_label** | **str** | The label engraved on the part cage. | [optional] 
**generate_mesh_label** | **bool** | Whether or not to physically emboss the label of the part cage | [optional] 
**model_spacing_mm** | **float** | Minimum distance between models in the cage. | [optional] 
**bar_spacing_mm** | **float** | Space between the bars of the cage | [optional] 
**bar_thickness_mm** | **float** | The space between the bars of the cage | [optional] 
**bar_width_mm** | **float** | Width of the bars of the cage. Defaults to the same as bar_thickness_mm | [optional] 
**distance_to_cage_mm** | **float** | Extra space between the models and the cage walls | [optional] 
**enable_round_edges** | **bool** | Rounds the edges of external cage corners | [optional] [default to False]
**enable_square_bars** | **bool** | Generate square bars for the cage | [optional] [default to True]

## Example

```python
from formlabs_local_api.models.pack_and_cage_request import PackAndCageRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PackAndCageRequest from a JSON string
pack_and_cage_request_instance = PackAndCageRequest.from_json(json)
# print the JSON string representation of the object
print(PackAndCageRequest.to_json())

# convert the object into a dict
pack_and_cage_request_dict = pack_and_cage_request_instance.to_dict()
# create an instance of PackAndCageRequest from a dict
pack_and_cage_request_from_dict = PackAndCageRequest.from_dict(pack_and_cage_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


