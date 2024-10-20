// frontend/src/components/Map.js
import React from 'react';
import { MapContainer, TileLayer, Polyline, Marker, Popup } from 'react-leaflet';

function Map({ hurricanes, vehicles }) {
  const position = [25.7617, -80.1918]; // Center on Miami

  return (
    <MapContainer center={position} zoom={4} style={{ height: '500px', width: '100%' }}>
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
      />
      {hurricanes && hurricanes.map(hurricane => (
        <React.Fragment key={hurricane.id}>
            {hurricane.forecasted_path && hurricane.forecasted_path.length > 0 && (
                <Polyline
                    positions={hurricane.forecasted_path.map(coord => [coord.latitude, coord.longitude])}
                    color="red"
                />
    )}
    {hurricane.past_path && hurricane.past_path.length > 0 && (
      <Polyline
        positions={hurricane.past_path.map(coord => [coord.latitude, coord.longitude])}
        color="orange"
      />
    )}
  </React.Fragment>
))}

      {vehicles && vehicles.map(vehicle => (
        <React.Fragment key={vehicle.id}>
          <Polyline
            positions={vehicle.route.map(coord => [coord.latitude, coord.longitude])}
            color="blue"
          />
          <Marker
            position={vehicle.current_location.split(',').map(Number)}
          >
            <Popup>
              {vehicle.type} en route to {vehicle.destination}
            </Popup>
          </Marker>
        </React.Fragment>
      ))}
    </MapContainer>
  );
}

export default Map;
