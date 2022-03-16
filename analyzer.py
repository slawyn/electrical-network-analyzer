from helpers import log
from network.network import Network
from drawer.drawer import NetworkDrawer

#external dependencies
import math
import sys

#http://www.nzdl.org/cgi-bin/library?e=d-00000-00---off-0cdl--00-0----0-10-0---0---0direct-10---4-------0-1l--11-en-50---20-help---00-0-1-00-0--4----0-0-11-10-0utfZz-8-00&a=d&c=cdl&cl=CL2.9&d=HASHc8dbb2e2a76e17266b27ec.9.3
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
        if(Re<0 and Im<0):
            phaseshift = math.atan(Im/Re) -math.pi
        elif(Re<0 and Im>=0):
            phaseshift = math.atan(Im/Re) + math.pi
        elif (Re == 0 and Im > 0):
            phaseshift = math.pi/2
        elif (Re == 0 and Im < 0):
            phaseshift = -math.pi/2
        else:
            phaseshift = math.atan(Im/Re)

        return phaseshift /math.pi*180

    # This is actually impedance, but should accept only B and Gs
    @staticmethod
    def calculateSusceptance(G, B):
        return 1/math.sqrt(G*G + B*B)

    # Normal calculation of the impedance
    @staticmethod
    def calculateImpedance(Re, Im):
        return  math.sqrt(Re*Re + Im*Im)

    @staticmethod
    def calculateParallel(components, frequency):
        G_total = 0
        B_total = 0

        for c in components:
            Re, Im = c.getValue(frequency)
            if Re!=0:
                G_total +=1/Re
            if Im!=0:
                B_total +=1/Im

        return NetworkAnalyzer.calculateSusceptance(G_total, B_total), NetworkAnalyzer.calculatePhaseshift(G_total, B_total)

    @staticmethod
    def calculateSeries(components, frequency):
        Re_total = 0
        Im_total = 0
        for c in components:
            Re, Im = c.getValue(frequency)
            Re_total+=Re
            Im_total+=Im

        return NetworkAnalyzer.calculateImpedance(Re_total, Im_total), NetworkAnalyzer.calculatePhaseshift(Re_total, Im_total)


if __name__ == "__main__":
    if(len(sys.argv)>1):
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

'''
def calculateParallelCircuitRR(Zr0, Zr1):
    Re = 0
    Im = 0
    if (Zr0+Zr1)>0:
        Re = (Zr0*Zr1)/(Zr0+Zr1)

    return Re, Im

def calculateParallelCircuitXX(Xcl0, Xcl1):
    Re = 0
    Im = 0


    #faktor = (R*R - 1/((w *C)*(w *C)))
    #Im = (R*R)/(w *C)/(faktor)
    #Re = -R/((w *C)*(w *C))/(faktor)

    if((Xcl0+Xcl1)!=0):
        Im = (Xcl0*Xcl1)/(Xcl0+Xcl1)
    return Re, Im

def calculateParallelCircuitRX(Zr, Xcl):

    Re = Zr
    Im = Xcl

    Factor = (Re*Re + Im*Im)
    if(Factor!= 0):

        Im_t = (Im * (Re * Re))/Factor
        Re_t = (Re * (Im * Im))/Factor
        Re = Re_t
        Im = Im_t
    return Re, Im

def calculateSeriesCircuit(Zr, Xcl):
    Re = Zr
    Im = Xcl
    return Re, Im

# Phase-Shift:
def calculatePhaseShiftAndImpedance(Re, Im):
    phaseshift = math.atan(Im/Re)
    if(Re<0 and Im<0):
        phaseshift -=math.pi
        print("arctan(y/x)- Pi")
    elif(Re<0 and Im>=0):
        phaseshift +=math.pi
        print("arctan(y/x)+ Pi")
    elif (Re == 0 and Im > 0):
        phaseshift = math.pi/2

    elif (Re == 0 and Im < 0):
        phaseshift = -math.pi/2

    degrees = phaseshift /math.pi*180
    impedance = math.sqrt(Re*Re + Im*Im)
    print("Degrees: [%f] Impedance: [%f] Re: %f  %fj"%(degrees, impedance,Re,Im))
    return degrees,impedance

def calculateTransistor():

    # Strom
    #################################################
    Vcc = 11
    Vre = 1
    Rlast = 1000
    Icmax= (Vcc -Vre )/Rlast
    Icq = (Vcc -Vre )/2/Rlast
    Ibq = Icq /100

    # Vorspannwiderstaende
    #################################################
    R2 = (1.7)/(Ibq*10)
    R1 = (11-1.7)/(Ibq*11)

    # Emitterwiderstand
    #################################################
    Ie = Icq + Ibq
    Re = Vre/Ie

    # Interner Emitter-Widerstand
    #################################################
    re = 0.025/Icq

    # Voltage gain
    #################################################
    g = -(Rlast )/(Re + re)

    # Bypass-Kondensator, Xc ist 1/10 vom Re bei fmin
    #################################################
# Impedance and phaseshift calculations
#################################################
R = 100000
Rx = 100000
f = 300    # kHz
C = 0.000000005 # 1n
L = 1


w = 2*math.pi*f
Re_total = 0
Im_total = 0

Re, Im = calculateSeriesCircuit( 1000,0)
Re_total +=Re
Im_total +=Im

Re, Im = calculateParallelCircuitRX(1000, (w*L))
Re_total +=Re
Im_total +=Im

deg, Z = calculatePhaseShiftAndImpedance(Re_total, Im_total)


Re, Im = calculateParallelCircuitRX( R, (-1/(w*C)))
Re_total +=Re
Im_total +=Im


Re, Im = calculateParallelCircuitRX( Rx, -1/(w*C*0.1) )


Re_total +=Re
Im_total +=Im

'''

'''
# Divider
faktor = (Re*Re - Im*Im)
Im_t = (Rx * (Im))/faktor
Re_t = (Rx * (Re))/faktor
Re = Re_t
Im = Im_t
'''
# Interview:
#1. microsoft teams, 1hour, hr and engineering, tech interview
#2. on-site interview, 3 hours, no tech
#3. more questions

# Company:
#1. company curretis, holskelingen, south
#2. biotech, develop for self, diagnostic equipment, bio-science, 9 people, 4 embedded developers, 3 c# engineers, cto Andreas, Wolfgang engineering director
#3. look at the website
#4. very international, public company, merged option group
# IVDA direktive, FDA


#5. r&d sell privately
#6. looking for one person
#7. summer, spring
#8. Permanent contract, 6 months Probe, no bonus structure, 50 euros vwl. Sickness pay. Early retirement scheme
