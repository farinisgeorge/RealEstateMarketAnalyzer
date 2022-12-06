from pydantic import BaseModel, validator


class DataValidator(BaseModel):
    """
    Pydantic model to validate the schema of the extracted files.
    """
    property_id: str
    zipcodes: str
    usage_type: str
    price: str
    space: str
    rooms: str
    url: str
    description: str
    price_form: float
    space_form: float
    rooms_form: float
    

    @validator('price')
    def not_null_price(cls,price):
        if price == '':
            raise ValueError("price can't be null")
        return price
    
    @validator('space')
    def not_null_space(cls,space):
        if space == '':
            raise ValueError("space can't be null")
        return space
    
    @validator('rooms')
    def not_null_rooms(cls,rooms):
        if rooms == '':
            raise ValueError("rooms can't be null")
        return rooms
    
    @validator('url')
    def not_null_url(cls,url):
        if url == '':
            raise ValueError("url can't be null")
        return url
    
    @validator('price_form')
    def not_null_price_form(cls,price_form):
        if price_form <0:
            raise ValueError("price_form can't be negative")
        return price_form
    
    @validator('space_form')
    def not_null_space_form(cls,space_form):
        if space_form <= 0:
            raise ValueError("space_form can't be negative")
        return space_form
    
    @validator('rooms_form')
    def not_null_rooms_form(cls,rooms_form):
        if rooms_form <= 0:
            raise ValueError("rooms_form can't be negative")
        return rooms_form