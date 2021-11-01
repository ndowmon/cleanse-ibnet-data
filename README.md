# Cleanse IBNET Data

This project takes an exported `.xlsx` file containing IBNET export data and transforms it into a 2d `.csv` table.

It does this in two steps:

1. For each sheet in the export, parse and merge the IBNET variables into a single table, and write a new `.csv` file to `./data/output/individual/sheet_<SHEET_NAME>.csv`
2. Separately, read each file in `./data/output/individual/*.csv` and merge the data into a single export, `./data/output/merged-ibnet-data.csv`

## Getting Started

1. Make sure you have python3 installed. You can check for python3 by running the following command in your terminal:
    
    ```
    python3 --version
    ```

    If `python3` is not installed, you can install it from <https://www.python.org/downloads/>



2. Install dependencies using pip3

    ```
    pip3 install -r requirements.txt
    ```

3. Set up your `data` directory to include the IBNET export file you'd like to transform

## Running the transformations

Using python3, you can execute step [1] above, producing many `.csv` files in `./data/output/individual/*.csv`:

```
python3 src/index.py
```

Once the transformations have completed, you can execute step [2] above, synthesizing the data into `./data/output/merged-ibnet-data.csv`:

```
python3 src/merge_csv_datasets.py
```