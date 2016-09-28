#!/bin/sh
nosetests -vv --with-coverage --cover-package=pypoint/ --cover-inclusive --cover-erase tests
