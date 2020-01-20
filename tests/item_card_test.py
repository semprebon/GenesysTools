import item_card

def test_card_face_minimal():
    card = item_card.ItemCard()
    elements = card.card_face({ 'name': "Rock", 'description': "A rock." })
    assert len(elements) == 3

def test_card_face_single_type():
    card = item_card.ItemCard()
    elements = card.card_face({
        'name': "Totem", 'description': "A small carved totem for summoning a spirit.", 'type': "implement",
        'implement': { 'effect': "Does something cool." } })
    assert len(elements) == 4

def test_card_face_multiple_types():
    card = item_card.ItemCard()
    elements = card.card_face({
        'name': "Totem", 'description': "A small carved totem for summoning a spirit.", 'type': "implement/weapon",
        'implement': { 'effect': "Does something cool." },
        'weapon': { 'skill': "Melee (Light)", 'damage': '+2', 'crit': '3', 'range': 'Enganged' } })
    assert len(elements) == 10
