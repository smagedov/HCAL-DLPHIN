import ROOT
import numpy as np
import uproot
import matplotlib as mpl
import matplotlib.pyplot as plt
import math


print("Yo we running now")

with uproot.open("reco_MC_RAW2DIGI_RECO.root") as f:
        print(f["DLPHINTree"].keys())
        SimHitEnergyVec = f["DLPHINTree"]["SimHitEnergyVec"].array(library="np")
        DLPHINEnergyVec = f["DLPHINTree"]["DLPHINEnergyVec"].array(library="np")
        iEtaVec = f["DLPHINTree"]["IetaVec"].array(library="np")
        PhiVec = f["DLPHINTree"]["IphiVec"].array(library="np")
        DepthVec = f["DLPHINTree"]["DepthVec"].array(library="np")
        SimHitRes = []
        for i in range(0, np.size(SimHitEnergyVec)):
                templist = []
                for j in range(0, np.size(SimHitEnergyVec[i])):
                        if (SimHitEnergyVec[i][j] != 0):
                                Res = ((DLPHINEnergyVec[i][j]-SimHitEnergyVec[i][j])/SimHitEnergyVec[i][j])
                        else:
                                Res = 0
                        templist.append(Res)
                SimHitRes.append(templist)

        SimHitResVec = np.array(SimHitRes, dtype=object)

        #print(SimHitEnergyVec[0][0])
        #print(iEtaVec[0])
        #print(DepthVec[0])
        #print(PhiVec[0])

        #Depths = []
        #for i in range(0, np.size(DepthVec)):
        #       temp = []
        #       for j in range(7):
        #               temp.append(np.where(DepthVec[i] == j+1))
        #       Depths.append(temp)

        #Depths = np.array(Depths, dtype=object)
        #print(Depths[0][0][0][0])

        #iEtas = []
        #for i in range(0, np.size(iEtaVec)):
        #       temp = []
        #       for j in range(-29, 30):
        #               temp.append(np.where(iEtaVec[i] == j))
        #       iEtas.append(temp)


        #summedDepth = []
        #summedSimHitRes = []
        #for i in range(0, np.size(SimHitResVec)):
        #       temp = []
        #       tempDepth = []
        #       for j in range(np.size(Depths[i])):
        #               sumRes = 0
        #               for k in range(np.size(Depths[i][j][0])):
        #                       sumRes = sumRes + SimHitResVec[i][Depths[i][j][0][k]]
        #               #print(sumRes)
        #               temp.append(sumRes)
        #               tempDepth.append(j+1)
        #       summedSimHitRes.append(temp)
        #       summedDepth.append(tempDepth)

        #summedDepth = np.array(summedDepth, dtype=object)
        #summedSimHitRes = np.array(summedSimHitRes, dtype=object)

        #print(summedSimHitRes[0])
        #print(summedDepth[0])

        FlatSimHitRes = np.concatenate(SimHitResVec)
        FlatSimHitEnergy = np.concatenate(SimHitEnergyVec)
        FlatiEta = np.concatenate(iEtaVec)
        FlatDepth = np.concatenate(DepthVec)

        #FSumDepth = np.concatenate(summedDepth)
        #FSumSimHitRes = np.concatenate(summedSimHitRes)

        #FSSHRNoZero = FSumSimHitRes[FSumSimHitRes != 0]
        #FSDNoZero = FSumDepth[FSumSimHitRes != 0]

        #Depths = []
        #for i in range(np.max(FlatDepth)):
        #        Depths.append(np.where(FlatDepth == i+1))
        #print(Depths)

        #summedDepth = 

        #print(np.max(FlatiEta))
        #print(np.max(FlatDepth))

        FSHRNoZero = FlatSimHitRes[FlatSimHitRes != 0.]
        FSHENoZero = FlatSimHitEnergy[FlatSimHitEnergy != 0.]
        FENoZero = FlatiEta[FlatSimHitEnergy != 0.]
        FDNoZero = FlatDepth[FlatSimHitEnergy != 0.]

        for i in range(32):
                FSHRChoiceEtaPos = FSHRNoZero[FENoZero == i+1]
                FSHRChoiceEtaNeg = FSHRNoZero[FENoZero == -i-1]
                FSHRChoiceDepth = np.concatenate((FSHRChoiceEtaPos, FSHRChoiceEtaNeg), axis=0)
                FSHRChoiceDepth = FSHRChoiceDepth[FSHRChoiceDepth <= 20.]

                fig, ax = plt.subplots()
                h = ax.hist(FSHRChoiceDepth, bins=100)
                plt.xlabel("Resolution")
                plt.ylabel("Count")
                plt.title("Resolution for "+str(i+1)+" iEta")
                plt.savefig("plots/iEtaHist/Res"+str(i+1)+"d.png", dpi='figure')
        #plt.show()

        #for i in range(0, np.size(FSHENoZero)):
        #        FSHENoZero[i] = 1/(FSHENoZero[i]**(0.9))

        #print(FSHRNoZero)

        #fig, ax = plt.subplots()
        #h = ax.scatter(FENoZero, FSHRNoZero)
        #plt.xlim(-30,30)
        #plt.ylim(-1,3)
        #h = ax.hist2d(FENoZero, FSHRNoZero, bins=100, cmin=2, range=[[-30,30],[-1,1000]])
        #fig.colorbar(h[3], ax=ax)
        #plt.xlabel("iEta")
        #plt.ylabel("Resolution")
        #plt.title("Resolution vs iEta")
        #plt.savefig("ResvEtaplot.png", dpi='figure')
        #plt.show()

        #fig, ax = plt.subplots()
        #h = ax.scatter(FDNoZero, FSHRNoZero)
        #plt.xlim(1,7)
        #plt.ylim(-1,3)
        #h = ax.hist2d(FDNoZero, FSHRNoZero, bins=100, cmin=2, range=[[1,7],[-1,1000]])
        #fig.colorbar(h[3], ax=ax)
        #plt.xlabel("Depth")
        #plt.ylabel("Resolution")
        #plt.title("Resolution vs Depth")
        #plt.savefig("ResvDepthplot.png", dpi='figure')
        #plt.show()

        #np.save("FSHENoZero.npy", FSHENoZero.astype(np.float64))
        #np.save("FSHRNoZero.npy", FSHRNoZero.astype(np.float64))

        #SimHitEnergyVec = SimHitEnergyVec.flatten()

        #plt.hist(SimHitEnergyVec, bins=100)
        #plt.show()

