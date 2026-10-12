"""
tts.py — Offline neural text-to-speech for the CAC Masters lecture series.

Engine : Piper (VITS, ONNX) — voice `en_US-joe-medium`, the voice of "Prof. Williams".
Runtime: onnxruntime (CPU), no network access required at synthesis time.

Exposes:
    PiperVoice   -> low-level engine (text -> 16-bit PCM bytes)
    speak()      -> text -> .wav file
    normalise()  -> legal/academic text normalisation so numerals, treaty
                    citations, chemical formulae and abbreviations are spoken
                    correctly rather than mangled by the phonemiser.

Copyright: Triune Biblical University Global Extension, USA.
"""

from __future__ import annotations

import json
import os
import re
import wave
from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np
import onnxruntime as ort

from piper_phonemize import phonemize_espeak

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

DEFAULT_MODEL = os.path.join(
    ROOT, "voices", "piper", "joe_us_piper_voice", "data", "en_US-joe-medium.onnx"
)

BOS = "^"
EOS = "$"
PAD = "_"


# --------------------------------------------------------------------------
# Text normalisation
# --------------------------------------------------------------------------

_ONES = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

_ORDINALS = {
    "1st": "first", "2nd": "second", "3rd": "third", "4th": "fourth",
    "5th": "fifth", "6th": "sixth", "7th": "seventh", "8th": "eighth",
    "9th": "ninth", "10th": "tenth", "11th": "eleventh", "12th": "twelfth",
    "13th": "thirteenth", "14th": "fourteenth", "15th": "fifteenth",
    "16th": "sixteenth", "17th": "seventeenth", "18th": "eighteenth",
    "19th": "nineteenth", "20th": "twentieth", "21st": "twenty-first",
    "22nd": "twenty-second", "23rd": "twenty-third", "24th": "twenty-fourth",
    "25th": "twenty-fifth",
}

# Abbreviations the phonemiser would otherwise spell out letter-by-letter.
_ABBREV = [
    (r"\bUNCLOS\b", "U N C L O S"),
    (r"\bUNFCCC\b", "U N F C C C"),
    (r"\bECT\b", "E C T"),
    (r"\bICSID\b", "I C S I D"),
    (r"\bOPEC\b", "OPEC"),
    (r"\bIEA\b", "I E A"),
    (r"\bGDP\b", "G D P"),
    (r"\bGDPs\b", "G D P s"),
    (r"\bFDI\b", "F D I"),
    (r"\bLNG\b", "L N G"),
    (r"\bPSA\b", "P S A"),
    (r"\bPSCs\b", "P S Cs"),
    (r"\bIOCs\b", "I O Cs"),
    (r"\bIOC\b", "I O C"),
    (r"\bNOC\b", "N O C"),
    (r"\bNOCs\b", "N O Cs"),
    (r"\bBITs\b", "B I Ts"),
    (r"\bBIT\b", "B I T"),
    (r"\bIIA\b", "I I A"),
    (r"\bIIAs\b", "I I As"),
    (r"\bUNCITRAL\b", "U N C I T R A L"),
    (r"\bIAEA\b", "I A E A"),
    (r"\bOECD\b", "O E C D"),
    (r"\bEITI\b", "E I T I"),
    (r"\bCSR\b", "C S R"),
    (r"\bSDG\s?7\b", "S D G seven"),
    (r"\bSDGs\b", "S D Gs"),
    (r"\bNDCs\b", "N D Cs"),
    (r"\bNDC\b", "N D C"),
    (r"\bIPCC\b", "I P C C"),
    (r"\bCOP\b", "C O P"),
    (r"\bOAU\b", "O A U"),
    (r"\bAU\b", "African Union"),
    (r"\bEU\b", "E U"),
    (r"\bUK\b", "U K"),
    (r"\bUS\b", "United States"),
    (r"\bUSA\b", "United States of America"),
    (r"\bUK\s", "U K "),
    (r"\bIP\b", "I P"),
    (r"\bTWh\b", "terawatt hours"),
    (r"\bGWh\b", "gigawatt hours"),
    (r"\bGW\b", "gigawatts"),
    (r"\bMW\b", "megawatts"),
    (r"\bkWh\b", "kilowatt hours"),
    (r"\bkW\b", "kilowatts"),
    (r"\bmb/d\b", "million barrels per day"),
    (r"\bbcm\b", "billion cubic metres"),
    (r"\bmboe\b", "million barrels of oil equivalent"),
    (r"\bMtCO2\b", "million tonnes of C O two"),
    (r"\bCO2\b", "C O two"),
    (r"\bCH4\b", "C H four"),
    (r"\bN2O\b", "N two O"),
    (r"\bvs\.", "versus"),
    (r"\be\.g\.", "for example"),
    (r"\bi\.e\.", "that is"),
    (r"\betc\.", "et cetera"),
    (r"\bcf\.", "compare"),
    (r"\bNo\.\s?(\d+)", lambda m: "number " + _num_words(m.group(1))),
    (r"\bpara\.", "paragraph"),
    (r"\bArt\.?\s?(\d+)", lambda m: "Article " + _num_words(m.group(1))),
    (r"\bss?\.\s?(\d+)", lambda m: "section " + _num_words(m.group(1))),
    (r"\bv\.\s", " versus "),
    (r"&", " and "),
    (r"§+\s?(\d+)", lambda m: "section " + _num_words(m.group(1))),
]


def _under_thousand(n: int) -> str:
    if n < 20:
        return _ONES[n]
    if n < 100:
        t, o = divmod(n, 10)
        return _TENS[t] + ((" " + _ONES[o]) if o else "")
    h, rem = divmod(n, 100)
    out = _ONES[h] + " hundred"
    if rem:
        out += " and " + _under_thousand(rem)
    return out


def _num_words(digits: str) -> str:
    """Spell a number as English words (tolerates a decimal point)."""
    digits = (digits or "0").strip()
    if "." in digits:
        whole, frac = digits.split(".", 1)
        return (_num_words(whole or "0") + " point "
                + " ".join(_ONES[int(c)] for c in frac if c.isdigit()))
    digits = digits.lstrip("0") or "0"
    n = int(digits)
    if n == 0:
        return "zero"
    if n < 0:
        return "minus " + _num_words(str(-n))
    if n < 1000:
        return _under_thousand(n)
    if n < 1_000_000:
        th, rem = divmod(n, 1000)
        out = _under_thousand(th) + " thousand"
        if rem:
            out += " " + _under_thousand(rem) if rem < 100 else " " + _under_thousand(rem)
        return out
    if n < 1_000_000_000:
        m, rem = divmod(n, 1_000_000)
        out = _under_thousand(m) + " million"
        if rem:
            out += " " + _num_words(str(rem))
        return out
    b, rem = divmod(n, 1_000_000_000)
    out = _under_thousand(b) + " billion"
    if rem:
        out += " " + _num_words(str(rem))
    return out


def _year(tok: str) -> str:
    """1945 -> nineteen forty-five; 1900s -> nineteen hundreds."""
    n = int(tok)
    if 1000 <= n <= 1999:
        h, rem = divmod(n, 100)
        head = _under_thousand(h)
        if rem == 0:
            return head + " hundred"
        if rem < 10:
            return f"{head} O {_ONES[rem]}"
        return head + " " + _under_thousand(rem)
    if 2000 <= n <= 2099:
        rem = n - 2000
        if rem == 0:
            return "two thousand"
        if rem < 10:
            return "two thousand and " + _ONES[rem]
        return "two thousand " + _under_thousand(rem)
    return _num_words(tok)


_TENS_IES = {0: "hundreds", 10: "tens", 20: "twenties", 30: "thirties",
             40: "forties", 50: "fifties", 60: "sixties", 70: "seventies",
             80: "eighties", 90: "nineties"}


def _decade(tok: str) -> str:
    """1990 -> 'nineteen nineties'; 2010 -> 'twenty tens'."""
    n = int(tok)
    if 1900 <= n <= 1999:
        head, rem = "nineteen", n - 1900
    elif 2000 <= n <= 2099:
        head, rem = "twenty", n - 2000
    elif 1800 <= n <= 1899:
        head, rem = "eighteen", n - 1800
    else:
        return _year(tok) + "s"
    if rem == 0 and head != "twenty":
        return head + " hundreds"
    if rem == 0:
        return "two thousands"
    return head + " " + _TENS_IES.get(rem, _TENS[rem // 10] + "s")


_DECIMAL = re.compile(r"(?<![\w.])(\d+)\.(\d+)(?!\d)")
_YEAR = re.compile(r"(?<![\d.])(\d{4})(?!\d)")
_DECADE = re.compile(r"(?<![\d.])(\d{4})s\b")
_INT = re.compile(r"(?<![\w.$])(\d{1,12})(?![\w.])")
_ORD = re.compile(r"\b(\d{1,2})(st|nd|rd|th)\b", re.I)


def normalise(text: str) -> str:
    """Prepare academic/legal prose for the phonemiser."""
    t = text
    t = t.replace("\u2019", "'").replace("\u2018", "'")
    t = t.replace("\u201c", '"').replace("\u201d", '"')
    t = t.replace("\u2014", " — ").replace("\u2013", " - ")
    t = re.sub(r"[ \t]+", " ", t)

    for pat, rep in _ABBREV:
        t = re.sub(pat, rep, t)

    # percentages, currencies
    t = re.sub(r"(\d+(?:\.\d+)?)\s?%", lambda m: _num_words(m.group(1)) + " per cent", t)
    t = re.sub(r"\$\s?(\d+(?:\.\d+)?)\s?(billion|million|trillion)?",
               lambda m: _num_words(m.group(1)) + (" " + m.group(2) if m.group(2) else "")
                         + " dollars", t)

    # ordinals
    t = _ORD.sub(lambda m: _ORDINALS.get(m.group(0).lower(),
                                         _num_words(m.group(1)) + "th"), t)

    # decades (before plain years)
    t = _DECADE.sub(lambda m: _decade(m.group(1)), t)
    # years
    t = _YEAR.sub(lambda m: _year(m.group(1)), t)
    # decimals
    t = _DECIMAL.sub(lambda m: _num_words(m.group(1)) + " point "
                               + " ".join(_ONES[int(c)] for c in m.group(2)), t)
    # remaining integers
    t = _INT.sub(lambda m: _num_words(m.group(1)), t)

    t = re.sub(r"\s+", " ", t).strip()
    return t


# --------------------------------------------------------------------------
# Engine
# --------------------------------------------------------------------------


@dataclass
class PiperVoice:
    model_path: str = DEFAULT_MODEL
    length_scale: float = 1.18      # >1 = slower, more deliberate delivery
    noise_scale: float = 0.667
    noise_w: float = 0.8
    sentence_silence: float = 0.45  # seconds of breath between sentences
    use_cuda: bool = False

    _sess: Optional[ort.InferenceSession] = field(default=None, repr=False)
    _cfg: dict = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        providers = (["CUDAExecutionProvider", "CPUExecutionProvider"]
                     if self.use_cuda else ["CPUExecutionProvider"])
        so = ort.SessionOptions()
        so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        so.intra_op_num_threads = max(1, (os.cpu_count() or 2))
        self._sess = ort.InferenceSession(self.model_path, sess_options=so,
                                          providers=providers)
        self._cfg = json.load(open(self.model_path + ".json", encoding="utf-8"))

    @property
    def sample_rate(self) -> int:
        return int(self._cfg["audio"]["sample_rate"])

    def phonemes_to_ids(self, phonemes: List[str]) -> List[int]:
        id_map = self._cfg["phoneme_id_map"]
        ids = list(id_map[BOS])
        for p in phonemes:
            if p in id_map:
                ids.extend(id_map[p])
                ids.extend(id_map[PAD])
        ids.extend(id_map[EOS])
        return ids

    def synth_ids(self, ids: List[int], length_scale: Optional[float] = None,
                  noise_scale: Optional[float] = None,
                  noise_w: Optional[float] = None) -> np.ndarray:
        ls = self.length_scale if length_scale is None else length_scale
        ns = self.noise_scale if noise_scale is None else noise_scale
        nw = self.noise_w if noise_w is None else noise_w

        arr = np.expand_dims(np.array(ids, dtype=np.int64), 0)
        lengths = np.array([arr.shape[1]], dtype=np.int64)
        scales = np.array([ns, ls, nw], dtype=np.float32)
        sid = None
        if self._cfg.get("num_speakers", 1) > 1:
            sid = np.array([0], dtype=np.int64)
        feeds = {"input": arr, "input_lengths": lengths, "scales": scales}
        input_names = {i.name for i in self._sess.get_inputs()}
        if "sid" in input_names and sid is not None:
            feeds["sid"] = sid
        audio = self._sess.run(None, feeds)[0]
        return np.asarray(audio, dtype=np.float32).reshape(-1)

    def speak(self, text: str, length_scale: Optional[float] = None,
              sentence_silence: Optional[float] = None) -> np.ndarray:
        """Return float32 mono audio in [-1, 1] for `text`."""
        text = normalise(text or "")
        if not text.strip():
            return np.zeros(0, dtype=np.float32)
        ss = self.sentence_silence if sentence_silence is None else sentence_silence
        chunks = []
        silence = np.zeros(int(ss * self.sample_rate), dtype=np.float32)
        for sentence in phonemize_espeak(text, self._cfg["espeak"]["voice"]):
            ids = self.phonemes_to_ids(sentence)
            if len(ids) <= 2:
                continue
            chunks.append(self.synth_ids(ids, length_scale=length_scale))
            chunks.append(silence)
        if not chunks:
            return np.zeros(0, dtype=np.float32)
        return np.concatenate(chunks)


    def sentences(self, text: str) -> List[List[str]]:
        """Phonemised sentences — the unit on which timing is calibrated."""
        return phonemize_espeak(normalise(text or ""), self._cfg["espeak"]["voice"])

    def speak_sentence(self, sentence: List[str],
                       length_scale: Optional[float] = None) -> np.ndarray:
        """Audio for one phonemised sentence, with no added silence."""
        ids = self.phonemes_to_ids(sentence)
        if len(ids) <= 2:
            return np.zeros(0, dtype=np.float32)
        return self.synth_ids(ids, length_scale=length_scale)


def write_wav(path: str, audio: np.ndarray, sample_rate: int) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    pcm = np.clip(audio, -1.0, 1.0)
    pcm = (pcm * 32767.0).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(pcm.tobytes())
    return path


def speak(text: str, out_path: str, **kw) -> float:
    """Synthesise `text` to `out_path` (.wav). Returns duration in seconds."""
    v = _VOICE_CACHE.get()
    audio = v.speak(text, **kw)
    write_wav(out_path, audio, v.sample_rate)
    return len(audio) / float(v.sample_rate)


class _VoiceCache:
    """One ONNX session per process — model load is expensive."""
    _v: Optional[PiperVoice] = None

    def get(self) -> PiperVoice:
        if self._v is None:
            self._v = PiperVoice()
        return self._v


_VOICE_CACHE = _VoiceCache()


if __name__ == "__main__":
    import argparse
    import time

    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--out", default="/tmp/tts_test.wav")
    ap.add_argument("--length-scale", type=float, default=None)
    ap.add_argument("--sentence-silence", type=float, default=None)
    a = ap.parse_args()

    t0 = time.time()
    dur = speak(a.text, a.out, length_scale=a.length_scale,
                sentence_silence=a.sentence_silence)
    el = time.time() - t0
    words = len(a.text.split())
    print(f"wrote {a.out}")
    print(f"chars={len(a.text)} words={words} audio={dur:.2f}s "
          f"rtf={el/max(dur,0.01):.3f} wpm={words/(dur/60):.1f}")
