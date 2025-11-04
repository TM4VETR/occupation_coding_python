# Occupation Coding – Python Wrapper

This repository provides a Python wrapper around the 
[**occupationCoding**](https://github.com/malsch/occupationCoding) R package by **Malte Schierholz** and collaborators.  
It aims to easily use occupation coding functionalities for German job titles from Python.


## Requirements

Before you start, ensure that you have the following installed:

- **Python** ≥ 3.10  
- **R** ≥ 4.2 

Recommendation: Set the *R_HOME* environment variable pointing to your R installation directory.


### Python Dependencies

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

All required R packages, including the *occupationCoding* package, will be installed automatically when you run the scripts for the first time.

### Required Data

The occupation coding package bases on the list of occupations provided by the Federal Employment Agency of Germany (Bundesagentur für Arbeit): [Gesamtberufsliste_der_BA.xlsx](https://rest.arbeitsagentur.de/infosysbub/download-portal-rest/ct/dkz-downloads/Gesamtberufsliste_der_BA.xlsx)   
It will be downloaded automatically when you run the scripts for the first time.

You can also run the downloading script by

```bash
python utils/data_util.py
```

or download the file manually.

## Getting Started

You can query an occupation directly from the command line:

```bash
python run.py --occupation "Bürokauffrau"
```

### CLI Help

To see available options and usage information:

```bash
python run.py --help
```

## Advanded Usage

### Querying Multiple Occupations

You can also query several job titles at once:

```python
from occupation_coding import code_occupations

results = code_occupations(
    occupations=["Bürokauffrau", "Stadtjugendpfleger", "Erzieherhelfer im Lehrlingswohnheim.", 
                "Mitarbeit bei einer Filmproduktion", "Abschleifer"]
)
print(results)
```

The script will return results for each occupation sequentially.

### Listing the Coding Index

To inspect the loaded coding index:

```python
from occupation_coding import retrieve_index

index = retrieve_index()
print(index)
```

## Credits

This project wraps [occupationCoding](https://github.com/malsch/occupationCoding) R package by Malte Schierholz and collaborators.
If you use this Python wrapper in your work, please cite the original [publication](https://doi.org/10.1093/jssam/smaa023) (Schierholz et al., 2021):

```bibtex
@article{schierholz2021machine,
  title={Machine Learning for Occupation Coding - A Comparison Study},
  author={Schierholz, Malte and Schonlau, Matthias},
  journal={Journal of Survey Statistics and Methodology},
  volume={9},
  number={5},
  pages={1013--1034},
  year={2021},
  publisher={Oxford University Press}
}
```

## Contributors

* [Alexander Esser](https://github.com/alexander-esser)



