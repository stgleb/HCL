import traceback
import json
import api
from flask import Flask, request, jsonify, Response, render_template
from pony.orm import db_session
from web_app.dto import ServerDTO, ComponentDTO, DriverDTO, FuelVersionDTO, CertificationDTO, TypeDTO

app = Flask(__name__)


@app.route('/api/search/server', methods=['POST'])
@db_session
def list_servers():
    d = json.loads(request.data)

    try:
        servers = api.select_servers(**d)
    except Exception:
        traceback.print_exception()

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
    d = json.loads(request.data)

    try:
        s = api.add_server(**d)
    except Exception:
        traceback.print_stack()

    dto = ServerDTO(s)
    components = ', '.join([c.name for c in s.components])
    fuel_versions = ' '.join([c.fuel_version.name for c in s.certifications])
    dto.components = components
    dto.fuel_versions = fuel_versions

    resp = Response(response=json.dumps(dto.__dict__),
                    status=202,
                    mimetype='application/json')
    return resp


@app.route('/api/server', methods=['PUT'])
@db_session
def update_server():
    d = json.loads(request.data)

    try:
        s = api.update_server(**d)
    except Exception:
        traceback.print_stack()

    dto = ServerDTO(s)
    components = ', '.join([c.name for c in s.components])
    fuel_versions = ' '.join([c.fuel_version.name for c in s.certifications])
    dto.components = components
    dto.fuel_versions = fuel_versions

    resp = Response(response=json.dumps(dto.__dict__),
                status=202,
                mimetype='application/json')

    return resp


@app.route('/api/server', methods=['DELETE'])
@db_session
def delete_server():
    d = json.loads(request.data)

    try:
        message = api.delete_server(**d)
    except Exception:
        traceback.print_stack()

    resp = Response(response=json.dumps(message),
                    status=202,
                    mimetype='application/json')
    return resp


@app.route('/api/search/driver', methods=['POST'])
@db_session
def list_drivers():
    d = json.loads(request.data)

    try:
        drivers = api.select_driver(**d)
    except Exception:
        traceback.print_stack()

    dtos = []

    for d in drivers:
        dtos.append(DriverDTO(d))

    resp = Response(response=json.dumps(
                    [dto.__dict__ for dto in dtos]),
                    status=200,
                    mimetype='application/json')
    return resp


@app.route('/api/driver', methods=['POST'])
@db_session
def add_driver():
    d = json.loads(request.data)

    try:
        s = api.add_driver(**d)
    except Exception:
        traceback.print_stack()

    dto = DriverDTO(s)
    resp = Response(response=json.dumps(dto.__dict__),
                    status=201,
                    mimetype='application/json')
    return resp


@app.route('/api/fuel/driver', methods=['POST'])
@db_session
def add_driver_to_fuel():
    d = json.loads(request.data)

    try:
        s = api.add_driver_to_fuel(**d)
    except Exception:
        traceback.print_stack()

    dto = DriverDTO(s)
    resp = Response(response=json.dumps(dto.__dict__),
                    status=201,
                    mimetype='application/json')
    return resp


@app.route('/api/fuel', methods=['POST'])
@db_session
def add_fuel_version():
    d = json.loads(request.data)

    s = api.add_fuel_version(**d)
    dto = FuelVersionDTO(s)
    resp = Response(response=json.dumps(dto.__dict__),
                    status=201,
                    mimetype='application/json')
    return resp


@db_session
def list_fuel_versions():
    versions = api.select_fuel_versions()
    dto_list = []

    for fv in versions:
        dto = FuelVersionDTO(fv)
        dto_list.append(dto)

    return dto_list


@db_session
def list_all_servers():
    servers = api.select_servers()
    dto_list = []

    for s in servers:
        dto = ServerDTO(s)
        dto_list.append(dto)

    return dto_list


@db_session
def list_all_types():
    types = api.select_types()
    dto_list = []

    for t in types:
        dto = TypeDTO(t)
        dto_list.append(dto)

    return dto_list


@app.route('/api/search/component', methods=['POST'])
@db_session
def list_components():
    d = json.loads(request.data)

    try:
        components = api.select_components(**d)
    except Exception:
        traceback.print_stack()

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
@db_session
def add_component():
    d = json.loads(request.data)

    try:
        c = api.add_component(**d)
    except Exception:
        traceback.print_stack()

    dto = ComponentDTO(c)
    fuel_versions_set = set()
    fuel_versions = ''

    for server in c.servers:
        [fuel_versions_set.add(x.fuel_version.name) for x in server.certifications]

    for fv in fuel_versions_set:
        fuel_versions += fv + ' '
    dto.fuel_versions = fuel_versions

    resp = Response(response=json.dumps(dto.__dict__),
                    status=201,
                    mimetype='application/json')
    return resp


@app.route('/api/component', methods=['PUT'])
@db_session
def update_component():
    d = json.loads(request.data)

    api.update_component(**d)
    resp = Response(status=202,
                    mimetype='application/json')
    return resp


@app.route('/api/component', methods=['DELETE'])
@db_session
def delete_component():
    d = json.loads(request.data)

    result = api.delete_component(**d)
    resp = Response(response=json.dumps(result),
                    status=202,
                    mimetype='application/json')
    return resp


@app.route('/api/certification', methods=['POST'])
@db_session
def add_certification():
    d = json.loads(request.data)

    s = api.add_certification(**d)
    dto = CertificationDTO(s)
    resp = Response(response=json.dumps(dto.__dict__),
                    status=201,
                    mimetype='application/json')
    return resp


@app.route('/', methods=['GET'])
@db_session
def index():
    fuel_versions = list_fuel_versions()
    types = list_all_types()
    servers = list_all_servers()

    return render_template("index.html", fuel_versions=fuel_versions,
                           types=types,
                           servers=servers)


if __name__ == '__main__':
    app.run()

