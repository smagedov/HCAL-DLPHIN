import ROOT
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser

ROOT.gROOT.SetBatch(1)

##____________________________________________________________________________||
parser = OptionParser()
parser.add_option('-i', '--inputPath', default = 'reco_MC_RAW2DIGI_RECO.root', action = 'store', type = 'string')
(options, args) = parser.parse_args(sys.argv)
inputPath = options.inputPath

##____________________________________________________________________________||
def main():

    printHeader()
    if getNEvents(inputPath):
        metpt = []
	metpx = []
	metpy = []
	genmetpt = []
	genmetpx = []
	genmetpy = []
	metpt, metpx, metpy, genmetpt, genmetpx, genmetpy = count(inputPath, metpt, metpx, metpy, genmetpt, genmetpx, genmetpy)

    metpt = np.asarray(metpt)
    metpy = np.asarray(metpy)
    metpx = np.asarray(metpx)
    genmetpt = np.asarray(genmetpt)
    genmetpx = np.asarray(genmetpx)
    genmetpy = np.asarray(genmetpy)

    respt = []
    respx = []
    respy = []
    for i in range(len(metpt)):
	resopt = (genmetpt[i]-metpt[i])/genmetpt[i]
	resopx = (genmetpx[i]-metpx[i])/genmetpx[i]
	resopy = (genmetpy[i]-metpy[i])/genmetpy[i]

	respt.append(resopt)
	respx.append(resopx)
	respy.append(resopy)

    respt = np.asarray(respt)
    respx = np.asarray(respx)
    respy = np.asarray(respy)

    fig, ax = plt.subplots()
    h = ax.scatter(metpt, respt)
    #plt.xlim(-30,30)
    #plt.ylim(-1,3)
    plt.xlabel("METpt")
    plt.ylabel("Resolution")
    plt.title("Total MET Resolution")
    plt.savefig("ResPTplot.png", dpi='figure')
    plt.show()

    fig, ax = plt.subplots()
    h = ax.scatter(metpx, respx)
    #plt.xlim(-30,30)
    #plt.ylim(-1,3)
    plt.xlabel("METpx")
    plt.ylabel("Resolution")
    plt.title("Parallel MET Resolution")
    plt.savefig("ResPXplot.png", dpi='figure')
    plt.show()

    fig, ax = plt.subplots()
    h = ax.scatter(metpt, respt)
    #plt.xlim(-30,30)
    #plt.ylim(-1,3)
    plt.xlabel("METpy")
    plt.ylabel("Resolution")
    plt.title("Perpendicular MET Resolution")
    plt.savefig("ResPYplot.png", dpi='figure')
    plt.show()




##____________________________________________________________________________||
def printHeader():
    print '%6s'  % 'run',
    print '%10s' % 'lumi',
    print '%9s'  % 'event',
    print '%18s' % 'module',
    print '%10s' % 'met.pt',
    print '%10s' % 'met.px',
    print '%10s' % 'met.py',
    print '%10s' % 'met.phi',
    print

##____________________________________________________________________________||
def count(inputPath, metpt, metpx, metpy, genmetpt, genmetpx, genmetpy):

    files = [inputPath]

    events = Events(files)

    handleGenMETs = Handle("std::vector<reco::GenMET>")
    handlePFMETs = Handle("std::vector<reco::PFMET>")
    handleCaloMETs = Handle("std::vector<reco::CaloMET>")
    handleMETs = Handle("std::vector<reco::MET>")

    METCollections = (
        ("pfMet",              "", "RECO", handlePFMETs   ),
        #("met",                "", "RECO", handleCaloMETs ),
        #("genMetTrue",         "" ,"DIGI2RAW",  handleGenMETS  ),
        )

    for event in events:

        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()

        event.getByLabel(("pfMet", "", "RECO"), handlePFMETs)
        met = handlePFMETs.product().front()

	metpt.append(met.pt())
	metpx.append(met.px())
        metpy.append(met.py())

	event.getByLabel(("caloMet", "", "RECO"), handleCaloMETs)
	genmet = handleCaloMETs.product().front()

	genmetpt.append(genmet.pt())
	genmetpx.append(genmet.px())
	genmetpy.append(genmet.py())

    return metpt, metpx, metpy, genmetpt, genmetpx, genmetpy

##____________________________________________________________________________||
def getNEvents(inputPath):
    file = ROOT.TFile.Open(inputPath)
    events = file.Get('Events')
    return events.GetEntries()

##____________________________________________________________________________||
def loadLibraries():
    argv_org = list(sys.argv)
    sys.argv = [e for e in sys.argv if e != '-h']
    ROOT.gSystem.Load("libFWCoreFWLite")
    ROOT.AutoLibraryLoader.enable()
    ROOT.gSystem.Load("libDataFormatsFWLite")
    ROOT.gSystem.Load("libDataFormatsPatCandidates")
    sys.argv = argv_org

##____________________________________________________________________________||
loadLibraries()
from DataFormats.FWLite import Events, Handle

##____________________________________________________________________________||
if __name__ == '__main__':
    main()
