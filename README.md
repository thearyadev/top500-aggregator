# Overwatch 2: Top 500 Aggregator
https://top500-aggregator.up.railway.app/

T500 Aggregator is a suite of tools and a web service to collect and provide data on the Overwatch 2 Top 500 leaderboards. 


## Information
The data for this is expected to be updated once every two weeks.
This data is collected by taking screenshots and running analysis on them. Detailed below. 

The hero data has ~99%, and the games played has <90% accuracy. 
This discrepancy is due to the different forms of data collection, detailed below. 

This data only consists of the data readily available in the top 500 leaderboards,
and does not include any information that would involve a single users profile. 



## Tools & Technologies Used

### OpenCV / CV2
CV2 is used to compare images and evaluate similarity. The data parser will go through every entry in top 500 and determine which heroes are in the players top 3 most played heroes, by taking a screenshot of a selected hero sprite, and comparing it to each of the saved assets. Once the results are sorted, the item with the lowest result is the correct hero. 

The method used for this is the Mean Squared Error between the images. 

```python
def similarity(image1, image2) -> float:
    return np.sum(cv2.subtract(image1, image2) ** 2) / (float(image1.shape[0] * image1.shape[1]))

```

### TesseractOCR / Pytesseract
TesseractOCR is used to extract the "games played" value from each top 500 entry. This is done using the python wrapper for TesseractOCR called Pytesseract. 

TesseractOCR is not trained on the specific environment i've given it, that being said there is a significant amount of errors that would cause the data to be inaccurate.
The data had a few outliers that had a very large variance from the mean. Demonstrated in the graphs below, these results have been filtered to increase the accuracy in the data. 

![](assets/unfiltered.png)  |  ![](assets/filtered.png)


### SQLite 
SQLite is used to store all of the leaderboard data for each season. This database is stored in the `./data` directory and is available in this github repository.

### Web
#### FastAPI / Uvicorn
FastAPI and Uvicorn are used to serve the web page. 
### Chart.js
Chart.js is used on the frontend to display all the data collected and generated by the application. 

## Building from Source

### Data Collection
1. Install all dependencies using poetry
2. Create a `./bin/tesseract` directory in the root of this project. Install TesseractOCR 5.0 to this folder. 
3. Run `python collector.py` to begin

### Serving Webpage 
#### Docker
Use docker to build the dockerfile.

#### Development 
1. Install all dependencies using poetry
2. Run 'uvicorn server:app --reload' to begin

## License
[hehe](/LICENSE)