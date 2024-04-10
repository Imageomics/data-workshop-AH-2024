# Mastering Data Management Workshop - All Hands 2024
Repository for Mastering Data Management Workshop at the Imageomics All Hands 2024.

**When**: April 16th, 8:30am to 11:45am ET.
**Where**: Collaborative Space in Pomerene Hall (3rd Floor).

This session will be interactive; bring your laptop ready to go (as described below).

## Before the Workshop

 Please make sure to bring your computer to the workshop with the following actions completed:
 1. Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).
 2. Create a conda environment on your machine with all required packages: Open a terminal/command line window and run:
    ```bash
    conda create -n data-workshop-2024 -c conda-forge pandas jupyterlab scikit-learn datasets pillow -y
    ```
3. Clone this repository to your local machine.

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
