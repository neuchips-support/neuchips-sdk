# Python API Documentation
## General

```python
neutorch.optimize(
    model,
    weight_dtype=dtype.ffp8,
    inplace=False,
    config_dir="")
```

Apply optimizations at Python frontend to the given model (nn.Module).

### Parameters
* model (<em>torch.nn.Module</em>): User model to apply optimizations on.
* weight_dtype (<em>neutorch.dtype</em>): Weight quantization data type. Default value is <code>ffp8</code>.
* inplace (<em>bool</em>):  Whether to perform inplace optimization. Default value is <code>False</code>.
* config_dir (<em>string</em>): The directory path to load previous compiled model data. Default value is <code>empty</code>.

### Returns
* Model (<em>torch.nn.Module</em>) modified according to the optimizations.

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
neutorch._C.set_device(device_list)
```
Set a list of devices for use.

### Parameters
* Device list (<em>list of strings</em>) to be used.

### Returns
* <em>None</em>

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


