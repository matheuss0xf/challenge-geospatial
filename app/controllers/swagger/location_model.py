from flask_restx import fields


class LocationModel:
    def __init__(self, namespace):
        self.namespace = namespace

    def location_post(self):
        return self.namespace.model(
            'LocationCreate',
            {'name': fields.String(required=True, description='Name of the location')},
        )

    def location_response(self):
        return self.namespace.model(
            'LocationResponse',
            {
                'id': fields.String(description='Location ID (UUID)'),
                'name': fields.String(description='Name of the location'),
                'lat': fields.Float(description='Latitude of the location'),
                'lon': fields.Float(description='Longitude of the location'),
            },
        )

    def location_nearby_response(self):
        return self.namespace.model(
            'LocationNearbyResponse',
            {
                'id': fields.String(description='Location ID (UUID)'),
                'name': fields.String(description='Name of the location'),
                'lat': fields.Float(description='Latitude of the location'),
                'lon': fields.Float(description='Longitude of the location'),
                'distance_km': fields.Float(description='Distance in kilometers from reference point', default=None),
            },
        )

    def error_response(self):
        return self.namespace.model(
            'ErrorResponse',
            {
                'error': fields.String(description='Error message', example='Location not found'),
                'details': fields.String(description='Detailed error message', example='Field invalid', default=None),
            },
        )
