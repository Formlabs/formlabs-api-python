# PrintRunWithFleetControlData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**guid** | **str** |  | 
**name** | **str** |  | 
**printer** | **str** |  | [readonly] 
**status** | [**StatusEnum**](StatusEnum.md) |  | [readonly] 
**using_open_mode** | **bool** |  | [readonly] 
**z_height_offset_mm** | **float** |  | [readonly] 
**print_started_at** | **datetime** |  | [readonly] 
**print_finished_at** | **datetime** |  | [readonly] 
**layer_count** | **int** |  | [readonly] 
**volume_ml** | **float** |  | [readonly] 
**material** | **str** |  | [readonly] 
**layer_thickness_mm** | **float** |  | [readonly] 
**currently_printing_layer** | **int** |  | [readonly] 
**estimated_duration_ms** | **int** |  | [readonly] 
**elapsed_duration_ms** | **int** |  | [readonly] 
**estimated_time_remaining_ms** | **int** |  | [readonly] 
**created_at** | **datetime** |  | [readonly] 
**print_run_success** | [**PrintRunSuccess**](PrintRunSuccess.md) |  | [readonly] 
**firmware_version** | **str** |  | [readonly] 
**cartridge** | **str** |  | [readonly] 
**front_cartridge** | **str** |  | [readonly] 
**back_cartridge** | **str** |  | [readonly] 
**tank** | **str** |  | [readonly] 
**cylinder** | **str** |  | [readonly] 
**note** | [**PrintRunNote**](PrintRunNote.md) |  | [readonly] 
**print_thumbnail** | [**PrintThumbnailSerializerOnlyThumbnail**](PrintThumbnailSerializerOnlyThumbnail.md) |  | [readonly] 
**post_print_photo_url** | **str** |  | [readonly] 
**user** | [**BasicUser**](BasicUser.md) |  | [readonly] 
**user_custom_label** | **str** |  | [readonly] 
**group** | [**PrinterGroup**](PrinterGroup.md) |  | [readonly] 
**adaptive_thickness** | **bool** |  | [readonly] 
**message** | **str** |  | [readonly] 
**print_job** | **str** |  | [readonly] 
**material_name** | **str** |  | [readonly] 
**print_settings_name** | **str** |  | [readonly] 
**print_settings_code** | **str** |  | [readonly] 
**cloud_queue_item** | **Dict[str, object]** |  | [readonly] 
**form_auto_serial** | **str** |  | [readonly] 
**form_auto_fw_version** | **str** |  | [readonly] 
**harvest_status** | [**HarvestStatusEnum**](HarvestStatusEnum.md) |  | [readonly] 
**parts** | [**List[PrintPart]**](PrintPart.md) |  | [readonly] 

## Example

```python
from formlabs_web_api.models.print_run_with_fleet_control_data import PrintRunWithFleetControlData

# TODO update the JSON string below
json = "{}"
# create an instance of PrintRunWithFleetControlData from a JSON string
print_run_with_fleet_control_data_instance = PrintRunWithFleetControlData.from_json(json)
# print the JSON string representation of the object
print(PrintRunWithFleetControlData.to_json())

# convert the object into a dict
print_run_with_fleet_control_data_dict = print_run_with_fleet_control_data_instance.to_dict()
# create an instance of PrintRunWithFleetControlData from a dict
print_run_with_fleet_control_data_from_dict = PrintRunWithFleetControlData.from_dict(print_run_with_fleet_control_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


