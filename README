nip is tool written in Python to provide environment isolation and installation
for Node.js. Installation is non-existent at this point. I am mostly scratching
my own itch with nip. Hopefully it is useful to others and others contribute
back.

nip is influenced by pip, virtualenv and rip.

Installation
------------

You can install nip in various ways. There is no official release yet, but
you can clone the source and within the cloned directory run::

    python setup.py install

You might need ``sudo`` to perform the install.

If you are familiar with ``pip`` you can run::

    pip install git+git://github.com/brosner/nip.git#egg=nip

Environment basics
------------------

Environments are created in your NIP_ENV_DIR. By default this is
``~/.nipenvs``. You can override two ways::

    NIP_ENV_DIR=... nip env list

or::

    nip -d ... env list

To create a new environment::

    nip env create myenv

You can delete environments::

    nip env delete myenv

You can list environments in the environment directory::

    nip env list

To run node within an environment currently you can do it two ways::

    NIP_ENV=test nip run code.js

or::

    nip -E test run code.js