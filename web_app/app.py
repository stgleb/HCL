import api
from flask import Flask, request

app = Flask(__name__)


@app.route('/api/search/server', methods=['POST'])
def list_servers():
    print request.form


@app.route('/api/server', methods=['POST'])
def add_server():
    print request.form.items()
    return ""


@app.route('/api/server', methods=['PUT'])
def update_server():
    pass


@app.route('/api/server', methods=['DELETE'])
def delete_server():
    pass


@app.route('/api/search/driver', methods=['POST'])
def list_drivers():

    d = {}

    for key, value in request.form.items():
        d[key] = value

    drivers = api.select_driver(**d)
    print drivers


@app.route('/api/driver', methods=['POST'])
def add_driver():
    pass


@app.route('/api/fuel/driver', methods=['POST'])
def add_driver_to_fuel():
    pass


@app.route('/api/fuel', methods=['POST'])
def add_fuel_version():
    pass


@app.route('/api/search/component', methods=['POST'])
def list_components():
    pass


@app.route('/api/component', methods=['POST'])
def add_component():
    pass


@app.route('/api/component', methods=['PUT'])
def update_component():
    pass


@app.route('/api/fuel/driver', methods=['delete'])
def delete_component():
    pass


@app.route('/api/certification', methods=['POST'])
def add_certification():
    pass

if __name__ == '__main__':
    app.run()

