# PrinterCartridgeStatus


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cartridge** | [**CartridgeReadOnly**](CartridgeReadOnly.md) |  | [readonly] 
**last_modified** | **datetime** |  | [readonly] 
**cartridge_slot** | [**CartridgeSlotEnum**](CartridgeSlotEnum.md) |  | [optional] 

## Example

```python
from formlabs_web_api.models.printer_cartridge_status import PrinterCartridgeStatus

# TODO update the JSON string below
json = "{}"
# create an instance of PrinterCartridgeStatus from a JSON string
printer_cartridge_status_instance = PrinterCartridgeStatus.from_json(json)
# print the JSON string representation of the object
print(PrinterCartridgeStatus.to_json())

# convert the object into a dict
printer_cartridge_status_dict = printer_cartridge_status_instance.to_dict()
# create an instance of PrinterCartridgeStatus from a dict
printer_cartridge_status_from_dict = PrinterCartridgeStatus.from_dict(printer_cartridge_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


