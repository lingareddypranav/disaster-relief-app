import React, { useEffect, useState } from 'react';
import { Polyline, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

function MovingMarker({ 
  coords, 
  iconUrl, 
  type, 
  popupText, 
  lineColor = 'blue', 
  intervalMs = 1000 
}) {
  const [position, setPosition] = useState(coords[0]); // Initialize with the starting point
  const [index, setIndex] = useState(0); // Track current index for shader effect

  // Create a custom icon based on the iconUrl parameter
  const customIcon = new L.Icon({
    iconUrl: iconUrl,
    iconSize: [40, 40],      // Customize size if needed
    iconAnchor: [20, 20],    // Anchor point to center the icon
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex(prevIndex => {
        const nextIndex = (prevIndex + 1) % coords.length; // Loop back to the beginning
        setPosition(coords[nextIndex]); // Update the position
        return nextIndex; // Update the index
      });
    }, intervalMs);

    return () => clearInterval(interval);
  }, [coords, intervalMs]);

  // Calculate the shader width based on the index
  const shaderWidth = Math.min(20, 5 + index); // Change this logic to adjust width dynamically

  return (
    <>
      {/* Draw a shader polyline for hurricanes */}
      {type === "Hurricane" && (
        <Polyline
          positions={coords.map(coord => [coord.latitude, coord.longitude])}
          color="rgba(255, 0, 0, 0.5)" // Semi-transparent red for shader effect
          weight={shaderWidth} // Dynamic width based on the current index
        />
      )}
      {/* Draw a regular polyline representing the path */}
      <Polyline
        positions={coords.map(coord => [coord.latitude, coord.longitude])}
        color={lineColor} // Use the lineColor prop
      />
      {/* Render the moving marker */}
      <Marker
        position={[position.latitude, position.longitude]}
        icon={customIcon}
      >
        <Popup>
          {type}: {popupText}
        </Popup>
      </Marker>
    </>
  );
}

export default MovingMarker;
