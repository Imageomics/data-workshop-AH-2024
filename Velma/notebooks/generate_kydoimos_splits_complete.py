# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import seaborn as sns

# We'll be making splits after cleaning
from sklearn.model_selection import train_test_split

sns.set_style("whitegrid")

# %% [markdown]
# # Explore Original Dataset
#
# Shaggy pulled his dataset from [johnbradley/Kydoimos](https://huggingface.co/datasets/johnbradley/Kydoimos). There's not much information there, but we can at least look at the original data and sort through it to get a usable dataset. The MD5s from Fred's attempt at re-alignment will be particularly helpful!
#
# **DISCLAIMER:** This is a toy example intended to demonstrate real-world challenges in data collection & curation in a digestible format; in reality, more data would be required for such a project.

# %%
df = pd.read_csv("../data/kydoimos.csv", low_memory = False)
df.info()

# %%
df.head()

# %%
df["Type Status"].value_counts()

# %%
print(f"We have {df.Subspecies.nunique()} unique subspecies and Type Status is in")
df.loc[df["Type Status"].notna(), "Subspecies"].nunique()

# %% [markdown]
# Nearly all of column `Type Status` is null, and it's only in one included subspecies. I believe it has to do with hybrids or species recognition, but we should probably ask a biologist....(Cue question to the room, fill in given answer and we'll drop) let's drop it.
#
# We'll make a note that it's being removed (in the Data Curation Section) since it's nearly all null and not applicable across the dataset.

# %%
cols = [col for col in list(df.columns) if col != "Type Status"]
df = df[cols]

# %%
df.head()

# %% [markdown]
# ## Rename Column with Space
#
# Spaces in column names makes things more complicated, so let's simplify the `NHM specimen number` column name (we will need to document that too).
#

# %%
df.rename(columns= {"NHM specimen number": "NHM_specimen_number"}, inplace = True)

# %% [markdown]
# Fred said Shaggy's data had some duplication, so let's check on our unique values here.

# %%
df.nunique()

# %% [markdown]
# It seems we only actually have 76 unique images of 38 specimens.
#
# What are all those different views? And different sexes?

# %%
print(df.View.unique())
print(df.Sex.unique())

# %% [markdown]
# Ah, we have `dorsal` and `dorsal ` in addition to variations in case for the `ventral` label. Similar issue with `male` and `female` labels.
#
# Let's standardize all of these to just the lowercase without a trailing space.

# %%
df["View"] = df.View.str.lower()
df["Sex"] = df.Sex.str.lower()
df.loc[df["View"] == "dorsal ", "View"] = "dorsal"
df.loc[df["Sex"] == "male ", "Sex"] = "male"

# Now look at distribution
print(df.View.value_counts())
df.Sex.value_counts()

# %% [markdown]
# That's a bit cleaner, but we still have a disagreement between unique IDs, specimen numbers, and MD5s!
#
# We don't want to lose metadata or keep an incorrect labelling, so let's check the duplication on MD5, View, Species, and Subspecies values.
# We'll check all the duplicates as a whole first.

# %%
df["duplicates"] = df.duplicated("md5", keep = False)
df["duplicates"].value_counts()

# %%
duplicates = df.loc[df["duplicates"]]
duplicates.nunique()

# %% [markdown]
# So all of our `id`s are unique, but we seem to have duplicates of 34 images. This is across both species, sexes, and views, as well as 3 of the 6 subspecies.
#
# Let's check for consistency across this metadata for each image.

# %%
STATS_COLS = ["NHM_specimen_number", "Species", "Subspecies", "View", "Sex", "md5"]
duplicates.duplicated(STATS_COLS, keep = "first").value_counts()

# %% [markdown]
# Great, it's an even split, so we'll just keep the first instance of each.

# %%
df["duplicates"] = df.duplicated(STATS_COLS, keep = "first")
df["duplicates"].value_counts()

# %%
cleaned_df = df.loc[~df["duplicates"]]
cleaned_df.info()

# %%
cleaned_df.nunique()

# %%
# Remove duplicates column (only run once!)
cleaned_df = cleaned_df[list(cleaned_df.columns)[:-1]]

# %% [markdown]
# ### Check Distribution of Data

# %%
sns.histplot(cleaned_df, y = "Subspecies", hue = "Species")

# %%
sns.histplot(cleaned_df, y = "Subspecies", hue = "View")

# %% [markdown]
# We have perfect balance of dorsal and ventral images.

# %%
sns.histplot(cleaned_df, y = "Subspecies", hue = "Sex")

# %% [markdown]
# We can't train an unbiased model to predict sex with only one sex represented for a subspecies, so we'll remove `amalfreda` and `lativitta` until we can maybe get more data in the future, but first let's save the cleaned dataset as it may be useful elsewhere.

# %% [markdown]
# ### Save Master Dataset File
#
# Let's save this cleaned up dataset file for easier reference later.

# %%
cleaned_df.to_csv("../data/kydoimos_cleaned.csv", index = False)

# %% [markdown]
# ## Make Splits
#
# Remove skewed subspecies.

# %%
skewed_ssp = ["amalfreda", "lativitta"]
reduced_df = cleaned_df.loc[~cleaned_df["Subspecies"].isin(skewed_ssp)].copy()

reduced_df.nunique()

# %%
# Get list of subspecies included for Dataset Card
reduced_df.Subspecies.unique()

# %% [markdown]
# Before we can make our splits, let's separate out a dorsal subset from the ventral. This way we can maintain uniqueness of specimens across splits. We'll add in the ventral images to each split based on specimen ID being in the training list or the test list for the dorsal images.

# %%
dorsal_df = reduced_df.loc[reduced_df["View"] == "dorsal"].copy()

# Quick check on uniqueness within this subset
dorsal_df.nunique()

# %%
sns.histplot(dorsal_df, y = "Subspecies", hue = "Sex")

# %% [markdown]
# It's still not balanced so let's stratify on `Sex` and `Species` (close enough balance), set a `random_state` for reproducibility.
#
# Not a large enough sample of images for stratifying on `Subspecies` (as we should)-—`stratify` ensures split distributions are representative of the distributions in the data

# %%
train_df, test_df = train_test_split(dorsal_df, 
                                     test_size = .2,
                                     stratify = dorsal_df[["Sex", "Species"]],
                                     random_state = 614)

# %% [markdown]
# ### Add Ventral Images to Splits
#
# Let's get a list of each split's specimen IDs so we can align all our images accordingly.

# %%
#train_ids = list(train_df["NHM_specimen_number"].unique())
test_ids = list(test_df["NHM_specimen_number"].unique())

# %%
# Now assign images
reduced_df["split"] = "train"
reduced_df.loc[reduced_df["NHM_specimen_number"].isin(test_ids), "split"] = "test"

# Check
reduced_df.split.value_counts()

# %% [markdown]
# We have a nice 80-20 split that should be representative of our data and will not have any data leakage as we have removed duplicate images and assigned all images of a specimen to the same split.

# %% [markdown]
# ### Save our Completed Dataset
#
# Let's save this dataset with the split column. We can start thinking about training now!

# %%
reduced_df.to_csv("../data/ButterflyImages_metadata.csv", index = False)

# %%
