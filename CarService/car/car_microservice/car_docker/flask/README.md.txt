$docker build -t order-system .

$docker run -it -d -p 5000:5000 order-system

$docker ps -a

check IP of docker:
$docker-machine ip default
my working IP is http://192.168.99.100:5000/registered_cars

exit docker:
$docker stop <ID>





