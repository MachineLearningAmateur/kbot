import requests, time, json, emoji, pprint, random, re
import auth #auth.py

#https://discord.gg/zvznJAyr62 karuta kit invite link
#automate the kd in random intervals

KARUTA = auth.KARUTA #personal karuta
KARUTA_DROP = 'https://discord.com/api/v9/channels/836605325821345843/messages' #2nd drop channel cause 1st drop channel has BIG delay not worth
KARUTA_CITY = 'https://discord.com/api/v9/channels/721066030088060938/messages' #server drops, where we grab the goodies
HEADERS = auth.HEADERS

r = requests

def post(address, payload):
    r.post(address, data=payload, headers=HEADERS)

def checkCD(limit = 1):
    print("checking cd")
    payload = {
        'content': 'krm'
    }
    flag = True
    while flag:
        try:
            post(KARUTA, payload)
            time.sleep(10 + random.randint(0,5))
            jsonn = json.loads(retrieve_messages(KARUTA, limit))
            dropCD = jsonn[0]['embeds'][0]['description']
            flag = False
        except:
            print("Temporarily waiting 10 mins.")
            time.sleep(10 * 60 + random.randint(0,30))
    coolDown = dropCD.split('\n') #0 = daily, 1 = vote, 2 = drop, 3 = grab, 4 = work
    searchCriteria = re.compile(r'in `(\d\d|\d) (hours|hour|minutes|minute|seconds|second)`')
    x = None
    case = None
    #mo0 = daily cd
    #mo1 = vote cd
    #mo2 = drop cd
    mo3 = searchCriteria.search(coolDown[3])
    if 'ready' in coolDown[0]:
        post(KARUTA, {'content': 'kdaily'})
    # elif 'ready in coolDown[1]:
    #     implement in the future
    #elif 'ready' in coolDown[2]: #drop case
        # if 'ready' in coolDown[3]:
            #drop()
        # else:
            #drop(10)
        #still need to implement pick up process
    if (mo3):
        if (mo3.group(2) == 'minutes' or mo3.group(2) == 'minute'): #grab case
            x = int(mo3.group(1))
            case = 60
        elif (mo3.group(2) == 'seconds' or mo3.group(2) == 'second'):
            x = int(mo3.group(1))
            case = 1
    else:
        grab_reaction()
        x = 10
        case = 60
    randSec = random.randint(0,30)
    print('approximately: ' + str((case * x) + randSec) )
    for i in range((case * x) + randSec):
        print(i + 1)
        time.sleep(1)

def drop():
    payload = {
        'content' : 'kd'
    }
    post(KARUTA_DROP, payload)

def check_success():
    payload = {
        'content' : 'kcd'
    }
    flag = True
    while flag:
        try:
            post(KARUTA, payload)
            time.sleep(10 + random.randint(0,5))
            jsonn = json.loads(retrieve_messages(KARUTA, 1))
            cd = jsonn[0]['embeds'][0]['description']
            flag = False
        except:
            print("Temporarily waiting 10 mins.") #time buffer just in case there's a server maintenance
            time.sleep(10 * 60 + random.randint(0,30))
    print(cd)
    if cd:
        searchCriteria = re.compile(r'in `(\d\d|\d) (minutes|minute|seconds|second)`')
        cdBroken = cd.split('\n')
        print(cdBroken)
        mo = searchCriteria.search(cdBroken[2]) #checks for grab only
        if (mo):
            if (mo.group(2) == 'minutes'):
                print("True")
                return True
        else:
            print("False")
            return False
    return False

def grab_reaction():
    print("initiating grab")
    drop_id(KARUTA_CITY)
    
    payload = {
        'content' : 'kt burn'
    }
    post(KARUTA, payload)
    print("Success!") 

def retrieve_messages(channel, limit):
    return r.get(channel + f'?limit={str(limit)}', headers=HEADERS).text

def drop_id(channel): #retrieves id of drop
    find_valid_drop = False
    drop = None
    while (not(find_valid_drop)):
        if (retrieve_messages(channel, 5)):
            time.sleep(1)
            jsonn = json.loads(retrieve_messages(channel, 5))
        for i in jsonn:
            #pprint.pprint(i)
            if (i['attachments']): #attachment means a drop
                drop = i
        if (not drop):
            continue
        pprint.pprint(drop)
        try: 
            if (drop['reactions']): # and len(drop['reactions']) == 4
                reactions = drop['reactions']
        except:
            continue
        choices = []
        for i in reactions:
            choices.append(i['count'])
        if (choose(choices) != -1):
            keycap = choose(choices)
            id = drop['id'] 
            print(id)
            react(KARUTA_CITY, str(id) , f'keycap_{str(keycap)}') 
            time.sleep(5)
            find_valid_drop = check_success()
            if (find_valid_drop):
                break
            else:
                for i in range(60 + random.randint(0, 5)):
                    print(i + 1)
                    time.sleep(1)
        else:
            print("will try copping again in a min")
            for i in range(60 + random.randint(0,5)):
                print(i+1)
                time.sleep(1)

def react(channel, id, choice):
    emoji_choice = emoji.emojize(':' + str(choice) + ':')
    r.put(f'{channel}/{id}/reactions/{emoji_choice}/%40me', headers=HEADERS)
    print(emoji_choice)
    
def choose(choices): #need a better method of choosing card; implement computer vision when free, also we assume only sets of 4 cards are possible due to server channel we are in
    one_two = random.randint(1,2)
    if (one_two == 1):
        for i in range(len(choices)):
            if (choices[i] == 1 or choices[i] >= 6):
                return i + 1
    else:
        k = len(choices) - 1
        while (k >= 0):
            if(choices[k] == 1 or choices[k] >= 6):
                return(k + 1)
            k = k - 1 
    return -1

user_input = input("How many cards do you want script to grab (10 mins * x cards): ")
if (user_input.isdigit()):
    print('Input is invalid so a random number will be generated between 60-65 cards.')
    num = random.randint(60, 65)
else:
    num = user_input

counter = 0
while (counter != num): 
    counter += 1
    checkCD()
    print(f'Iteration #{counter}')
    time.sleep(5)
