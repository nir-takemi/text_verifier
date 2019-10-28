# Installation

1. clone this repository.

2. install other package.

```
pip install pyyaml
pip install pytest
```

# Usage

```
python3 verify_text.py "directory or file to verify"

# ex)python3 verify_text.py ~/Sample/www/
```

## Option
You can change target files'suffix, or etc... 
Definition file is textverifier/config.yaml . 

# Developer
## Define pattern
You can define patterns with regular expressions in textverifier/pattern.yaml .

## Test

```
pytest
```
