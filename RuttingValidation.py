'''
Speed Validator
This application is used to validate the crew's speed during their RSP validations.  To use the application, the validation runs must be in their own folder.

Created on Oct 9, 2013

@author: Elliott Locke
'''
from Tkinter import Tk
from tkFileDialog import askdirectory
import xml.etree.ElementTree as ET
import tkMessageBox
import os, sys, glob
import numpy
import matplotlib.pyplot as plt
from matplotlib.pyplot import legend
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
# These imports below needed to be added in order to get a usable py app.  
from reportlab.pdfbase import _fontdata_enc_winansi
from reportlab.pdfbase import _fontdata_enc_macroman
from reportlab.pdfbase import _fontdata_enc_standard
from reportlab.pdfbase import _fontdata_enc_symbol
from reportlab.pdfbase import _fontdata_enc_zapfdingbats
from reportlab.pdfbase import _fontdata_enc_pdfdoc
from reportlab.pdfbase import _fontdata_enc_macexpert
from reportlab.pdfbase import _fontdata_widths_courier
from reportlab.pdfbase import _fontdata_widths_courierbold
from reportlab.pdfbase import _fontdata_widths_courieroblique
from reportlab.pdfbase import _fontdata_widths_courierboldoblique
from reportlab.pdfbase import _fontdata_widths_helvetica
from reportlab.pdfbase import _fontdata_widths_helveticabold
from reportlab.pdfbase import _fontdata_widths_helveticaoblique
from reportlab.pdfbase import _fontdata_widths_helveticaboldoblique
from reportlab.pdfbase import _fontdata_widths_timesroman
from reportlab.pdfbase import _fontdata_widths_timesbold
from reportlab.pdfbase import _fontdata_widths_timesitalic
from reportlab.pdfbase import _fontdata_widths_timesbolditalic
from reportlab.pdfbase import _fontdata_widths_symbol
from reportlab.pdfbase import _fontdata_widths_zapfdingbats

def ruttingValidation():
    #Get the folder to the route paths
    Tk().withdraw() #Not a full GUI
    options={"title": "Choose the folder which contains the validation runs.", "message": "This script will create a speed validation report based from the RSP files in your folder."}
    fileDir = askdirectory(**options) #show an open dialog box - This is for the folder containing multiple routes.


    RouteDirs = get_immediate_subdirectories(fileDir)

    for dirs in RouteDirs:
        xmlPath = fileDir + '/' + dirs + "/LCMSDistress/"
        if os.path.exists(xmlPath) == True:
            fulldir = xmlPath
        else:
            fulldir = 0
        
        if fulldir > 0:
            xmlfilepaths = []
            os.chdir(fulldir)
            for files in glob.glob("*.xml"):
                xmlfilepaths.append(fulldir + files)
        
def parseXMLRut(filePath):
    tree = ET.parse(filePath)
    root = tree.getroot()
    
   
def get_immediate_subdirectories(dirs):
    return [name for name in os.listdir(dirs) if os.path.isdir(os.path.join(dirs, name))]
    

if __name__ == '__main__':
    ruttingValidation()
    
    
    