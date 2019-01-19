from hashlib import md5

def format_volume_name(template, spawner):

    username = spawner.escaped_name;
   
    # Compute shard number: 
    # Grab first 4 bytes from MD5 digest of the username, parse as a hex integer
    NUMBER_OF_SHARDS = 5
    shard_number = int(md5(username.encode('ascii')).hexdigest()[0:8], 16)
    shard_number = shard_number % NUMBER_OF_SHARDS

    # Format 
    return template.format(username=username, shard_number=str(shard_number)) 
