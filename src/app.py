from flask import Flask, request, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from pprint import pprint
from optparse import OptionParser

from TrackerLocator import Extractor
from QBittorrentClient import QbTorrentClient

import atexit
import os

class TorrentApp:
    def __init__(self):
        # Initialisation of variables
        print("App is initializing...")
        self.qb_client = None

        # Create Flask app
        self.app = Flask(__name__)
        self.scheduler = BackgroundScheduler()

        # Add routes
        self.add_routes()

        # Start the periodic task every 24 hours
        print("Registering periodic task...")
        self.scheduler.add_job(func=self.daily_task, trigger="interval", hours=24)
        # self.scheduler.add_job(func=self.daily_task, trigger="interval", minutes=2)
        self.scheduler.start()

        # Ensure scheduler is shutdown properly on exit
        atexit.register(lambda: self.scheduler.shutdown())

        # Execute routing at start
        self.daily_task()

    def daily_task(self):
        # Connecting to Qbittorrent host
        qb_user = os.environ["QB_USER"]
        qb_pwd = os.environ["QB_PWD"]
        qb_host = os.environ["QB_HOST"]
        qb_port = os.environ["QB_PORT"]

        print("  Connecting to Qbittorrent...")
        self.qb_client = QbTorrentClient.connect(
        qb_user, qb_pwd, qb_host, qb_port)

        # Collecting Torrents
        categories = QbTorrentClient.print(self.qb_client)

    def add_routes(self):
        @self.app.route('/index', methods=['GET'])
        def index():
            return render_template('index.html')

        @self.app.route('/submit', methods=['POST'])
        def submit():
            # Process submitted text
            input_text = request.form['input_text']
            return f'Text processed: {input_text}'

    def run(self):
        # Run Flask app on port 5000
        self.app.run(host='0.0.0.0', port=5000)

def run(options):
    # Initialize and run the app
    app = TorrentApp()

    if not options.dry_run:
        print("Running dry run service")
        app.daily_task()
    else:
        print("Running daily service")
        app.run()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--dry_run", dest="dry_run", 
                      default=True,
                      action="store_true",
                      help="Execute only connections, no app")
    (options, args) = parser.parse_args()
    
    run(options)
