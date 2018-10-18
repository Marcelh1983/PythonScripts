# from enum import Enum
# from typing import List
# class Alternative:

#     def __init__(self, identifier ='', content = ''):
#         self.identifier = identifier
#         self.content = content

# class InteractionType(Enum):
#     Choice = 0
#     TextEntry = 1
#     GapMatch = 2
#     InlineChoice = 3
#     ExtendedText = 4
#     HotText = 5
#     Info = 6
#     SelectPoint = 7
#     GraphicAssociate = 8
#     GraphicGapMatch = 9
#     Slider = 10
#     MatchInteraction = 11
#     Order = 12
#     Combined = 13
#     NotDetermined = 14

# class Item:
#     identifier = str
#     interaction_type = InteractionType
#     body = str
#     correct_response = str
#     content = str
#     alternatives = List[Alternative]

#     def __init__(self, identifier ='', interaction_type = InteractionType.NotDetermined, \
#     body = '', correct_response = '', content = '', alternatives = []):
#         self.identifier = identifier
#         self.content = content
#         self.alternatives = alternatives