from optparse import OptionParser
from pprint import pprint
from collections import defaultdict

from qbittorrent import Client
from TrackerLocator import Extractor

import os

class QbTorrentClient:

    @staticmethod
    def connect(user, pwd, host, port) -> Client:
        try:
            url = "http://"+host+":"+port
            print("     Connecting to host: "+url)
            qb = Client(url)
            qb.login(user, pwd)
            return qb
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst) 

    @staticmethod
    def print(qb_client) -> None:
        try:
            torrents = qb_client.torrents()
            print("  Found %d torrents"%len(torrents))
            for torrent in torrents:
                prefix = "   "
                if torrent['progress'] == 1:
                    torrent['state'] = "finished"
                    prefix = "***"
                print("%s %90s|%15s|%3.2f"%(prefix, torrent['name'], 
                                            torrent['state'], 
                                            torrent['progress']*100))
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

    @staticmethod
    def reannounce(qb_client) -> None:
        stalled = []
        try:
            # get imported trackers
            print("  Fetching trackers...")
            trackers = Extractor.encoded_trackers()

            # collect torrents from server
            torrents = qb_client.torrents()
            print("  Found %d torrents"%len(torrents))
            for idx, torrent in enumerate(torrents):
                torrent = torrents[idx]
                if torrent['progress'] == 1.0:
                    print("* %90s :> completed"%torrent['name'])
                    continue
            
                # send magnet with latest versions
                hash = torrent['hash']
                magnet_link = Extractor.magnet(hash, trackers)
                qb_client.download_from_link(magnet_link)
                qb_client.reannounce(hash)
                print("  %90s :> reannounced"%torrent['name'])

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

def run(options):
    # from BittorrentClient import BittorrentClient
    print("Connecting bitorrent...")
    qb_client = QbTorrentClient.connect(
        options.username, options.password, 
        options.host, options.port)
    
    QbTorrentClient.reannounce(qb_client)
# Example of usage
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--username", dest="username", 
                      default=os.environ["QB_USER"],
                      action="store", type="string", 
                      help="Bittorrent username")
    parser.add_option("--password", dest="password", 
                      default=os.environ["QB_PWD"],
                      action="store", type="string", 
                      help="Bittorrent password")
    parser.add_option("--host", dest="host", 
                      default=os.environ["QB_HOST"],
                      action="store", type="string", 
                      help="Bittorrent host")
    parser.add_option("--port", dest="port", 
                      default=os.environ["QB_PORT"],
                      action="store", type="string", 
                      help="Bittorrent port")

    (options, args) = parser.parse_args()
    if not options.username:
        parser.error("Input 'user' is invalid required")
    if not options.password:
        parser.error("Input 'password' is invalid required")
    if not options.host:
        parser.error("Input 'host' is invalid required")
    if not options.port:
        parser.error("Input 'port' is invalid required")
    # print(options)

    run(options)
