sudo yum update -y
sudo yum install git -y

git clone https://github.com/ukokuja/meod_ml_api.git

cd /home/ec2-user/meod_ml_api
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip

pip install --only-binary :all: pandas

pip install -r requirements.txt

sudo yum install -y amazon-linux-extras
sudo amazon-linux-extras enable python3.8 -y
sudo ln -s /usr/local/bin/python3.8 /usr/local/bin/python3
sudo ln -s /usr/local/bin/pip3.8 /usr/local/bin/pip3

sudo amazon-linux-extras install epel

sudo yum install supervisor

sudo chmod 777 /etc/supervisord.conf
sudo echo '' > /etc/supervisord.conf
sudo cp /home/ec2-user/meod_ml_api/supervisord.conf /etc/supervisord.conf

sudo mkdir /var/log/meod
sudo touch /var/log/meod/meod.err.log
sudo chmod 777 /var/log/meod/meod.err.log
sudo touch /var/log/meod/meod.out.log
sudo chmod 777 /var/log/meod/meod.out.log


sudo mkdir /var/log/celery/
sudo touch /var/log/celery/beat.err.log
sudo chmod 777 /var/log/celery/beat.err.log
sudo touch /var/log/celery/beat.out.log
sudo chmod 777 /var/log/celery/beat.out.log

sudo touch /var/log/celery/worker.out.log
sudo chmod 777 /var/log/celery/worker.out.log
sudo touch /var/log/celery/worker.err.log
sudo chmod 777 /var/log/celery/worker.err.log


sudo yum update -y
sudo amazon-linux-extras install docker

sudo yum install docker
sudo service docker start


sudo docker run -it --rm -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management


#set personal keys
cd /home/ec2-user/
mkdir .aws
cd .aws
touch credentials
touch 777 credentials
vim credentials

supervisord
supervisorctl restart all


tail -f  /var/log/celery/worker.err.log