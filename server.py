from flask import Blueprint, Flask
from prometheus_client import make_wsgi_app, Gauge, CollectorRegistry, generate_latest
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask_prometheus_metrics import register_metrics
import psutil

#
# Constants
#

CONFIG = {"version": "v0.1.2", "config": "staging"}
MAIN = Blueprint("main", __name__)

#
# Custom Metrics
#

registry = CollectorRegistry()
cpu_usage_percentage = Gauge('cpu_usage_percentage', 'CPU usage percentage', registry=registry)

def collect_cpu_metrics():
    """
    Collect CPU usage metrics.
    """
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_usage_percentage.set(cpu_percent)
    print(cpu_percent, cpu_usage_percentage)

#
# Main app
#

@MAIN.route("/")
def index():
    return "This is the main page."

@MAIN.route("/banana")
def banana():
    return "A banana is an elongated, edible fruit – botanically a berry – produced by several kinds of large herbaceous flowering plants in the genus Musa."

@MAIN.route("/apple")
def apple():
    return "An apple is an edible fruit produced by an apple tree (Malus domestica). Apple trees are cultivated worldwide and are the most widely grown species in the genus Malus."

@MAIN.route("/dragonfruit")
def dragonfruit():
    return "A pitaya (/pɪˈtaɪ.ə/) or pitahaya (/ˌpɪtəˈhaɪ.ə/) is the fruit of several different cactus species indigenous to the Americas. Pitaya usually refers to fruit of the genus Stenocereus, while pitahaya or dragon fruit refers to fruit of the genus Hylocereus, both in the family Cactaceae."

def register_blueprints(app):
    """
    Register blueprints to the app
    """
    app.register_blueprint(MAIN)

def create_app(config):
    """
    Application factory
    """
    app = Flask(__name__)
    register_blueprints(app)
    register_metrics(app, app_version=config["version"], app_config=config["config"])
    return app

#
# Dispatcher
#

def create_dispatcher() -> DispatcherMiddleware:
    """
    App factory for dispatcher middleware managing multiple WSGI apps
    """
    main_app = create_app(config=CONFIG)
    print(registry)
    return DispatcherMiddleware(main_app.wsgi_app, {"/metrics": make_wsgi_app(registry=registry)})

#
# Run
#

if __name__ == "__main__":
    run_simple(
        "0.0.0.0",
        5000,
        create_dispatcher(),
        use_reloader=True,
        use_debugger=True,
        use_evalex=True,
    )
