# Further Reading

This folder provides more detailed information on topics covered during the Mastering Data Management Workshop. It also highights other important related topics that we did not have the time to cover in as much detail, and provides resources to learn more.

## The Power of Unique Identifiers

Adding a unique identifier can help prevent some of the issues discussed in this training, while simplifying operations applied across datasets (especially as they get larger and combine multiple sources). The `uuid` package can be used to easily assign a unique identifier to all metadata entries:
```python
import uuid

# Add uuid column
df["uuid"] = [uuid.uuid4() for i in range(df.shape[0])]
```

## Avoiding Duplicates and Data Leakage

### Check for byte-wise duplication

This can be done with checksums, though be sure to open all images with the same package (eg., PIL) as this can impact the _intrinsic_ metadata, though it will not impact the image content. MD5s check both.

For more on this, see the `implementation_details` notebook.

### Ensure Provenance is trackable for all images

This ensures the reproducibility of your dataset and that appropriate credit is given (in both the academic and legal senses). It also provides you peace of mind; in the event of a corrupted file or other image-altering event, maintaining the link back to the original image ensures that the information is recoverable. 

### Summary
- Open files to be compared with the same method.
- Use MD5 checksum to compare content of data and intrinsic metadata.
- Use a library like PIL to read images to ensure they're not accidentally corrupted.


## Resources
- [Imageomics Internal Guidelines Repo](https://github.com/Imageomics/internal-guidelines)
    - [HF templates](https://github.com/Imageomics/internal-guidelines/tree/main/templates): Dataset and Model Card templates for Imageomics Datasets and Models. These include some general keywords, grant acknowledgement, and general guidance and recommendations for various sections, along with some HF-flavored markdown tips.
        - We covered the sections of a Dataset Card pertaining to information about the data itself, but don't forget about the other sections for a real dataset or model!
        - The `yaml` portion at the top is a place to add keywords and other useful information to help index your model or dataset in searches on Hugging Face (eg., by size, task, and license).
        - Adding an appropriate [license](https://github.com/Imageomics/internal-guidelines/wiki/3.2.-Hugging-Face-Repo-Guide#license) and citation allow others to re-use and then properly cite your model or dataset more easily.
    - [Wiki](https://github.com/Imageomics/internal-guidelines/wiki): Repo guides, Workflows, and more!
- Overview and further reading on [FAIR Principles](https://book.the-turing-way.org/reproducible-research/rdm/rdm-fair) from the [Turing Way](https://book.the-turing-way.org/).
