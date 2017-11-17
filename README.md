# Building Energy Analysis on 41 Cooper Sq Academic Building

## TODO: 
compare night and day -- increase averaging window size and make graphs look better <br />
check ashrae recommended night vs day energy consumption <br />
prototype regression model for fault detection <br />

## Progress: 
11/13:
compared weekdays and weekends on jupyter notebook
compared energy usage with weather correlations on jupyter notebook

11/9:
compared night and day

## Preliminary Results:

### Night vs. Day Energy Usage
After comparing differences between the 12AM and 12PM energy levels, the average
difference across the year is compared for each distribution board. <br />
<p align="center">![Alt text](/saved_images/average_energy_use.png)<br /></p>


### Weekday vs. Weekend Energy Usage
Weekend energy usage is expected to be less than weekday usage. The data is segregated into days
of the week, and then averaged for each of those days. The initial results are below: <br />
<p align="center">![Alt text](/saved_images/weekend/raw.png)<br /></p>

The graph is then "normalized" by dividing each averaged energy level by that particular distribution board's 
maximum average energy level. This gives an idea of how much the energy level is changing over the weekend<br />
<p align="center">![Alt text](/saved_images/weekend/percent_max.png)<br /></p>

The weekend is most important: some distribution boards clearly show greater changes in energy use over the
weekend than others <br />
<p align="center">![Alt text](/saved_images/weekend/percent_max_weekend.png)<br /></p>

### Comparing Energy with Weather
Temperature data gathered from NOAA is used to judge how correlated (and possibly how much it causes) 
it changes building energy usage. <br />
<p align="center">![Alt text](/saved_images/weather/weather.png)<br /></p>

The above time series is compared to each distribution board. <br /></p>
<p align="center">![Alt text](/saved_images/weather/weather_building.png)<br /></p>

The correlations are calculated and compared. 
<p align="center">![Alt text](/saved_images/weather/corrs.png)<br /></p>


