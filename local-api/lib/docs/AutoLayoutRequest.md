# AutoLayoutRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**models** | [**ModelsSelectionModel**](ModelsSelectionModel.md) |  | [optional] 
**mode** | **str** | &#x60;\&quot;DENTAL\&quot;&#x60; mode applies algorithms used in PreForm&#39;s Dental Workspace. Leave mode unset to use algorithms from the Standard Workspace. | [optional] 
**model_spacing_mm** | **float** | Minimum (non-zero) distance between models in the scene. | [optional] 
**allow_overlapping_supports** | **bool** | Whether to allow rafts to overlap. | [optional] 
**lock_rotation** | **bool** | Whether to keep model rotation about Z fixed during layout. | [optional] 
**build_platform_2_optimized** | **bool** | Whether to optimize the build platform for two models. | [optional] 
**custom_bounds** | [**AutoLayoutRequestCustomBounds**](AutoLayoutRequestCustomBounds.md) |  | [optional] 
**seed** | **int** | 32-bit unsigned integer seed for the random number generator (0 to 2³²−1 / 4 294 967 295). When set and &#x60;models&#x60; is a list of IDs, the layout result is fully deterministic: the submission order of those IDs is preserved, and &#x60;layout_attempts&#x60; and &#x60;iterations_per_attempt&#x60; are automatically pinned to their defaults (200 and 25 000) if not provided, eliminating thread-scheduling non-determinism. When &#x60;models&#x60; is &#x60;\&quot;ALL\&quot;&#x60;, models are ordered by their model IDs, which are randomly assigned at import time, so results are not deterministic across different import sessions even with a seed.  | [optional] 
**layout_attempts** | **int** | Number of independent layout attempts to run in parallel across CPU cores. Each attempt starts from a different point in the RNG sequence, so increasing this value improves layout quality without proportionally increasing latency (compare &#x60;iterations_per_attempt&#x60;, which adds sequential work within each attempt). When &#x60;seed&#x60; is unset, results are non-deterministic regardless of this value. When &#x60;seed&#x60; is set, defaults to 200 if omitted. Maximum: 2500.  | [optional] 
**iterations_per_attempt** | **int** | Maximum number of iterations the algorithm runs within each layout attempt (sequential, within a single core; compare &#x60;layout_attempts&#x60;, which adds parallel attempts). When &#x60;seed&#x60; is unset, this parameter has no effect on determinism; results remain non-deterministic. When &#x60;seed&#x60; is set, defaults to 25 000 if omitted. Maximum: 250 000.  | [optional] 

## Example

```python
from formlabs_local_api.models.auto_layout_request import AutoLayoutRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AutoLayoutRequest from a JSON string
auto_layout_request_instance = AutoLayoutRequest.from_json(json)
# print the JSON string representation of the object
print(AutoLayoutRequest.to_json())

# convert the object into a dict
auto_layout_request_dict = auto_layout_request_instance.to_dict()
# create an instance of AutoLayoutRequest from a dict
auto_layout_request_from_dict = AutoLayoutRequest.from_dict(auto_layout_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


