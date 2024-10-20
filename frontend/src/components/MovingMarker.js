import React, { useEffect, useState } from 'react';
import { Polyline, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

function MovingMarker({ 
  coords = [], 
  iconUrl, 
  type, 
  quantity, 
  popupText, 
  lineColor = 'blue', 
  intervalMs = 1000 
}) {

  // Initialize position
  const initialPosition = coords.length > 0 ? coords[0] : null;
  const [position, setPosition] = useState(initialPosition);
  const [index, setIndex] = useState(0); // Track current index

  // Create a custom icon based on the iconUrl parameter
  const customIcon = L.icon({
    iconUrl: iconUrl,
    iconSize: [40, 40],      // Customize size if needed
    iconAnchor: [20, 20], 
    popupAnchor: [0, -40],   // Anchor point to center the icon
  });

  useEffect(() => {
    if (!coords.length) return; // Do nothing if coords is empty

    const interval = setInterval(() => {
      setIndex(prevIndex => {
        const nextIndex = prevIndex + 1;
        if (nextIndex < coords.length) {
          setPosition(coords[nextIndex]); // Update the position
          return nextIndex;
        } else {
          clearInterval(interval); // Stop the interval when reaching the end
          return prevIndex;
        }
      });
    }, intervalMs);

    return () => clearInterval(interval);
  }, [coords, intervalMs]);

  // If coords is empty or position is null, do not render anything
  if (!coords.length || !position) {
    return null;
  }

  // Calculate the shader width based on the index
  const shaderWidth = Math.min(20, 5 + index); // Adjust as needed

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
