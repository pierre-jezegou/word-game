import tikzplotlib
'''Implementation of a tries data structure to store words'''

class TrieNode():
    '''Implementation of the structure of a trie node'''
    def __init__(self) -> None:
        self.children: dict[TrieNode] = {}
        self.is_end_word: bool = False
        self.value: str | None = ""
        self.depth: int = 0
    
    def leaves_counter_recursive(self) -> int:
        if not self.children:
            return 1
        counter = 0
        for _, child in enumerate(self.children):
            counter += self.children[child].leaves_counter_recursive()
        return counter



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
                node.children[char].value = char
            node = node.children[char]
            node.depth = depth
        node.is_end_word = True
    

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_word



HORIZONTAL_DISTORSION = 1.2


def generate_tikz_trie(node: TrieNode, is_root= False, horizontal_distorsion: float = HORIZONTAL_DISTORSION) -> str:
    
    tikz_code = ""
    if is_root:
        tikz_code += node.depth*"\t"+'\\node [circle, fill=blue!50]{%s}[sibling distance=%scm]\n' % (node.value, horizontal_distorsion * node.leaves_counter_recursive())
    else:
        tikz_code += node.depth*"\t"+'child{node[circle, fill=red!%f]{%s}[sibling distance=%scm]\n' % ((1/node.depth)*100*0.5, node.value, horizontal_distorsion * node.leaves_counter_recursive())

    for _, child in enumerate(node.children):
        tikz_code += generate_tikz_trie(node.children[child])
        tikz_code += (node.depth+1)*"\t"+'}\n'
    
    if is_root:
        tikz_code += ';\n'
    return tikz_code

        
    

# # Generate TikZ code
def generate_complete_tikz_block():
    tikz_code = '\\begin{tikzpicture}[scale=0.45]\n'
    tikz_code += generate_tikz_trie(trie.root, True)
    tikz_code += '\\end{tikzpicture}\n'

    return (tikz_code)





dictionary = ["FOR", "HER", "THE", "HERE", "THEREFORE", "HEY", "HEAT", "TELEVISION", "THIS", "THAT", "FIRE", "TELEPHONE", "TELEPHONY", "FORCE", "FORWARD"]
# dictionary = ["MAN", "MANAGE", "MANNER", "MANDATE", "MANUSCRIPT", "MANUFACTURE", "MANEUVER", "MANICURE", "MANSION", "MANIFEST", "PORT", "PORTAL", "PORTION", "PORTFOLIO", "PORTRAY", "PORTABLE", "PORTLAND", "PORTUGAL", "PORTION", "PORTICO"]

trie = Trie()

for word in dictionary:
    trie.insert_word(word=word)

print(generate_complete_tikz_block())

