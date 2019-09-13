from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

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

    sequence_identity = ObjectProperty(None)

    def identity(self):
        result_handle = open("my_blast.xml")
        blast_record = NCBIXML.read(result_handle)

        counter = 1
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if counter < 2:  #takes only the first result
                    sequence_identity = alignment.title
                    print(sequence_identity)
                    counter = counter + 1
                    print("end of if; counter: ", counter)
        return sequence_identity

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MyApp(App): # <- Main Class
    def build(self):
        return kv

if __name__ == "__main__":
    MyApp().run()