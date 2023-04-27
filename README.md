# Overwatch 2: Top 500 Aggregator
https://top500-aggregator.up.railway.app/

T500 Aggregator is a suite of tools and a web service to collect and provide data on the Overwatch 2 Top 500 leaderboards. 


## Information
The data for this is expected to be updated once every two weeks.
This data is collected by taking screenshots and running analysis on them. Detailed below. 

This data only consists of the data readily available in the top 500 leaderboards,
and does not include any information that would involve a single users profile. 

## How Does This Work?

### Data Collection: 
Multiple scripts are used to collect and pre-process the data. This data is information collected from the Top 500 leaderboards in-game. Most of this data collection occurs in `./collector.py`

### Identifying Heroes
Currently a neural network ([Contributed by Autopoietico](https://github.com/thearyadev/top500-aggregator/pull/1)) is being used for image classification. The dataset used to train this model is located in `./assets/top_500_mnist_images`, and the model and params files are located in `./neural_network/`. This model will need to be re-trained for each hero release, or top 500 hero image change. The tools for training are located in `./train.py`


## Tools & Technologies Used

### SQLite 
SQLite is used to store all of the leaderboard data for each season. This database is stored in the `./data` directory and is available in this github repository.

### Web
#### FastAPI / Uvicorn
FastAPI and Uvicorn are used to serve the web page. 
#### Google Charts
Google Charts is used on the frontend to display all the data collected and generated by the application. 

## Building from Source

### Data Collection
1. Install all dependencies using poetry
2. Run `python collector.py` to begin

### Generating Databse Entries
1. Install all dependencies
2. Prepare the raw leaderboard images, place them in `./assets/leaderboard_images`
3. Configure the correct settings for the season identifier in `./generator.py`
4. Run `python generator.py`


### Serving Webpage 
#### Docker
Use docker to build the dockerfile, or run `uvicorn server:app --reload` after installing dependencies.


#### Development 
Install all dependencies using poetry. There are some dev dependencies for code formatting. 

`./assets` contains hero images, neural network dataset, and some t500 images used during testing. Do not modify these files. Create the directory `./assets/leaderboard_images` as a supply for `generator.py`

`./data` contains the sqlite3 database.

`./leaderboards` contains all the tools required for loading, parsing, and converting leaderboard images into lists of LeaderboardEntry objects. 

`./neural_network` contains the models and model structure.

`./benchmarks.py` is used for performance testing the selected hero identification method. This uses pre-defined files with an answer key to validate performance. 

`deblank2ify.py` is used to filter the database. This converts all 'Blank2' entries to 'Blank'

`server.py` is a FastAPI server which loads the data from the database, conducts calculations and filtering on the data, and stores it in memory. It then serves the webpage(s) displaying this data.

`train.py` is used to train the model. See inline documentation for more details. 


# Todo & Roadmap
- Clean up codebase
- Re-train model for LifeWeaver
- Move all Neural Network related files into a package for easier access
- Use in-memory database instead of dictionary for datastore. 
- Purge season 2, 3, and 4 data. 
- Add a browser icon
- improve frontend



## Contributing

There are no contributing guidelines (for now). 


## 🚀 About Me
I'm a developer. Actively learning and looking for new and interesting opportunities. Send me a message: aryan@aryankothari.dev

## License
[Apache-2.0](/LICENSE)