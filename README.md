# Climate_Analysis

## Background
I am planning a vacation to Hawaii.  In order to decide the best time to go, I will do some analysis of weather data for Hawaii.


## Weather Analyisis
I analyzed the data using python in a jupyter notebook focusing on preciptiation and temperature in order to inform on the conditions for selecting a vacation time.

#### Precipitation Analysis

* I found the most recent date in the dataset.

* Using this date, I retrieved the previous 12 months of precipitation data.

* I plotted the results and printed the summary statistics for the precipitation data.

#### Temperature/Station Analysis

* I was curious as to where the data was coming from so I calculated the total number of stations in the dataset.  

* Then I identified the most active station and calculated that station's lowest, highest and average temperature.

* The final step in my analysis was to gather the last 12 months of temperature observations for the most active station and great a historgram representing the results.


## API creation
I created the following Flask APIs in order to make the analysis/data accesible for future analysis. The APIs are not server hosted, so need to be run on the users local host.

* `/`

    * Homepage.

    * Lists all available routes.

* `/api/v1.0/precipitation`

    * Returns the JSON representation of precipitation dictionary (date: precip).

* `/api/v1.0/stations`

    * Returns a JSON list of stations from the dataset.

* `/api/v1.0/tobs`

    * Returns a JSON list of temperature observations (TOBS) for the previous year for the most active station.

* `/api/v1.0/stats/<start>` and `/api/v1.0/stats/<start>/<end>`

    * Returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.
        * When given the start only, calculations will be for all dates greater than or equal to the start date.
        * When given the start and the end date, calculations will be for dates from the start date through the end date (inclusive).
