# WiFi Localization - Yuheng Zhan

## Introduction

Considering there is a subset of APs within a floor, we can measure the signal strength of different APs on several points. Then we can build a signal strength vector, i.e. the vector where each component represents the signal strength to a given AP.

Based on the signal strength vector, we can: 

1. **Localization**: Calculate the position of a random point according to the AP signal strength measured on that point.
2. **Prediction**: Predict the AP signal strength on a random point according to the position of that point.

![application_screenshot](https://raw.githubusercontent.com/aaaahern/WiFiLocalization/master/img/localization.png)

## Usage

### Measure AP signal strength on OS X
`/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport
eth0 -s`

You can also use my script `AP_signal.sh` (I created a soft link to airport)

### Localize point according to the signal strength file
Click the button "Localize" and choose the test file `target_location_signal.txt`

### Predict the AP signal strength
Click random point on the map
![prediction](https://raw.githubusercontent.com/aaaahern/WiFiLocalization/master/img/prediction.png)

## Algorithm

### Localization


1. Find nearby points to the target point:

	1.1 Calculate average RSSI of different AP signal on the target point
	
	1.2 Find all AP whose signal strength is stronger than the average RSSI from step 1.1
	
	1.3 Find nearby points which can receive the AP signal from step 2.
	
2. Calculate the distance to every nearby points
![distance formula](https://raw.githubusercontent.com/aaaahern/WiFiLocalization/master/img/distance_formula.png)


3. Calculate the coordinate of target point according to distance
![coordinate formula](https://raw.githubusercontent.com/aaaahern/WiFiLocalization/master/img/coordinate_formula.png)


### Prediction

1. Find all points whose distance to target point is less than 100

2. Calculate all possible AP signal
![signal formula](https://raw.githubusercontent.com/aaaahern/WiFiLocalization/master/img/signal_prediction_formula.png)


## Observation and causes of errors
1. Accuracy is high if the target point is surrounding by other points and is low when there is no point on the one side of the target point. For example, accuracy is low when target point is on windows. This algorithm is like trilateration, using triangle to localize. I think that having test points on window could guarantee all target point is surrounding by test points, and then increase accuracy. 

![window_point](https://raw.githubusercontent.com/aaaahern/WiFiLocalization/master/img/test_point_on_window.png)

2. Due to the blocking by bookshelfs and walls, using the distance between target point to test point is naive. 

![wall_effect](https://raw.githubusercontent.com/aaaahern/WiFiLocalization/master/img/wall_effect.png)


