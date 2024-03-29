# Known issues list

## Verified environment
The SDK has been tested with the following configurations:

| OS | Kernel |
|----|--------|
| Ubuntu 22.04 LTS | 5.15.0, 5.18.17, 6.2.0 |


| CPU |
|-----|
|Intel(R) Xeon(R) w9-3475X|
|Intel(R) Core(TM) i5-14600K|
|Intel(R) Core(TM) i5-13600K|
|AMD Ryzen 7 7800X3D|
|AMD EPYC 7742|


and at least 64GB of RAM

## Hardware issues
1. When restarting your computer, you need to completely disconnect the power for 10 seconds, then turn on the computer's power, otherwise the computer may not be able to recognize the N3000 acceleration card. 

## Software issues
1. If the execution of `n3k_smu_clock` fails and the clock information cannot be read correctly, check if dmesg contains a line similar to the following:
```
Lockdown: n3k_smu_clock: direct PCI access is restricted, see man kernel_lockdown.7
```
Please try disabling the secure boot setting in the BIOS.

2. If you want to use `test_llama_for_release.py` in the repo to perform multi-threaded operations in a multi-GPU environment, remember to adjust the value of `OMP_NUM_THREADS` to avoid overusing server resources and causing a decrease in generation efficiency. (Reference: https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html)
