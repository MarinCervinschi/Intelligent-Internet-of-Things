# Python - Laboratory CoAP

This project is associated to the CoAP Laboratory in order to design and create a simple CoAP application emulating
an IoT scenario where a CoAP client interacts with a CoAP Coffee Machine in order to:

- Read Temperature (GET Request)
- Read the presence of a Capsule in the machine (GET Request)
- Make a default Coffee (POST Request)
- Make a custom Coffee (Short, Medium, Long) (PUT Request)

## Get Started

First, create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

Then, install the required libraries using `pip` with the `pyproject.toml` file:

```bash
pip install -e .
```

### Running the CoAP Server
Navigate to the project directory and start the CoAP server:

```bash
python coffee_machine_coap_process.py
```

### Running the CoAP Client
To test the CoAP client, navigate to the [`client`](client) folder.    
From this folder, you can directly execute client requests to interact with the CoAP Coffee Machine.
