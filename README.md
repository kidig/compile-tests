# compile-tests
Compile python tests by Cython

## How it works

- Extract code block between 'HIDDEN BLOCK' tags from source
- Make a new 'tests' package and place that code block inside
- Set import from the package to the source
- Compile the package by Cython
- Cleanup

After that, you can run new source as regular python file.


## Requirements
* Python 3.5+
* Cython

## 0. Installation
`pip install -r requirements.txt`

## 1. Compile
`python run.py`

## 2. Run
`python dist/example.py`
