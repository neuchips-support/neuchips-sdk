# Python API Documentation
## General

```python
neutorch.optimize(
    model,
    usage_pattern="general",
    weight_dtype=dtype.ffp8,
    inplace=False,
    config_dir="")
```

Apply optimizations at Python frontend to the given model (nn.Module).

### Parameters
* model (<em>torch.nn.Module</em>): User model to apply optimizations on.
* usage_pattern (<em>string</em>): Specifies the user scenario. The value can be either <code>general</code> for normal purposes (e.g., chat, QA) or <code>long</code> for scenarios like Retrieval-Augmented Generation (RAG), where the average input prompt is longer. This only applicable when <code>use_matrix</code> in <code>set_device</code> is <code>True</code>. Default value is <code>general</code>.
* weight_dtype (<em>neutorch.dtype</em>): Weight quantization data type. Default value is <code>ffp8</code>.
* inplace (<em>bool</em>):  Whether to perform inplace optimization. Default value is <code>False</code>.
* config_dir (<em>string</em>): The directory path to load previous compiled model data. Default value is <code>empty</code>.

### Returns
* Model (<em>torch.nn.Module</em>) modified according to the optimizations.

## Get version
```python
neutorch._C.codegen_version()
```
Get Neuchips code gneration compiler library version.

### Parameters
* <em>None</em>

### Returns
* Version (<em>string</em>)

```python
neutorch._C.host_runtime_version()
```
Get Neuchips host runtime version.

### Parameters
* <em>None</em>

### Returns
* Version (<em>string</em>)

```python
neutorch._C.target_runtime_version(device)
```
Get Neuchips target runtime version.

### Parameters
* device (<em>string</em>) to get version

### Returns
* Version (<em>string</em>)


## Device configuration
```python
neutorch._C.get_available_devices()
```
Get available devices.

### Parameters
* <em>None</em>

### Returns
* Devices (<em>list of strings</em>) which are available to use.

<br>

```python
neutorch._C.set_device(device_list, use_emb=True, use_matrix=False)
```
Set a list of devices for use and determine which engines, if any, are used for acceleration.

### Parameters
* device_list (<em>list of strings</em>): List of devices to be used.
* use_emb (<em>bool</em>): Enable embedding and vector engine acceleration. Default is <code>True</code>.
* use_matrix (<em>bool</em>): Enable matrix engine acceleration, especially for long prompts. Default is <code>False</code>.

### Returns
* <em>None</em>

</br>

```python
neutorch._C.current_using_device()
```
Get the list of devices currently in use.

### Parameters
* <em>None</em>

### Returns
* Devices (<em>list of strings</em>) that are currently being used.

<br>

```python
neutorch._C.device_info()
```
List information about all devices.

### Parameters
* <em>None</em>

### Returns
* Prints detailed device information, including chip ID, runtime version, temperature, and RAM usage.

<br>

```python
neutorch._C.using_device_info()
```
List information about the devices currently in use.

### Parameters
* <em>None</em>

### Returns
* Prints detailed information about the devices being used, including chip ID, runtime version, temperature, and RAM usage.

<br>

```python
neutorch._C.get_device_info(device_id)
```
Get the information of a specific device.

### Parameters
* device_id (<em>string</em>): The name of the device to retrieve information for.

### Returns
* **dict**: A dictionary containing the following keys:
  * **name** (<em>string</em>): The device name.
  * **runtime_version** (<em>string</em>): The runtime version of the device.
  * **temp** (<em>int</em>): The current temperature of the device.
  * **ram** (<em>dict</em>): A dictionary with the following keys:
    * **used** (<em>int</em>): The amount of RAM used by the device (in MB).
    * **total** (<em>int</em>): The total amount of RAM available on the device (in MB).

<br>

