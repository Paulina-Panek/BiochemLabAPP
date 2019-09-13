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

class SecondWindow(Screen):
    def blastsearch(self):  ## takes fasta file, runs BLAST search over internet
        fasta_string = open("sequence.fasta").read()
        print("fasta_string:", fasta_string)
        result_handle = NCBIWWW.qblast("blastp", "nr", fasta_string )  ##using database nr in blastp
        # with open("my_blast.xml", "w") as out_handle:   # this code generates xml file with output (my_blast.xml)
        #     out_handle.write(result_handle.read())      # useful for testing & might be needed later
        # result_handle.close()
        #
        # result_handle.open()
        blast_record = NCBIXML.read(result_handle)

        counter = 1
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if counter < 2:
                    print("Alignment #: ", counter)
                    sequence_identity = alignment.title
                    counter = counter + 1


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MyApp(App): # <- Main Class
    def build(self):
        return kv

if __name__ == "__main__":
    MyApp().run()