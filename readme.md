# Greek Synonymous Parser

This python script aims to create a dictionary of Greek synonymous word based on retroningeenering. It is not perfect, but it has the merit to exist.

## Method
### 1. Creation of a list of english words
We created a list of english words by selecting the key word of the JSON file of [S. C. Woodhouse, English-Greek Dictionary (1910)](https://archive.org/details/Woodhouse_201805), accessible online on [Perseids Project](https://perseids-project.github.io/woodhouse-js/), the JSON file is accessible on this [Github repository](https://github.com/perseids-project/woodhouse-js)

### 2. Creating the semantic constellation (more than synonyms)
We search each word on the English-to-Greek Word Search of the [Perseus Project](http://www.perseus.tufts.edu/hopper/definitionlookup?redirect=true&lang=greek). On the basis of the result we selected each greek work which has the english word in its Short Definition. As the encodage of this dictionary is aproximative (for example the Greek word πατήρ has "pitṛ[snull ]u" as Short Definition), we also selected all results attested between 2000 and 100000 occurences. These values can be changed through the respective constants `occur_min` and `occur_max`.  


## Install requirements
`pip install -r requirements.txt`

## Launch the script
`python3 main.py`



activate virtual environment
`source venv/bin/activate`
