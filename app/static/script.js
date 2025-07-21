const { createApp, ref, onMounted } = Vue;
const app = createApp({
  setup() {
    const city = ref('');
    const date = ref('');
    const weather = ref(null);

    const fetchForecast = async () => {
      if (!city.value || !date.value) {
        console.warn("City or date missing");
        return;
      }

       try {
        
        const response = await fetch('/predict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            city: city.value,
            datetime: date.value,
          }),
        });

        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        weather.value = data['weather_metrics'];
        } catch (error) {
            console.error('Error fetching forecast:', error);
            weather.value = null;
        }
    };

    const getIconPath = (iconKey) => {
      const iconMap = {
        'clear-day': 'clear-day.svg',
        'cloudy': 'cloudy.svg',
        'fog': 'fog.svg',
        'partly-cloudy-day': 'partly-cloudy-day-rain.svg',
        'rain': 'extreme-rain.svg'
      };
      return `/static/icons/${iconMap[iconKey]}`

              
    };

    // watch([city, date], fetchForecast); // Automatically refetch on change

    onMounted(() => {
      // Optional: Set default values
      city.value = 'Hamburg';
      const today = new Date().toISOString().split('T')[0];
      date.value = today;
    });

    return {
      city,
      date,
      weather,
      fetchForecast,
      getIconPath
    };
  },
}).mount('.container');
