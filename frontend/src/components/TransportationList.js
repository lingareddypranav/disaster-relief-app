// src/components/TransportationList.js
import React from 'react';

function TransportationList({ vehicles }) {
  return (
    <div>
      <h3>Transportation Vehicles</h3>
      <ul>
        {vehicles.map(vehicle => (
          <li key={vehicle.id}>
            {vehicle.type} from {vehicle.current_location} to {vehicle.destination} - {vehicle.status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TransportationList;
