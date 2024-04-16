---
license: cc0-1.0
language:
- en
pretty_name: ButterflyImages
task_categories:
- image-classification
tags:
- biology
- image
- animals
- CV
- butterfly
- erato
- melpomene
- dorsal
- ventral
size_categories:
- n<1K
---


<!--
Image with caption:
|![Figure #](https://huggingface.co/imageomics/<data-repo>/resolve/main/<filename>)|
|:--|
|**Figure #.** [Image of <>](https://huggingface.co/imageomics/<data-repo>/raw/main/<filename>) <caption description>.|
-->

<!--
Notes on styling:

To render LaTex in your README, wrap the code in `\\(` and `\\)`. Example: \\(\frac{1}{2}\\)

Escape underscores ("_") with a "\". Example: image\_RGB
-->

# Dataset Card for ButterflyImages

<!-- Provide a quick summary of what the data is or can be used for. --> 
Images of butterflies with sex metadata sourced from [Kydoimos Dataset](https://huggingface.co/datasets/johnbradley/Kydoimos).

## Dataset Description

<!-- Provide the basic links for the dataset. -->

- **Homepage:** 
- **Repository:** [related project repo]
- **Paper:** 
- **Leaderboard:** 
- **Point of Contact:** 

### Dataset Summary

<!-- Provide a longer summary of what this data is. -->

<!--This dataset card aims to be a base template for new datasets. It has been generated using [this raw template](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md?plain=1).-->

### Supported Tasks and Leaderboards
[More Information Needed]

### Languages
[More Information Needed]

## Dataset Structure

```
images/
   <id_1>.tif
   <id_2>.tif
   ...
   <id_50>.tif
ButterflyImages_metadata.csv
```

### Data Instances
[More Information Needed]

- Type: TIFF
- Size ~ 3 KB - 20 KB
- background color - grey

TODO: Verify the image size range.

<!--
Describe data files
-->

### Data Fields

- `id`: Unique identifier for dataset (`KDS######`).
- `NHM_specimen_number`: Identifier that is associated with the butterfly in the image (assigned by NHM).
- `View`: the view of the butterfly in the image, `dorsal` or `ventral`.
- `Species`: the species of the butterfly in the image: 'melpomene', 'erato'.
- `Subspecies`: the subspecies of the butterfly in the image: 'thelxiopeia', 'melpomene', 'guarica', 'etylus'.
- `Sex`: Sex of the butterfly in the image either 'male' or 'female'.
- `md5`: the MD5 of the image after reading with PIL.
- `split`: Train test split either 'train' or 'test'.

### Data Splits

Splits are marked in the metadata file as "train" or "test". The test set is 20% of the data, balanced for species and sex, as view is already balanced in the dataset. Both images of a given specimen are in one or the other split.

## Dataset Creation

The following steps were performed in the `generate_kydoimos_splits` notebook, using the `kydoimos.csv` created in `Fred/mystery-thickens.ipynb`.

- Kydoimos image metadata was augmented with md5 column
- Removed `Type Status` column that was nearly all null.
- Renamed "NHM specimen number" as "NHM_specimen_number" for easier processing.
- Standardized column contents.
- Checked consistency across metadata, and removed duplicates based on matching MD5s and other identifying information.
- Saved a cleaned copy of the metadata `data/kydoimos_cleaned.csv`.
- Removed two subspecies of erato that did not have images of any female specimens: 'amalfreda', 'lativitta'.
- Separated dorsal images into their own dataframe to run the `train_test_split` package from `sklearn`, stratified on `Sex` and `Species`. Then images of both views were assigned to train or test spilts based on `NHM_specimen_number` to avoid data leakage.
- Saved metadata file `data/ButterflyImages_metadata.csv`.



### Curation Rationale
[More Information Needed]

### Source Data

We downloaded this from [Kydoimos Dataset](https://huggingface.co/datasets/johnbradley/Kydoimos).

TODO: Get later information from original source

#### Initial Data Collection and Normalization
[More Information Needed]

#### Who are the source language producers?
[More Information Needed]

### Annotations

#### Annotation process
[More Information Needed]

Source annotation was maintained, views and sexes were standardized (case, spaces).

#### Who are the annotators?
[More Information Needed]

### Personal and Sensitive Information
[More Information Needed]

<!-- For instance, if your data includes people or endangered species. -->

## Considerations for Using the Data
### Social Impact of Dataset
[More Information Needed]

### Discussion of Biases
[More Information Needed]

### Other Known Limitations
[More Information Needed]



<!-- For instance, if your data exhibits a long-tailed distribution (and why). -->

## Additional Information

### Dataset Curators
[More Information Needed]

### Licensing Information
[More Information Needed]

### Citation Information
[More Information Needed]
<!--
If you want to include BibTex, replace "<>"s with your info 
-for an associated paper:
```
@article{<ref_code>,
  title    = {<title>},
  author   = {<author1 and author2>},
  journal  = {<journal_name>},
  year     =  <year>,
  url      = {<DOI_URL>},
  doi      = {<DOI>}
}
```
-just for data:
```
@misc{<ref_code>,
  author = {<author1 and author2>},
  title = {<title>},
  year = {<year>},
  url = {https://huggingface.co/datasets/imageomics/<dataset_name>},
  doi = {<doi once generated>},
  publisher = {Hugging Face}
}
```
-->

<!---
If the data is modified from another source, add the following. 

Please be sure to also cite the original data source:
<citation>
-->


### Contributions

The [Imageomics Institute](https://imageomics.org) is funded by the US National Science Foundation's Harnessing the Data Revolution (HDR) program under [Award #2118240](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2118240) (Imageomics: A New Frontier of Biological Information Powered by Knowledge-Guided Machine Learning). Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.

<!-- You may also want to credit the source of your data, i.e., if you went to a museum or nature preserve to collect it. -->
