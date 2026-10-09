# Mastering Data Management Workshop - All Hands 2024 [![DOI](https://zenodo.org/badge/784343261.svg)](https://doi.org/10.5281/zenodo.17429276)

This data training was originally presented as an in-person, interactive session at the Imageomics All Hands in 2024: the Mastering Data Management Workshop. It runs through an initial analysis of a simplified dataset, filling in a dataset card as the data is explored, cleaned, and prepared for training. All materials used for the workshop are provided in this repository to allow for continued, asynchronous re-use. To complete the training, follow the below instructions.

## Post-Workshop Use

How to use this repo post-workshop: If you missed the workshop or would like to review the materials, there are both blank and complete versions of the notebooks completed during the workshop available in this repo. There is also a [`further_reading` folder](https://github.com/Imageomics/data-workshop-AH-2024/tree/main/further_reading) with more information on topics covered during the workshop, as well as resources to learn more.

### Tutorial step-by-step instructions

1. Clone this repository and follow the [pre-workshop set up instructions](#before-the-workshop) to prepare your local environment.
2. Read the [Key Learning Objectives](#key-learning-objectives).
3. Read the [Story of the Workshop](#story-of-the-workshop).
4. Follow along with the [workshop lesson](https://youtu.be/71Ww42ddz9s).
5. Review extra notes in the [Further Reading](further_reading) section, which contains pointers and links to other resources.

## Before the Workshop

 Please make sure to bring your computer to the workshop with the following actions completed:
 1. Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).
 2. Create a conda environment on your machine with all required packages: Open a terminal/command line window and run:
    ```bash
    conda create -n data-workshop-2024 -c conda-forge pandas jupyterlab ipywidgets scikit-learn datasets pillow seaborn opencv -y
    ```
3. Clone this repository to the home directory of your local machine.

> Note: We will use Unix commands in the workshop. If you are using Windows, you can use Git Bash to run these commands.

### Key Packages

The key packages used in this workshop are described below, organized by their use-cases.

- Data wrangling: `pandas` (DataFrames, the data structure), `datasets` (for accessing the data from Hugging Face).
- Notebooks (where the work is done): `jupyterlab`, `ipywidgets` .
    - The notebooks can be run in VSCode or by launching Jupyter from the command line (as done in the tutorial itself).
- Image handling and visualizations: `pillow`, `seaborn`.
- Machine learning tools: `scikit-learn`, `opencv`.

## During the Workshop

Navigate into the workshop repository, retrieve any updates, activate the environment, and launch a Jupyter notebook:

```bash
cd ~/data-workshop-AH-2024 # or wherever you have it stored
```
```bash
git pull origin main
conda activate data-workshop-2024
jupyter lab
```

Follow along with the hands-on instructions.

## Key Learning Objectives

- **_Provenance_**
    - What is it?
    - Why does it matter?
    - How do we document and preserve it?
- **_Data Analysis/Exploration_**
    - Key factors to check when exploring new data.
    - Why do we explore data before training and what should we establish about the data prior to training?
- **_Documentation_**
    - How and where to document information about data.
    - _Always_ record assumptions.

## Story of the Workshop

Last semester/year, Shaggy did a project predicting the sex of butterflies based on images. The `Shaggy` folder is his repo; it contains the collection of images that he used, along with a notebook for generating the dataset, a CSV, and a README pointing to the original source (a toy dataset we created for this lesson). You want to build on Shaggy's work, so you go to look at his data and fill in a [Dataset Card](https://imageomics.github.io/Imageomics-guide/wiki-guide/HF_DatasetCard_Template_mkdocs/) with more information (alternatively, see the template in the `Files` folder to get a copy of the template as of April 2024).

Looking at Shaggy's work, you discover that the notebook _cannot_ be run:
- the source file is missing,
- `py` files used for manipulating the data are not included,
- his general descriptions are lacking,
- ultimately his dataset creation cannot be reproduced.

The project gets handed to Fred to investigate and try to match back to the original dataset to recover the metadata.

The `Fred` folder walks us through investigating Shaggy's dataset more closely and comparing to the original dataset. It goes over some use of MD5s for comparison and duplicate-detection, with more details provided in `further_reading`. The completed notebook is in `Fred/finished`.

In `Fred/mystery-thickens.ipynb`, we learn about duplication in both Shaggy's dataset and the upstream source, as well as corrupted and erroneous files. The dataset is pulled from Hugging Face and explored, then a new CSV documenting all available upstream image metadata is created with MD5s of all images as an additional column.

This new CSV is passed to Velma, along with the Dataset Card from the initial exploration of Shaggy's data to explore and re-create a dataset to predict the sex of butterflies based on images.

The `Velma` folder is entirely self-contained, though the README and data file (`kydoimos.csv`) are created in the first two parts of the workshop. There are complete versions of the README and notebook as done during the workshop (as well as an earlier completed version with a paired `py` file). A recording of this part of the workshop--where we explore the data, clean it (standardizing terms and removing duplicates), and generate splits--can be found on the [Imageomics YouTube Channel](https://www.youtube.com/@ImageomicsInstitute/videos); it is an hour and 15 minutes long.

## Images

All images in [`Shaggy/images/`](https://github.com/Imageomics/data-workshop-AH-2024/blob/main/Shaggy/images) are public domain, sourced from [(Hoyal Cuthill et al., 2019)](https://doi.org/10.5061/dryad.2hp1978), _**except**_ [`thelxiopeia_13.tif`](https://github.com/Imageomics/data-workshop-AH-2024/blob/main/Shaggy/images/thelxiopeia_13.tif) which was sourced from [this website](https://www.scoobydudes.com/episode-17-scoobra-kadoobra) and is copyrighted by [Hanna-Barbera and Warner Bros. Entertainment](https://scoobydoo.fandom.com/wiki/Scoobypedia:Legal_Disclaimer).

