# HCM-AI-Challenge
A contest about building a smart system for traffic tracking via cameras. Get to know more the contest http://aichallenge.hochiminhcity.gov.vn/huong-dan-nhom-1

Following are our concise steps:
1. Use YOLOV4 for detecting cars, cyclists, trucks, bus,...
2. Extract videos to frames.
3. Predict interested objects in the frames, include their bouding boxes, coordinates
2. Read Regions of Interested, directions indicated in json files then predict direction of the predicted objects.

This repo does not include detection processing, it is for tracking task.
###This project is just for my team in the contest, therefore it's not readable for everyone:( 

Update list: 
- Update 1: By increasing number of batch, from 20 to 30, we got better results in tracking task.

