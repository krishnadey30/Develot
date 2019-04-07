# Develot

## Requirements

* [Python](https://www.python.org/)   (3.5.2 tested)
* [Falcon](https://falconframework.org/)
* [RabbitMQ](https://www.rabbitmq.com/)
* [Mysql](https://www.mysql.com/)
## Getting Started

To clone and run this application, you'll need Git,Python,RabbitMQ, Mysql installed on your computer.

### Installing MYSQL
``` bash
$ sudo apt-get install mysql-server
```
Note: set the password of the mysql as **root**

### Installing RabbitMQ 
``` bash
$ sudo apt-get install rabbitmq-server
```

#### Creating a new None Administrative User
``` bash
$ sudo rabbitmqctl add_user develot develot
```

This command instructs the RabbitMQ broker to create a (non-administrative) user named `develot` with (initial) password `develot`.
#### Creating a new virtual host
``` bash
$ sudo rabbitmqctl add_vhost develot_host
```
This command instructs the RabbitMQ broker to create a new virtual host called “sample_host”.
#### Making new user administrator
``` bash
$ sudo rabbitmqctl set_user_tags develot administrator
```

This command instructs the RabbitMQ broker to ensure the user named “krishna” is an administrator.

#### Seting user permissions
``` bash
$ sudo rabbitmqctl set_permissions -p develot_host develot ".*" ".*" ".*"
```

This command instructs the RabbitMQ broker to grant the user named `develot` access to the virtual host called `develot_host`, with configure ,write and read permissions on all resources.

### Install **pip** 
``` bash
sudo apt-get install python3-pip
```
### Then install **virtualenv** using pip3
``` bash
sudo pip3 install virtualenv 
```
### Create a virtual environment
```
$ virtualenv -p python3 .env
```
### Activate the virtualenv
```
$ source .env/bin/activate
```
### Clone this repository
```
$ git clone https://github.com/krishnadey30/Develot.git
$ cd Develot
```

### Install the requirements
```
$ pip install -r requirements.txt
```

### Create a Database
Open mysql and create a database-develot
``` mysql
mysql> CREATE DATABASE develot CHARACTER SET UTF8;
mysql> USE develot;
```
### Create Tables
#### Docs
```mysql
mysql> CREATE TABLE Docs(Did INT NOT NULL PRIMARY KEY AUTO_INCREMENT,Documentation_Url VARCHAR(1200),para TEXT NOT NULL); 
```

| Field             | Type          | Null | Key | Default | Extra          |
|-------------------|---------------|------|-----|---------|----------------|
| Did               | int(11)       | NO   | PRI | NULL    | auto_increment |
| Documentation_Url | varchar(1200) | YES  |     | NULL    |                |
| para              | text          | NO   |     | NULL    |                |


#### Sentences
```mysql
mysql> CREATE TABLE Sentences(Sid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,sentence TEXT NOT NULL,Date_of_Creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, Did INT NULL, FOREIGN KEY(Did) REFERENCES Docs(Did));
```

| Field            | Type      | Null | Key | Default           | Extra                       |
|------------------|-----------|------|-----|-------------------|-----------------------------|
| Sid              | int(11)   | NO   | PRI | NULL              | auto_increment              |
| sentence         | text      | NO   |     | NULL              |                             |
| Date_of_Creation | timestamp | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
| Did              | int(11)   | YES  | MUL | NULL              |                             |


#### Vector_data
```mysql
mysql> CREATE TABLE Vector_data(data_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,value DOUBLE(14,13) NOT NULL,Sid INT NOT NULL,FOREIGN KEY(Sid) REFERENCES Sentences(Sid));
```

| Field   | Type          | Null | Key | Default | Extra          |
|---------|---------------|------|-----|---------|----------------|
| data_id | int(11)       | NO   | PRI | NULL    | auto_increment |
| value   | double(14,13) | NO   |     | NULL    |                |
| Sid     | int(11)       | NO   | MUL | NULL    |                |


### Installing the Consine Similarity module
```bash
$ cd Develot/Api
$ pip install .
```

### Running the celery workers
```bash
$ celery -A tasks worker -loglevel=INFO --concurrency=10
```

### Running Falcon Server
* Open a new terminal session
* Activate the virtual enviroment
*  `cd Develot/Api`
``` bash
$ gunicorn -b localhost:5000 app --reload
```


## Using the API
Currently the API is hosted for evaluation purpose on
http://35.167.192.186

### API Endpoints
#### SEARCH
*http://35.167.192.186/search*

* HTTP Request: **PUT**

* Parameters:
  * key: "sentence"
  * value: "Any Sentence you want to search"
#### Add Document
*http://35.167.192.186/add_doc*

* HTTP Request: **POST**

* BODY:
  ```json
  {
    "doc":{
            "url": "url_of_the_document",
            "para": "the paragraph"
          }
  }
  ```
