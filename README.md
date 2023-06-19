# Scoreboard-detection

## Problem Statement

We are tasked with developing an automated system to detect scoreboards from videos and extract
the team names and their respective scores. The system will further analyze the scores to determine
the winner of the match based on the extracted information.

## Project Description

Given video footage of a sports match, the objective is to design an algorithm or system capable
of detecting and localizing scoreboards, which are graphical overlays displaying team names and
their respective scores. The scoreboards can appear at various positions and have different styles,
such as static images or dynamic elements.

The algorithm should identify the scoreboard regions within the video frames and extract the
textual information corresponding to the team names and scores. It should handle variations in font
styles, background colors, and potential occlusions caused by other on-screen graphics or players.
Once the team names and scores are extracted, the algorithm must compare the scores to determine
the winner of the match. The team with the higher score is declared the winner, assuming the
scoring system is the same for both teams.

**Note:** It is important to note that the algorithm does not need to recognize the sport being played
or interpret any specific game rules. It focuses solely on detecting and extracting scoreboard
information for score comparison and winner determination.

The solution should be efficient, accurate, and scalable, as it will be applied to many videos from
different sports matches. The system should handle various video resolutions and formats,
allowing it to process both live footage and pre-recorded videos.

**Expected Input:**

* Video footage of a sports match containing scoreboards.
* The footage can be in various resolutions and formats (e.g., MP4, AVI, etc.).
* The scoreboard regions may vary in size, position, and appearance.
* The scoreboard content includes team names and their respective scores.

**Expected Output:**
* Detected scoreboard regions with their respective team names and scores.
* The winner of the match is based on the extracted scores.

**Constraints:**

The algorithm should be robust enough to handle different sports, including but not limited to
soccer, basketball, etc.

* The algorithm should work on pre-recorded footage.
* The solution should be computationally efficient, considering potential resource limitations.

**Note:** The problem does not involve real-time video analysis for live broadcasting but instead
focuses on an offline analysis of recorded videos. The emphasis is on developing an accurate
scoreboard detection algorithm and determining the winner based on the extracted scores.

## Setting Up Envieronment

To download the repository, you can use the following command:

```
bash
git clone https://github.com/shahzebelexoft/scoreboard-detection.git
```

This command will clone the repository from the specified URL and create a local copy on your machine.

Before starting the project, it is necessary to install Anaconda on your PC. If you are a Windows user, 
please follow the installation guide available at https://docs.anaconda.com/free/anaconda/install/windows/. 
For Linux users, you can refer to the installation guide at https://docs.anaconda.com/free/anaconda/install/linux/.

To navigate to the project directory, open the terminal and use the 'cd' command:

```
bash
cd {PROJECT_DIRECTORY}
```

Replace `PROJECT_DIRECTORY}` with the actual path of your project directory.

To create the environment and install the required dependencies, enter the following commands in the terminal:

```
bash
conda env create -f environment.yml
```

Please make sure you have an environment.yml file in your project directory containing the necessary specifications for the environment setup.

## TO-DO:

**Gather more dataset:** Collect additional data to enhance the dataset.
**Label a few datasets and clone the labels:** Manually annotate a subset of the dataset and replicate the labels to speed up the labeling process.
**Train models on the dataset:** Train various models using the dataset.
**Evaluate the model on every available video:** Assess the model's performance by testing it on each video in the dataset.
**Perform Optical Character Recognition (OCR) on the detected scoreboard:** Utilize OCR techniques to extract text information from the identified scoreboards.
**Determine the winning team based on respective scores:** Analyze the scores of the respective teams and declare the winner based on the comparison.

