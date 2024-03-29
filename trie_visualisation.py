'''Build tries'''
# import tikzplotlib
from tries import *

HORIZONTAL_DISTORSION = 1


def generate_tikz_trie(node: TrieNode,
                       is_root= False,
                       horizontal_distorsion: float = HORIZONTAL_DISTORSION
                       ) -> str:
    '''Generate simple tikz trie'''

    tikz_code = ""
    if is_root:
        tikz_code += (node.depth*"\t"
                      + '\\node [circle, fill=blue!50]{%s}[sibling distance=%scm]\n'
                      % (node.value, horizontal_distorsion * compression_tree(node)))
    else:
        tikz_code += (node.depth*"\t"
                      + 'child{node[circle, fill=red!%f]{%s}[sibling distance=%scm]\n'
                      % ((1/node.depth)*100*0.5,
                         node.value,
                         horizontal_distorsion * compression_tree(node)))

    for _, child in enumerate(node.children):
        tikz_code += generate_tikz_trie(node.children[child])
        tikz_code += (node.depth+1)*"\t"+'}\n'

    if is_root:
        tikz_code += ';\n'
    return tikz_code


FIND_PATH_COLOR = "green!70!black!70"
NOT_FIND_PATH_COLOR = "black!30"

def generate_search_path(node: TrieNode,
                       is_root= False,
                       horizontal_distorsion: float = HORIZONTAL_DISTORSION,
                       search_word: str = None,
                       good_path: bool = True) -> str:
    '''Generate given search path'''
    tikz_code = ""

    if node.depth <= len(search_word) and good_path is True:
        search_letter = search_word[node.depth-1]
    else:
        search_letter = None

    if node.depth == 0:
        node_color_computed = FIND_PATH_COLOR
    else:
        node_color_computed = node_color(search_letter, node.value)


    if is_root:
        tikz_code += (node.depth*"\t"
                      + '\\node [circle, fill=%s]{%s}[sibling distance=%scm]\n'
                      % (node_color_computed,
                         node.value,
                         horizontal_distorsion * compression_tree(node)))
    else:
        tikz_code += (node.depth*"\t"
                      + 'child{node[circle, fill=%s]{%s}[sibling distance=%scm]\n'
                      % (node_color_computed,
                         node.value,
                         horizontal_distorsion * compression_tree(node)))


    for _, child in enumerate(node.children):
        if node_color_computed == FIND_PATH_COLOR:
            tikz_code += generate_search_path(node.children[child],
                                              search_word=search_word,
                                              good_path=True)
        else:
            tikz_code += generate_search_path(node.children[child],
                                              search_word=search_word,
                                              good_path=False)

        tikz_code += (node.depth+1)*"\t"+'}\n'

    if is_root:
        tikz_code += ';\n'
    return tikz_code

def node_color(search_letter: str | None, first_letter: str | None) -> str:
    '''Give comparaison color'''
    if search_letter:
        if search_letter[0] == first_letter:
            return FIND_PATH_COLOR
    return NOT_FIND_PATH_COLOR


# # Generate TikZ code
def generate_complete_tikz_block_search():
    '''Generate tikz trie'''
    tikz_code = '\\begin{tikzpicture}[scale=0.8]\n'
    tikz_code += generate_search_path(trie.root, True, search_word="HEIGHT")
    tikz_code += '\\end{tikzpicture}\n'
    return tikz_code

def generate_complete_tikz_block_draw():
    '''Generate tikz search path in trie'''
    tikz_code = '\\begin{tikzpicture}[scale=0.8]\n'
    tikz_code += generate_tikz_trie(trie.root, True)
    tikz_code += '\\end{tikzpicture}\n'
    return tikz_code


dictionary = ["FOR", "HER", "HERE", "HEY", "HEAT", "FIRE", "FORCE", "FORWARD", "FORWARDER", "FIRM", "FIRSTLY", "FIRSTS", "FIREWORK", "HEIGHTY", "HEIGHTEEN"]

trie = Trie()

for word in dictionary:
    trie.insert_word(word=word)

# print(generate_complete_tikz_block_search())
print(generate_complete_tikz_block_draw())
