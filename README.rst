=============================
Signbank-Feedback
=============================

.. image:: https://badge.fury.io/py/signbank-feedback.png
    :target: https://badge.fury.io/py/signbank-feedback

.. image:: https://travis-ci.org/stevecassidy/signbank-feedback.png?branch=master
    :target: https://travis-ci.org/stevecassidy/signbank-feedback

.. image:: https://codecov.io/gh/stevecassidy/signbank-feedback/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/stevecassidy/signbank-feedback

The feedback component of Signbank

Documentation
-------------

The full documentation is at https://signbank-feedback.readthedocs.org.

Quickstart
----------

Install Signbank-Feedback::

    pip install signbank-feedback

Then use it in a project::

    import feedback


You must define the following variables in ``settings.py``:

* ``LANGUAGE_NAME = "Auslan"``
* ``COUNTRY_NAME = "Australia"``
* ``SITE_TITLE = "Signbank"``

That's for the Auslan site. For BSL, or another sign language,
you would use different values for those three variables.

You must also add ``bootstrap3`` and ``feedback`` to your ``INSTALLED_APPS`` variable.

Features
--------

* TODO

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
