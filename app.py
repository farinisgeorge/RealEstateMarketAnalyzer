from api.main import main_func
from api.tools.postgresManager import PostgresManager
import json
from flask import Flask, request
import logging

app = Flask(__name__)
# Create `parent` logger
logger = logging.getLogger()

# Set parent's level to INFO and assign a new handler
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@app.route('/scrape_location', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    zipcodes = record.get("zipcodes")
    usage_type = record.get("usage_type")
    
    try:
        df = main_func(zipcodes, usage_type)
        json_str = df.to_json(orient = "record")
        return json_str, 201
    
    except Exception as e:
        logger.exception(e)
        return 400


@app.route('/records', methods=['POST'])
def query_records():
    postgres = PostgresManager()
    record = json.loads(request.data)
    property_id = record.get('property_id')
    usage_type = record.get('usage_type')
    space_min = record.get('space_min')
    space_max = record.get('space_max')
    rooms = record.get('rooms')
    europersqm_min = record.get('europersqm_min')
    europersqm_max = record.get('europersqm_max')
    price_min = record.get('price_min')
    price_max = record.get('price_max')
    
    try:
        ans = postgres.run_query_to_postgres(property_id, usage_type, space_min, space_max, rooms,\
                                             europersqm_min, europersqm_max, price_min, price_max)
        return ans, 201
    except Exception as e:
        logger.exception(e)
        return 400
    
