Run in docker:
```
docker-compose up --build
```
check IP of docker:
```
docker-machine ip default
```

my IP:
192.168.99.100 - this is localhost

Paste the below url in browser
```
http://192.168.99.100:8000/
```
Connect to MySQL database using the properties from ```docker-compose.yml``` file with host as ```localhost```.
```
The DB port to be used is ```33000``` 
```
Stop all containers
```
docker container stop
```
Remove all containers
```
docker-compose down
```
