import ROOT
import numpy as np
import array
import os
import pandas as pd
import matplotlib.pyplot as plt

class Plotting:
    def __init__(self,ana_text,energy,intLumi,output_dir):
        self.ana_tex = ana_tex
        self.s_tex = "#bf{#it{"+"#sqrt{{s}} = {:.1f} GeV".format(energy)+"}}"
        self.lumi_tex = "#bf{#it{" +"L = {:.0f} ab^{{-1}}".format(intLumi) + "}}"
        self.col_tex = "FCC-ee Simulation (Delphes)"

        if not os.path.exists(output_dir):
                os.mkdir(output_dir)
        self.output_dir = output_dir

    ###   Figure   ###
    def drawFigure(self,mN,Ve,Z,func_text,out_name,histo_name="histo",zrange=[],plot_pred=False):
        
        #Set bins for the plots
        logBins = 6
        stopBin = 0.99#1e-5
        startBin = 0.01 #1e-12
        logWidth = []
        # for i in range(0,logBins): 
        #     logWidth.append(ROOT.Math.pow(10,ROOT.TMath.Log10(startBin)+((ROOT.TMath.Log10(stopBin)-ROOT.TMath.Log10(startBin))/logBins)*i))

        logWidth=[0, 0.2, 0.4, 0.6, 0.8, 1]
        logArray = array.array('d',logWidth)
        #print(logArray)

        linBins = 11
        linBins0 = 11
        linWidth = [0.25, 0.6, 0.8, 2, 4, 6, 8, 13, 17, 23, 28]
        linWidth0 = np.linspace(0.25,30,linBins0)
        linArray = array.array('d', linWidth)
        linArray0 = array.array('d', linWidth0)
        # logBinMass = 8
        # stopBinMass = 80
        # startBinMass = 9
        # logWidthMass = []
        # for i in range(0,logBinMass):
        #     logWidthMass.append(ROOT.Math.pow(10,ROOT.TMath.Log10(startBinMass)+((ROOT.TMath.Log10(stopBinMass)-ROOT.TMath.Log10(startBinMass))/logBinMass)*i))
        # logMassArray = array.array('d',logWidthMass)

        c = ROOT.TCanvas("c_"+histo_name,"canvas title")
        c.cd()
        # ROOT.gPad.SetLogx(1)
        #ROOT.gPad.SetLogy(1)
        ROOT.gPad.SetLogz(1)
        ROOT.gPad.SetRightMargin(0.15)
        ROOT.gStyle.SetOptStat(0)

        # A base histogram to correctly set the bins
        h0 = ROOT.TH2F("h0",r";m_{a} [GeV];c_{YY}", linBins0-1, linArray0, logBins-1, logArray)
        h0.GetZaxis().SetRangeUser(zrange[0],zrange[1])
        h0.Draw()

        h = ROOT.TH2F(histo_name,r";m_{a}  [GeV];c_{YY}", linBins-1, linArray, logBins-1, logArray)
        h.GetZaxis().SetTitle(func_text)
        h.GetZaxis().SetRangeUser(zrange[0],zrange[1])
        for m,v,z in zip(mN,Ve,Z):
            #print(m,v**2,z)
            h.Fill(m,v,z)
            #h.Fill(m,v**2,z)
        # if zrange:
        #     h.SetMinimum(zrange[0])
        #     h.SetMaximum(zrange[1])
        h.Draw("same COLZ")
        h.GetXaxis().SetRangeUser(0,35)

        ## Print text in figure
        Text = ROOT.TLatex()
        Text.SetNDC()
        Text.SetTextAlign(31)
        Text.SetTextSize(0.04)
        Text.SetTextAlign(12)
        Text.DrawLatex(0.090, 0.92, self.col_tex)
        Text.SetNDC(ROOT.kTRUE)
        Text.SetTextSize(0.04)
        # Text.DrawLatex(0.62, 0.83, func_text)
        Text.DrawLatex(0.56, 0.83, self.s_tex)
        Text.DrawLatex(0.56, 0.78, self.lumi_tex)
        Text.DrawLatex(0.56, 0.73, self.ana_tex)

        c.Modified()
        c.Update()

        if (plot_pred):
            x4,y4,x1,y1 = self.get_pred()
            # X = np.power(10,x)
            # Y = np.power(10,y)
            X4 = array.array('d',x4)
            Y4 = array.array('d',y4)
            X1 = array.array('d',x1)
            Y1 = array.array('d',y1)

            c.cd()
            gr4 = ROOT.TGraph(len(X4),X4,Y4)
            gr4.SetLineColor(2)
            gr4.SetLineWidth(2)
            gr4.Draw("same L")
            gr4.GetXaxis().SetRangeUser(0,90)

            gr1 = ROOT.TGraph(len(X1),X1,Y1)
            gr1.SetLineColor(1)
            gr1.SetLineWidth(2)
            gr1.Draw("same L")
            gr1.GetXaxis().SetRangeUser(0,90)

            c.Modified()
            c.Update()

            leg = ROOT.TLegend(0.56,0.13,0.73,0.17)
            leg.SetFillColor(0)
            leg.SetFillStyle(0)
            leg.SetLineColor(0)
            leg.SetShadowColor(10)
            leg.SetTextSize(0.035)
            leg.SetTextFont(42)
            leg.AddEntry(gr1, "Theoretical prediction")
            leg.AddEntry(gr4, "Theoretical prediction")
            leg.Draw()

        c.SaveAs(os.path.join(self.output_dir, out_name))

    def drawFigureWithNumbers(self,mN,Ve,Z,func_text,out_name,histo_name="histo",zrange=[]):
        
        #Set bins for the plots
        logBins = 15
        stopBin = 1e-5
        startBin = 1e-12
        logWidth = []
        for i in range(0,logBins): 
            logWidth.append(ROOT.Math.pow(10,ROOT.TMath.Log10(startBin)+((ROOT.TMath.Log10(stopBin)-ROOT.TMath.Log10(startBin))/logBins)*i))
        logArray = array.array('d',logWidth)

        linBins = 10
        linBins0 = 10
        linWidth = [0,5,10,20,30,40,50,60,70,80]
        linWidth0 = np.linspace(0,90,linBins0)
        linArray = array.array('d', linWidth)
        linArray0 = array.array('d', linWidth0)

        c = ROOT.TCanvas("c_"+histo_name,"canvas title")
        c.cd()
        # ROOT.gPad.SetLogx(1)
        ROOT.gPad.SetLogy(1)
        ROOT.gPad.SetLogz(1)
        ROOT.gPad.SetRightMargin(0.15)
        ROOT.gStyle.SetOptStat(0)

        # A base histogram to correctly set the bins
        h0 = ROOT.TH2F("h0",r";m_{N}  [GeV];\left|V_{eN}\right|^{2}", linBins0-1, linArray0, logBins-1, logArray)
        h0.GetZaxis().SetRangeUser(zrange[0],zrange[1])
        h0.Draw()

        h = ROOT.TH2F(histo_name,r";m_{N}  [GeV];\left|V_{eN}\right|^{2}", linBins-1, linArray, logBins-1, logArray)
        h.GetZaxis().SetTitle(func_text)
        h.GetZaxis().SetRangeUser(zrange[0],zrange[1])
        for m,v,z in zip(mN,Ve,Z):
            h.Fill(m,v**2,z)
        h.Draw("same COLZ text")
        h.GetXaxis().SetRangeUser(0,90)

        ## Print text in figure
        Text = ROOT.TLatex()
        Text.SetNDC()
        Text.SetTextAlign(31)
        Text.SetTextSize(0.04)
        Text.SetTextAlign(12)
        Text.DrawLatex(0.090, 0.92, self.col_tex)
        Text.SetNDC(ROOT.kTRUE)
        Text.SetTextSize(0.04)
        # Text.DrawLatex(0.62, 0.83, func_text)
        Text.DrawLatex(0.56, 0.83, self.s_tex)
        Text.DrawLatex(0.56, 0.78, self.lumi_tex)
        Text.DrawLatex(0.56, 0.73, self.ana_tex)

        c.Modified()
        c.Update()

        c.SaveAs(os.path.join(self.output_dir, out_name))

    def drawFigureWithLimit(self,mN,Ve,Z,func_text,out_name,S=[],histo_name="histo",zrange=[],plot_pred=False):
        
        #Set bins for the plots
        logBins = 15
        stopBin = 1e-5
        startBin = 1e-12
        logWidth = []
        for i in range(0,logBins): 
            logWidth.append(ROOT.Math.pow(10,ROOT.TMath.Log10(startBin)+((ROOT.TMath.Log10(stopBin)-ROOT.TMath.Log10(startBin))/logBins)*i))
        logArray = array.array('d',logWidth)

        linBins = 11
        linBins0 = 10
        linWidth = [0,5,10,20,30,40,50,60,70,80,90]
        linWidth0 = np.linspace(0,90,linBins0)
        linArray = array.array('d', linWidth)
        linArray0 = array.array('d', linWidth0)

        c = ROOT.TCanvas("c_"+histo_name,"canvas title")
        c.cd()
        # ROOT.gPad.SetLogx(1)
        ROOT.gPad.SetLogy(1)
        ROOT.gPad.SetLogz(1)
        ROOT.gPad.SetRightMargin(0.15)
        ROOT.gStyle.SetOptStat(0)

        # A base histogram to correctly set the bins
        h0 = ROOT.TH2F("h0",r";m_{N}  [GeV];\left|V_{eN}\right|^{2}", linBins0-1, linArray0, logBins-1, logArray)
        h0.GetZaxis().SetRangeUser(zrange[0],zrange[1])
        h0.Draw()

        h = ROOT.TH2F(histo_name,r";m_{N}  [GeV];\left|V_{eN}\right|^{2}", linBins-1, linArray, logBins-1, logArray)
        h.GetZaxis().SetTitle(func_text)
        h.GetZaxis().SetRangeUser(zrange[0],zrange[1])
        for m,v,z in zip(mN,Ve,Z):
            h.Fill(m,v**2,z)
        # h.Draw("same COLZ text")
        # h.DrawCopy("same COLZ")
        h.GetXaxis().SetRangeUser(0,90)

        ## Print text in figure
        Text = ROOT.TLatex()
        Text.SetNDC()
        Text.SetTextAlign(31)
        Text.SetTextSize(0.04)
        Text.SetTextAlign(12)
        Text.DrawLatex(0.090, 0.92, self.col_tex)
        Text.SetNDC(ROOT.kTRUE)
        Text.SetTextSize(0.04)
        # Text.DrawLatex(0.62, 0.83, func_text)
        # Text.DrawLatex(0.56, 0.83, self.s_tex)
        # Text.DrawLatex(0.56, 0.78, self.lumi_tex)
        # Text.DrawLatex(0.56, 0.73, self.ana_tex)

        leg = ROOT.TLegend(0.28,0.73,0.63,0.87)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetLineColor(0)
        leg.SetShadowColor(10)
        leg.SetTextSize(0.035)
        leg.SetTextFont(42)

        c.Modified()
        c.Update()

        if (plot_pred):
            x4,y4,x1,y1 = self.get_pred()
            # X = np.power(10,x)
            # Y = np.power(10,y)
            X4 = array.array('d',x4)
            Y4 = array.array('d',y4)
            X1 = array.array('d',x1)
            Y1 = array.array('d',y1)

            c.cd()
            gr4 = ROOT.TGraph(len(X4),X4,Y4)
            gr4.SetLineColor(3)
            gr4.SetLineWidth(3)
            gr4.Draw("same L")
            gr4.GetXaxis().SetRangeUser(0,90)

            gr1 = ROOT.TGraph(len(X1),X1,Y1)
            gr1.SetLineColor(3)
            gr1.SetLineWidth(3)
            gr1.SetLineStyle(7)
            gr1.Draw("same L")
            gr1.GetXaxis().SetRangeUser(0,90)

            c.Modified()
            c.Update()

            leg.AddEntry(gr1, "Prediction","l")
            leg.AddEntry(gr4, "Prediction","l")
            # leg.Draw()
            # Text.SetTextColor(2)
            # Text.SetTextSize(0.04)
            # Text.DrawLatex(0.67,0.32,"#bf{Prediction}")

        x = array.array('d')
        x.append(0.01)
        # # 3 signal event contour
        if S:
            hS = ROOT.TH2F("hS",r";m_{N}  [GeV];\left|V_{eN}\right|^{2}", linBins-1, linArray, logBins-1, logArray)
            hS.GetZaxis().SetTitle(func_text)
            hS.GetZaxis().SetRangeUser(zrange[0],zrange[1])
            for m,v,s in zip(mN,Ve,S):
                hS.Fill(m,v**2,s)
            x[0] = 3
            hS.SetContour(1,x)
            hS.SetLineColor(3)
            hS.SetLineWidth(2)
            hS.Draw("cont3 C")
            # leg.AddEntry(hS,"3 signal event")
            # Text.SetTextColor(3)
            # Text.DrawLatex(0.67,0.41,"#bf{3 signal event}")

        x[0] = 0.01
        h.SetContour(1,x)
        h.SetLineWidth(3)
        h.SetLineColor(5)
        # Text.SetTextColor(2)
        # Text.DrawLatex(0.3,0.6,"#bf{s = 0.01}")
        # h.DrawCopy("cont3 C same")
        leg.AddEntry(h,"s = 0.01","l")
        h22 = h.Clone()
        x[0] = 0.05
        h22.SetContour(1,x)
        h.SetLineWidth(3)
        h22.SetLineColor(4)
        # Text.SetTextColor(3)
        # Text.DrawLatex(0.3,0.7,"#bf{s = 0.05}")
        # h22.DrawCopy("cont3 C same")
        leg.AddEntry(h22,"s = 0.05","l")

        leg.Draw()
        c.Modified()
        c.Update()

        c.SaveAs(os.path.join(self.output_dir, out_name))

    def drawFigureWithLimitZoom(self,mN,Ve,Z,func_text,out_name,S=[],histo_name="histo",zrange=[],plot_pred=False):

        #Set bins for the plots
        logBins = 10
        stopBin = 2.9e-7
        startBin = 2e-12
        logWidth = []
        for i in range(0,logBins): 
            logWidth.append(ROOT.Math.pow(10,ROOT.TMath.Log10(startBin)+((ROOT.TMath.Log10(stopBin)-ROOT.TMath.Log10(startBin))/logBins)*i))
        logArray = array.array('d',logWidth)

        linBins = 9
        linBins0 = 10
        linWidth = [5,10,20,30,40,50,60,70,80]
        linWidth0 = np.linspace(0,80,linBins0)
        linArray = array.array('d', linWidth)
        linArray0 = array.array('d', linWidth0)

        c = ROOT.TCanvas("c_"+histo_name,"canvas title",360,250)
        c.cd()
        # ROOT.gPad.SetLogx(1)
        ROOT.gPad.SetLogy(1)
        ROOT.gPad.SetLogz(1)
        ROOT.gPad.SetRightMargin(0.3)
        ROOT.gStyle.SetOptStat(0)

        # A base histogram to correctly set the bins
        # h0 = ROOT.TH2F("h0",r";m_{N};\left|V_{eN}\right|^{2}", linBins0-1, linArray0, logBins-1, logArray)
        # h0.GetZaxis().SetRangeUser(zrange[0],zrange[1])
        # h0.Draw()

        h = ROOT.TH2F(histo_name,r";m_{N}  [GeV];\left|V_{eN}\right|^{2}", linBins-1, linArray, logBins-1, logArray)
        h.GetZaxis().SetTitle(func_text)
        h.GetZaxis().SetRangeUser(zrange[0],zrange[1])
        for m,v,z in zip(mN,Ve,Z):
            h.Fill(m,v**2,z)
        h.DrawCopy("COLZ")
        h.GetXaxis().SetRangeUser(0,90)

        ## Print text in figure
        Text = ROOT.TLatex()
        Text.SetNDC()
        Text.SetTextAlign(31)
        Text.SetTextSize(0.04)
        Text.SetTextAlign(12)
        Text.DrawLatex(0.090, 0.92, self.col_tex)
        Text.SetNDC(ROOT.kTRUE)
        Text.SetTextSize(0.04)
        # Text.DrawLatex(0.62, 0.83, func_text)
        # Text.DrawLatex(0.47, 0.86, self.s_tex)
        # Text.DrawLatex(0.47, 0.81, self.lumi_tex)
        # Text.DrawLatex(0.47, 0.76, self.ana_tex)     

        x = array.array('d')
        x.append(0.01)

        # 3 signal event contour
        if S:
            hS = ROOT.TH2F("hS",r";m_{N}  [GeV];\left|V_{eN}\right|^{2}", linBins-1, linArray, logBins-1, logArray)
            hS.GetZaxis().SetTitle(func_text)
            hS.GetZaxis().SetRangeUser(zrange[0],zrange[1])
            for m,v,s in zip(mN,Ve,S):
                hS.Fill(m,v**2,s)
            x[0] = 1
            hS.SetContour(1,x)
            hS.SetLineColor(2)
            hS.SetLineWidth(2)
            hS.Draw("cont3 same")
            Text.SetTextColor(3)
            # Text.DrawLatex(0.67,0.41,"#bf{3 signal event}")

        x[0] = 0.01
        h.SetContour(1,x)
        h.SetLineWidth(2)
        h.SetLineColor(5)
        Text.SetTextColor(5)
        # Text.DrawLatex(0.3,0.6,"#bf{s = 0.01}")
        h.DrawCopy("cont3 same")
        x[0] = 0.05
        h.SetContour(1,x)
        h.SetLineColor(4)
        Text.SetTextColor(4)
        # Text.DrawLatex(0.3,0.7,"#bf{s = 0.05}")
        h.DrawCopy("cont3 same")
        x[0] = 0.5
        h.SetContour(1,x)
        h.SetLineColor(4)
        # Text.SetTextColor(4)
        # Text.DrawLatex(0.3,0.6,"#bf{s = 0.5}")
        h.DrawCopy("cont3 same")
        
        if (plot_pred):
            x4,y4,x1,y1 = self.get_pred()
            # X = np.power(10,x)
            # Y = np.power(10,y)
            X4 = array.array('d',x4)
            Y4 = array.array('d',y4)
            X1 = array.array('d',x1)
            Y1 = array.array('d',y1)

            c.cd()
            gr4 = ROOT.TGraph(len(X4),X4,Y4)
            gr4.SetLineColor(3)
            gr4.SetLineWidth(2)
            gr4.Draw("same L")
            gr4.GetXaxis().SetRangeUser(0,90)

            gr1 = ROOT.TGraph(len(X1),X1,Y1)
            gr1.SetLineColor(3)
            gr1.SetLineWidth(2)
            gr1.SetLineStyle(7)
            gr1.Draw("same L")
            gr1.GetXaxis().SetRangeUser(0,90)

            c.Modified()
            c.Update()

            # leg = ROOT.TLegend(0.56,0.13,0.73,0.17)
            # leg.SetFillColor(0)
            # leg.SetFillStyle(0)
            # leg.SetLineColor(0)
            # leg.SetShadowColor(10)
            # leg.SetTextSize(0.035)
            # leg.SetTextFont(42)
            # leg.AddEntry(gr, "Theoretical prediction")
            # leg.Draw()
            Text.SetTextColor(2)
            Text.SetTextSize(0.04)
            # Text.DrawLatex(0.67,0.32,"#bf{Prediction}")

        c.Modified()
        c.Update()

        c.SaveAs(os.path.join(self.output_dir, out_name))


    ###   returns S/sqrt(S+B)   ###
    def func1(self,S,B):
        ret = []
        for s in S:
            if s == 0:
                ret.append(0)
                # print(0)
            else:
                ret.append(s/ROOT.Math.sqrt(s+B))
                # print(s/ROOT.Math.sqrt(s+B))
        return ret

    ###   returns S/sqrt(S+B+DeltaB)   ###
    def func2(self,S,B,DeltaB):
        ret = []
        for s in S:
            if s == 0:
                ret.append(0)
                # print(0)
            else:
                ret.append(s/ROOT.Math.sqrt(s+B+DeltaB))
                # print(s/ROOT.Math.sqrt(s+B+DeltaB))
        return ret

    ###   returns S/sqrt(B+DeltaB)   ###
    def func3(self,S,B,DeltaB):
        ret = []
        for s in S:
            ret.append(s/ROOT.Math.sqrt(B+DeltaB))
        return ret

    ###   returns decay length approximation   ###
    def func_L(self,mN,Ve):
        ret = []
        for m,v in zip(mN,Ve):
            ret.append(25*((1e-6/v)**2)*(np.power((100/m),5)))
        return ret

    
    ##   Print tabular with all values   ###
    def saveTab(self,mN,Ve,S,Z,name1,Z2,name2):
        f = open("sensitivityTabular.txt","w")
        print('\n\n\n\\begin{table}[H] \n    \\centering \n    \\begin{tabular}{|c|c|c|c|c|} \hline \n        $m_N$ & $|V_{eN}|^2$ & S & $',name1,'$ & $',name2,'$ \\\\ \\hline',file=f)
        for m,v,s,z,z2 in zip(mN,Ve,S,Z,Z2): 
            print(f'        {m} & {v**2:.2e} & {s:.3f} & {z:.3f} & {z2:.2e}\\\\', file=f)
        print('        \\hline \n    \\end{tabular} \n    \\caption{Caption} \n    \\label{tab:my_label} \n\\end{table}', file=f)
        f.close()

    def get_pred(self):
        # X: log(mN/GeV)
        # pred_data = pd.read_csv("/afs/cern.ch/user/l/lrygaard/public/FCC_ee_data.csv",header=None, sep=",", names = ["X", "Y"])
        pred_data4 = pd.read_csv("HNLe-FCC-ee-IDEA-4-events.csv",header=None, sep='\t', names = ["X", "Y"])
        pred_data1 = pd.read_csv("HNLe-FCC-ee-IDEA-1-event.csv",header=None, sep='\t', names = ["X", "Y"])
        x4, y4, x1, y1 = [], [], [], []
        for i in range(len(pred_data4.index)):
            x4.append(pred_data4.iloc[i]['X'])
            y4.append(pred_data4.iloc[i]['Y'])

        for i in range(len(pred_data1.index)):
            x1.append(pred_data1.iloc[i]['X'])
            y1.append(pred_data1.iloc[i]['Y'])

        return x4,y4,x1,y1
        

if __name__=="__main__":
    
    ana_tex        = 'e^{+}e^{-} #rightarrow Z #rightarrow a #gamma #rightarrow 3 #gamma'
    collider       = 'FCC-ee'
    energy         = 91
    intLumi        = 150

    output_dir = "plots_sensitivity/"
    plotting = Plotting(ana_tex,energy,intLumi,output_dir)
    
    #Background
    B = 0 + 4.48e+07
    # Signal #
    mN = [0.5, 0.5, 0.5, 0.5, 0.5, 
        0.7, 0.7, 0.7, 0.7, 0.7, 
        1.0, 1.0, 1.0, 1.0, 1.0, 
        3.0, 3.0, 3.0, 3.0, 3.0, 
        5.0, 5.0, 5.0, 5.0, 5.0, 
        7.0, 7.0, 7.0, 7.0, 7.0, 
        10.0, 10.0, 10.0, 10.0, 10.0, 
        15.0, 15.0, 15.0, 15.0, 15.0, 
        20.0, 20.0, 20.0, 20.0, 20.0, 
        25.0, 25.0, 25.0, 25.0, 25.0, 
        30.0, 30.0, 30.0, 30.0, 30.0]
    
    cYY = [0.1, 0.3, 0.5, 0.7, 0.9,
        0.1, 0.3, 0.5, 0.7, 0.9,
        0.1, 0.3, 0.5, 0.7, 0.9,
        0.1, 0.3, 0.5, 0.7, 0.9,
        0.1, 0.3, 0.5, 0.7, 0.9,
        0.1, 0.3, 0.5, 0.7, 0.9,
        0.1, 0.3, 0.5, 0.7, 0.9,
        0.1, 0.3, 0.5, 0.7, 0.9,
        0.1, 0.3, 0.5, 0.7, 0.9,
        0.1, 0.3, 0.5, 0.7, 0.9,
        0.1, 0.3, 0.5, 0.7, 0.9]

    # S =  [1.24e+02, 1.11e+03, 3.09e+03, 6.05e+03, 1.00e+04,
    #     1.23e+02, 1.11e+03, 3.08e+03, 6.05e+03, 9.99e+03,
    #     1.23e+02, 1.11e+03, 3.08e+03, 6.03e+03, 9.98e+03, 
    #     1.22e+02, 1.10e+03, 3.06e+03, 6.00e+03, 9.91e+03,
    #     1.22e+02, 1.10e+03, 3.05e+03, 5.97e+03, 9.87e+03,
    #     1.21e+02, 1.09e+03, 3.03e+03, 5.94e+03, 9.82e+03,
    #     1.20e+02, 1.08e+03, 3.00e+03, 5.89e+03, 9.73e+03,
    #     1.18e+02, 1.06e+03, 2.95e+03, 5.78e+03, 9.56e+03,
    #     1.15e+02, 1.04e+03, 2.89e+03, 5.66e+03, 9.35e+03,
    #     1.13e+02, 1.01e+03, 2.81e+03, 5.51e+03, 9.12e+03,
    #     1.09e+02, 9.77e+02, 2.71e+03, 5.32e+03, 8.79e+03]

    S =  [1.24E+02, 1.11E+03, 3.09E+03, 6.05E+03, 1.00E+04, 
        1.23E+02, 1.11E+03, 3.08E+03, 6.05E+03, 9.99E+03, 
        1.23E+02, 1.11E+03, 3.08E+03, 6.03E+03, 9.98E+03, 
        1.22E+02, 1.10E+03, 3.06E+03, 6.00E+03, 9.91E+03, 
        1.22E+02, 1.10E+03, 3.05E+03, 5.97E+03, 9.87E+03, 
        1.21E+02, 1.09E+03, 3.03E+03, 5.94E+03, 9.82E+03, 
        1.20E+02, 1.08E+03, 3.00E+03, 5.89E+03, 9.73E+03, 
        1.18E+02, 1.06E+03, 2.95E+03, 5.78E+03, 9.56E+03, 
        1.15E+02, 1.04E+03, 2.89E+03, 5.66E+03, 9.35E+03, 
        1.13E+02, 1.01E+03, 2.81E+03, 5.51E+03, 9.12E+03, 
        1.09E+02, 9.77E+02, 2.71E+03, 5.32E+03, 8.79E+03]

    # SEN=[]
    # for i in S:
    #     SEN.append(i/np.sqrt(i+B))
    #     print(i/np.sqrt(i+B))
    ## Figure
    func_text1 = "s = #frac{S}{#sqrt{S+B}}"
    out_name = "sensitivity.pdf"
    plotting.drawFigure(mN,cYY,plotting.func1(S,B),func_text1,out_name,"histo1",zrange=[0.011,1.5],plot_pred=False)