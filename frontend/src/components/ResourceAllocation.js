// src/components/ResourceAllocation.js
import React, { useState, useEffect } from 'react';

function ResourceAllocation({ predictedNeeds, onApprove }) {
  const [adjustedNeeds, setAdjustedNeeds] = useState({});

  useEffect(() => {
    setAdjustedNeeds(predictedNeeds);
  }, [predictedNeeds]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setAdjustedNeeds({
      ...adjustedNeeds,
      [name]: Number(value),
    });
  };

  const handleSubmit = () => {
    onApprove(adjustedNeeds);
  };

  return (
    <div>
      <h3>Adjust Resource Allocations</h3>
      {Object.keys(predictedNeeds).map((resType) => (
        <div key={resType}>
          <label>{resType}:</label>
          <input
            type="number"
            name={resType}
            value={adjustedNeeds[resType] || ''}
            onChange={handleChange}
          />
        </div>
      ))}
      <button onClick={handleSubmit}>Approve and Dispatch Resources</button>
    </div>
  );
}

export default ResourceAllocation;
