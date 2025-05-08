# RESTful HTTP API Laboratory - Python

## IoT Inventory

This project shows a demo implementation of a simple IoT device inventory through an HTTP RESTful API.

The implementation is based on the following Python Frameworks 

- Flask: https://flask.palletsprojects.com/en/2.0.x/
- Flask RESTful: https://flask-restful.readthedocs.io/en/latest/index.html

APIs are exposed through a configurable port (7070) and accessible locally at: http://127.0.0.1:7070/api/iot/inventory

## Modeled REST Resources

The IoT Inventory resources currently modeled are:

- Device (/device): A generic representation of an IoT device with basic information and customizable attributes. 
In the current implementation device's data are not handled and they are out of the scope of the demo inventory.

## Project Structure
The project structure is as follows:

```text
.
├── README.md
├── app.py
├── model
│   └── device_model.py
├── persistence
│   └── data_manager.py
├── requirements.txt
├── .flaskenv.example
├── resources
│   ├── device_resource.py
│   └── devices_resource.py
└── run.sh

4 directories, 9 files
```

## To set up the python environment

There is a run.sh script that can be used to set up the python environment and run the application. See [run.sh](run.sh) for more details.
```bash
chmod +x run.sh
./run.sh
```
This script automates the setup process by performing the following steps:

1. Creates a virtual environment for the project.
2. Installs all required dependencies listed in `requirements.txt`.
3. Generates a `.flaskenv` file from the `.flaskenv.example` template. You can customize the `.flaskenv.example` file to define your own environment variables.
4. Launches the application.

## To run the application

To only run the application, you can use the following command:
```bash
flask run
```
This command will start the Flask development server, and you can access the API at http://127.0.0.1:7070/api/iot/inventory.
