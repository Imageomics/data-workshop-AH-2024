# Mastering Data Management Workshop - All Hands 2024
Repository for Mastering Data Management Workshop at the Imageomics All Hands 2024.

- **When**: April 16th, 8:30am to 11:45am ET.
- **Where**: 320 TDAI Ideation Zone, Pomerene Hall.

This session will be interactive; bring your laptop ready to go (as described below).

## Before the Workshop

 Please make sure to bring your computer to the workshop with the following actions completed:
 1. Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).
 2. Create a conda environment on your machine with all required packages: Open a terminal/command line window and run:
    ```bash
    conda create -n data-workshop-2024 -c conda-forge pandas jupyterlab ipywidgets scikit-learn datasets pillow seaborn opencv -y
    ```
3. Clone this repository to the home directory of your local machine.

> Note: We will use Unix commands in the workshop. If you are using Windows, you can use Git Bash to run these commands.

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

Last semester/year, Shaggy did a project predicting the sex of butterflies based on images. The `Shaggy` folder is his repo; it contains the collection of images that he used, along with a notebook for generating the dataset, a CSV, and a README pointing to the original source (a toy dataset we created for this lesson). You want to build on Shaggy's work, so you go to look at his data and fill in a [Dataset Card](https://github.com/Imageomics/internal-guidelines/blob/main/templates/HF_DatasetCard_Template_Imageomics.md?plain=1) with more information (for non-Imageomics members, see the template in the `Files` folder to get a copy of the template as of April 2024). 

Looking at Shaggy's work, you discover that the notebook _cannot_ be run:
- the source file is missing,
- `py` files used for manipulating the data are not included,
- his general descriptions are lacking,
- ultimately his dataset creation cannot be reproduced.

The project gets handed to Fred to investigate and try to match back to the original dataset to recover the metadata.

The `Fred` folder walks us through investigating Shaggy's dataset more closely and comparing to the original dataset. It goes over some use of MD5s for comparison and duplicate-detection, with more details provided in `further_reading`. The completed notebook is in `Fred/finished`.

In `Fred/mystery-thickens.ipynb`, we learn about duplication in both Shaggy's dataset and the upstream source, as well as corrupted and erroneous files. The dataset is pulled from Hugging Face and explored, then a new CSV documenting all available upstream image metadata is created with MD5s of all images as an additional column.

This new CSV is passed to Velma, along with the Dataset Card from the initial exploration of Shaggy's data to explore and re-create a dataset to predict the sex of butterflies based on images.

The `Velma` folder is entirely self-contained, though the README and data file (`kydoimos.csv`) are created in the first two parts of the workshop. There are complete versions of the README and notebook as done during the workshop (as well as an earlier completed version with a paired `py` file). A recording of this part of the workshop--where we explore the data, clean it (standardizing terms and removing duplicates), and generate splits--can be found [here](); it is an hour and 15 minutes long.


# Post-Workshop Use

How to use this repo post-workshop: If you missed the workshop or would like to review the materials, there are both blank and complete versions of the notebooks completed during the workshop available in this repo. There is also a [`further_reading` folder](https://github.com/Imageomics/data-workshop-AH-2024/tree/main/further_reading) with more information on topics covered during the workshop, as well as resources to learn more.


# Images

All images in [`Shaggy/images/`](https://github.com/Imageomics/data-workshop-AH-2024/blob/main/Shaggy/images) are public domain, sourced from [(Hoyal Cuthill et al., 2019)](https://doi.org/10.5061/dryad.2hp1978), _**except**_ [`thelxiopeia_13.tif`](https://github.com/Imageomics/data-workshop-AH-2024/blob/main/Shaggy/images/thelxiopeia_13.tif) which was sourced from [this website](https://www.scoobydudes.com/episode-17-scoobra-kadoobra) and is copyrighted by [Hanna-Barbera and Warner Bros. Entertainment](https://scoobydoo.fandom.com/wiki/Scoobypedia:Legal_Disclaimer).

