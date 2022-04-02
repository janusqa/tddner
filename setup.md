# Create a package in current directory at "/dist"
```
 python3 setup.py sdist
```
# Publish package // Requires an account on [PyPi](https://pypi.org)
```
$ pip install twine 
$ twine upload dist/* 
```
# Use your package in developer mode 
Use this during development. When changes are made no need to re-install
```
$ pip install . -e
```

# Use a package 
Use this during production.
```
$ pip install . 
```
