# Installation

Clone the repo and go in the folder.

    git clone https://github.com/Zepmanbc/oc_dapython_pr5.git
    cd oc_python_pr5

Create a virtual environment and activate.

    virtualenv env -p python3
    . env/bin/activate

Install libraries.

    pip install -r requirements.txt

Set executable.

    chmod +x pur_beurre.py

# Configure LAMP server with docker

If you already have apache2 and mysql running, please stop the services.

    sudo service apache2 stop
    sudo service mysql stop

Install docker if you don't already got it. (For Debian family, for other OS search on Google)

    sudo apt-get update && sudo apt-get install docker.io

Download and run the LAMP docker.

    docker pull lioshi/lamp:php5
    docker run -d --name=LAMP -v ~/www:/var/www/html -v ~/mysql:/var/lib/mysql -p 80:80 -p 3306:3306 --restart=always lioshi/lamp:php5

set all the rights to root

    docker exec -i -t LAMP /bin/bash 

    >mysql -p

password is "root"

    mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root';
    mysql> exit
    exit

Now you got a full running LAMP server running in docker.

# Configure Database

Modify `config.py` file (this configuration is default for the LAMP docker version described before)

    "QUANTITY_PRODUCTS" : 200,
    "HOST" : "localhost",
    "USER" : "root",
    "PASSWD" :"root",
    "DATABASE" : "offdb",
    "SQL_FILE" : "app/static/dboff.sql",
    "STRUCTURE" : "app/static/categories.json"

QUANTITY_PRODUCTS define the max downloaded products (step is 200), if it is set to 0, there is no limitation.

# Run the software

(I suppose your virtualenv is activated and LAMP is running)

    ./pur_beurre.py

The first time you run it, the database (MySQL) will be created and be filled.

You can force to delete DATABASE and download again the data:
    
    ./createdb.py

## Search a substitute

You will have to select what you want to do

    1 . Select a category
    2 . Show saved products

Press `1` and validate with `Enter`.

Select your category and validate.

Select a product with the number, if you want to go back use `0`. Use `N` and `P` to navigate throw pages.

Select a substitute with the number, if you want to go back use `0`. Use `N` and `P` to navigate throw pages.

if you want to save the combinaison, use `1`.

## Show favorites

On the main screen select `2`.

    1 . Select a category
    2 . Show saved products

Select your saved product to see details.

if you want to remove the combinaison, use `1`.