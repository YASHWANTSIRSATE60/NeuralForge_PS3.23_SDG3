export async function getLocation(onSuccess, onError) {
    if (!navigator.geolocation) {
        onError("Geolocation not supported");
        return;
    }

    navigator.geolocation.getCurrentPosition(async (position) => {
        const { latitude, longitude, accuracy } = position.coords;
        
        try {
            // Reverse geocoding using OpenStreetMap (Nominatim)
            const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`);
            const data = await response.json();
            const address = data.display_name || `${latitude}, ${longitude}`;
            onSuccess({ address, latitude, longitude, accuracy });
        } catch (e) {
            onSuccess({ address: `${latitude}, ${longitude}`, latitude, longitude, accuracy });
        }
    }, (err) => {
        onError(err.message);
    }, {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
    });
}
