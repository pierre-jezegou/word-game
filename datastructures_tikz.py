from wordle_keeper import *
from tries import *
from additional_algorithms.set_dictionary import *
from jinja2 import Template


dictionary_trie = build_trie("dictionary.txt")
alphabet = set_alphabet("dictionary.txt")
guess = Guess(6, dictionary_trie, alphabet)
letter = WordLetter(2)
trie = Trie()
trie_node = TrieNode()

tikz_code = ""

EXPORT_PATH = "documentation/images/visualizations/"
TEMPLATE_PATH = "additional_algorithms/class_description_tikz.tex"

class TikzObject():
    def __init__(self, object, template_path: str) -> None:
        self.object = object
        self.classname = self.object.__class__.__name__
        self.attributes = self.object.__dict__.keys()
        self.methods = [method for method in dir(self.object) if callable(getattr(self.object, method)) and not method.startswith('__')]
        self.template_path = template_path


    def build_elements(self, elements) -> str:
        attributes_code = ""
        for i, key in enumerate(list(elements)):
            attributes_code += r"\small{%d}: \verb|%s|" % (i, key)
            if i != len(list(elements)) - 1:
                attributes_code += "\\\\\n"
        return attributes_code

    def save_drawing(self) -> None:
        filename = f"class_%s.tex" % self.classname

        with open(self.template_path, 'r') as f:
            template_content = f.read()
        
        template = Template(template_content)

        context = {
            'title': self.classname,
            'attributes': self.build_elements(self.attributes),
            'methods': self.build_elements(self.methods)
        }
        with open(EXPORT_PATH + filename, 'w') as f:
            f.write(template.render(context))


objects = [
    TikzObject(object=guess, template_path=TEMPLATE_PATH),
    TikzObject(object=letter, template_path=TEMPLATE_PATH),
    TikzObject(object=trie, template_path=TEMPLATE_PATH),
    TikzObject(object=trie_node, template_path=TEMPLATE_PATH)
]
    
for object in objects:
    object.save_drawing()
