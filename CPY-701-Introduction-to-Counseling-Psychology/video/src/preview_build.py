#!/usr/bin/env python3
"""
CPY 701 - builds preview/data.js for the Weeks-in-review player.

Narrated weeks (audio present) get real cue timings from their SRT and real
slide-boundary times from the measured narration chunks. Weeks whose narrated
MP4 was already delivered and is not in this sandbox get caption-synced slide
playback with estimated timing (~15.2 chars/sec, the measured series average).
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_video import caption_sentences, probe, ffmpeg_exe  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
DIST = os.path.join(ROOT, 'dist')
RATE = 15.2  # chars per second, measured series average


def load(week):
    man = json.load(open(os.path.join(DIST, 'slides', week, 'manifest.json')))
    return man


def srt_cues(path):
    cues = []
    for b in open(path).read().strip().split('\n\n'):
        ln = b.split('\n')
        if len(ln) < 3:
            continue
        a, e = ln[1].split(' --> ')
        def sec(t):
            t = t.strip().replace(',', '.')
            h, m, s = t.split(':')
            return int(h) * 3600 + int(m) * 60 + float(s)
        cues.append({'s': round(sec(a), 2), 'e': round(sec(e), 2), 't': ' '.join(ln[2:])})
    return cues


def week_entry(week, num, title, narrated):
    man = load(week)
    slides = man['slides']
    chars = {s['i']: max(1, len(s['narration'])) for s in slides}
    entry = {'id': week, 'num': num, 'title': title, 'slides': [], 'cues': []}
    if narrated:
        plan = json.load(open(os.path.join(DIST, 'audio', week, 'plan.json')))
        chunks = sorted(f for f in os.listdir(os.path.join(DIST, 'audio', week))
                        if re.match(r'chunk-\d\d\.mp3$', f))
        durs = [probe(os.path.join(DIST, 'audio', week, f)) for f in chunks]
        starts, t = {}, 0.0
        for f, d in zip(chunks, durs):
            ch = next(c for c in plan['chunks'] if f == f"chunk-{c['chunk']:02d}.mp3")
            tot = sum(chars[i] for i in ch['slides'])
            for i in ch['slides']:
                starts[i] = t
                t += d * chars[i] / tot
        entry['mode'] = 'narrated'
        entry['duration'] = round(t, 2)
        entry['video'] = f'/dist/CPY701-{week.upper()}-lecture.mp4'
        entry['vtt'] = f'/dist/{week}-captions.vtt'
        entry['cues'] = srt_cues(os.path.join(DIST, f'{week}-captions.srt'))
    else:
        starts, t = {}, 0.0
        for s in slides:
            starts[s['i']] = t
            t += chars[s['i']] / RATE
        entry['mode'] = 'captions'
        entry['duration'] = round(t, 2)
        for s in slides:
            a, b = starts[s['i']], starts[s['i']] + chars[s['i']] / RATE
            sentences = caption_sentences(s['narration'])
            tot = sum(len(x) for x in sentences) or 1
            ct = a
            for x in sentences:
                d = (b - a) * len(x) / tot
                entry['cues'].append({'s': round(ct, 2), 'e': round(ct + d, 2), 't': x})
                ct += d
    for s in slides:
        end = starts[s['i'] + 1] if s['i'] + 1 in starts else entry['duration']
        entry['slides'].append({'file': f"/dist/slides/{week}/{s['file']}",
                                'title': s.get('title') or s.get('slug'),
                                'start': round(starts[s['i']], 2), 'end': round(end, 2)})
    return entry


def main():
    titles = {
        'w01': (1, 'The Nature and Concept of Counseling Psychology'),
        'w02': (2, 'Historical and Philosophical Development'),
        'w03': (3, 'Relationship to Other Disciplines and Helping Professions'),
        'w04': (4, 'Theoretical Orientations I: Psychodynamic, Humanistic and Existential'),
        'w05': (5, 'Theoretical Orientations II: CBT, Constructivist, Systemic and Third-Wave'),
        'w06': (6, 'The Counseling Process and Core Microskills'),
        'w07': (7, 'The Counseling Relationship, Diversity and Multicultural Counseling'),
        'w08': (8, 'Mid-Semester Assessment and Consolidation Seminar'),
        'w09': (9, 'Assessment, Diagnosis and Case Formulation'),
        'w10': (10, 'Prevention, Development and Psychoeducation'),
        'w11': (11, 'Counseling Across Specialization Settings and Populations'),
        'w12': (12, 'Group, Family and Crisis/Emergency Counseling'),
        'w13': (13, 'Ethics, Law and Professional Regulation'),
        'w14': (14, 'Research, Evidence-Based Practice and Technology'),
        'w15': (15, 'The Counselor as Person and Professional'),
        'w16': (16, 'Integration, Revision and Course Examination'),
    }
    weeks = []
    for wid in sorted(titles, key=lambda k: int(k[1:])):
        deck = os.path.join(DIST, 'slides', wid, 'manifest.json')
        if not os.path.exists(deck):
            continue
        num, title = titles[wid]
        narrated = os.path.exists(os.path.join(DIST, f'CPY701-{wid.upper()}-lecture.mp4'))
        weeks.append((wid, num, title, narrated))
    data = {'course': 'CPY 701 · Introduction to Counseling Psychology',
            'programme': "Master's Degree in Counseling Psychology",
            'weeks': [week_entry(*w) for w in weeks]}
    out = os.path.join(ROOT, 'preview', 'data.js')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write('window.CPY701 = ' + json.dumps(data) + ';\n')
    print('wrote', out, '| weeks:', [(w['id'], w['mode'], w['duration']) for w in data['weeks']])


if __name__ == '__main__':
    main()
