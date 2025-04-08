import http

from flask import request
from flask_restx import Namespace, Resource
from pydantic import ValidationError

from app.controllers.swagger.location_model import LocationModel
from app.exceptions import ConflictError, NotFoundError, UnprocessableEntityError
from app.registry import Registry
from app.schemas.location_schema import LocationIn, LocationNearbyIn

location_ns = Namespace('locations', description='Location operations')
location_model = LocationModel(location_ns)


@location_ns.route('/')
class CreateLocationController(Resource):
    @staticmethod
    @location_ns.expect(location_model.location_post(), validate=False)
    @location_ns.response(http.HTTPStatus.CREATED, 'Created', location_model.location_response())
    @location_ns.response(http.HTTPStatus.BAD_REQUEST, 'Failed to search for name', location_model.error_response())
    @location_ns.response(
        http.HTTPStatus.UNPROCESSABLE_ENTITY,
        'Failed to search for name',
        location_model.error_response(),
    )
    @location_ns.response(http.HTTPStatus.CONFLICT, 'Location already exists', location_model.error_response())
    @location_ns.response(http.HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server', location_model.error_response())
    def post():
        try:
            data = LocationIn(**location_ns.payload)
            registry = Registry()
            location_service = registry.location()
            location = location_service.create_location(data.name)
            return location.model_dump(), http.HTTPStatus.CREATED
        except ValidationError as e:
            return {'error': 'Invalid fields', 'details': e.errors()}, http.HTTPStatus.BAD_REQUEST
        except UnprocessableEntityError:
            return {'error': 'Failed to search for name'}, http.HTTPStatus.UNPROCESSABLE_ENTITY
        except ConflictError:
            return {'error': 'Location already exists'}, http.HTTPStatus.CONFLICT
        except Exception:
            return {'error': 'Internal server'}, http.HTTPStatus.INTERNAL_SERVER_ERROR


@location_ns.route('/<string:id>')
class LocationController(Resource):
    @staticmethod
    @location_ns.response(http.HTTPStatus.OK, 'Ok', location_model.location_response())
    @location_ns.response(http.HTTPStatus.NOT_FOUND, 'Location not found', location_model.error_response())
    @location_ns.response(http.HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server', location_model.error_response())
    def get(id):
        try:
            registry = Registry()
            location_service = registry.location()
            location = location_service.get_location_by_id(id)
            return location.model_dump(), http.HTTPStatus.OK

        except NotFoundError:
            return {'error': 'Location not found'}, http.HTTPStatus.NOT_FOUND
        except Exception:
            return {'error': 'Internal server'}, http.HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    @location_ns.expect(location_model.location_post(), validate=False)
    @location_ns.response(http.HTTPStatus.OK, 'Ok', location_model.location_response())
    @location_ns.response(http.HTTPStatus.BAD_REQUEST, 'Failed to search for name', location_model.error_response())
    @location_ns.response(
        http.HTTPStatus.UNPROCESSABLE_ENTITY,
        'Failed to search for name',
        location_model.error_response(),
    )
    @location_ns.response(http.HTTPStatus.NOT_FOUND, 'Location not found', location_model.error_response())
    @location_ns.response(http.HTTPStatus.CONFLICT, 'Location already exists', location_model.error_response())
    @location_ns.response(http.HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server', location_model.error_response())
    def put(id):
        try:
            data = LocationIn(**location_ns.payload)
            registry = Registry()
            location_service = registry.location()
            location = location_service.update_location(id, data.name)
            return location.model_dump(), http.HTTPStatus.OK
        except ValidationError as e:
            return {'error': 'Invalid fields', 'details': e.errors()}, http.HTTPStatus.BAD_REQUEST
        except UnprocessableEntityError:
            return {'error': 'Failed to search for name'}, http.HTTPStatus.UNPROCESSABLE_ENTITY
        except NotFoundError:
            return {'error': 'Location not found'}, http.HTTPStatus.NOT_FOUND
        except ConflictError:
            return {'error': 'Location already exists'}, http.HTTPStatus.CONFLICT
        except Exception:
            return {'error': 'Internal server'}, http.HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    @location_ns.response(http.HTTPStatus.NO_CONTENT, 'No content', location_model.location_response())
    @location_ns.response(http.HTTPStatus.NOT_FOUND, 'Location not found', location_model.error_response())
    def delete(id):
        try:
            registry = Registry()
            location_service = registry.location()
            if location_service.delete_location(id):
                return '', http.HTTPStatus.NO_CONTENT
        except NotFoundError:
            return {'error': 'Location not found'}, http.HTTPStatus.NOT_FOUND


@location_ns.route('/nearby')
class NearbyLocationsController(Resource):
    @staticmethod
    @location_ns.param('lat', 'Latitude of the reference point', required=True)
    @location_ns.param('lon', 'Longitude of the reference point', required=True)
    @location_ns.param('radius_km', 'Radius in kilometers', required=False)
    @location_ns.response(http.HTTPStatus.OK, 'Ok', location_model.location_nearby_response())
    @location_ns.response(http.HTTPStatus.BAD_REQUEST, 'Failed fields', location_model.error_response())
    @location_ns.response(http.HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server', location_model.error_response())
    def get():
        try:
            payload = LocationNearbyIn(**request.args)
            registry = Registry()
            location_service = registry.location()
            locations = location_service.get_nearby_locations(payload.lat, payload.lon, payload.radius_km)
            return [loc.model_dump() for loc in locations], http.HTTPStatus.OK
        except ValidationError as e:
            return {'error': 'Invalid fields', 'details': e.errors()}, http.HTTPStatus.BAD_REQUEST
        except Exception:
            return {'error': 'Internal server'}, http.HTTPStatus.INTERNAL_SERVER_ERROR
