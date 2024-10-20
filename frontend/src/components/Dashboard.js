// frontend/src/components/Dashboard.js
import React, { useEffect, useState } from 'react';
import { getHurricanes, getVehicles, getResourceNeeds, dispatchResources } from '../services/apiService';
import Map from './Map';
import MapWithVehicles from './MapWithVehicles';
import ResourceAllocation from './ResourceAllocation';
import TransportationList from './TransportationList';

function Dashboard() {
  const [hurricanes, setHurricanes] = useState([]);
  const [vehicles, setVehicles] = useState([]);
  const [resourceNeeds, setResourceNeeds] = useState({});
  const [allocations, setAllocations] = useState([]);

  useEffect(() => {
    getHurricanes().then(response => {
      setHurricanes(response.data);
      // Assume the first hurricane for demo purposes
      const hurricane = response.data[0];

      getResourceNeeds().then(res => {
        setResourceNeeds(res.data);
      });
    });

    getVehicles().then(response => {
      setVehicles(response.data);
    });
  }, []);

  const handleApprove = (adjustedNeeds) => {
    // Implement logic to dispatch resources
    dispatchResources(adjustedNeeds).then(() => {
      // Update vehicles and allocations after dispatching
      getVehicles().then(response => {
        setVehicles(response.data);
      });
    });
  };

  return (
    <div>
      <h1>Disaster Relief Dashboard</h1>
      <MapWithVehicles/>
      <ResourceAllocation predictedNeeds={resourceNeeds} onApprove={handleApprove} />
      <TransportationList vehicles={vehicles} />
    </div>
  );
}

export default Dashboard;
