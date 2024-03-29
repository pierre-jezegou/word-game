'''Implementation of a tries data structure to store words'''

class TrieNode():
    '''Implementation of the structure of a trie node'''
    def __init__(self) -> None:
        self.children: dict[TrieNode] = {}
        self.is_end_word: bool = False
        self.value: str | None = ""
        self.depth: int = 0

    def leaves_counter_recursive(self) -> int:
        '''Count leaves'''
        if not self.children:
            return 1
        counter = 0
        for _, child in enumerate(self.children):
            counter += self.children[child].leaves_counter_recursive()
        return counter


def compression_tree(node: TrieNode) -> float:
    '''Compress horizontal size of the tikz plot'''
    no_child = 0
    not_much_child = 0

    for _, child in enumerate(node.children):
        no_child += len(node.children[child].children)
        not_much_child += int(not node.children[child].leaves_counter_recursive() <= 1)

    if no_child == 0 or not_much_child <= 1:
        return 1

    return node.leaves_counter_recursive()



class Trie():
    '''Implementation of a trie : operations and build procedure'''
    def __init__(self) -> None:
        self.root = TrieNode()


    def insert_word(self, word: str) -> None:
        '''Insert word in a trie'''
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
        '''Search word in a trie'''
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_word
