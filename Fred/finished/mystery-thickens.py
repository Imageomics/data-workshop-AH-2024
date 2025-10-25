# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python (dw-uv)
#     language: python
#     name: dw-uv
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
from io import BytesIO
from PIL import Image
from PIL.TiffTags import TAGS

# %% [markdown]
# ## 1. Download the original/upstream/source dataset (Kydoimos) 

# %%
# The upstream dataset is on Hugging Face: https://huggingface.co/datasets/johnbradley/Kydoimos

dataset_path = "johnbradley/Kydoimos"

# Note that if the dataset does not load using the dataset ID above, try the following two lines instead:
# # !git clone https://huggingface.co/datasets/johnbradley/Kydoimos ../../Kydoimos
# dataset_path = "../../Kydoimos"

kydoimos = load_dataset(dataset_path)

# %% [markdown]
# ### Explore the upstream dataset

# %%
# View the upstream dataset contents
# Note that the full dataset is in the 'train' split only because that is the default split when loading the dataset
kydoimos

# %%
# Look at a sample image
kydoimos['train']['image'][1]

# %%
# See that the image is a PIL object
print(kydoimos['train']['image'][0])

# %% [markdown]
# ### Load the upstream dataset into a Pandas dataframe for simpler exploration

# %%
kydoimos_df = pd.DataFrame(kydoimos['train'])
# This command loads the image data into the dataframe as a column. This is not recommended for large datasets. Since our dataset is small, it's OK.

# To make a dataframe without the image column, use the following command instead: 
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
shaggy_dir = '../../Shaggy/'
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

# Note that a small change in the data will result in a completely different checksum.

# Review the 'further-reading.ipynb' notebook for more info on computing MD5 checksums.

# %%
# Create functions for MD5 checksums

# For use with reading files from disk
def file_md5_checksum(file_path):
    hash = hashlib.md5()
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        hash.update(file_bytes)
    checksum = hash.hexdigest()
    return checksum

# For use with decoded PIL image objects
def pil_md5_checksum(image):
    hash = hashlib.md5()
    buffer = BytesIO()
    # Normalize to RGB and consistent encoding
    img = image.convert("RGB")
    img.save(buffer, format="TIFF")
    hash.update(buffer.getvalue())
    checksum = hash.hexdigest()
    return checksum


# %%
# Run MD5 checksum on Shaggy's and Kydoimos datasets
shaggy_df['md5'] = shaggy_df['rel_file_path'].apply(file_md5_checksum)
kydoimos_df['md5'] = kydoimos_df['image'].apply(pil_md5_checksum)

# %%
kydoimos_df.head(3)

# %%
# Now that we have the MD5 checksums, we can save them to a CSV file for future use (omitting the 'image' column).
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
# *The intrinsic metadata is dropped when the image is decoded as a PIL object.*
#
# The pixel contents might not be different, but the _file representation_ has changed. When saving to bytes for hashing, each image was re-encoded, rewriting the metadata, which changed the binary content. 
#
# To make a good comparison, we'll load Shaggy's dataset into Pillow objects the same way before hashing.

# %%
# The plan for this cell is to load the images from disk into the dataframe as PIL objects and compute the MD5 checksums.
# Expect this cell to yield an UnidentifiedImageError: cannot identify image file '<path-to->/amalfreda_0.tif'
# We also got a warning stating "UserWarning: Corrupt EXIF data.  Expecting to read 2 bytes but only got 0. 

shaggy_df['image'] = shaggy_df['rel_file_path'].apply(lambda x: Image.open(x)) 

shaggy_df['pil_md5'] = shaggy_df['image'].apply(pil_md5_checksum)

shaggy_df

# %%
# To get a fresh preview at the dataframe:
shaggy_df

# %%
# We can try to open the individual image causing a problem.
img = Image.open('../../Shaggy/images/amalfreda_0.tif') # try with amalfreda_1.tif, which will work
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

# %%
# Now we can apply the `pil_md5_checksum` function (same as the code that failed above)
shaggy_df['image'] = shaggy_df['rel_file_path'].apply(lambda x: Image.open(x)) 

shaggy_df['pil_md5'] = shaggy_df['image'].apply(pil_md5_checksum)

shaggy_df

# We can see below that the "md5" and "pil_md5" values for each entry are different. This is because the "md5" column was computed from the file on disk, while the "pil_md5" column was computed from the PIL image object. The PIL image object may have been modified in memory, which is why the checksums differ.

# %%
kydoimos_df.info()
# After fix, 110 in kydoimos

# %%
shaggy_df.info()
# After fix, 107 in shaggy

# %%
# Retry the merge using the PIL checksums for each image
merge_df = pd.merge(shaggy_df, kydoimos_df, left_on="pil_md5", right_on="md5", how="inner", suffixes=("_shaggy", "_kydoimos"))
merge_df

# %%
merge_df.info()

# %%
merge_df['file_name'].nunique() # But Shaggy had 107 images ... where's the extra one hiding? Did something change size?

# %%
# Let's find the images that don't match between the two datasets and display them

from IPython.display import display

mismatches = shaggy_df.loc[~shaggy_df['pil_md5'].isin(merge_df['pil_md5']), :]
mismatches['image'].apply(display)


# %% [markdown]
# ### Looks like some of Shaggy's personal photos found their way into the dataset while he was organizing things ...

# %%
# We can remove the images that don't match from the Shaggy dataframe
shaggy_df = shaggy_df.drop(shaggy_df.loc[~shaggy_df['pil_md5'].isin(merge_df['pil_md5'])].index)


# %%
shaggy_df.info() # Now the number of images in Shaggy's dataframe matches the number that were merged.

# %%
merge_df['file_name'].nunique()

# %%
merge_df.info()

# However, we have more images in the merged dataframe compared to either input dataframe. There must be duplicates.

# %%
# We can identify the duplicates using the MD5 checksums for the PIL object form of each image.
shaggy_dup_mask = shaggy_df.duplicated(subset="pil_md5", keep=False)
shaggy_dups = shaggy_df[shaggy_dup_mask].sort_values(by='pil_md5')
shaggy_dups.info()

# %%
kydoimos_dup_mask = kydoimos_df.duplicated(subset="md5", keep=False)
kydoimos_dups = kydoimos_df[kydoimos_dup_mask].sort_values(by="md5")
kydoimos_dups.info()

# %%
# Look at a sample of the duplicates
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
# This shows that there is data leakage between the test and train splits.
# That's the final nail in the coffin for Shaggy's dataset. 
# At this point, it will be simpler to start over from Kydoimos and organize a new dataset.

# %%
