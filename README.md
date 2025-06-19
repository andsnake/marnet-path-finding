To speed up booting, its better to first run preprocess_network.py
This will load the geojson network and process it into a .pkl graph file that is then loaded on web service start up. 
This speeds up the start up time of the web service.

You can make changes to the geojson netwrok file using mapshaper https://mapshaper.org/, then export the geojson file and convert to pkl.
then just reload the webservice docker


to use the api just call 'http://0.0.0.0:8000/route?start_lat=6.303333&start_lon=139.121674&end_lat=32.0166667&end_lon=120.8500000

The response will be a json object with the coordinates of the route.