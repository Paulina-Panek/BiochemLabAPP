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
from kivy.uix.label import Label

class HomeWindow(Screen):
    pass

##############################
#  PROTEIN IDENTITY MODULE  ##
##############################

class MainWindow(Screen):
    sequence = ObjectProperty(None)

    def btn(self):
        print("sequence: ", self.sequence.text)   #prints input on terminal(internal check)
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
        print(no_header_sequence)

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
                        sequence_identity = alignment.title
                        print(sequence_identity)
                        counter = counter + 1
        self.protname.text = sequence_identity   #updates sequence identity on the app screen

class PostAnalysisWindow(Screen):
    pass

########################
# EXPRESSION MODULE    ###########################################
########################

class ExpressionWindow(Screen):
    pass

class BacterialWindow(Screen):
    def showpet(self):
        show_popup()

class Expression3Window(Screen):
    pass

def show_popup():
    show = Image(source='pET-3a.jpg')

    popupWindow = Popup(title= "pET3A Vector", content = show, size_hint = (None, None), size=(400,400))
    popupWindow.open()

class P():
    pass

class Expression4Window(Screen):

    def showpetseq(self):
        show_popup2()

def show_popup2():

    petseqlinear = Image(source = 'linear_map.PNG')

    popupWindow2 = Popup(title="pET3A Sequence", content = petseqlinear, size_hint = (1, 1))
    popupWindow2.open()

class BamhiWindow(Screen):
    def showends(self):
        show_popup3()


def show_popup3():
    ends = Image(source='blunt_sticky.jpg')

    popupWindow3 = Popup(title="Example", content=ends, size_hint=(1, 1))
    popupWindow3.open()

#########################
#  PURIFICATION MODULE  ##########################################
#########################

class PurificationWindow(Screen):
    pass

class IonExchangeWindow(Screen):
    isoelectric = ObjectProperty(None)

    def on_enter(self, *args):
        pI = ObjectProperty(None)

        fasta_string = open("no_header_sequence.txt").read()

        YourProt = ProteinAnalysis(fasta_string)
        pI = YourProt.isoelectric_point()
        pI_round = round(pI, 3)
        self.isoelectric.text = "Your protein has pI = " + str(pI_round)

class LastExpressionWindow(Screen):
    pass

class SECWindow(Screen):
    pass

class HydrophobicWindow(Screen):
    pass

class AffinityWindow(Screen):
    pass

class AffinityQuestionWindow(Screen):
    pass

class AffinityQbWindow(Screen):
    pass

class AffinityQcWindow(Screen):
    pass

##################################

class WrongWindow(Screen):
    pass

class FinalWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MyApp(App): # <- Main Class
    def build(self):
        return kv

if __name__ == "__main__":
    MyApp().run()