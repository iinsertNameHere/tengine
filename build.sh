python -m venv venv
source venv/bin/activate
pip install build
pip install twine
python -m build
python3 -m twine upload --repository pypi dist/*
deactivate
rm -rf venv
rm -rf dist