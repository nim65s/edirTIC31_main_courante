Déploiement de la main courante
===============================

Ce petit guide indique comment déployer le projet Django ``edirtic`` sur une Raspberry-Pi.

Installation de Raspbian
------------------------

* Télécharger Raspbian sur https://www.raspberrypi.org/downloads/raspbian/
* Dézipper le fichier :

.. code::

    # unzip 2015-09-24-raspbian-jessie.zip

* Copier l’image sur la carte SD (ici, celle-ci s’appelle ``mmcblk0``) :

.. code::

    # dd bs=4M if=2015-09-24-raspbian-jessie.img of=/dev/mmcblk0

* S’assurer que toutes les données ont bien été écrite :

.. code::

    # sync

* Retirer la carte SD puis la remettre pour provoquer une relecture des partitions par le noyau.

* Monter la deuxième partition :
  
.. code::

    # sudo mount /dev/mmcblk0p2 /mnt

* Rajouter une clef ssh pour se connecter en tant que root :

.. code::

    $ mkdir /mnt/root/.ssh
    $ cp /home/<user>/.ssh/id_rsa.pub /mnt/root/.ssh/authorized_keys


Configuration de Raspbian
-------------------------

* Se connecter à la raspberry pi en tant que root grâce à la clef ssh.

* Installer quelques paquets :
  
.. code::

    $ apt-get install htop tmux vim python3-virtualenv \
                      uwsgi uwsgi-plugin-python3 apache2

* Créer un compte système ``edirtic`` :
  
.. code::

    $ useradd -r edirtic -d /srv/www/edirtic

* Créer un home pour cette utilisateur :

.. code::
  
    $ mkdir -p /srv/www/edirtic
    $ chown edirtic:edirtic /srv/www/edirtic

* Rajouter ``www-data`` au groupe ``edirtic`` :
  
.. code::

    $ usermod -aG edirtic www-data

..

 Ceci permettera à *apache* de lire les fichiers statiques appartenant à *edirtic*.

* Créer le fichier ``~edirtic/.bashrc`` :

.. code::

    $ su edirtic
    # cat > ~/.bashrc << EOF

    #
    # ~/.bashrc
    #

    # If not running interactively, don't do anything
    [[ $- != *i* ]] && return

    export EDITOR="vim"

    alias ls='ls --color=auto'
    alias ll='ls --color=auto -hl'
    alias l='ls --color=auto -al'

    alias rm='rm -i'
    alias cp='cp -i'
    alias mv='mv -i'

    PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

    umask 0027

    export DJANGO_SETTINGS_MODULE=edirtic.local_settings

    . ~/env/bin/activate

    EOF

* Cloner le dépôt git dans le dossier ``edirtic`` :

.. code::

    # git clone https://github.com/edirTIC31/edirTIC31_main_courante edirtic

* Éventuellement, se déplacer sur la branche voulue, par exemple sur la branche ``prod`` :

.. code::

    # cd ~/edirtic/
    # git checkout prod

Virtualenv
``````````

* Créer un *virtualenv* :

.. code::

    # python3 -m virtualenv -p /usr/bin/python3 ~/env

* Charger le *virtualenv* :

.. code::

    # source ~/env/bin/activate

..

 Il est également possible de se déconnecter puis de se réconnecter.
 Le *virtualenv* sera alors automatiquement activé grâce au ``.bashrc``.

* Installer les paquets python nécessaire :

.. code::

    # pip3 install -r ~/edirtic/edirtic/requirements.dev.txt

Django
``````

* Créer le dossier qui va contenir les paramètres secrets :

.. code::

    $ mkdir /etc/django/edirtic/
    $ chown edirtic:edirtic /etc/django/edirtic
    # chmod 755 /etc/django
    # chmod 750 /etc/django/edirtic

* Créer une secret key :

.. code::

    # openssl rand -hex 16 > /etc/django/edirtic/SECRET_KEY

* Créer la base de données et sa structure :

.. code::

    # cd ~/edirtic/edirtic/
    # ./manage.py migrate

* Créer un super utilisateur :

.. code::

    # ./manage.py createsuperuser

* Collecter les fichiers statiques :

.. code::

    # ./manage.py collectstatic

..

  Ceux-ci sont placer dans le dossier ``~/static``.

uwsgi
`````

* Créer un dossier pour les logs Django et apache :

.. code::

    # mkdir ~/log

* Copier la configuration *uwsgi* puis l’activer :

.. code::

    $ cd /etc/uwsgi/apps-available
    $ cp /srv/www/edirtic/edirtic/conf/uwsgi.ini edirtic.ini

    $ cd /etc/uwsgi/apps-enabled
    $ ln -s ../apps-available/edirtic.ini

* Redémarrer *uwsgi* :

.. code::

    $ service uwsgi start

* Vérifier les logs *uwsgi* :

.. code::

    $ tail /var/log/uwsgi/app/edirtic.log

* Vérifier que *uwsgi* est bien lancé :

.. code::

    $ ps aux | grep uwsgi

* Vérifier que çamarche™ :

.. code::

    $ nc -v 127.0.0.1 8010
    Connection to 127.0.0.1 8010 port [tcp/*] succeeded!
    ^C

* Les logs Django se trouve dans le fichier ``~/log/debug.log``.

Apache
``````

* Copier la configuration *apache* :

.. code::

    $ cd /etc/apache2/site-available
    $ cp /var/www/edirtic/edirtic/conf/apache.conf edirtic.conf

    $ cd /etc/apache2/site-enabled
    $ rm 000-default.conf
    $ ln -s ../site-available/edirtic.conf 000-edirtic.conf

* Activer les modules apache ``proxy`` et ``proxy_http`` :

.. code::

    $ a2enmod proxy
    $ a2enmod proxy_http

* Créer le dossier ``/var/empty`` pour éviter un warning :

.. code::

    $ mkdir /var/empty