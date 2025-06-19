To speed up booting, its better to first run preprocess_network.py
This will load the geojson network and process it into a .pkl graph file that is then loaded on web service start up. 
This speeds up the start up time of the we service.

You can make changes to the geojson netwrok file using mapshaper https://mapshaper.org/, then export the geojson file and convert to pkl.
the just reload the webservice docker
