from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import os
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio import SeqIO
from kivy.uix.image import Image, AsyncImage
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
import os
import webbrowser

class HomeWindow(Screen):
    def remove_files(self):
        try:
            os.remove('sequence.fasta')
            os.remove('no_header_sequence.txt')
            os.remove('my_blast.xml')
            print("generated files were deleted")

        except FileNotFoundError:
            print("no files were found")

class InstructionWindow(Screen):
    pass

class AboutWindow(Screen):

    def OpenLink(address):
        webbrowser.open("https://manoa.hawaii.edu/")

class LinkstoolsWindow(Screen):
    pass

class LinksvideoWindow(Screen):

    def OpenLink1(address):
        webbrowser.open("https://www.khanacademy.org/science/biology/biotech-dna-technology/dna-cloning-tutorial/v/dna-cloning-and-recombinant-dna")

    def OpenLink2(address):
        webbrowser.open("https://www.khanacademy.org/science/ap-biology/gene-expression-and-regulation/biotechnology/v/dna-sequencing")

    def OpenLink3(address):
        webbrowser.open("https://www.khanacademy.org/science/biology/macromolecules/proteins-and-amino-acids/v/tertiary-structure-of-proteins")

    def OpenLink4(address):
        webbrowser.open("https://www.khanacademy.org/science/class-11-chemistry-india/xfbb6cb8fc2bd00c8:in-in-organic-chemistry-some-basic-principles-and-techniques/xfbb6cb8fc2bd00c8:in-in-methods-of-purification-of-organic-compounds/v/basics-of-chromatography")

    def OpenLink5(address):
        webbrowser.open("https://www.khanacademy.org/science/class-11-chemistry-india/xfbb6cb8fc2bd00c8:in-in-organic-chemistry-some-basic-principles-and-techniques/xfbb6cb8fc2bd00c8:in-in-methods-of-purification-of-organic-compounds/v/column-chromatography")

class RefsWindow(Screen):
    pass

##############################
#  PROTEIN IDENTITY MODULE  ##
##############################

class ChoiceWindow(Screen):
    pass

class PreprogrammedWindow(Screen):
    pass

class MainWindow(Screen):
    sequence = ObjectProperty(None)

    def btn(self):
        with open("sequence.fasta", "w") as out_handle1:    # create a file with the fasta sequence from user input
            out_handle1.write(self.sequence.text)

class SecondWindow(Screen):
    inputfasta = ObjectProperty(None)

    def header_remover(self, fasta_file):
        for seq_record in SeqIO.parse(fasta_file, "fasta"):
            sequence = str(seq_record.seq).upper()
        return sequence

    def on_enter(self, *args):    # prints entered sequence in app, so it can be verified & creates file with no header
        entered_seq = open("sequence.fasta").read()
        self.inputfasta.text = entered_seq

        # Create no header file
        no_header_sequence = self.header_remover("sequence.fasta")

        file1 = open("no_header_sequence.txt", "w")   # create a file with sequence no header
        file1.write(no_header_sequence)

    def blastsearch(self):  ## takes fasta file, runs BLAST search over internet
        fasta_string = open("sequence.fasta").read()
        result_handle = NCBIWWW.qblast("blastp", "nr", fasta_string)  ##using database nr in blastp

        with open("my_blast.xml", "w") as out_handle:   # generates xml file with output (my_blast.xml)
             out_handle.write(result_handle.read())
        result_handle.close()
        print("Exiting blastsearch()")

class ProteinWindow(Screen):
    protname = ObjectProperty(None)
    weight = ObjectProperty(None)

    def on_enter(self, *args):   #what happens as you enter screen #3
        sequence_identity = ObjectProperty(None)

        # reads the no_header_sequence.txt file to calculate Mw in kDa
        noHeader = open("no_header_sequence.txt").read()
        print("noHeader: ", noHeader)
        analysed_seq = ProteinAnalysis(noHeader)
        Mw = analysed_seq.molecular_weight()   # Mw g/mol
        Mw_kDa = round(Mw/1000, 3)                       # Mw kDa

        print(analysed_seq.count_amino_acids())    # Dictionary with count for each amino acid

        heaviness = str(Mw_kDa) + " kDa"
        self.weight.text = heaviness    # updates protein weight in kDa on the screen

        statinfo = os.stat('my_blast.xml')
        size = statinfo.st_size

        if size == 0:     #if no xml file created
            sequence_identity = "BLAST search failed.\nCheck your FASTA file and try again."
        else:
            result_handle = open("my_blast.xml")
            blast_record = NCBIXML.read(result_handle)

            counter = 1
            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    if counter < 2:  #takes only the first result
                        sequence_identity = alignment.hit_def
                        print("hit_def:", alignment.hit_def)
                        title_split = sequence_identity.split('>')
                        reduced_title = title_split[0]
                        print(title_split[0])
                        counter = counter + 1
        self.protname.text = reduced_title   #updates sequence identity on the app screen

class BioinfChoiceWindow(Screen):
    pass

class bioinfquizWindow(Screen):
    pass

class bq2Window(Screen):
    pass

class bq3Window(Screen):
    pass

class bq4Window(Screen):
    pass

class bq5Window(Screen):
    pass

class LastbioinfWindow(Screen):
    def on_pre_enter(self, *args):
        color(3)

    def on_pre_leave(self, *args):
        color(2)

class pidWindow(Screen):
    pass

class bphysWindow(Screen):
    pass

class ThreeDWindow(Screen):
    pass

class BlastWindow(Screen):
    def OpenLink(address):
        webbrowser.open("https://blast.ncbi.nlm.nih.gov/Blast.cgi")

    def OpenLinkBlast(address):
        webbrowser.open("https://drive.google.com/file/d/1_hxb-hqc0CD3F3BrdXUcjSXDRXksEP3U/view?usp=sharing")

class ToolsWindow(Screen):
    pass

class UniprotWindow(Screen):
    def OpenLinkPfam(address):
        webbrowser.open("https://drive.google.com/file/d/1IzliKPJ-4d4KsOanRBFEGBmwLBXOYSBx/view?usp=sharing")

class PfamWindow(Screen):
    def OpenLinkPfam(address):
        webbrowser.open("https://drive.google.com/file/d/1IzliKPJ-4d4KsOanRBFEGBmwLBXOYSBx/view?usp=sharing")

class FrustWindow(Screen):
    def OpenLinkFrust(address):
        webbrowser.open("https://drive.google.com/file/d/1pnCdCOnIybvxA_2JmAdkNC_s6iVF2hQK/view?usp=sharing")

class PymolWindow(Screen):
    def OpenLinkPyMOL(address):
        webbrowser.open("https://drive.google.com/file/d/1_NsBqk78hfae3WKgf7ZhxfUi5W8JaUfJ/view?usp=sharing")

class WaltzWindow(Screen):
    def OpenLinkWaltz(address):
        webbrowser.open("https://drive.google.com/open?id=1YDycii_5sMWtL-FYT0ilSG2-l7qs1Sv-")

class CamsolWindow(Screen):
    def OpenLinkCamsol(address):
        webbrowser.open("https://drive.google.com/file/d/10GpMevocaVDd2yDvAZihz1KzgI3ohe8h/view?usp=sharing")

class LogprotWindow(Screen):
    def OpenLinkWebLogo(address):
        webbrowser.open("https://drive.google.com/file/d/1xaHEMzcDAQq-IRwrxSzLy_QTHsVoFqu9/view?usp=sharing")


########################
# EXPRESSION MODULE    ###########################################
########################

class RevbeWindow(Screen):
    pass

class RevvecWindow(Screen):
    pass

class RevclWindow(Screen):
    pass
class Revbequiz1Window(Screen):
    pass
class Revbequiz2Window(Screen):
    pass

class ExpressionWindow(Screen):
    pass

class Exp01Window(Screen):
    pass

class BacterialWindow(Screen):
    def showpet(self):
        show_popup()

class Expression3Window(Screen):
    pass

def show_popup():
    show = Image(source='pET-3a.jpg')

    popupWindow = Popup(title= "pET3A Vector", content = show, size_hint = (0.8, 0.8))
    popupWindow.open()

class P():
    pass

class Expression4Window(Screen):

    def showpetseq(self):
        show_popup2()

def show_popup2():

    petseqlinear = Image(source = 'linear_map.PNG')

    popupWindow2 = Popup(title="pET3A Sequence", content = petseqlinear, size_hint = (0.8, 0.8))
    popupWindow2.open()

class BamhiWindow(Screen):
    def showends(self):
        show_popup3()

def show_popup3():
    ends = Image(source='blunt_sticky.jpg')

    popupWindow3 = Popup(title="Example", content=ends, size_hint=(0.8, 0.8))
    popupWindow3.open()

class StickyAmpicilinWindow(Screen):
    pass

class LacWindow(Screen):
    pass

class LastExpressionWindow(Screen):
    def on_pre_enter(self, *args):
        color(3)

    def on_pre_leave(self, *args):
        color(2)

class RevvecquizWindow(Screen):
    pass
#########################
#  PURIFICATION MODULE  ##########################################
#########################

class PurificationWindow(Screen):
    def showallpurification(self):
        show_popup10()

class IonExchangeWindow(Screen):

    def showiex(self):
        show_popup7()

def show_popup7():
    IEX = Image(source='IEX.png')

    popupWindow7 = Popup(title="Ion-exchange chromatography", content=IEX, size_hint=(0.8, 0.8))
    popupWindow7.open()

class iex2Window(Screen):
    isoelectric = ObjectProperty(None)

    def on_enter(self, *args):
        pI = ObjectProperty(None)

        try:
            fasta_string = open("no_header_sequence.txt").read()

            YourProt = ProteinAnalysis(fasta_string)
            pI = YourProt.isoelectric_point()
            pI_round = round(pI, 3)
            self.isoelectric.text = "Your protein has pI = " + str(pI_round)

        except FileNotFoundError:
            self.isoelectric.text = "pI of your protein will be displayed here\nonce you analyze a sequence"

    def showiexrule(self):
        show_popup8()

def show_popup8():
    IEXrule = Image(source='IEXrule.jpg')

    popupWindow8 = Popup(title="Buffer selection", content=IEXrule, size_hint=(0.8, 0.8))
    popupWindow8.open()

class iex2bWindow(Screen):
    pass

class iex3Window(Screen):
    pass

class SECWindow(Screen):
    def showSEC(self):
        show_popup6()

def show_popup6():
    SEC = Image(source='SEC.jpg')

    popupWindow6 = Popup(title="Size exclusion chromatography", content=SEC, size_hint=(0.8, 0.8))
    popupWindow6.open()

class SEC1bWindow(Screen):
    pass

class SEC2Window(Screen):
    pass

class BackPurificationWindow(Screen):
    def on_pre_enter(self, *args):
        color(3)

    def on_pre_leave(self, *args):
        color(2)

class HydrophobicWindow(Screen):
    def showhic(self):
        show_popup9()


def show_popup9():
    schemehic = Image(source='HIC.png')

    popupWindow9 = Popup(title="Hydrophobic Interaction Chromatography", content=schemehic, size_hint=(0.8, 0.8))
    popupWindow9.open()

class hic2Window(Screen):
    def showaa(self):
        show_popupa()


def show_popupa():
    aa = Image(source='aa.png')

    popupWindow11 = Popup(title="Amino Acid Classification", content=aa, size_hint=(0.8, 0.8))
    popupWindow11.open()

class hic3Window(Screen):
    pass

class AffinityWindow(Screen):
    def showaffinity(self):
        show_popup4()

def show_popup4():
    scheme = Image(source='affinity.jpg')

    popupWindow4 = Popup(title="Affinity Chromatography", content=scheme, size_hint=(0.8, 0.8))
    popupWindow4.open()

class AffinityQuestionWindow(Screen):
    pass

class AffinityQbWindow(Screen):
    pass

class AffinityQcWindow(Screen):
    pass

class AffinityQdWindow(Screen):
    pass

class AffinityQeWindow(Screen):
    def showimidazole(self):
        show_popup5()

def show_popup5():
    imidazole = Image(source='imidazole.png')

    popupWindow5 = Popup(title="Imidazole structure", content=imidazole, size_hint=(0.8, 0.8))
    popupWindow5.open()


##################################

class WrongWindow(Screen):
    pass

class Wrong1Window(Screen):

    def on_pre_enter(self, *args):
        color(1)
    def on_pre_leave(self, *args):
        color(2)

class Wrong2Window(Screen):
    def on_pre_enter(self, *args):
        color(1)
    def on_pre_leave(self, *args):
        color(2)

class Wrong3Window(Screen):
    def on_pre_enter(self, *args):
        color(1)
    def on_pre_leave(self, *args):
        color(2)

class Wrong4Window(Screen):
    def on_pre_enter(self, *args):
        color(1)
    def on_pre_leave(self, *args):
        color(2)

class Wrong5Window(Screen):
    def on_pre_enter(self, *args):
        color(1)
    def on_pre_leave(self, *args):
        color(2)

class Wrong6Window(Screen):
    def on_pre_enter(self, *args):
        color(1)
    def on_pre_leave(self, *args):
        color(2)

class Wrong7Window(Screen):
    def on_pre_enter(self, *args):
        color(1)
    def on_pre_leave(self, *args):
        color(2)

class Wrong8Window(Screen):
    def on_pre_enter(self, *args):
        color(1)
    def on_pre_leave(self, *args):
        color(2)

class Wrong9Window(Screen):
    def on_pre_enter(self, *args):
        color(1)
    def on_pre_leave(self, *args):
        color(2)

class Wrong10Window(Screen):
    def on_pre_enter(self, *args):
        color(1)
    def on_pre_leave(self, *args):
        color(2)

class Wrong11Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong12Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong13Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong14Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong15Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)


class Wrong16Window(Screen):
    def on_pre_enter(self, *args):
        color(1)
    def on_pre_leave(self, *args):
        color(2)

class Wrong17Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong18Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong19Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong20Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong21Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong22Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong23Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong24Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong25Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)


class Wrong26Window(Screen):
    def on_pre_enter(self, *args):
        color(1)
    def on_pre_leave(self, *args):
        color(2)

class Wrong27Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong28Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong29Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

class Wrong30Window(Screen):
    def on_pre_enter(self, *args):
        color(1)

    def on_pre_leave(self, *args):
        color(2)

def color(a):
    #switched background color for incorrect answer
    if a == 1: #reddish incorrect answer
        Window.clearcolor = (0.27, 0.21, 0.23, 1)

    elif a == 2: #back to black
        Window.clearcolor =  (0,0,0,1)

    elif a == 3: #greenish completed module
        Window.clearcolor = (0.13, 0.33, 0.33, 1)

def show_popup10():
    allpur= Image(source='allPurification.jpg')

    popupWindow10 = Popup(title="Chromatography types compared", content=allpur, size_hint=(0.8, 0.8))
    popupWindow10.open()

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("AlohaBioChemistry.kv")

class AlohaBioChemistryApp(App): # <- Main Class
    def build(self):
        return kv

if __name__ == "__main__":
    AlohaBioChemistryApp().run()