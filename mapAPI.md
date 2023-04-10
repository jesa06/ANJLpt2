<script>
    
    function locationButtonClick(location) {
        
        if (!location.trim()) {
            alert("Enter origins described as semicolon-delimited coordinate pairs with latitudes and longitudes. Max: 25.");
            return;
        }  
       const url = 'https://google-maps-geocoding.p.rapidapi.com/geocode/json?address=Del%20Norte%2C%20San%20Diego%2C%20CA&language=en' + location ;

//alert(url);
//alert("2: " + url);
            
        const headers = {
            method: 'GET', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, *cors, same-origin
            cache: 'default', // *default, no-cache, reload, force-cache, only-if-cached 
            credentials: 'omit', // include, *same-origin, omit
            headers: {
                'Content-Type': 'application/json',
                'X-RapidAPI-Key': '0b6ef107f7msh5606de624633ceap17521ejsn27566d20ff5b',
		        'X-RapidAPI-Host': 'google-maps-geocoding.p.rapidapi.com'
            },
        };

//alert("3: " + headers)

//alert("3a: pre-fetch" + headers);

        // fetch the API
        fetch(url, headers)
        // response is a RESTful "promise" on any successful fetch
        .then(response => {
            // check for response errors
            if (response.status !== 200) {

                const errorMsg = 'Database response error: ' + response.status;
                console.log(errorMsg);
                const tr = document.createElement("tr");
                const td = document.createElement("td");
                td.innerHTML = errorMsg;
                tr.appendChild(td);
                resultContainer.appendChild(tr);

                return;
            }
            // valid response will have json data
            response.json().then(data => {
                console.log(data);
                console.log(data.results)
            alert(data.results.0.formatted_address);

            

                // Weather Data
                document.getElementById("formatted_address").innerHTML = data.results.0.formatted_address;
                document.getElementById("region").innerHTML = data.location.region;
                document.getElementById("country").innerHTML = data.location.country;          
                document.getElementById("lat").innerHTML = data.location.lat;
                document.getElementById("lon").innerHTML = data.location.lon;      
                document.getElementById("tz_id").innerHTML = data.location.tz_id;
                document.getElementById("localtime_epoch").innerHTML = data.location.localtime_epoch;
                document.getElementById("localtime").innerHTML = data.location.localtime;

                // Current Conditions
                document.getElementById("temp_f").innerHTML = data.current.temp_f;
                document.getElementById("wind_mph").innerHTML = data.current.wind_mph;
                document.getElementById("humidity").innerHTML = data.current.humidity;                
                document.getElementById("cloud").innerHTML = data.current.cloud;
                document.getElementById("feelslike_f").innerHTML = data.current.feelslike_f;
                document.getElementById("condition_text").innerHTML = data.current.condition.text;

                // Weather Forecast
                // day 1
                document.getElementById("date_1").innerHTML = data.forecast.forecastday[0].date;
                document.getElementById("maxtemp_f_1").innerHTML = data.forecast.forecastday[0].day.maxtemp_f;
                document.getElementById("mintemp_f_1").innerHTML = data.forecast.forecastday[0].day.mintemp_f;
                document.getElementById("avgtemp_f_1").innerHTML = data.forecast.forecastday[0].day.avgtemp_f;
                document.getElementById("maxwind_mph_1").innerHTML = data.forecast.forecastday[0].day.maxwind_mph;
                document.getElementById("totalprecip_in_1").innerHTML = data.forecast.forecastday[0].day.totalprecip_in;
                document.getElementById("daily_will_it_rain_1").innerHTML = data.forecast.forecastday[0].day.daily_will_it_rain;
                document.getElementById("daily_chance_of_rain_1").innerHTML = data.forecast.forecastday[0].day.daily_chance_of_rain;
                document.getElementById("forecast_text_1").innerHTML = data.forecast.forecastday[0].day.condition.text;
                // day 2
                document.getElementById("date_2").innerHTML = data.forecast.forecastday[1].date;
                document.getElementById("maxtemp_f_2").innerHTML = data.forecast.forecastday[1].day.maxtemp_f;
                document.getElementById("mintemp_f_2").innerHTML = data.forecast.forecastday[1].day.mintemp_f;
                document.getElementById("avgtemp_f_2").innerHTML = data.forecast.forecastday[1].day.avgtemp_f;
                document.getElementById("maxwind_mph_2").innerHTML = data.forecast.forecastday[1].day.maxwind_mph;
                document.getElementById("totalprecip_in_2").innerHTML = data.forecast.forecastday[1].day.totalprecip_in;
                document.getElementById("daily_will_it_rain_2").innerHTML = data.forecast.forecastday[1].day.daily_will_it_rain;
                document.getElementById("daily_chance_of_rain_2").innerHTML = data.forecast.forecastday[1].day.daily_chance_of_rain;
                document.getElementById("forecast_text_2").innerHTML = data.forecast.forecastday[1].day.condition.text;
                // day 3 
                document.getElementById("date_3").innerHTML = data.forecast.forecastday[2].date;
                document.getElementById("maxtemp_f_3").innerHTML = data.forecast.forecastday[2].day.maxtemp_f;
                document.getElementById("mintemp_f_3").innerHTML = data.forecast.forecastday[2].day.mintemp_f;
                document.getElementById("avgtemp_f_3").innerHTML = data.forecast.forecastday[2].day.avgtemp_f;
                document.getElementById("maxwind_mph_3").innerHTML = data.forecast.forecastday[2].day.maxwind_mph;
                document.getElementById("totalprecip_in_3").innerHTML = data.forecast.forecastday[2].day.totalprecip_in;
                document.getElementById("daily_will_it_rain_3").innerHTML = data.forecast.forecastday[2].day.daily_will_it_rain;
                document.getElementById("daily_chance_of_rain_3").innerHTML = data.forecast.forecastday[2].day.daily_chance_of_rain;
                document.getElementById("forecast_text_3").innerHTML = data.forecast.forecastday[2].day.condition.text;


</script>