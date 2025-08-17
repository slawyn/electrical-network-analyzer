import math


class NetworkAnalyzer:
    @staticmethod
    def analyze(network):
        frequency = network.getFrequency()
        for connection in network.get_connections():
            impedance, phaseshift = NetworkAnalyzer.calculateParallel(connection.get_components(), frequency)
            connection.set_properties(impedance, phaseshift)

        # Calculate forward impedance for whole network
        impedance_total = 0
        phaseshift_total = 0

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
