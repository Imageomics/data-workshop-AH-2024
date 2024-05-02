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

# %% [markdown]
# ### Re-State Our Goal
# *Goal:* We want to use Shaggy's dataset to train a male/female butterfly classifier. And we need to describe the dataset work that Shaggy's done.
#
# ### State Our Assumptions About the Dataset
# When we started, our assumptions were:
# - Shaggy's dataset is derived from Kydoimos
# - No changes have been made to the image data content
# - No images have been added or removed
# - Each component of Shaggy's dataset can be linked to its corresponding component into the source dataset (provenance is intact)
# - Test/train splits are done appropriately
#
# Apparently, some, or all of these assumptions weren't accurate.
#
# ### Make an Intermediate Goal
# *Goal:* We want to see if we can re-link Shaggy's work to the original dataset.</br>
#  To test which of our assumptions are off, let's do the following:
# 1. Download the original/upstream/source dataset (Kydoimos)
# 2. Load Shaggy's dataset
# 3. Run MD5 checksums on all images in Kydoimos and Shaggy's dataset
# 4. Merge on MD5

# %%
# All imports
import pandas as pd
from datasets import load_dataset
import os
import hashlib
import io
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from PIL.TiffTags import TAGS
import numpy as np

# %% [markdown]
# ## 1. Download the original/upstream/source dataset (Kydoimos) 

# %%
# The upstream dataset is on Hugging Face: https://huggingface.co/datasets/johnbradley/Kydoimos

dataset_path = "johnbradley/Kydoimos"
# # !git clone https://huggingface.co/datasets/johnbradley/Kydoimos ../../Kydoimos
# dataset_path = "../../Kydoimos"

kydoimos = load_dataset(dataset_path)

# %% [markdown]
# ### Explore the upstream dataset

# %%
kydoimos

# %%
kydoimos['train']['image'][1]

# %%
print(kydoimos['train']['image'][0])

# %% [markdown]
# ### Load the upstream dataset into a Pandas dataframe for simpler exploration

# %%
kydoimos_df = pd.DataFrame(kydoimos['train'])

# Do this if you would rather not have the actual image data as entries in the dataframe. Since the dataset is small, it's OK.
# kydoimos_df = pd.DataFrame(kydoimos['train'].remove_columns(['image'])) 

# %%
kydoimos_df.head(3)

# %%
kydoimos_df.info()

# %%
# kydoimos_df.nunique() # Note that this gives an error due to the 'image' column
kydoimos_df.drop(columns=['image']).nunique()

# %% [markdown]
# ## 2. Load Shaggy's dataset

# %%
# Load the metadata table into a dataframe
shaggy_dir = '../Shaggy/'
shaggy_df = pd.read_csv(os.path.join(shaggy_dir, 'metadata.csv'), encoding = 'utf-8', low_memory=False)

# Add a column showing how to get to each image from here.
shaggy_df['rel_file_path'] = shaggy_dir + shaggy_df['file_name']

# %%
shaggy_df.head(3)

# %%
shaggy_df.info()

# %%
shaggy_df.nunique()

# %% [markdown]
# ## 3. Run MD5 checksums on all images in Kydoimos and Shaggy's dataset

# %%
# MD5 checksum practice ...
hash = hashlib.md5()
hash.update(b'abcdefg')
checksum = hash.hexdigest()
print(f'abcdefg: {checksum}')

hash = hashlib.md5()
hash.update(b'abcdefG')
checksum = hash.hexdigest()
print(f'abcdefG: {checksum}')

# We have further reading available!

# %%
# Create function for MD5 checksums

# Simple, but could cause OOM error on a massive file
def file_md5_checksum(file_path):
    hash = hashlib.md5()
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        hash.update(file_bytes)
    checksum = hash.hexdigest()
    return checksum

def pil_md5_checksum(image):
    hash = hashlib.md5()
    buffer = BytesIO()
    image.save(buffer, format=image.format)
    hash.update(buffer.getvalue())
    checksum = hash.hexdigest()
    return checksum


# %%
# Run MD5 checksum on Shaggy's and Kydoimos datasets
shaggy_df['md5'] = shaggy_df['rel_file_path'].apply(file_md5_checksum)
kydoimos_df['md5'] = kydoimos_df['image'].apply(pil_md5_checksum)
# kydoimos_df['md5'] = [compute_md5(image) for image in kydoimos['train']['image']]

# %%
kydoimos_df.head(3)

# %%
kydoimos_df.drop(columns=['image']).to_csv('kydoimos.csv', index=False)

# %%
shaggy_df.head(3)

# %% [markdown]
# ## 4. Merge the datasets on MD5 to link them together

# %%
merge_df = pd.merge(shaggy_df, kydoimos_df, on="md5", how="inner")

# %%
merge_df.head()

# %% [markdown]
# ### No matches???
# Like, zoinks Scooby. Something is strange here.
#
# There must be something about the image data that has been changed between the Kydoimos dataset and Shaggy's dataset.
#
# Let's list out the things that could affect the MD5 checksum on the binary data for two images:
# - Image data content (resizing, cropping, color changes, compression, corruption)
# - Image intrinsic metadata
#
# As a shortcut for this class, we'll skip the detective work and get to the solution:
#
# *The intrinsic metadata is changed when the image is loaded as a PIL object, which was done automatically with the Kydoimos dataset by the `datasets` library.*
#
# To address this, we'll load Shaggy's dataset with PIL before taking MD5s again.

# %%
# Expect UnidentifiedImageError: cannot identify image file 'C:\\...\\all-hands-2024-data-workshop\\Shaggy\\images\\amalfreda_0.tif'
shaggy_df['image'] = shaggy_df['rel_file_path'].apply(lambda x: Image.open(x)) 

shaggy_df['pil_md5'] = shaggy_df['image'].apply(pil_md5_checksum)

shaggy_df

# %%
shaggy_df

# %%
img = Image.open('../Shaggy/images/amalfreda_0.tif') # try with amalfreda_1.tif, which will work
img

# %%
img = Image.open('../Shaggy/images/amalfreda_1.tif') # try with amalfreda_1.tif, which will work
img


# %%
# Let's look through the whole set of Shaggy's images and verify the data integrity for each ...

def verify_image(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception as e:
        print(f"Corrupted image detected: {image_path}, error: {e}")
        return False

# Apply the function to each image path in the DataFrame
shaggy_df['valid_image'] = shaggy_df['rel_file_path'].apply(verify_image)

# Optionally, you can drop the 'valid_image' column if it's no longer needed
# shaggy_df.drop(columns=['valid_image'], inplace=True)


# %%
# Filter the dataframe to remove rows with corrupt images
shaggy_df = shaggy_df[shaggy_df['valid_image']]
# Now go back to apply the `pil_md5_checksum` function

# %%
kydoimos_df.info()
# After fix, 110 in kydoimos

# %%
shaggy_df.info()
# After fix, 107 in shaggy

# %%
merge_df = pd.merge(shaggy_df, kydoimos_df, left_on="pil_md5", right_on="md5", how="inner", suffixes=("_shaggy", "_kydoimos"))
merge_df

# %%
merge_df.info()

# %%
merge_df['file_name'].nunique() # But Shaggy had 107 images ... where's the extra one hiding? Did something change size?

# %%
from IPython.display import display
matches = shaggy_df.loc[~shaggy_df['pil_md5'].isin(merge_df['pil_md5']), :]
matches['image'].apply(display)
# shaggy_df.loc[~shaggy_df['pil_md5'].isin(merge_df['pil_md5']), 'image'].apply(display)

# %% [markdown]
# ### Looks like some of Shaggy's personal photos found their way into the dataset while he was organizing things ...

# %%
shaggy_df = shaggy_df.drop(shaggy_df.loc[~shaggy_df['pil_md5'].isin(merge_df['pil_md5'])].index)


# %%
merge_df

# %%
# We have more images in the merged dataframe compared to either input dataframe. There must be duplicates.
shaggy_dup_mask = shaggy_df.duplicated(subset="pil_md5", keep=False)
shaggy_dups = shaggy_df[shaggy_dup_mask].sort_values(by='pil_md5')
shaggy_dups.info()

# %%
kydoimos_dup_mask = kydoimos_df.duplicated(subset="md5", keep=False)
kydoimos_dups = kydoimos_df[kydoimos_dup_mask].sort_values(by="md5")
kydoimos_dups.info()

# %%
kydoimos_dups.head(8)

# %% [markdown]
# Quite a few duplicates come from the upstream dataset
# It looks like these are coming from unique "id" but identical "NHM specimen number" entries. 
#
# Now that we know duplicates are an issue, we should check if we have duplicates between our test and train splits.

# %%
# shaggy_dups
grouped = shaggy_dups.groupby('pil_md5')['split'].unique()

# Filter groups where both 'test' and 'train' are present
both_splits = grouped[grouped.apply(lambda x: 'test' in x and 'train' in x)]

# Count the number of 'pil_md5' values present in both 'test' and 'train'
print(both_splits.size)

# %% [markdown]
# That's the final nail in the coffin for Shaggy's dataset. We are going to need to start over!
