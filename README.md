# compile-tests
Compile python tests by Cython

## How it works

- Pick up all 'test_' functions from source
- Make a new 'tests' package and place that functions inside
- Set import to the package in the source
- Compile the package by Cython
- Cleanup

After, you can run new source as regular python file.


## Requirements
* Python 3.5+
* astor
* Cython

## 0. Installation
`pip install -r requirements.txt`

## 1. Compile
`python run.py`

## 2. Run
`python dist/example.py`
