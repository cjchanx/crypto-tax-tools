# Converters
convert.py is a small, rough script designed to convert simple .csv files from specific platforms to the tax.crypto.com format as specified here [CSV Format](https://help.crypto.com/en/articles/5019792-data-import)
## Usage
`python3 convert.py [-h] [-f FILE] [-o OUTPUT]`

`-h, --help` 	Shows help message and exits
`-f, --file` 	Specify input file name/path default is data.csv
`-o, --output`	Specify output file name/path default is output.csv

### Example
We have a file from either BlockFi or Celcius in the containing directory and renamed as 
`input.csv`
Run the following command
`python3 convert.py`
Output can be found in the containing directory
`output.csv`

## Supported Input File Platforms
- BlockFi
- Celcius

## Disclaimer
Script is meant to be a rough initial conversion to make it easier to do the rest manually, not to be the final step in the calculation.

The code may have errors and manual checking or adjustments are required to ensure accurate conversion. Please refer to the "assumptions" column below to understand specific assumptions and adjustments that may need to be made to suit your situation. All errored rows will be mentioned after the conversion takes place, errored rows require manually adding the transaction type to the if-else interpretation.



## Assumptions
### BlockFi
- "Crypto Transfer" is (received crypto) is configured to be "mining" by default, edit to the most common type and manually check as required
- "Withdrawal" assumed to be a transfer by default
### Celcius
- "Withdrawal" assumed to be transfer by default
- "Transfer" assumed to be transfer by default