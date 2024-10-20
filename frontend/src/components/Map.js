import React from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
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

      {/* Render hurricanes as moving markers */}
      {hurricanes && hurricanes.map(hurricane => (
        hurricane.forecasted_path && hurricane.forecasted_path.length > 0 && (
          <MovingMarker
            key={`hurricane-${hurricane.id}`}
            coords={hurricane.forecasted_path}     // Pass the forecasted path as coordinates
            iconUrl='/hurricane.png'          // Pass a hurricane icon URL
            type="Hurricane"                       // Type of marker
            popupText={`Hurricane ${hurricane.name}`} // Customize the popup text
            lineColor="red"                        // Set the line color for hurricanes (optional)
            intervalMs={2000}                      // Customize the interval speed if needed
          />
        )
      ))}

      {/* Render vehicles as moving markers */}
      {vehicles && vehicles.map(vehicle => (
        <MovingMarker
          key={`vehicle-${vehicle.id}`}
          coords={vehicle.route}              // Pass the route coordinates
          iconUrl= {vehicle.image}          // Pass the icon URL (e.g., car image)
          type={vehicle.type}                // Pass the type of vehicle
          popupText={`en route to ${vehicle.destination}`} // Customize the popup text
          lineColor="blue"                   // Set the line color for vehicles
          intervalMs={1000}                  // Customize the interval for animation if needed
        />
      ))}
    </MapContainer>
  );
}

export default Map;
