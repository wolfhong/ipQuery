mkdir -p samples

# wget http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip -O samples/GeoIPCountryCSV.zip
wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity_CSV/GeoLiteCity-latest.zip -O samples/GeoLiteCity-latest.zip

cd samples/
# unzip GeoIPCountryCSV.zip
unzip GeoLiteCity-latest.zip
mv GeoLiteCity_*/GeoLiteCity-Blocks.csv ./
mv GeoLiteCity_*/GeoLiteCity-Location.csv ./

cd ../

python manage.py syncdb
python write_into_db.py
