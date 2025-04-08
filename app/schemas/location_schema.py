from pydantic import BaseModel, ConfigDict, Field


class LocationIn(BaseModel):
    name: str = Field(..., min_length=1, description='Name of the location')


class LocationOut(BaseModel):
    id: str = Field(..., description='Location ID')
    name: str = Field(..., description='Name of the location')
    lat: float = Field(..., description='Latitude of the location')
    lon: float = Field(..., description='Longitude of the location')
    model_config = ConfigDict(from_attributes=True)


class LocationNearbyIn(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description='Latitude between -90 and 90')
    lon: float = Field(..., ge=-180, le=180, description='Longitude between -180 and 180')
    radius_km: float = Field(default=10, gt=0, description='Radius must be greater than zero')


class LocationNearbyOut(LocationOut):
    distance_km: float = Field(..., description='Distance in kilometers from the reference point')
