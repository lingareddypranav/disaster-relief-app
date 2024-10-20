// src/components/MapWithVehicles.js

import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import MovingMarker from './MovingMarker';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';

function MapWithVehicles() {
  const [vehicles, setVehicles] = useState([]);
  const [hurricane, setHurricane] = useState(null);

  useEffect(() => {
    // Fetch vehicles data
    axios.get('http://localhost:8000/api/vehicles/')
      .then(response => {
        setVehicles(response.data);
      })
      .catch(error => {
        console.error('Error fetching vehicles data:', error);
      });

    // Fetch hurricane data
    axios.get('http://localhost:8000/api/hurricanes/')
      .then(response => {
        if (response.data.length > 0) {
          setHurricane(response.data[0]);
        }
      })
      .catch(error => {
        console.error('Error fetching hurricane data:', error);
      });
  }, []);

  // Define the map center and zoom level
  const mapCenter = [27.6648, -81.5158]; // Florida's coordinates
  const zoomLevel = 6;

  // Map vehicle types to icon filenames
  const iconMapping = {
    food: 'assets/food_truck.png',
    water: 'assets/water_tanker.png',
    medical: 'assets/ambulance.png',
    plane: 'assets/plane.png',
    Hurricane: 'assets/hurricane.png',
  };

  return (
    <MapContainer center={mapCenter} zoom={zoomLevel} style={{ height: '100vh', width: '100%' }}>
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
      />
      {/* Render hurricane path */}
      {hurricane && (
        <MovingMarker
          coords={hurricane.past_path}
          iconUrl={`/assets/${iconMapping['Hurricane']}`}
          type='Hurricane'
          popupText={hurricane.name}
          lineColor='red'
          intervalMs={1000}
        />
      )}
      {/* Render vehicles */}
      {vehicles.map(vehicle => (
        <MovingMarker
          key={vehicle.id}
          coords={vehicle.route}
          iconUrl={`/assets/${iconMapping[vehicle.type]}`}
          type={vehicle.type}
          quantity={vehicle.quantity}
          popupText={`Carrying ${vehicle.quantity} units of ${vehicle.type}`}
          lineColor='blue'
          intervalMs={1000}
        />
      ))}
    </MapContainer>
  );
}

export default MapWithVehicles;
