"""Shared selection of an existing painted palm; image anchors remain unchanged."""
def hand_key(row,school,anchors):
    override=row.get('held_hand_by_school',{}).get(school)
    if override:return override
    return 'grip' if row.get('held_hand')=='grip' or anchors['grip'][0]>=anchors['far_hand'][0] else 'far_hand'
