class Screenplay:
    screenplay_lst = []
    screenplay_dict = {}
    character_dialogue_dict = {}
    scene_index = []
    scene_lst = []
    script_no_spaces = []
    script_no_parentheticals = []
    character_lst = []
    CHARACTER_SPACE_NUM = 37
    DIALOGUE_SPACE_NUM = 25
    
    def __init__(self, script):
        with open(script) as f:
            self.script = f.readlines()
        self.script_no_spaces = self.noScriptSpaces()
        self.parse()
        self.screenplayElements()
        self.dataframe = self.screenplayDataframe()
        self.characterList()
        self.scene_lst = self.getScenes()
        self.script_no_parentheticals = self.noScriptParenthetical()
        self.getDialogue()
        self.scene_index = self.sceneIndex()
    
    def whiteSpaceNum(self, string):
        counter = 0
        for char in string:
            if char == ' ':
                counter += 1
            else:
                break
        return counter
    
    def parse(self):
        # Remove newlines
        self.script = [self.script[i] for i in range(len(self.script)) if self.script[i] != "\n"]
        for i in range(len(self.script)):
        # Parse Scene Headings
            if "INT." in self.script[i] or "EXT." in self.script[i]:
                self.screenplay_lst.append("Scene heading")
        # Parse Parenthenticals 
            elif "(" in self.script[i] or ")" in self.script[i]:
                self.screenplay_lst.append("Parenthetical")
        # Parse Characters
            elif self.whiteSpaceNum(self.script[i]) == self.CHARACTER_SPACE_NUM:
                self.screenplay_lst.append("Character")
        # Parse Dialogue
            elif self.whiteSpaceNum(self.script[i]) == self.DIALOGUE_SPACE_NUM:
                self.screenplay_lst.append("Dialogue")
        # Parse Action Lines
            else:
                self.screenplay_lst.append("Action Line")
    
    def screenplayElements(self):
        for i in range(len(self.script_no_spaces)):
            if self.script_no_spaces[i] not in self.screenplay_dict:
                self.screenplay_dict[self.script_no_spaces[i]] = self.screenplay_lst[i]
                
    def screenplayDataframe(self):
        screenplay_df = pd.DataFrame(self.screenplay_lst, self.script)
        return screenplay_df
    
    def characterList(self):
        for key, value in self.screenplay_dict.items():
            if value == "Character":
                self.character_lst.append(key)
                
    def noScriptSpaces(self):
        s1 = [elem.lstrip()[:-1] for elem in self.script]
        s1 = [elem for elem in s1 if elem != '']
        return s1
    
    def noScriptParenthetical(self):
        s1 = [self.script_no_spaces[i] for i in range(len(self.script)) if self.screenplay_lst[i] != 'Parenthetical']
        return s1
    
    def getScenes(self):
        i = 0
        scene_string = ""
        while i < len(self.screenplay_lst):
            if self.screenplay_lst[i] == "Scene heading":
                scene_string += self.script_no_spaces[i]
                i+=1
                while  i < len(self.screenplay_lst) and self.screenplay_lst[i] != "Scene heading":
                    scene_string += self.script_no_spaces[i]
                    i+=1
                self.scene_lst.append(scene_string)
            i+=1
        return self.scene_lst
    
    def sceneIndex(self):
        i = 0
        list_of_index = []
        while i < len(self.screenplay_lst):
            if self.screenplay_lst[i] == "Scene heading":
                while  i < len(self.screenplay_lst) and self.screenplay_lst[i] != "Scene heading":
                    i+=1
                list_of_index.append(i)
            i+=1
        return list_of_index
    
    def getDialogue(self):
        i = 0
        character_string = ""
        dialogue_lst = []
        screenplay_lst_no_parentheticals = [elem for elem in self.screenplay_lst if elem != 'Parenthetical']
        while i < len(screenplay_lst_no_parentheticals):
            if screenplay_lst_no_parentheticals[i] == "Character":
                character_string = self.script_no_parentheticals[i]
                i+=1
                while screenplay_lst_no_parentheticals[i] == "Dialogue":
                    dialogue_lst.append(self.script_no_parentheticals[i])
                    i+=1
                if character_string in self.character_dialogue_dict:
                    self.character_dialogue_dict[character_string].append(dialogue_lst)
                else:
                    self.character_dialogue_dict[character_string] = dialogue_lst
                dialogue_lst = []
            i+=1