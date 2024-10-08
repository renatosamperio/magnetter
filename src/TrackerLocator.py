from optparse import OptionParser
import urllib.parse
import requests

class Extractor:
    url = 'https://raw.githubusercontent.com/ngosang/trackerslist/refs/heads/master/trackers_all.txt'

    @staticmethod
    def encoded_trackers() -> str:
        try:
            # Send a GET request to the URL
            response = requests.get(Extractor.url)
            # Raise an error for a bad status code (e.g., 404)
            response.raise_for_status()
            
            # Read the content of the file
            trackers = response.text
            trackers_encoded = urllib.parse.quote_plus(trackers)
            return trackers_encoded

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the file: {e}")

    @staticmethod
    def magnet(hash, trackers) -> str:
        try:
            prefix = "magnet:?xt=urn:btih:"
            magnet_uri = "&tr=" + trackers
            return prefix+hash+magnet_uri
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst) 

def run(options):
    # from TrackerLocator import Extractor
    trackers = Extractor.encoded_trackers()
    print("Getting trackers...")
    # print(trackers)
    magnet = Extractor.magnet(options.hash, trackers)
    print("Getting magnet...")
    print(magnet)

# Example of usage
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-s", "--hash", 
                      dest="hash", 
                      default=None,
                      action="store", 
                      type="string", 
                      help="Torrent hash")

    (options, args) = parser.parse_args()
    if not options.hash:
        parser.error("Input 'hash' is invalid required")
    run(options)
