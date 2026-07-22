import json

SCENES = [
    (1, 0.0, 'Aeroporto'),
    (2, 20.0, 'Aviao'),
    (3, 31.0, 'Paris'),
    (4, 33.0, 'Roma'),
    (5, 36.0, 'Marrocos'),
    (6, 39.0, 'Dubai'),
    (7, 83.0, 'Toquio'),
    (8, 89.0, 'India'),
    (9, 94.0, 'NovaYork'),
    (10, 160.0, 'China'),
    (11, 165.0, 'Rio'),
    (12, 226.0, 'Final'),
]
SONG_END = 237.72
CLIP_DUR = 10.005
FILLER_LEN = 4.5
KENBURNS_THRESHOLD = 3.0  # below this, just hold last frame with slow zoom instead of cutting away

def build_chunks():
    chunks = []  # each: dict(kind='clip'|'stillzoom', scene, offset, length, main=bool)
    all_scene_nums = [s[0] for s in SCENES]
    for i, (num, start, label) in enumerate(SCENES):
        end = SCENES[i+1][1] if i+1 < len(SCENES) else SONG_END
        dur = round(end - start, 3)
        if dur <= CLIP_DUR:
            chunks.append(dict(kind='clip', scene=num, offset=0.0, length=dur, main=True, label=label))
        else:
            extra = dur - CLIP_DUR
            chunks.append(dict(kind='clip', scene=num, offset=0.0, length=CLIP_DUR, main=True, label=label))
            if extra < KENBURNS_THRESHOLD:
                chunks.append(dict(kind='stillzoom', scene=num, offset=CLIP_DUR, length=round(extra, 3), main=False, label=label + '-hold'))
            else:
                # filler montage using other scenes, rotating order starting after current
                remaining = round(extra, 3)
                order = all_scene_nums[i+1:] + all_scene_nums[:i+1]
                order = [n for n in order if n != num]
                oi = 0
                toggle_offset = True
                while remaining > 0.05:
                    seg_len = min(FILLER_LEN, remaining)
                    filler_scene = order[oi % len(order)]
                    oi += 1
                    off = 2.5 if toggle_offset else 0.0
                    toggle_offset = not toggle_offset
                    # keep within clip bounds
                    if off + seg_len > CLIP_DUR:
                        off = max(0.0, CLIP_DUR - seg_len)
                    chunks.append(dict(kind='clip', scene=filler_scene, offset=off, length=round(seg_len, 3), main=False, label=f'filler-of-{SCENES[filler_scene-1][2]}'))
                    remaining = round(remaining - seg_len, 3)
    return chunks

if __name__ == '__main__':
    chunks = build_chunks()
    total = sum(c['length'] for c in chunks)
    print(f'Total chunks: {len(chunks)}  total_duration={total:.3f}  song_end={SONG_END}')
    for idx, c in enumerate(chunks):
        print(f"{idx:03d} {c['kind']:9s} cena{c['scene']:02d} off={c['offset']:6.2f} len={c['length']:6.2f} {c['label']}")
    with open('chunks.json', 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2)
