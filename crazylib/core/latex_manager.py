



class LatexManager():
    def __init__(self,doc_file_name):
        from pylatex import Document
        self.doc_file_name = doc_file_name
        geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
        self.doc = Document(geometry_options=geometry_options)

    def add_image(self,image_filename,title_name):
        from pylatex import Subsection,Figure

        with self.doc.create(Subsection(title_name)):
            with self.doc.create(Figure(position='h!')) as kitten_pic:
                kitten_pic.add_image(image_filename, width='360px')
                kitten_pic.add_caption('image_description')

    def __del__(self):
        self.doc.generate_pdf(self.doc_file_name, clean_tex=True)

