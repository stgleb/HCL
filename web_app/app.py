import json
import pickle
import api
from flask import Flask, request, jsonify, Response
from pony.orm import db_session
from web_app.dto import ServerDTO, ComponentDTO, DriverDTO

app = Flask(__name__)


@app.route('/api/search/server', methods=['POST'])
@db_session
def list_servers():
    d = {}

    for key, value in request.form.items():
        d[key] = value

    servers = api.select_servers(**d)
    dtos = []

    for s in servers:
        dto = ServerDTO(s)
        components = ', '.join([c.name for c in s.components])
        fuel_versions = ' '.join([c.fuel_version.name for c in s.certifications])
        dto.components = components
        dto.fuel_versions = fuel_versions
        dtos.append(dto)

    resp = Response(response=json.dumps(
                    [dto.__dict__ for dto in dtos]),
                    status=200,
                    mimetype='application/json')
    return resp


@app.route('/api/server', methods=['POST'])
def add_server():
    d = {}
    for key, value in request.form.items():
        d[key] = value

    s = api.add_server(**d)

    dto = ServerDTO(s)
    components = ', '.join([c.name for c in s.components])
    fuel_versions = ' '.join([c.fuel_version.name for c in s.certifications])
    dto.components = components
    dto.fuel_versions = fuel_versions

    resp = Response(response=json.dumps(dto.__dict__),
                    status=200,
                    mimetype='application/json')
    return resp


@app.route('/api/server', methods=['PUT'])
def update_server():
    d = {}
    for key, value in request.form.items():
        d[key] = value

    s = api.update_server(**d)

    dto = ServerDTO(s)
    components = ', '.join([c.name for c in s.components])
    fuel_versions = ' '.join([c.fuel_version.name for c in s.certifications])
    dto.components = components
    dto.fuel_versions = fuel_versions

    return ""


@app.route('/api/server', methods=['DELETE'])
def delete_server():
    d = {}
    for key, value in request.form.items():
        d[key] = value

    return api.delete_server(**d)


@app.route('/api/search/driver', methods=['POST'])
def list_drivers():
    d = {}

    for key, value in request.form.items():
        d[key] = value

    drivers = api.select_driver(**d)
    dtos = []

    for d in drivers:
        dtos.append(DriverDTO(d))

    resp = Response(response=json.dumps(
                    [dto.__dict__ for dto in dtos]),
                    status=200,
                    mimetype='application/json')
    return resp


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
@db_session
def list_components():
    d = {}

    for key, value in request.form.items():
        d[key] = value

    components = api.select_components(**d)
    dtos = []

    for c in components:
        dto = ComponentDTO(c)
        fuel_versions_set = set()
        fuel_versions = ''

        for server in c.servers:
            [fuel_versions_set.add(x.fuel_version.name) for x in server.certifications]

        for fv in fuel_versions_set:
            fuel_versions += fv + ' '
        dto.fuel_versions = fuel_versions
        dtos.append(dto)

    resp = Response(response=json.dumps(
                    [dto.__dict__ for dto in dtos]),
                    status=200,
                    mimetype='application/json')
    return resp


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

