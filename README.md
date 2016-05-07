# WiFi Localization

## Introduction

Considering there is a subset of APs within a floor, we can measure the signal strength of different APs on several points. Then we can build a signal strength vector, i.e. the vector where each component represents the signal strength to a given AP.

Based on the signal strength vector, we can: 

1. **Localization**: Calculate the position of a random point according to the AP signal strength measured on that point.
2. **Prediction**: Predict the AP signal strength on a random point according to the position of that point.



