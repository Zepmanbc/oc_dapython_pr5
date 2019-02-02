"""
pip install pytest pytest-cov coverage
touch .coveragerc
echo "[run]" >> .coveragerc
echo "omit = env/*" >> .coveragerc

## run pytest with coverage ##
pytest --cov=./ --cov-report html

## pytest with arguments ##
py.test -vv --capture=no --showlocals --exitfirst

"""
