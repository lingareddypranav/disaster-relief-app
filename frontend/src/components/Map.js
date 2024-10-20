import React from 'react';
import { MapContainer, TileLayer, Polyline } from 'react-leaflet';
import MovingMarker from './MovingMarker'; // Import the MovingMarker component
import 'leaflet/dist/leaflet.css';

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
        <MovingMarker
          key={vehicle.id}
          coords={vehicle.route}              // Pass the route coordinates
          iconUrl='/car-icon.png'            // Pass the icon URL (e.g., car image)
          type={vehicle.type}                // Pass the type of vehicle
          popupText={`en route to ${vehicle.destination}`} // Customize the popup text
          intervalMs={1000}                  // Customize the interval for animation if needed
        />
      ))}
    </MapContainer>
  );
}

export default Map;