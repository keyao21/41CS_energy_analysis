# Building Energy Analysis on 41 Cooper Sq Academic Building

## TODO: 
compare night and day -- increase averaging window size and make graphs look better <br />
check ashrae recommended night vs day energy consumption <br />
prototype regression model for fault detection <br />

## Progress: 
2/7 Continued building predictive pipeline for various parts of building

## Working energy prediction / fault detection
So for these parts of the building, I've looked 2015 data and implemented the "fault detection" algorithm on it:<br />
![Alt text](/saved_images/predicts/demo_roof_2015.png)<br />
![Alt text](/saved_images/predicts/demo_overall_2015.png)<br />




## Preliminary Results:

### Night vs. Day Energy Usage
After comparing differences between the 12AM and 12PM energy levels, the average
difference across the year is compared for each distribution board. <br />
![Alt text](/saved_images/average_energy_use.png)<br />


### Weekday vs. Weekend Energy Usage
Weekend energy usage is expected to be less than weekday usage. The data is segregated into days
of the week, and then averaged for each of those days. The initial results are below: <br />
![Alt text](/saved_images/weekend/raw.png)<br />

The graph is then "normalized" by dividing each averaged energy level by that particular distribution board's 
maximum average energy level. This gives an idea of how much the energy level is changing over the weekend<br />
![Alt text](/saved_images/weekend/percent_max.png)<br />

The weekend is most important: some distribution boards clearly show greater changes in energy use over the
weekend than others <br />
![Alt text](/saved_images/weekend/percent_max_weekend.png)<br />

### Comparing Energy with Weather
Temperature data gathered from NOAA is used to judge how correlated (and possibly how much it causes) 
it changes building energy usage. <br />
![Alt text](/saved_images/weather/weather.png)<br />

The above time series is compared to each distribution board. <br />
![Alt text](/saved_images/weather/weather_building.png)<br />

The correlations are calculated and compared. 
![Alt text](/saved_images/weather/corrs.png)<br />


