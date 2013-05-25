Ecommerce
=========
This repository is for the e-commerce course assignment described at http://www.cs.ubbcluj.ro/~deiush/ce/cerinte_ce.htm

### Install Guide ###
* Install [Python 2.7](http://www.python.org/download/releases/2.7/).
* Install [Git](http://git-scm.com/downloads).
* Install pip, a tool for installing and managing Python packages.`easy_install pip`
* Install virtualenv. `pip install virtualenv`
* Go to the folder where the application and application environment will reside.
* Create new virtual environment. `virtualenv ecommerce_env`
* Activate virtual environment. `source ecommerce_env/Scripts/activate`
* Install Django. `pip install Django==1.4.5`
* Clone project. `git clone https://github.com/adriana-saroz/ecommerce.git`
* Install additional project requirements. `pip install -r ecommerce/requirements.txt`

### Setting Up The Project ###
* Create database and load initial data. `python manage.py syncdb` When prompted, create admin user account.
* Start server. `python manage.py runserver`
* Access application at http://127.0.0.1:8000/

### Used Technologies ###
* Python
* Django
* Sqlite (can be easily switched to MySql)
* [Bootstrap](http://twitter.github.io/bootstrap/)

### Features ###
User features:
* Homepage featuring a gallery of random product images.
* Paginated product lists.
* Dynamic categories with the ability to add sub-categories.
* Product details.
* Cart functionality (using user session).
* Check-out page with credit card validation.
* Order history for logged in users.
* Search funtionality.
* Top items.
* Dynamic advertisement.
* User accounts functionality.
Admin features:
* Add/edit/delete functionality for users, categories, products, orders and advertisements.

### Screenshots ###
![Homepage](/docs/screenshots/1_homepage.png)
![Product List](/docs/screenshots/2_product_list.png)
![Pagination + Top Items + Ads](/docs/screenshots/3_pagination_topitems_ads.png)
![Product Details](/docs/screenshots/4_product_details.png)
![Product Image](/docs/screenshots/5_product_image.png)
![Shopping Cart](/docs/screenshots/6_shopping_cart.png)
![Checkout](/docs/screenshots/7_checkout.png)
![Orders List](/docs/screenshots/8_orders.png)