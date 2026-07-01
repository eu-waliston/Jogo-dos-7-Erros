"""
Musica de fundo sintetizada em tempo real (sem arquivo externo).
Usa numpy + pygame.sndarray para gerar uma melodia chiptune em loop.
Se numpy nao estiver disponivel, desabilita silenciosamente.
"""
import pygame
import threading

_playing = False
_muted = False
_volume = 0.18
_thread = None
_stop_event = threading.Event()

def _generate_tone(freq, duration_ms, sample_rate=22050, wave="square"):
    try:
        import numpy as np
        n = int(sample_rate * duration_ms / 1000)
        t = np.linspace(0, duration_ms / 1000, n, endpoint=False)
        if wave == "square":
            raw = np.sign(np.sin(2 * np.pi * freq * t))
        elif wave == "triangle":
            raw = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
        else:
            raw = np.sin(2 * np.pi * freq * t)
        # envelope ADSR simples
        env = np.ones(n)
        att = min(int(0.02 * sample_rate), n)
        rel = min(int(0.08 * sample_rate), n)
        env[:att] = np.linspace(0, 1, att)
        env[n - rel:] = np.linspace(1, 0, rel)
        raw = (raw * env * 32767 * _volume).astype(np.int16)
        stereo = np.column_stack([raw, raw])
        return pygame.sndarray.make_sound(stereo)
    except Exception:
        return None

# Sequencia: (freq_hz, duracao_ms)
_MELODY = [
    (392, 200), (440, 200), (523, 200), (440, 200),
    (392, 200), (349, 200), (392, 400),
    (440, 200), (523, 200), (587, 200), (523, 200),
    (440, 200), (392, 200), (349, 400),
    (0,   300),
]

def _music_loop():
    global _playing
    sample_rate = 22050
    try:
        pygame.mixer.init(frequency=sample_rate, size=-16, channels=2, buffer=512)
    except Exception:
        return
    cache = {}
    while not _stop_event.is_set():
        for freq, dur in _MELODY:
            if _stop_event.is_set():
                break
            if _muted or freq == 0:
                pygame.time.wait(dur)
                continue
            key = (freq, dur)
            if key not in cache:
                cache[key] = _generate_tone(freq, dur, sample_rate)
            snd = cache[key]
            if snd:
                snd.play()
            pygame.time.wait(dur)

def start():
    global _thread, _playing
    if _playing:
        return
    _stop_event.clear()
    _playing = True
    _thread = threading.Thread(target=_music_loop, daemon=True)
    _thread.start()

def stop():
    global _playing
    _playing = False
    _stop_event.set()

def toggle_mute():
    global _muted
    _muted = not _muted
    return _muted

def set_volume(v):
    global _volume
    _volume = max(0.0, min(1.0, v))
