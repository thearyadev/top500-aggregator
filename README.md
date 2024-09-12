# NOTE: As of March 12, 2024 this `README.md` is outdated. Many large changes have been made to the codebase (see latest PR's). The README will be updated in the coming days. 

# Overwatch 2: Top 500 Aggregator
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fthearyadev%2Ftop500-aggregator.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fthearyadev%2Ftop500-aggregator?ref=badge_shield)

https://t500-aggregator.aryankothari.dev/

T500 Aggregator is a suite of tools and a web service to collect and display data on the Overwatch 2 Top 500 leaderboards. 


## Information
The data for this is expected to be updated at the end of each season.
This data is collected by taking screenshots and running analysis on them. Detailed below. 

This data only consists of the data readily available in the top 500 leaderboards,
and does not include any information that would involve a single users profile. 

## How Does This Work ?

### Data Collection: 
Multiple scripts are used to collect and pre-process the data. This data is information collected from the Top 500 leaderboards in-game. Most of this data collection occurs in `./collector.py`

### Identifying Heroes
A neural network is used to conduct image classification on the leaderboard images. In the early stages of this project, ([a contribution by Autopoietico](https://github.com/thearyadev/top500-aggregator/pull/1)) included this neural network. As of season 9 in Overwatch 2, aafter the changes in the appearance of the top 500 leaderboards, I've recreated the neural network using PyTorch. More details can be found [Here](https://github.com/thearyadev/top500-aggregator/pull/147).


### Development 

Note: Some of the mentioned scripts have been moved to `./utils/`
Install all dependencies using poetry. There are some dev dependencies for code formatting. 

`./assets` contains hero images, neural network dataset, and some t500 images used during testing. Do not modify these files. Create the directory `./assets/leaderboard_images` as a supply for `generator.py`

`./data` contains the sqlite3 database.

`./leaderboards` contains all the tools required for loading, parsing, and converting leaderboard images into lists of LeaderboardEntry objects. 

`./classifier` contains the neural network related

`./benchmarks.py` is used for performance testing the selected hero identification method. This uses pre-defined files with an answer key to validate performance. 

`deblank2ify.py` is used to filter the database. This converts all 'Blank2' entries to 'Blank'

`server.py` is a FastAPI server which loads the data from the database, conducts calculations and filtering on the data, and stores it in memory. It then serves the webpage(s) displaying this data.

`train.py` is used to train the model. See inline documentation for more details. 

#### Neural Network
The neural network uses a dataset which lives in `./assets/heroes`. This dataset includes a single image for each hero, at specific markers, which is two white pixels at each corner of the image. When beginning training, this dataset is preprocessed by PyTorch into grayscale, then duplicated 250 times per class. Note: This duplication is done in memory, and will start many disk write operations. 

The generated dataset is created in `./assets/dataset/`. This directory should not be added to the repository. 

The resulting models will be placed in the `./models` directory automatically, the generated models are tracked by git. 

Each model contains a few files: 
- `classes`: a linebreak delimited ordered list of classnames derived from the initial dataset. It is indexed at prediction time.
- `detail`: information about the trained model.
- `frozen_model.py`: a copy of `./classifier/model.py` ('versioned' models).
- `model.pth`: the state dict as generated by PyTorch.
- `__init__.py`: allows the model directory to be imported as a package. Can't be imported directly, use `importlib`. 

##### Using the models 
The model needs to be imported using `importlib`. The module imported will have two members, `FrozenNNModel` and `transformer`. The transformer is the transformer used during training. Use the transformer to prepare the input image, then run the model. See `./heroes/hero_comparison.py` for an example of how to use the model. 

## License
[WTFPL](/LICENSE)


[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fthearyadev%2Ftop500-aggregator.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fthearyadev%2Ftop500-aggregator?ref=badge_large)
