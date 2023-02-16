# online-store-backend   

## Run 
``` bash
# clone and navigate to the online-store-backend
git clone git@github.com:mhrashvand1/online-store-backend.git  
cd online-store-backend  
# run docker compose
docker-compose -f docker-compose.dev.yml up   
```   

For create superuser:   
 
``` bash   
docker-compose -f docker-compose.dev.yml exec app python manage.py createsuperuser2 <phone_number> # --password=<password>  
# You can set a password for using django admin panel otherwise a random password will be generate.
```