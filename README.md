# ota_tool
- Validates firmware image (size, checksum, semantic version)
- Staged rollout with canary percentage
- Generates report JSON

## Usage
```
python3 ota.py sign build/fw.bin 1.2.3
python3 ota.py rollout build/fw.bin --canary 5 --fleet devices.txt
```
