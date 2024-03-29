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