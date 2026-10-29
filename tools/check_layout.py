#!/usr/bin/env python3
"""Check authored ASCII layouts against read-only A0 metrics; no game code generated.

Coordinates are zero-based cells; actors stand at bottom centre of their marker.
The mandatory path is the lowest exposed, head-clear support in each column.
Optional one-way shelves are not silently treated as mandatory floor. Closed
quest doors are annotations: reachability is checked in their traversable state.
"""
import argparse
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TILE = 32
HEIGHT = 540
VIEWPORTS = (960, 1200)
SYMBOLS = set('.#=~^LSERNmMBFTGcD')


def a0():
    text = (ROOT / 'prototype/config/tuning.gd').read_text()
    def value(name):
        rhs = re.search(rf'^const {re.escape(name)} := (.*?)\s*(?:#.*)?$', text, re.M)
        if not rhs:
            raise ValueError(f'Missing A0 constant {name}')
        raw = rhs[1].strip()
        if raw.startswith('Vector2('):
            return tuple(float(v.strip()) for v in raw[8:-1].split(','))
        return float(raw)
    names = ['RUN_SPEED', 'JUMP_HEIGHT', 'TIME_TO_APEX', 'PLAYER_BOX',
             'CAMERA_DEAD_ZONE', 'CAMERA_LOOK_AHEAD', 'CAMERA_RESPONSE',
             'TOUCH_BUTTON_SIZE', 'TOUCH_MARGIN', 'TOUCH_GAP',
             'DPAD_RIGHT_OFFSET_RATIO', 'DPAD_UP_OFFSET_RATIO', 'DIAGONAL_WIDTH_RATIO',
             'SLASH_BUTTON_RATIO', 'SMALL_BUTTON_RATIO', 'SKILL_BUTTON_RATIO',
             'SKILL_COUNT', 'SKILL_GAP', 'CLASSIC_DIAGONAL_SPEED_RATIO',
             'AIR_JUMP_WINDOW_RATIO', 'AIR_JUMP_SPEED_RATIO',
             'HUD_LEVEL_SIZE','HUD_BAR_SIZE','HUD_BAR_GAP','HUD_MAP_SIZE','HUD_MENU_SIZE','GEAR_SIZE']
    result = {name: value(name) for name in names}
    result['g'] = 2 * result['JUMP_HEIGHT'] / result['TIME_TO_APEX'] ** 2
    result['v'] = 2 * result['JUMP_HEIGHT'] / result['TIME_TO_APEX']
    return result


def load_layout(path):
    text = Path(path).read_text()
    block = re.search(r'^```layout\s*\n(.*?)^```', text, re.M | re.S)
    if not block:
        raise ValueError('Missing layout block')
    rows = block[1].splitlines()
    if not rows or not rows[0] or len({len(r) for r in rows}) != 1:
        raise ValueError('Layout must be nonempty and rectangular')
    bad = set(''.join(rows)) - SYMBOLS
    if bad:
        raise ValueError(f'Unknown grid symbols: {sorted(bad)}')
    meta = re.search(r'^```layout-meta\s*\n(.*?)^```', text, re.M | re.S)
    config = json.loads(meta[1]) if meta else {}
    if config.get('tile_px', TILE) != TILE:
        raise ValueError('This A0 layout uses temporary 32 px tiles')
    if not any('S' in r for r in rows):
        raise ValueError('Missing S')
    return rows, config


def markers(rows, symbols):
    return [(x, y, c) for y, row in enumerate(rows) for x, c in enumerate(row) if c in symbols]


def support_rows(rows, col, metrics):
    clear = math.ceil(metrics['PLAYER_BOX'][1] / TILE)
    return [y for y in range(clear, len(rows)) if rows[y][col] in '#='
            and all(rows[z][col] != '#' for z in range(y-clear, y))]


def profile(rows, metrics):
    return [max(s) if (s := support_rows(rows, x, metrics)) else None for x in range(len(rows[0]))]


def hazards(rows):
    cells = {}
    for x, y, ch in markers(rows, '^~'):
        # ~ directly above solid ground is shallow. A vertical stack, or no ground
        # immediately below, denotes deep water and is hazardous.
        deep = ch == '~' and (y+1 >= len(rows) or rows[y+1][x] not in '#=')
        if ch == '^' or deep:
            cells.setdefault((y, 'trap' if ch == '^' else 'deep_water'), []).append(x)
    result = []
    for (y, kind), cols in cells.items():
        start = previous = cols[0]
        for col in cols[1:] + [None]:
            if col is not None and col == previous+1:
                previous = col
                continue
            result.append(dict(kind=kind, left=start, right=previous+1, row=y))
            start = previous = col
    return result


def challenges(rows, metrics):
    path = profile(rows, metrics)
    result = []
    x = 0
    while x < len(path):
        if path[x] is None:
            start = x
            while x < len(path) and path[x] is None:
                x += 1
            if start == 0 or x == len(path):
                raise ValueError('Mandatory floor has an open map edge')
            result.append(dict(kind='gap', left=start, right=x, row=path[start-1],
                               target_row=path[x]))
        else:
            if x and path[x-1] is not None and path[x] != path[x-1]:
                result.append(dict(kind='step', left=x, right=x, row=path[x-1], target_row=path[x]))
            x += 1
    for h in hazards(rows):
        # Every hazard is checked for HUD occlusion; only hazards on the lowest
        # support route become mandatory jumps. Unsupported deep water is a gap.
        if h['kind'] == 'trap' and any(path[x] == h['row']+1 for x in range(h['left'], h['right'])):
            result.append(dict(h, row=h['row']+1, target_row=h['row']+1))
    return path, sorted(result, key=lambda c: (c['left'], c['kind']))


def intersects(a, b):
    return a[0] <= b[2] and a[2] >= b[0] and a[1] <= b[3] and a[3] >= b[1]


def controls(width, m):
    # Direct transcription of touch_controls.gd::layout; rectangles include the
    # entire touch area of circles, and both invisible diagonal touch regions.
    d = m['TOUCH_BUTTON_SIZE'][0]; margin = m['TOUCH_MARGIN']; gap = m['TOUCH_GAP']
    bottom = HEIGHT-margin; low = bottom-d; up = low-m['DPAD_UP_OFFSET_RATIO']*d
    jump = margin+m['DPAD_RIGHT_OFFSET_RATIO']*d/2; diag = d*m['DIAGONAL_WIDTH_RATIO']
    boxes = {'left': (margin, low, d, d),
             'right': (margin+m['DPAD_RIGHT_OFFSET_RATIO']*d, low, d, d),
             'jump': (jump, up, d, d), 'diag_left': (jump-diag, up, diag, d),
             'diag_right': (jump+d, up, diag, d)}
    big = d*m['SLASH_BUTTON_RATIO']; small = d*m['SMALL_BUTTON_RATIO']
    sx = width-margin-big; sy = bottom-big
    boxes.update(slash=(sx, sy, big, big),
                 target=(sx+(big-small)/2, sy-gap-small, small, small),
                 health=(sx-gap-small, sy-gap-small, small, small),
                 mana=(sx-gap-small, sy+(big-small)/2, small, small))
    side = d*m['SKILL_BUTTON_RATIO']; count = int(m['SKILL_COUNT'])
    row_width = count*side+(count-1)*m['SKILL_GAP']
    for i in range(count):
        boxes[f'skill_{i+1}'] = (width/2-row_width/2+i*(side+m['SKILL_GAP']), bottom-side, side, side)
    return {k: (x, y, x+w, y+h) for k, (x, y, w, h) in boxes.items()}


def hud_spec():
    """Temporary SCR-06 numeric proposal is authored once in 06_screens.md."""
    text = (ROOT/'docs/06_screens.md').read_text()
    match = re.search(r'^```hud-metrics\s*\n(.*?)^```',text,re.M|re.S)
    if not match: raise ValueError('Missing SCR-06 hud-metrics in docs/06_screens.md')
    return json.loads(match[1])['scr06']


def upper_controls(width, m, kind='field'):
    """A0 touch_controls.layout + tuning_panel._layout; boss bar from SCR-06."""
    margin=m['TOUCH_MARGIN'];gap=m['TOUCH_GAP'];lx,ly=m['HUD_LEVEL_SIZE'];bw,bh=m['HUD_BAR_SIZE']
    mw,mh=m['HUD_MAP_SIZE'];menuw,menuh=m['HUD_MENU_SIZE'];gw,gh=m['GEAR_SIZE']
    boxes={'level':(margin,margin,margin+lx,margin+ly),
           'hp':(margin+lx+gap,margin,margin+lx+gap+bw,margin+bh),
           'mp':(margin+lx+gap,margin+bh+m['HUD_BAR_GAP'],margin+lx+gap+bw,margin+2*bh+m['HUD_BAR_GAP']),
           'menu':(width-margin-mw-gap-menuw,margin,width-margin-mw-gap,margin+menuh),
           'gear':(width-margin-mw-menuw-2*gap-gw,margin,width-margin-mw-menuw-2*gap,margin+gh)}
    if kind!='boss' or hud_spec()['show_minimap']:
        boxes['minimap']=(width-margin-mw,margin,width-margin,margin+mh)
    if kind=='boss':
        spec=hud_spec();w,h=spec['boss_bar_size'];top=spec['boss_bar_top']
        boxes['boss_hp']=((width-w)/2,top,(width+w)/2,top+h)
    return boxes


def figure_box(cell, symbol, m):
    # Use the whole 128px / 192px authored frame width, with requested actual
    # standing height 96 / 132 (not the 88px physical collider or debug labels).
    width,height=(192,132) if symbol=='B' else (128,96)
    x,y=cell;foot=((x+.5)*TILE,(y+1)*TILE)
    return (foot[0]-width/2,foot[1]-height,foot[0]+width/2,foot[1])


def top_hud_checks(rows, config, m):
    kind=config.get('kind','field');size=(len(rows[0])*TILE,len(rows)*TILE)
    targets=markers(rows,'mB' if kind=='boss' else 'mMNB')
    errors=[];lines=[];tests=0
    def probe(actor, player_cell, width, facing):
        nonlocal tests
        x,y,symbol=actor;px,py=player_cell
        camera=camera_envelope(((px+.5)*TILE,py*TILE),size,width,m,facing)
        image=screen_sweep(figure_box((x,y),symbol,m),camera,width)
        if not intersects(image,(0,0,width,HEIGHT)):
            return [],False
        tests+=1
        hits=[name for name,box in upper_controls(width,m,kind).items() if intersects(image,box)]
        return [f'{symbol}@{x},{y}/{name}' for name in hits],True
    if kind=='boss':
        # ALL head-clear standing surfaces, including optional shelves if added.
        for col in range(len(rows[0])):
            for row in support_rows(rows,col,m):
                for width in VIEWPORTS:
                    for facing in [-1,1]:
                        hits=[];seen=[]
                        for actor in targets:
                            found,visible=probe(actor,(col,row),width,facing)
                            if visible:seen.append(f'{actor[2]}c{actor[0]}')
                            hits+=found
                        # Also protect the standing player, not just m/B targets.
                        player=(col,row-1,'S')
                        found,_=probe(player,(col,row),width,facing);hits+=found
                        if hits:errors.append(f'boss col{col}/row{row}/{width}/{facing}: '+','.join(hits))
                        lines.append(f'| SCR-06 c{col}, chân r{row} | {width} | face {facing:+d}; visible={",".join(seen) or "none"}; player96 | {"FAIL "+",".join(hits) if hits else "PASS"} |')
    else:
        for actor in targets:
            ax,ay,symbol=actor
            for width in VIEWPORTS:
                bad=[];cases=0
                # Distances 0..6 to either side, BOTH facings at each position.
                for col in range(max(0,ax-6),min(len(rows[0]),ax+7)):
                    for row in support_rows(rows,col,m):
                        for facing in [-1,1]:
                            found,visible=probe(actor,(col,row),width,facing)
                            cases+=visible
                            if found:bad.append(f'player c{col},foot r{row},face{facing}: '+','.join(found))
                if bad:errors.append(f'field {symbol}c{ax},r{ay}/{width}: '+bad[0])
                lines.append(f'| SCR-05 {symbol} c{ax},r{ay}, h96 | {width} | 0–6 ô hai phía; hai hướng; {cases} visible cases | {"FAIL "+bad[0] if bad else "PASS"} |')
    for x,y,symbol in markers(rows,'SR'):
        for width in VIEWPORTS:
            cam=camera_envelope(((x+.5)*TILE,(y+1)*TILE),size,width,m)
            image=screen_sweep(figure_box((x,y),symbol,m),cam,width)
            boxes={**upper_controls(width,m,kind),**controls(width,m)}
            hits=[name for name,box in boxes.items() if intersects(image,box)]
            if hits:errors.append(f'{symbol}c{x},r{y}/{width} image96: '+','.join(hits))
            lines.append(f'| {symbol} c{x},r{y}, image128×96 | {width} | top+bottom; {_rect(image)} | {"FAIL "+",".join(hits) if hits else "PASS"} |')
    return errors,'\n'.join(['| HUD / actor / player column | Viewport | Standing-camera cases (clamped) | Result |','|---|---|---|---|']+lines),tests


def clamp_center(value, extent, view):
    return min(max(value, view/2), extent-view/2) if extent > view else extent/2


def camera_envelope(point, size, width, metrics, facing=0):
    # Horizontal dead zone, look-ahead and bounded moving-follow lag v/response.
    # Vertical: ALL legal clamped camera centres, covering smoothing/history as
    # well as both dead-zone extremes; deliberately more conservative than A0.
    px, py = point; world_w, world_h = size
    lag = metrics['RUN_SPEED']/metrics['CAMERA_RESPONSE']
    reach = metrics['CAMERA_DEAD_ZONE'][0]+lag
    looks = [facing*metrics['CAMERA_LOOK_AHEAD']] if facing else [-metrics['CAMERA_LOOK_AHEAD'], metrics['CAMERA_LOOK_AHEAD']]
    xs = [clamp_center(px+a+look, world_w, width) for a in [-reach, reach] for look in looks]
    ys = [clamp_center(v, world_h, HEIGHT) for v in [0, world_h]]
    return min(xs), min(ys), max(xs), max(ys)


def camera_at(point, size, width, metrics, facing=1):
    return (clamp_center(point[0]+facing*metrics['CAMERA_LOOK_AHEAD'], size[0], width),
            clamp_center(point[1], size[1], HEIGHT))


def screen_sweep(rect, camera, width):
    x1, y1, x2, y2 = rect; cx1, cy1, cx2, cy2 = camera
    return (x1-cx2+width/2, y1-cy2+HEIGHT/2, x2-cx1+width/2, y2-cy1+HEIGHT/2)


def trajectory(m, start, direction, mode, target_y=None, trigger_ratio=.3):
    speed = m['RUN_SPEED']*(m['CLASSIC_DIAGONAL_SPEED_RATIO'] if mode == 'diagonal' else 1)
    g = m['g']; v = m['v']; sx, sy = start
    if mode == 'air_jump':
        trigger = m['TIME_TO_APEX']*(1-trigger_ratio)
        y_trigger = sy-v*trigger+g*trigger*trigger/2
        v2 = m['AIR_JUMP_SPEED_RATIO']*v
        target_y = sy if target_y is None else target_y
        after = (v2+math.sqrt(v2*v2+2*g*(target_y-y_trigger)))/g
        duration = trigger+after
        def y(t):
            return sy-v*t+g*t*t/2 if t <= trigger else y_trigger-v2*(t-trigger)+g*(t-trigger)**2/2
    else:
        target_y = sy if target_y is None else target_y
        discriminant = v*v+2*g*(target_y-sy)
        if discriminant < 0:
            return []
        duration = (v+math.sqrt(discriminant))/g
        def y(t): return sy-v*t+g*t*t/2
    n = max(2, math.ceil(duration*240))
    return [(sx+direction*speed*(i*duration/n), y(i*duration/n)) for i in range(n+1)]


def flight_clear(rows, points, m):
    if not points:
        return False
    w, h = m['PLAYER_BOX']; maxx = len(rows[0])*TILE
    previous_foot = points[0][1]
    for x, foot in points:
        if x-w/2 < 0 or x+w/2 > maxx or foot-h < 0:
            return False
        # Shrink by epsilon: touching the supporting face is not penetration.
        x0 = math.floor((x-w/2+1e-5)/TILE); x1 = math.floor((x+w/2-1e-5)/TILE)
        y0 = max(0, math.floor((foot-h+1e-5)/TILE)); y1 = min(len(rows)-1, math.floor((foot-1e-5)/TILE))
        for yy in range(y0, y1+1):
            for xx in range(x0, x1+1):
                if rows[yy][xx] in '#^':
                    return False
        if foot > previous_foot:
            for yy in range(max(0, math.floor(previous_foot/TILE)), min(len(rows)-1, math.floor((foot-1e-5)/TILE))+1):
                if previous_foot <= yy*TILE+1e-5 and foot > yy*TILE+1e-5 and any(rows[yy][xx] == '=' for xx in range(x0,x1+1)):
                    return False
        previous_foot = foot
    x, y = points[-1]; col = int(x//TILE); row = round(y/TILE)
    return 0 <= row < len(rows) and rows[row][col] in '#='


def jump_paths(rows, challenge, m, mode='diagonal'):
    paths = {}
    for direction in [1, -1]:
        boundary = challenge['left']*TILE if direction == 1 else challenge['right']*TILE
        start_y = (challenge['row'] if direction == 1 else challenge['target_row'])*TILE
        end_y = (challenge['target_row'] if direction == 1 else challenge['row'])*TILE
        if challenge['kind'] == 'step' and end_y > start_y:
            # Walk off a down-step, then free-fall; no forced jump at a high ledge.
            speed = m['RUN_SPEED']*m['CLASSIC_DIAGONAL_SPEED_RATIO']
            t = math.sqrt(2*(end_y-start_y)/m['g']); edge = boundary+direction*m['PLAYER_BOX'][0]/2
            points = [(boundary-direction*64,start_y),(edge,start_y)] + [(edge+direction*speed*t*i/80,start_y+m['g']*(t*i/80)**2/2) for i in range(1,81)]
            if flight_clear(rows,points,m): paths[direction] = points
            continue
        choices = [64, 48, 40, 32] if challenge['kind'] == 'step' else [32, 24, 40, 16] if challenge['kind'] == 'trap' else [16, 24, 32]
        for back in choices:
            start = (boundary-direction*back, start_y)
            points = trajectory(m, start, direction, mode, end_y)
            far_edge = (challenge['right'] if direction == 1 else challenge['left'])*TILE
            if points and (points[-1][0]-far_edge)*direction >= m['PLAYER_BOX'][0]/2 and flight_clear(rows, points, m):
                paths[direction] = points
                break
    return paths


def evaluate(path):
    rows, config = load_layout(path); m = a0(); size = (len(rows[0])*TILE, len(rows)*TILE)
    route, items = challenges(rows, m); failures = []; metric_lines = []
    diagonal = m['RUN_SPEED']*m['CLASSIC_DIAGONAL_SPEED_RATIO']*2*m['TIME_TO_APEX']
    normal = m['RUN_SPEED']*2*m['TIME_TO_APEX']
    if not 120 <= len(rows[0]) <= 180 and config.get('kind') == 'field': failures.append('field width outside 120..180')
    if not 45 <= len(rows[0]) <= 60 and config.get('kind') == 'boss': failures.append('boss width outside 45..60')
    for c in items:
        span = (c['right']-c['left'])*TILE
        rise = abs(c['target_row']-c['row'])*TILE
        if c['kind'] == 'trap': rise = TILE
        safe = span <= 2*TILE and rise <= 2*TILE and diagonal >= 1.5*span and m['JUMP_HEIGHT'] >= 1.5*rise
        paths = jump_paths(rows, c, m); c['paths'] = paths
        good = safe and len(paths) == 2
        if not good: failures.append(f'{c["kind"]}@{c["left"]}:{c["right"]}')
        metric_lines.append(f'| {c["kind"]} | c{c["left"]}..{c["right"]}, r{c["row"]}→r{c["target_row"]} | {span}/{rise} | nhảy chéo, không khinh công | {diagonal/1.5:.2f}/{m["JUMP_HEIGHT"]/1.5:.2f} | {"PASS" if good else "FAIL"} (quỹ đạo +24×88 hai hướng) |')
    # Validate every actor marker's support and all optional platform headroom separately.
    for x, y, symbol in markers(rows, 'SER'):
        if y+1 >= len(rows) or rows[y+1][x] not in '#=':
            failures.append(f'{symbol}@{x},{y} has no ground')
        if route[x] != y+1:
            failures.append(f'{symbol}@{x},{y} outside mandatory route')
    hud_lines = []
    bounds = []
    for width in VIEWPORTS:
        boxes = controls(width, m)
        for key, box in boxes.items():
            if not (0 <= box[0] < box[2] <= width and 0 <= box[1] < box[3] <= HEIGHT): failures.append(f'control {key} outside viewport')
        # Conservative cluster bounding boxes, also including the empty space
        # between buttons, are used for rejection (stronger than per-button tests).
        for label, names in [('left', ['left','right','jump','diag_left','diag_right']), ('right', ['slash','target','health','mana']), ('skills', [k for k in boxes if k.startswith('skill_')])]:
            rect = (min(boxes[k][0] for k in names), min(boxes[k][1] for k in names), max(boxes[k][2] for k in names), max(boxes[k][3] for k in names))
            bounds.append((width, label, rect))
    cluster_boxes = {w: {key: rect for vw, key, rect in bounds if vw == w} for w in VIEWPORTS}
    # S and explicit R are independent of approaching direction.
    for x, y, symbol in markers(rows, 'SR'):
        foot = ((x+.5)*TILE, (y+1)*TILE); half, high = m['PLAYER_BOX'][0]/2, m['PLAYER_BOX'][1]
        world = (foot[0]-half, foot[1]-high, foot[0]+half, foot[1])
        for width in VIEWPORTS:
            cam = camera_envelope(foot, size, width, m)
            screen = screen_sweep(world, cam, width)
            collisions = [key for key, box in cluster_boxes[width].items() if intersects(screen, box)]
            good = not collisions and screen[0] >= 0 and screen[2] <= width and screen[1] >= 0 and screen[3] <= HEIGHT
            # A reset must also have a collision-free full 24x88 body.
            col0 = math.floor(world[0]/TILE); col1 = math.floor((world[2]-1e-5)/TILE)
            row0 = math.floor(world[1]/TILE); row1 = math.floor((world[3]-1e-5)/TILE)
            good = good and all(rows[yy][xx] not in '#=^' for yy in range(row0,row1+1) for xx in range(col0,col1+1))
            if not good: failures.append(f'HUD {symbol}@{x},{y}/{width}')
            hud_lines.append(f'| {symbol} c{x},r{y} hitbox24×88 | {width} | hai hướng + mép chặn | {_rect(screen)} | cx={cam[0]:.1f}..{cam[2]:.1f}, cy={cam[1]:.1f}..{cam[3]:.1f} | {"PASS" if good else "FAIL"} |')
    hazard_items = [dict(c, row=c['row']) for c in items if c['kind']=='gap'] + hazards(rows)
    for h in hazard_items:
        for direction in [1,-1]:
            edge = h['left']*TILE if direction == 1 else h['right']*TILE
            # Row of the rim/visible trap top, not the bottom of a pit.
            rim_y = h['row']*TILE
            for cells in range(4):
                # Distance is from the nearest edge of the player's 24px box.
                player_x = edge-direction*(m['PLAYER_BOX'][0]/2+cells*TILE)
                for width in VIEWPORTS:
                    cam = camera_envelope((player_x, rim_y), size, width, m, direction)
                    rim = (edge-1, rim_y-1, edge+1, rim_y+1)
                    screen = screen_sweep(rim, cam, width)
                    bad = [key for key, box in cluster_boxes[width].items() if intersects(screen, box)]
                    good = not bad and screen[0]>=0 and screen[2]<=width and screen[1]>=0 and screen[3]<=HEIGHT
                    if not good: failures.append(f'HUD {h["kind"]}@{edge}/{direction}/{cells}/{width}')
                    hud_lines.append(f'| {h["kind"]} mép c{edge/TILE:g},r{h["row"]} | {width} | {"→" if direction==1 else "←"}, trước {cells} ô | {_rect(screen)} | cx={cam[0]:.1f}..{cam[2]:.1f}, cy={cam[1]:.1f}..{cam[3]:.1f} | {"PASS" if good else "FAIL"} |')
    # End clamps explicitly exercise both map borders even without a nearby pit.
    for edge in [0, size[0]]:
        for width in VIEWPORTS:
            foot = (12 if edge==0 else size[0]-12, route[0 if edge==0 else -1]*TILE)
            cam = camera_envelope(foot, size, width, m)
            line = screen_sweep((edge,foot[1]-1,edge,foot[1]+1),cam,width)
            good = all(not intersects(line,b) for b in cluster_boxes[width].values())
            if not good: failures.append(f'edge clamp {edge}/{width}')
            hud_lines.append(f'| biên {edge:g}px | {width} | chặn camera | {_rect(line)} | cx={cam[0]:.1f}..{cam[2]:.1f}, cy={cam[1]:.1f}..{cam[3]:.1f} | {"PASS" if good else "FAIL"} |')
    if config.get('kind') == 'boss':
        bosses = markers(rows, 'B'); archers = markers(rows, 'm')
        if len(bosses) != 1 or len(archers) != 4: failures.append('boss needs exactly 1 B and 4 phase-2 m markers')
        for x,y,_ in archers:
            if y+1 not in support_rows(rows,x,m) or route[x] != y+1: failures.append(f'archer c{x},r{y} not on reachable rampart')
        for x,y,_ in bosses:
            # Reserve the entire temporary 192x192 frame above the B feet.
            left = (x+.5)*TILE-96; right = left+192; top = (y+1)*TILE-192
            if top < 0: failures.append('boss frame leaves top of map')
            for yy in range(max(0,math.floor(top/TILE)),y+1):
                for xx in range(math.floor(left/TILE),math.ceil(right/TILE)):
                    if not 0<=xx<len(rows[0]) or rows[yy][xx] in '#=^': failures.append('boss 192px frame obstructed')
        if not markers(rows,'R') or not markers(rows,'D'): failures.append('boss needs respawn and closing entrance')
    top_errors,top_table,top_cases=top_hud_checks(rows,config,m)
    failures.extend(top_errors)
    metric_table = '\n'.join(['| Loại | Vị trí (c/r từ 0) | ngang/cao px | Cách qua bắt buộc | tầm/1,5; cao/1,5 px | Kết quả |','|---|---|---|---|---|---|']+metric_lines)
    hud_table = '\n'.join(['| Điểm/hố/bẫy | Viewport | Hướng/khoảng cách | Hộp màn hình quét [x1,y1,x2,y2] | Camera đã chặn | Kết quả |','|---|---|---|---|---|---|']+hud_lines)
    return dict(rows=rows, config=config, metrics=m, size=size, profile=route, challenges=items,
                bounds=bounds, metric_table=metric_table, hud_table=hud_table, failures=failures, normal=normal, diagonal=diagonal, top_table=top_table, top_cases=top_cases)


def _rect(values): return '['+', '.join(f'{v:.1f}' for v in values)+']'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('layout'); parser.add_argument('--write-tables', action='store_true')
    args = parser.parse_args()
    try: report = evaluate(args.layout)
    except (ValueError, IndexError, KeyError) as exc:
        print('FAIL:', exc); return 1
    m = report['metrics']
    print(f'FILE {args.layout}; grid={len(report["rows"][0])}x{len(report["rows"])}; tile={TILE}px (Tạm thời)')
    print(f'A0 read-only tuning.gd: speed={m["RUN_SPEED"]:g}; H={m["JUMP_HEIGHT"]:g}; apex={m["TIME_TO_APEX"]:g}; g={m["g"]:.6f}; v={-m["v"]:.6f}')
    print(f'Range normal={report["normal"]:.2f}px; diagonal={report["diagonal"]:.2f}px; safety gap={report["diagonal"]/1.5:.2f}px; step={m["JUMP_HEIGHT"]/1.5:.2f}px')
    for w, name, rect in report['bounds']: print(f'HUD {w} {name}: {_rect(rect)}; source=touch_controls.gd::layout + tuning.gd')
    for width in VIEWPORTS:
        for name,rect in upper_controls(width,m,report['config'].get('kind','field')).items():
            source='06_screens.md::hud-metrics (Tạm thời)' if name=='boss_hp' else 'touch_controls.gd::layout + tuning.gd; gear=tuning_panel.gd::_layout'
            print(f'TOP HUD {width} {name}: {_rect(rect)}; source={source}')
    print('TOP HUD TABLE\n'+report['top_table'])
    print(f'TOP HUD: {report["top_cases"]} visible actor/camera cases; human frame width128/height96, boss192/132 (docs/13 + user); debug coordinate/back labels excluded; camera model=world.gd')
    print('METRIC TABLE\n'+report['metric_table']); print('HUD TABLE\n'+report['hud_table'])
    print('MODEL: lowest head-clear exposed support per column; optional shelves excluded; doors traversable; 240Hz continuous arcs/24x88 AABB; one-way shelves traversable on ascent; no coyote or khinh-cong credit.')
    print('CAMERA: deadzone(100,60), lookahead100, response5; horizontal envelope includes v/response lag; vertical ALL legal clamped centres; both map-edge clamps tested. Not an engine/Android playtest.')
    print(f'CHECKS: {len(report["challenges"])} required obstacles; failures={len(report["failures"])} '+str(report['failures']))
    if args.write_tables:
        text = Path(args.layout).read_text()
        for key, value in [('metrics', report['metric_table']), ('hud', report['hud_table']),('top-hud',report['top_table'])]:
            text, count = re.subn(rf'<!-- BEGIN {key} -->.*?<!-- END {key} -->', f'<!-- BEGIN {key} -->\n{value}\n<!-- END {key} -->', text, flags=re.S)
            if count==0 and key=='top-hud':
                text=text.replace('## 6. Câu hỏi còn mở',f'<!-- BEGIN {key} -->\n{value}\n<!-- END {key} -->\n\n## 6. Câu hỏi còn mở',1)
            elif count != 1: raise ValueError(f'Need exactly one {key} table marker')
        Path(args.layout).write_text(text)
    return 1 if report['failures'] else 0


if __name__ == '__main__': raise SystemExit(main())
