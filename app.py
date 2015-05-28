import requests
import random
import json
import os
import base64
import boto
from boto.s3.key import Key
from textstat.textstat import textstat

from flask import Flask, request, render_template

from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
@app.route('/', methods=['GET', 'POST'])
def index():

    # If user has submitted the form...
    if request.method == 'POST':

        # Connect to Amazon S3
        s3 = boto.connect_s3()

        # Get a handle to the S3 bucket
        bucket_name = 'poeticam'
        bucket = s3.get_bucket(bucket_name)
        k = Key(bucket)

        # Loop over the list of files from the HTML input control
        data_files = request.files.getlist('file[]')
        for data_file in data_files:

            # Read the contents of the file
            file_contents = data_file.read()

            # Use Boto to upload the file to the S3 bucket
            k.key = data_file.filename
            print "Uploading some data to " + bucket_name + " with key: " + k.key
            k.set_contents_from_string(file_contents)
        return generatehaiku("https://s3-us-west-2.amazonaws.com/poeticam/" + k.key)

    return render_template('index.html')

def generatehaiku(url):
    authheader = "Basic " + base64.b64encode(os.environ['IMAGGA_API_KEY'] + ":" + os.environ['IMAGGA_API_SECRET'])
    headers = {'accept': "application/json", 'authorization':authheader}
    imaggaurl = "http://api.imagga.com/v1/tagging?url={}".format(url)
    r = requests.get(imaggaurl, headers=headers)
    imgtags = r.json()['results'][0]['tags']
    tags = []
    for tag in imgtags:
        tags.append([tag['tag'], int(textstat.syllable_count(tag['tag']))])
    tagsbysyllable = {}
    for tag in tags:
        key = tag[1]
        value = tag[0]
        if key not in tagsbysyllable:
            tagsbysyllable[key] = list()
        tagsbysyllable[key].append(value)
    random.seed(url)
    haikuline1=nsyllables(5,tagsbysyllable) 
    haikuline2=nsyllables(7, haikuline1[1])
    haikuline3=nsyllables(5, haikuline2[1])
    return render_template('haiku.html',
                           url=url, 
                           haikuline1=haikuline1[0],
                           haikuline2=haikuline2[0],
                           haikuline3=haikuline3[0])

def nsyllables(numsyls, tags):
    """ Finds an n-syllable phrase in a dict
        with keys for number of syllables, with values of
        lists of applicable words,  eg:

         {'5': ['polysyllabic', 'proletariat'],
          '4': ['polyganol', 'pollywantsa'],
          '3': ['Pauly Shore', 'polishing'],
          '2': ['poly', 'goner']
          '1': ['Paul', 'pole', 'Pawn'] }
    """
    if numsyls <= 0:
        return [randomonesyl(), tags]
    if numsyls in tags and len(tags[numsyls]) >= 1:
            return [tags[numsyls].pop(0), tags]
    part = nsyllables(numsyls - 1, tags)[0]
    remainder = nsyllables(numsyls - int(textstat.syllable_count(part)) - 1, tags)[0]
    return [str(part) + " " + str(remainder), tags]
    

def randomonesyl():
    words = ['bid', 'big', 'bill', 'bit', 'brick', 'bridge', 'bring', 'chill',
             'chin', 'cliff', 'cling', 'did', 'dig', 'dim', 'dip', 'dish', 
             'ditch', 'drift', 'drill', 'drink', 'fifth', 'fill', 'film',
             'fish', 'fist', 'fit', 'fix', 'gift', 'glimpse', 'grim', 'grin',
             'hid', 'hill', 'him', 'hint', 'his', 'hit', 'if', 'ill', 'in',
             'inch', 'ink', 'inn', 'is', 'it', 'kick', 'kill', 'king', 'kiss',
             'knit', 'lick', 'lift', 'limb', 'link', 'lip', 'list', 'midst', 
             'milk', 'mill', 'miss', 'mist', 'pick', 'pig', 'pin', 'pinch', 
             'pink', 'pit', 'pitch', 'prince', 'print', 'quick', 'quit', 'rib',
             'rich', 'rid', 'ridge', 'ring', 'risk', 'shift', 'ship', 'sick',
             'silk', 'sin', 'since', 'sing', 'sink', 'sit', 'six', 'sixth', 
             'skill', 'skin', 'slip', 'spin', 'split', 'stick', 'stiff',
             'still', 'sting', 'swift', 'swim', 'swing', 'thick', 'thin', 
             'thing', 'think', 'this', 'thrill', 'till', 'tin', 'tip', 'trick',
             'trim', 'trip', 'twig', 'twin', 'twist', 'which', 'whip', 'width',
             'will', 'wilt', 'win', 'wind', 'wing', 'wink', 'wish', 'wit',
             'witch', 'with', 'build', 'built', 'give', 'live', 'bee', 'beef',
             'breed', 'breeze', 'cheek', 'cheese', 'creek', 'creep', 'deed',
             'deep', 'fee', 'feed', 'feel', 'feet', 'fleet', 'free', 'freeze',
             'geese', 'Greece', 'Greek', 'green', 'greet', 'heed', 'heel', 
             'keep', 'keen', 'knee', 'kneel', 'meet', 'need', 'peep', 'queen', 
             'reed', 'reel', 'screen', 'see', 'seed', 'seek', 'seem', 'seen', 
             'sheep', 'sheet', 'sleep', 'sleeve', 'speech', 'steel', 'steep', 
             'street', 'sweep', 'sweet', 'teeth', 'thee', 'three', 'tree', 
             'weed', 'week', 'weep', 'wheel', 'beam', 'bean', 'beast', 'beat', 
             'breathe', 'cease', 'cheap', 'cheat', 'clean', 'cream', 'deal', 
             'dream', 'ease', 'east', 'eat', 'feast', 'gleam', 'heal', 'heap', 
             'heat', 'lead', 'leaf', 'league', 'lean', 'leap', 'least', 'mean',
             'meat', 'neat', 'pea', 'peace', 'peach', 'peak', 'plead', 'please',
             'preach', 'reach', 'read', 'real', 'scream', 'sea', 'seal', 'seat',
             'speak', 'steal', 'steam', 'stream', 'tea', 'teach', 'team', 
             'treat', 'weak', 'weave', 'wheat', 'wreath', 'key', 'scheme', 
             'these', 'be', 'he', 'me', 'she', 'we', 'chief', 'field', 'grief', 
             'piece', 'priest', 'shield', 'shriek', 'thief', 'yield', 'seize', 
             'been', 'bed', 'bell', 'bench', 'bend', 'bent', 'best', 'bet', 
             'bless', 'cell', 'cent', 'check', 'chest', 'crept', 'debt', 
             'deck', 'den', 'dense', 'depth', 'desk', 'dress', 'dwell']
    return words[random.randint(0,len(words)-1)]



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int('8080'),
        debug=True
    )
