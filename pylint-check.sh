#!/bin/bash

pipenv run pylint --load-plugins pylint_django chat/ dictionary/ immortalfighters/ base/ utils/
