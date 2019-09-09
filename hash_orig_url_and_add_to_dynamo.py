import sys
sys.getsizeof("abcdef")

import boto3
import hashlib
import time
import base64


def get_short_url(original_url):
    '''
    given the original url this function returns a 6 character long string 
    which will be used to shorten the url
    '''
    #add the current unix epoch time to original url to make it unique
    modified_url = original_url + str(int(time.time()))    
    #apply MD5 hashing to the modified url
    #this creates a 128 bit value which maps to 22 characters
    hashed = hashlib.md5(modified_url.encode())
    #take the first 6 characters of the hash which will be the shortened url
    hashed = base64.urlsafe_b64encode(hashed.digest())[:6].decode("utf-8") 
    
    return hashed


def check_short_url_in_DB(six_char_url):
    '''
    given a short url returns true if the short url already used
    '''
    dynamodb = boto3.resource("dynamodb", region_name = "us-east-1")
    table = dynamodb.Table('url')
    response = {}
    response = table.get_item(
            Key={
                'hash': six_char_url,
            }
        )
    #if key exists in the dynamoDB it returns a dictionary with two elements
    #one is the item itself and the other is metadata
    if(len(response) == 2):
        return True
    #if the item doesn't exist in the database it only returns metadata
    else:
        return False
    
def insert_short_url_into_DB(original_url, short_url, expiration_period_days=90):
    '''
    given original_url, six character short_url function inserts the entry into DynamoDB
    by default urls expire in 90 days
    '''
    expiration_seconds_delta = expiration_period_days * 86400 #1day = 86400 seconds
    table.put_item(
       Item={
            'hash':short_url,
            'original_url': original_url,
            'creation_date': int(time.time()),
            'expiration_date': int(time.time()) + expiration_seconds_delta,
        }
    )



def get_long_url(short_url):
    '''
    given the six character short_url function returns the original url
    will be used for redirecting clients to the actual page they are trying to connect
    return None if there is no corresponding entry in the database
    '''
    response = {}
    response = table.get_item(
        Key={
            'hash': short_url,
        }
    )

    #if key exists in the dynamoDB it returns a dictionary with two elements
    #one is the item itself and the other is metadata
    if(len(response) == 2):
        return response["Item"]["original_url"]
    #if the item doesn't exist in the database it only returns metadata
    else:
        return None


dynamodb = boto3.resource("dynamodb", region_name = "us-east-1")
table = dynamodb.Table('url')

original_url = "www.google.com"

#get the short url 
six_char_url = get_short_url(original_url)
#make sure that the short url is unique and hasn't been used before
while(check_short_url_in_DB(six_char_url) == True):
    six_char_url = get_short_url(original_url)
    
    
    

        

    
    
    

        
    
    

table.put_item(
   Item={
        'hash':hashed,
        'original_url': original_url,
        'creation_date': int(time.time()),
        'expiration_date': int(time.time()) + expiration_seconds_delta,
    }
)

response = table.get_item(
    Key={
        'hash': 'f7DdzJ',
    }
)
item = response['Item']
print(item)



