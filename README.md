# online-store-backend   

## Run 
``` bash
# Clone and navigate to the online-store-backend
git clone git@github.com:mhrashvand1/online-store-backend.git  
cd online-store-backend  
# Run docker compose
docker-compose -f docker-compose.dev.yml up  
# Note that you shouldn't run docker-compose with the '-d' flag   
# because SMSs will print in the terminal   
# and you need to monitor them for sign up, sign in, and other related activities.   
```   
The project will be accessed on `localhost` at port `8000`.   

To create a superuser:   
 
``` bash   
docker-compose -f docker-compose.dev.yml exec app python manage.py createsuperuser2 <phone_number> # --password=<password>  
# You can set a password for using django admin panel otherwise a random password will be generate.
```   

swagger:   
- `http://127.0.0.1:8000/swagger/`  
- `http://127.0.0.1:8000/redoc/`  
