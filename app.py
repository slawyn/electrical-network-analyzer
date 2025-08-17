
import sys
import argparse
import traceback

from source.helpers import log
from source.network.network import Network
from source.network.analyzer import NetworkAnalyzer
from source.drawer.drawer import NetworkDrawer

# http://www.nzdl.org/cgi-bin/library?e=d-00000-00---off-0cdl--00-0----0-10-0---0---0direct-10---4-------0-1l--11-en-50---20-help---00-0-1-00-0--4----0-0-11-10-0utfZz-8-00&a=d&c=cdl&cl=CL2.9&d=HASHc8dbb2e2a76e17266b27ec.9.3


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", type=str, required=True)
        parser.add_argument("--output", default="output", type=str)
        self._execute(parser.parse_args(argv))

    def _execute(self, args):
        try:
            network = Network(args.input)
            NetworkAnalyzer.analyze(network)

            network.printContents()

            drawer = NetworkDrawer(args.output)
            drawer.draw_network(network)
        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    App(sys.argv[1:])
