# PyOG

A python library for interfacing with OutGauge in a (hopefully) simple way.

Designed for WinPython 3.11, but should run on most past Python versions.


### Usage
1. Clone the project
  * `git clone https://github.com/jeepracer98/pyog.git`
2. Change directory to the top level folder of `pyog`
  * `cd pyog`
3. Create and activate a virtual enviroment (recommended)
  * `python3 -m venv win-venv`
  * `win-venv\Scripts\activate`
4. Install `pyog` with pip
  * `python3 -m pip install -e .`
  * This will only work if you are in the `pyog` folder where `setup.py` is.
5. If you plan to be commiting to the `pyog` project, install pre-commit with:
  * `python3 -m pip install -r requirements-dev.txt`
  * `pre-commit install`

Then you can integrate `pyog` into programs by opening the socket and reading data from
it. Here's a simple example which will keep trying to read data until you press Ctrl+C.
```python
import pyog

IP = "127.0.0.1"
PORT = 4444

with pyog.create_socket(IP, PORT) as sock:
    while True:
        print(pyog.read_outgauge_data(sock))
```
