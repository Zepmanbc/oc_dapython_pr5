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

    chmod +x purebeurre.py

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

# Run the software

(I suppose your virtualenv is activated and LAMP is running)

    ./purebeurre.py

The first time you run it, the database (MySQL) will be created and be filled.

## Search a product

You will have to select what you want to do

    1 . Select a category
    2 . Show saved products

Press `1` and validate with `Enter`.

Select your category and validate.

Select your product type and validate.

Select a product with the number, if you want to go back use `0`.

if you want to save a product to your favorites, use `1`.

# Show favorites

On the main screen select `2`.

    1 . Select a category
    2 . Show saved products

Select your saved product to see details.