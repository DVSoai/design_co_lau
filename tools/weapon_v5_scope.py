"""Exact exceptions for the authorized shared-weapon art replacement."""
import copy

RETIRED={'sword_hold','sword_run','bow_hold','run_v3_bow','carry_v4_bow'}
REPAINTED={'attack_blade','attack_blade_only'}|{f'{prefix}_{i}' for prefix in ['swing','swing_skill'] for i in range(5)}
HELD=[0,1,2,3,4,5,6,7,12,21]

def frame_without_weapon(row):
    row=copy.deepcopy(row)
    if row['id'] in HELD:
        row['layers']['weapon'].pop('cung_asset',None)
        row.pop('held_weapon_z',None)
        row.pop('held_hand_by_school',None)
        row.pop('held_lower_leg_foreground',None)
        for school in ['kiem','cung']:row['registrations'][school].pop('weapon',None)
    return row

def asset_is_unchanged(id,old,current):
    return id in RETIRED and id not in current or id in REPAINTED or current.get(id)==old

def parts_without_weapon(data):
    data=copy.deepcopy(data);data.pop('assets',None);data.pop('weapon_masters',None)
    data['levels']['1'].pop('weapons',None);data['levels']['1'].pop('run_weapon',None)
    return data
