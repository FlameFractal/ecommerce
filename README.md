Ecommerce
=========
This repository is for the e-commerce course assignment described at http://www.cs.ubbcluj.ro/~deiush/ce/cerinte_ce.htm

### Install Guide:

+   Install [Python 2.7](http://www.python.org/download/releases/2.7/).
+   Install [Git](http://git-scm.com/downloads).
+   Install pip, a tool for installing and managing Python packages.
```
easy_install pip
```
+   Install virtualenv.
```
pip install virtualenv
```
+   Create new virtual environment.
```
cd ecommerce
virtualenv ecommerce_env
```
+   Activate virtual environment.
```
source ecommerce_env/Scripts/activate
```
+   Install Django.
```
pip install Django==1.4.5
```
+   Clone project.
```
git clone https://github.com/adriana-saroz/ecommerce.git
```
+   Install additional project requirements.
```
cd ecommerce
pip install -r requirements.txt
```

### Setting Up The Project:

+   Create database and load initial data. When prompted, create admin user account.
```
cd ecommerce
python manage.py syncdb
```
+   Start server.
```
python manage.py runserver
```
+   Access application at http://127.0.0.1:8000/
