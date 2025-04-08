import math
import uuid
from typing import Dict, List, Optional


class LocationRepository:
    def __init__(self, config, db):
        self.config = config
        self.db = db

    def create_location(self, name: str, lat: float, lon: float) -> Dict:
        location_id = str(uuid.uuid4())
        with self.db.get_cursor() as (conn, cur):
            cur.execute(
                'INSERT INTO locations (id, name, geom) VALUES (?, ?, MakePoint(?, ?, 4326))',
                (location_id, name, lon, lat),
            )

            return {'id': location_id, 'name': name, 'lat': lat, 'lon': lon}

    def get_location_by_id(self, location_id: str) -> Optional[Dict]:
        with self.db.get_cursor() as (conn, cur):
            cur.execute(
                'SELECT id, name, X(geom) AS lon, Y(geom) AS lat FROM locations WHERE id = ?',
                (location_id,),
            )
            row = cur.fetchone()
            if row:
                return dict(row)
            return None

    def get_location_by_name(self, name: str) -> Optional[Dict]:
        with self.db.get_cursor() as (conn, cur):
            cur.execute(
                'SELECT id, name, X(geom) AS lon, Y(geom) AS lat FROM locations WHERE name = ?',
                (name,),
            )
            row = cur.fetchone()
            if row:
                return dict(row)
            return None

    def get_nearby_locations(self, lat: float, lon: float, radius_km: float) -> List[Dict]:
        min_lat, max_lat, min_lon, max_lon = _bounding_box(lat, lon, radius_km)

        spatial_sql = """
            SELECT id, name, X(geom) as lon, Y(geom) as lat, haversine(?, ?, Y(geom), X(geom)) as distance_km
            FROM locations
            WHERE Y(geom) BETWEEN ? AND ? AND X(geom) BETWEEN ? AND ? AND haversine(?, ?, Y(geom), X(geom)) <= ?
            ORDER BY distance_km
        """

        with self.db.get_cursor() as (conn, cur):
            cur.execute(spatial_sql, (lat, lon, min_lat, max_lat, min_lon, max_lon, lat, lon, radius_km))
            return [dict(row) for row in cur.fetchall()]

    def update_location(self, location_id: str, name: str, lat: float, lon: float) -> Optional[Dict]:
        with self.db.get_cursor() as (conn, cur):
            cur.execute(
                'UPDATE locations SET name = ?, geom = MakePoint(?, ?, 4326) WHERE id = ?',
                (name, lon, lat, location_id),
            )
            if cur.rowcount > 0:
                return {'id': location_id, 'name': name, 'lat': lat, 'lon': lon}
            return None

    def delete_location(self, location_id: str) -> bool:
        with self.db.get_cursor() as (conn, cur):
            cur.execute('DELETE FROM locations WHERE id = ?', (location_id,))
            return cur.rowcount > 0


def _bounding_box(lat, lon, radius_km):
    radius_deg_lat = radius_km / 111  # ~111 km por grau latitude
    radius_deg_lon = radius_km / (111 * math.cos(math.radians(lat)))

    min_lat = lat - radius_deg_lat
    max_lat = lat + radius_deg_lat
    min_lon = lon - radius_deg_lon
    max_lon = lon + radius_deg_lon

    return min_lat, max_lat, min_lon, max_lon
