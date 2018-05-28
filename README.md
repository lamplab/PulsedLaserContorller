# Pulsed Laser Controller #

Control software for LAMP's IPG pulse lasers.

### Installation ###
1) clone repo
2) create python virtual environment: ```virtualenv env```
3) activate the virtual environment: ```source env/bin/activate```
4) install the python dependencies: ```pip install -r requirements.txt```
5) run the script: ```python test.py <power_percent> <ontime_seconds>```
6) when you're done, deactivate the virtual environment: ```deactivate```

### Usage ###
Make sure to activate your virtual environment before running the code:
```source env/bin/activate```

Command format:
```python test.py <power_percent> <ontime_seconds>```

Example:
```python test.py 40 0.05```
(turns pulsed laser on at 40% for 0.05 seconds = 50 milliseconds)

