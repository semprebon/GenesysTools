import adversary_card
import genesys_common


def test_card_face_minion():
    setting = genesys_common.load_setting('BadaarSetting')
    card = adversary_card.AdversaryCard(setting)
    elements = card.card_face(
        { 'name': 'Thug', 'type': 'minion',
            'characteristics': { 'BR': 3, 'AG': 2, 'INT': 1, 'CUN': 2, 'WILL': 1, 'PR': 2 },
            'soak_value': 4, 'wound_threshold': 4, 'melee_defense': 0, 'ranged_defense': 0,
            'skills': [ 'Melee (Light)' ],
            'power_levels': { 'combat': 1, 'social': 2, 'general': 3 },
            'equipment': [
                { 'name': 'Mace', 'type': 'weapon', 'skill': "Melee (Light)", 'damage': 3, 'crit': 4,
                  'range': 'Enganged' } ] })
    assert len(elements) > 0

def test_card_face_rival():
    setting = genesys_common.load_setting('BadaarSetting')
    card = adversary_card.AdversaryCard(setting)
    elements = card.card_face(
        { 'name': 'Thug', 'type': 'rival',
            'characteristics': { 'BR': 3, 'AG': 2, 'INT': 1, 'CUN': 2, 'WILL': 1, 'PR': 2 },
            'soak_value': 4, 'wound_threshold': 4, 'melee_defense': 0, 'ranged_defense': 0,
            'skills': { 'Melee (Light)': 1 },
            'power_levels': { 'combat': 1, 'social': 2, 'general': 3 },
            'equipment': [
                { 'name': 'Mace', 'type': 'weapon', 'skill': "Melee (Light)", 'damage': 3, 'crit': 4,
                  'range': 'Enganged' } ] })
    assert len(elements) > 0

# def test_card_face_single_type():
#     card = adversary_card.AdversaryCard()
#     elements = card.card_face({
#         'name': "Totem", 'description': "A small carved totem for summoning a spirit.", 'type': "implement",
#         'implement': { 'effect': "Does something cool." } })
#     assert len(elements) == 4
#
# def test_card_face_multiple_types():
#     card = adversary_card.AdversaryCard()
#     elements = card.card_face({
#         'name': "Totem", 'description': "A small carved totem for summoning a spirit.", 'type': "implement/weapon",
#         'implement': { 'effect': "Does something cool." },
#         'weapon': { 'skill': "Melee (Light)", 'damage': '+2', 'crit': '3', 'range': 'Enganged' } })
#     assert len(elements) == 10
