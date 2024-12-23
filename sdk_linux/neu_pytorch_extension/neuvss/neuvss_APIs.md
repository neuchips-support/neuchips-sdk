## Get version
```python
version = neuvss.PyNeuVssCalculator.get_version()
```
Get Neuchips VSS library version.

### Parameters
* *None*

### Returns
* version (*string*)

## Get available devices
```python
devices = neuvss.PyNeuVssCalculator.get_available_device()
```
Get available Neuchips devices.

### Parameters
* *None*

### Returns
* devices (*list of strings*) which are available to use.

## Convert database
```python
success = neuvss.PyNeuVssCalculator.convert_db(row_size, db_path, weight_dir)
```
Convert the VSS database to the weights in Neuchips format.

### Parameters
* row_size (*int*):  The length of each row in the database.
* db_path (*string*): The file path of the database.
* weight_dir (*string*): The destination directory path for the converted weight files.

### Returns
* *bool*

## Get VSS calculator
```python
vss_calc = neuvss.PyNeuVssCalculator()
```
Get VSS calculator instance.

### Parameters
* *None*

### Returns
* An instance of Neuchips VSS calculator.

## Bind device
```python
success = vss_calc.bind_device(device)
```
Bind an available device to the VSS calculator.

### Parameters
* device (*string*): The available device used to run the VSS calculation.

### Returns
* *bool*

## Initialize VSS calculator
```python
success = vss_calc.initialize(input_dim, table_dir, q_scale)
```
Initialize VSS calculator with paramters input dimension, weight tables, and scaling factor.

### Parameters
* input_dim (*int*): The input dimension. It is equal to the row size of the VSS database.
* table_dir (*string*): The directory path of the converted weight files.
* q_scale (*float*): The scaling factor. It is equal to (Input scale x Weight scale / Output scale).

### Returns
* *bool*

## Run
```python
success = vss_calc.run(input_data, output_data)
```
Run the VSS calculation.

### Parameters
* input_data (array of *int8* or *uint8*): The input array in format *int8* or *uint8*.
* output_data (array of *int8* or *uint8*): The output array in format *int8* or *uint8*.

### Returns
* *bool*
