# NOTE: The information in this README is outdated as of Febuary 15th 2024. It will be updated when pending changes are completed.


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
Currently a neural network ([Contributed by Autopoietico](https://github.com/thearyadev/top500-aggregator/pull/1)) is being used for image classification. The dataset used to train this model is located in `./assets/top_500_mnist_images`, and the model and params files are located in `./neural_network/`. This model will need to be re-trained for each hero release, or top 500 hero image change. The tools for training are located in `./train.py`

## Building from Source

### Data Collection
1. Install all dependencies using poetry
2. Run `python utils/collector.py` to begin

### Generating Databse Entries
1. Install all dependencies
2. Prepare the raw leaderboard images, place them in `./assets/leaderboard_images`
3. Configure the correct settings for the season identifier in `./utils/generator.py`
4. Run `python utils/generator.py`

*Note: Some of the paths have been moved. Please see project file tree.*

### Development 

Note: Some of the mentioned scripts have been moved to `./utils/`
Install all dependencies using poetry. There are some dev dependencies for code formatting. 

`./assets` contains hero images, neural network dataset, and some t500 images used during testing. Do not modify these files. Create the directory `./assets/leaderboard_images` as a supply for `generator.py`

`./data` contains the sqlite3 database.

`./leaderboards` contains all the tools required for loading, parsing, and converting leaderboard images into lists of LeaderboardEntry objects. 

`./neural_network` contains the models and model structure.

`./benchmarks.py` is used for performance testing the selected hero identification method. This uses pre-defined files with an answer key to validate performance. 

`deblank2ify.py` is used to filter the database. This converts all 'Blank2' entries to 'Blank'

`server.py` is a FastAPI server which loads the data from the database, conducts calculations and filtering on the data, and stores it in memory. It then serves the webpage(s) displaying this data.

`train.py` is used to train the model. See inline documentation for more details. 

#### Neural Network 
The neural network is trained on the dataset located in `./assets/top_500_mnist_images`. This dataset is a collection of images of the top 500 leaderboard for each hero. The images are 49x50 pixels. Labels are numbered and indexed in line 50 of `./heroes/her0_comparison.py`. 

The images in the dataset are processed using `./process_mnist.py`. This scriipt converts the images to grayscale, and then converts it to an array of 8 bit signed integers. This array is then saved to its same path, except in in `./assets/top_500_mnist_images/`.

The model is trained using `./train.py`. This script loads the dataset, and trains the model. This script is a CLI tool and a proxy script for training the model. 

In order to add labels to the model, follow these steps:
1. Create a new directory in `./assets/top_500_unprocessed_images/`. This folder will be named a number, which is the new label. Open `./assets/top_500_mnist_images/test/` and look for the highest number. You can create a new label which is one greater than this number. 
2. Populate the dataset. Currently, all images are identical. Test: 18 images; Train: 108 images. `./srcfile_duplicator.py` can be used to duplicate a single image into multiple images. Modify the path as needed. 
3. Run `./process_mnist.py` on the new directory. This will make modifications to the images in the directory, and save them to `./assets/top_500_mnist_images/`. 
4. Open `./train.py` and modify the model dense layer to support the new number of labels. These labels are sequential 0-38, so the last dense layer should be `model.add(Layer_Dense(128, 39))`. or one greater than the number of your label. 
5. Run `./train.py` to train the model. The model name should be your github username, and the current date. For example `thearyadev-2023-04-30`. The model description should be differences or reason that the model is being trained. For example `added lifeweaver`.
6. In `./heroes/hero_comparison.py`, add the new label to the `hero_labels` dict. This list is used to map the label to the hero name.
7. Do manual validation of the model. Using `./benchmarks.py`, you can test the model against a set of images that have been manually classified. This script will output the results of the test. If the model is not performing well, you can re-train the model.
8. In your pull request, include a screenshot of the results of `./benchmarks.py` and a screenshot of the "Training Progress" table shown during training. 


## Contributing Guidelines

1. Install dev dependencies using Poetry. 
2. Use [isort](https://pypi.org/project/isort/) to sort imports, THEN use [black](https://pypi.org/project/black/) for formatting. Black will format the imports differently than isort. (i dont have precommit configured for this project, sorry...)
3. Be descriptive in pull requests. 

## 🚀 About Me
I'm a developer. Actively learning and looking for new and interesting opportunities. Send me a message: aryan@aryankothari.dev


## License
[Apache-2.0](/LICENSE)


[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fthearyadev%2Ftop500-aggregator.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fthearyadev%2Ftop500-aggregator?ref=badge_large)
