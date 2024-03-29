import tikzplotlib
'''Implementation of a tries data structure to store words'''

class TrieNode():
    '''Implementation of the structure of a trie node'''
    def __init__(self) -> None:
        self.children: dict[TrieNode] = {}
        self.is_end_word: bool = False
        self.value: str | None = ""
        self.depth: int | None = 0


class Trie():
    '''Implementation of a trie : operations and build procedure'''
    def __init__(self) -> None:
        self.root = TrieNode()
    

    def insert_word(self, word: str):
        node = self.root
        depth = 0
        for char in word:
            depth += 1
            if char not in node.children:
                node.children[char] = TrieNode()
                node.depth = depth
                node.children[char].value = char
            node = node.children[char]
        node.is_end_word = True
    

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_word



def generate_tikz_trie(node: TrieNode,
                       x_offset: float = 0,
                       y_offset: float = 0,
                       parent_node_label: str | None = None
                       ) -> str:
    
    tikz_code = ""
    if parent_node_label is None:
        tikz_code += '\\node [fill=blue!50](%s) {%s};\n' % (node.value + "_" + str(node.depth) + "_node", node.value)
    else:
        tikz_code += '\\node [below=of %s, level distance=2.5cm, sibling distance=3cm, circle, fill=red!20](%s) {%s};\n' % (parent_node_label, node.value + "_" + str(node.depth) + "_node", node.value)

    parent_node_label_str = str(node.value) + "_" + str(node.depth) + "_node"

    for i, child in enumerate(node.children):
        child_x_offset = 1.5 * (i - len(node.children)/2)
        tikz_code += generate_tikz_trie(node.children[child], child_x_offset, y_offset -1, parent_node_label_str)
        tikz_code += '\\draw (%s) -- (%s);\n' % (parent_node_label_str, (node.children[child].value + "_" + str(node.children[child].depth) + "_node"))
        
    return tikz_code

# # Generate TikZ code
def test():
    tikz_code = '\\begin{tikzpicture}\n'
    tikz_code += generate_tikz_trie(trie.root)
    tikz_code += '\\end{tikzpicture}\n'

    print(tikz_code)





dictionary = ["FOR", "HER", "ORE", "THE", "HERE", "THEREFORE", "HEY", "HEAT"]

trie = Trie()

for word in dictionary:
    trie.insert_word(word=word)

test()
    
# print(trie.search('TRE'))