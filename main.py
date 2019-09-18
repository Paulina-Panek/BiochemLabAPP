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

class MainWindow(Screen):
    sequence = ObjectProperty(None)

    def btn(self):
        print("sequence: ", self.sequence.text)   #prints input on terminal(internal check)
        with open("sequence.fasta", "w") as out_handle1:    # create a file with the fasta sequence from user input
            out_handle1.write(self.sequence.text)

class SecondWindow(Screen):

    def blastsearch(self):  ## takes fasta file, runs BLAST search over internet
        fasta_string = open("sequence.fasta").read()
        result_handle = NCBIWWW.qblast("blastp", "nr", fasta_string)  ##using database nr in blastp

        with open("my_blast.xml", "w") as out_handle:   # generates xml file with output (my_blast.xml)
             out_handle.write(result_handle.read())
        result_handle.close()
        print("Exiting blastsearch()")


class ProteinWindow(Screen):
    protname = ObjectProperty(None)

    def header_remover(self, fasta_file):
        for seq_record in SeqIO.parse(fasta_file, "fasta"):
            sequence = str(seq_record.seq).upper()
        return sequence

    def on_enter(self, *args):   #what happens as you enter screen #3
        sequence_identity = ObjectProperty(None)

        no_header_sequence = self.header_remover("sequence.fasta")

        analysed_seq = ProteinAnalysis(no_header_sequence)
        Mw = analysed_seq.molecular_weight()   # Mw g/mol
        Mw_kDa = Mw/1000                       # Mw kDa
        print("Molecular Weight: ", Mw_kDa)
        print(analysed_seq.count_amino_acids())    # Dictionary with count for each amino acid

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

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MyApp(App): # <- Main Class
    def build(self):
        return kv

if __name__ == "__main__":
    MyApp().run()