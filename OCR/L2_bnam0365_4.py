class CharacterRepresentation:
    def __init__(self, character, representation):
        self.character = character
        self.representation = representation

    def __repr__(self):
        return f"CharacterRepresentation(character={self.character}, representation={self.representation})"

    def __lt__(self, other):
        return self.representation < other.representation