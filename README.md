# Dynamic Window Capture for OBS

This python script allows capturing of windows in OBS that have a dynamic title. This is useful for capturing WhatsApp or other programs where you want to capture a window based on a regular expression.

This script only works on Windows.

## Installation

OBS requires you to install a compatible version of Python.

After installing Python, you will also need pywin32 which can be downloaded from [here](https://github.com/mhammond/pywin32/releases).

To install other dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Add the script to OBS.
2. Specify an executable (case insensitive) - e.g. "whatsapp.exe".
3. Provide a regular expression for the window title - e.g. ".*video call".

## License
[MIT](https://choosealicense.com/licenses/mit/)