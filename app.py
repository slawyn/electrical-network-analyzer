from analyzer.helpers import log
from analyzer.network.network import Network
from analyzer.drawer.drawer import NetworkDrawer

# external dependencies
import math
import sys

# http://www.nzdl.org/cgi-bin/library?e=d-00000-00---off-0cdl--00-0----0-10-0---0---0direct-10---4-------0-1l--11-en-50---20-help---00-0-1-00-0--4----0-0-11-10-0utfZz-8-00&a=d&c=cdl&cl=CL2.9&d=HASHc8dbb2e2a76e17266b27ec.9.3


class NetworkAnalyzer:
    @staticmethod
    def analyze(network):
        try:
            nodes = network.getSortedNodes()
            frequency = network.getFrequency()

            # Calculate impedance and phaseshift for all segments, separately
            # Put the values into the segments
            for node in nodes:
                comps = node.getComponents()
                for c in comps:
                    parallel_comps = comps[c]

                    impedance, phaseshift = NetworkAnalyzer.calculateParallel(parallel_comps, frequency)
                    node.setProperties(c, impedance, phaseshift)

            # Calculate forward impedance for whole network
            impedance_total = 0
            phaseshift_total = 0
        except Exception as e:
            log(e)

    @staticmethod
    def calculatePhaseshift(Re, Im):
        phaseshift = 0
        if (Re < 0 and Im < 0):
            phaseshift = math.atan(Im/Re) - math.pi
        elif (Re < 0 and Im >= 0):
            phaseshift = math.atan(Im/Re) + math.pi
        elif (Re == 0 and Im > 0):
            phaseshift = math.pi/2
        elif (Re == 0 and Im < 0):
            phaseshift = -math.pi/2
        else:
            phaseshift = math.atan(Im/Re)

        return phaseshift / math.pi*180

    # This is actually impedance, but should accept only B and Gs
    @staticmethod
    def calculateSusceptance(G, B):
        return 1/math.sqrt(G*G + B*B)

    # Normal calculation of the impedance
    @staticmethod
    def calculateImpedance(Re, Im):
        return math.sqrt(Re*Re + Im*Im)

    @staticmethod
    def calculateParallel(components, frequency):
        G_total = 0
        B_total = 0

        for c in components:
            Re, Im = c.getValue(frequency)
            if Re != 0:
                G_total += 1/Re
            if Im != 0:
                B_total += 1/Im

        return NetworkAnalyzer.calculateSusceptance(G_total, B_total), NetworkAnalyzer.calculatePhaseshift(G_total, B_total)

    @staticmethod
    def calculateSeries(components, frequency):
        Re_total = 0
        Im_total = 0
        for c in components:
            Re, Im = c.getValue(frequency)
            Re_total += Re
            Im_total += Im

        return NetworkAnalyzer.calculateImpedance(Re_total, Im_total), NetworkAnalyzer.calculatePhaseshift(Re_total, Im_total)


if __name__ == "__main__":
    if (len(sys.argv) > 1):
        try:
            filepath = sys.argv[1]
            network = Network(filepath)
            NetworkAnalyzer.analyze(network)

            # Print contents after analysis
            network.printContents()

            # Draw network
            networkdrawer = NetworkDrawer(network)
            networkdrawer.drawNetwork()
        except Exception as e:
            log(e)
