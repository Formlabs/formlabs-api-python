# CartridgeReadOnly


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**serial** | **str** |  | [readonly] 
**material** | **str** |  | [readonly] 
**consumable_type** | **str** |  | [readonly] 
**initial_volume_ml** | **float** |  | [readonly] 
**volume_dispensed_ml** | **float** |  | [readonly] 
**display_name** | **str** |  | [optional] 
**is_empty** | **bool** |  | [readonly] 
**inside_printer** | **str** |  | [readonly] 
**connected_group** | **str** |  | [readonly] 
**created_at** | **datetime** |  | [readonly] 
**last_print_date** | **datetime** |  | [readonly] 
**machine_type_id** | **str** |  | [readonly] 

## Example

```python
from formlabs_web_api.models.cartridge_read_only import CartridgeReadOnly

# TODO update the JSON string below
json = "{}"
# create an instance of CartridgeReadOnly from a JSON string
cartridge_read_only_instance = CartridgeReadOnly.from_json(json)
# print the JSON string representation of the object
print(CartridgeReadOnly.to_json())

# convert the object into a dict
cartridge_read_only_dict = cartridge_read_only_instance.to_dict()
# create an instance of CartridgeReadOnly from a dict
cartridge_read_only_from_dict = CartridgeReadOnly.from_dict(cartridge_read_only_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


