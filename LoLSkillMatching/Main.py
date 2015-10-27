# -*- coding: utf-8 -*-
__author__ = 'Vance'
import riotwatcher as rw
import json
import time
import os
w = rw.RiotWatcher('a66b170f-ecc4-4173-84cc-9371cb61ab24')
player_list = []
all_match_ids = []
player_offset = 0
def get_match_from_summoner_name(summoner_name):
    global player_list
    global all_match_ids

    ret = 0
    print 'Player:', summoner_name
    me = w.get_summoner(name=summoner_name)
    #print me
    my_id = me['id']
    #print my_id
    #print w.get_ranked_stats(my_id)
    try:
        my_match_list = w.get_match_list(summoner_id=my_id, begin_time=1441065600000, ranked_queues='RANKED_SOLO_5x5') #patch 5.16
    except:
        print 'Error in API'
        my_match_list = []
    #print my_match_list

    if 'matches' in my_match_list:
        for match in my_match_list['matches']:
            #print match
            match_id = match['matchId']
            #print mid
            if match_id not in all_match_ids:
                print 'Match:', match_id
                all_match_ids.append(match_id)
                ret += 1
                filename = './match_data/' + str(match_id) + '.json'
                if os.path.isfile(filename):
                    pass
                    #todo
                else:
                    while not w.can_make_request():
                        pass
                    try:
                        match_detail = w.get_match(match_id=match_id)
                    except rw.riotwatcher.LoLException, e:
                        print str(e)
                        if str(e) == 'Too many requests':
                            time.sleep(5)
                            match_detail = w.get_match(match_id=match_id)
                        else:
                            continue
                    time.sleep(2)
                    with open(filename, 'w') as fp:
                        json.dump(match_detail, fp)
                    for player_info in match_detail['participantIdentities']:
                        player_name = player_info['player']['summonerName']
                        if player_name not in player_list:
                            player_list.append(player_name)
    return ret
def main():
    global all_match_ids
    global player_offset
    global player_list
    if os.path.isfile('match_ids.txt'):
        print 'Loading matches...'
        with open('match_ids.txt', 'r') as f:
            all_match_ids = ''.join((f.readlines())).split('\n')
        print 'Done. Totally',len(all_match_ids),'loaded!'
    else:
        all_match_ids = []
    if os.path.isfile('player_ids.txt'):
        print 'Loading players...'
        with open('player_ids.txt', 'r') as f:
            player_list = u''.join(f.readlines()).lower().split('\n')
        print 'Done. Totally',len(player_list),'loaded!'
    else:
        player_list = []
    if os.path.isfile('poffset.txt'):
        with open('poffset.txt', 'r') as f:
            player_offset = int(f.readlines()[0])
        print "Offset =", player_offset
    num = int(raw_input('How many more matches do you want:\n'))
    if len(player_list) == 0:
        player_list = ['wtke222', 'meowm', 'YYiiiYY', 'VanGod', 'NightBlue3']
    try:
        while w.can_make_request() and player_offset < len(player_list):
            summoner_name = player_list[player_offset]
            player_offset += 1
            dnum = get_match_from_summoner_name(summoner_name)
            num -= dnum
            if num < 0:
                break
            time.sleep(1)
            print 'Need', num, 'more'
        print 'Done'
    except Exception, e:
        print repr(e), str(e)
    print 'Totally', len(player_list), 'players and', len(all_match_ids), 'matches recorded.'
    with open('player_ids.txt', 'w') as f:
        for pid in player_list:
            f.write(pid+u'\n')
    with open('match_ids.txt', 'w') as f:
        for match_id in all_match_ids:
            f.write(str(match_id)+u'\n')
    with open('poffset.txt', 'w') as f:
        f.write('%d\n' % player_offset)


if __name__ == '__main__':
    main()
