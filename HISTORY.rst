=======
History
=======

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


Unreleased
----------


0.0.5 (2020-01-24)
------------------

* changes:
    - version number
    - long_description_conent_type in setup.py
    - travis API token fixed


0.0.4 (2020-01-24)
------------------

* changed:
    - requirements_dev.txt to updated packades
    - requirements.txt
* fixed:
    - upload to pypi with API Token


0.0.3 (2020-01-24)
------------------

* First release on PyPI.

* add class Material2D - base class for all materials used in this package.
* add class IsotropicMaterial - Material2D class for isotropic materials.
* add class AnisotropicMaterial - Material2D class for anisotropic materials.
* add class FiberReinforcedMaterialUD - Material2D class that combines two materials.
* add class Ply - generates defined ply/layer of Material2D.
* add class Laminate - combines mulitple Ply instances to composite laminate.
* dev setup:
    * add .pre-commit-config.yaml - formating with black
    * changed travis - add ``black --check`` on 'before_script' method
    * changed requirements_dev.txt
    * add requirements.txt
    * add tests for classes
    * fix tox python 3.8 and flake8 checking
    * add flake8 ignore: E501, W503, F841
* update mail adress
* docs:
    * changed usage.rst - new Version update to use package

0.0.2 (2020-01-22)
------------------
* setup of package
* first ideas of structure
