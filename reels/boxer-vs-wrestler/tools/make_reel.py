#!/usr/bin/env python3
"""Сборка рилса «Боксёр vs борец» по BRIEF.md (шаги 5-11 раздела 8).

  python3 tools/make_reel.py stills  # stills/NNx.png -> clips/raw/NN.mp4 (позы, наезд, тряска)
  python3 tools/make_reel.py cut     # clips/raw/NN.* -> clips/cut/NN.mp4
  python3 tools/make_reel.py build   # склейка, грейдинг, субтитры, звук -> out/reel.mp4
  python3 tools/make_reel.py check   # контакт-лист кадров с безопасными зонами -> out/check.png
  python3 tools/make_reel.py all     # cut + build + check

Запускать из любой папки. --root указывает на папку проекта (по умолчанию родитель tools/).
"""
import argparse
import glob
import os
import subprocess
import sys

W, H, FPS = 1080, 1920, 30

# Раздел 4: (кадр, длительность в сек, точка входа в сыром клипе, скорость).
# Точку входа подобрать после отбора клипов. speed < 1 замедляет.
TIMELINE = [
    (1, 3.0, 0.0, 1.0),
    (2, 3.0, 0.0, 1.0),
    (3, 4.0, 0.0, 1.0),
    (4, 3.0, 0.0, 1.0),
    (5, 3.0, 0.0, 1.0),
    (6, 3.0, 0.0, 1.0),
    (7, 3.0, 0.0, 1.0),
    (8, 4.0, 0.0, 1.0),
    (9, 3.0, 0.0, 1.0),
    (10, 4.0, 0.0, 1.0),
]
FREEZE_DUR = 3.0  # кадр 11: стоп-кадр из конца кадра 10
TOTAL = sum(t[1] for t in TIMELINE) + FREEZE_DUR  # 36 сек
FADE_START, FADE_DUR = 33.3, 2.2

# Раздел 6. Голос -6 dB, музыка -20 dB, пауза музыки на кадре 8.
VOICE_DB = -6
MUSIC_DB = -20
MUSIC_MUTE = (22.0, 26.0)

# Раздел 6, звуки: (время, файл в audio/sfx/, громкость dB). Подогнать под голос.
SFX = [
    (3.1, "step.wav", -10),        # кадр 2: шорох, проход
    (6.0, "whoosh.wav", -8),       # «Но»
    (7.3, "punch_swish.wav", -6),  # кадр 3: свист удара, склейка до контакта
    (10.3, "punch_swish.wav", -8), # кадр 4: серия
    (10.8, "punch_swish.wav", -8),
    (11.2, "punch_swish.wav", -8),
    (13.0, "whoosh.wav", -8),      # «Но»
    (13.4, "step.wav", -10),       # кадр 5: клинч
    (18.7, "thud.wav", -3),        # кадр 6: глухой удар сразу после склейки
    (19.0, "whoosh.wav", -8),      # «Но»
    (19.5, "step.wav", -12),       # кадр 7
    (22.3, "footsteps.wav", -8),   # кадр 8: шаги второго
]

# Раздел 7: холодная ночь, тёплые фонари. Без зерна.
GRADE = ("colorbalance=rs=-0.04:gs=-0.01:bs=0.06:rm=-0.02:bm=0.03:"
         "rh=0.05:gh=0.02:bh=-0.04,eq=contrast=1.06:saturation=1.08")

# Режим stills: кадр собирается из поз stills/NNa.png, NNb.png ... по порядку.
# (наезд за позу, тряска в px на склейке поз). Остальные кадры: STILL_FX_DEFAULT.
STILL_FX_DEFAULT = (0.06, 14)
STILL_FX = {
    1: (0.10, 0),   # медленный наезд
    6: (0.12, 0),   # слоумо, без тряски
    7: (0.05, 0),
    10: (0.04, 0),  # стоп-кадр
}

CONFORM = (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
           f"crop={W}:{H},fps={FPS},setsar=1,format=yuv420p")


def run(cmd):
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def ff(*args):
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args])


def find_raw(root, n):
    hits = sorted(glob.glob(os.path.join(root, "clips", "raw", f"{n:02d}.*")))
    if not hits:
        sys.exit(f"Нет clips/raw/{n:02d}.mp4. Сначала сгенерировать и отобрать клип {n}.")
    return hits[0]


def pose_clip(src, dur, zoom, shake, out):
    """Одна поза: фон из размытой копии, если не 9:16, плавный наезд, затухающая тряска."""
    w2, h2 = W * 2, H * 2  # zoompan на увеличенной картинке, чтобы наезд не дёргался
    zw, zh = int(W * 1.1) // 2 * 2, int(H * 1.1) // 2 * 2
    n = int(round(dur * FPS))
    vf = (f"split[a][b];"
          f"[a]scale={w2}:{h2}:force_original_aspect_ratio=increase,crop={w2}:{h2},"
          f"boxblur=40:2,eq=brightness=-0.12[bg];"
          f"[b]scale={w2}:{h2}:force_original_aspect_ratio=decrease[fg];"
          f"[bg][fg]overlay=(W-w)/2:(H-h)/2,"
          f"zoompan=z='1+{zoom}*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':"
          f"d=1:s={zw}x{zh}:fps={FPS},"
          f"crop={W}:{H}:x='(iw-ow)/2+{shake}*sin(t*70)*exp(-t*12)':"
          f"y='(ih-oh)/2+{shake}*cos(t*55)*exp(-t*12)',setsar=1,format=yuv420p")
    ff("-loop", "1", "-framerate", str(FPS), "-i", src, "-filter_complex", vf,
       "-frames:v", str(n), "-c:v", "libx264", "-preset", "fast", "-crf", "14", out)


def stills(root, stills_dir):
    raw_dir = os.path.join(root, "clips", "raw")
    tmp = os.path.join(root, "clips", "poses")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(tmp, exist_ok=True)
    for n, dur, _, _ in TIMELINE:
        poses = sorted(glob.glob(os.path.join(stills_dir, f"{n:02d}[a-z].*")))
        if not poses:
            print(f"! нет {stills_dir}/{n:02d}a.png, кадр {n} пропускаю")
            continue
        zoom, shake = STILL_FX.get(n, STILL_FX_DEFAULT)
        parts = []
        for i, src in enumerate(poses):
            out = os.path.join(tmp, f"{n:02d}_{i}.mp4")
            # первая поза кадра без тряски: склейка между кадрами и так резкая
            pose_clip(src, dur / len(poses), zoom, shake if i else 0, out)
            parts.append(out)
        lst = os.path.join(tmp, f"{n:02d}.txt")
        with open(lst, "w") as f:
            f.writelines(f"file '{os.path.abspath(p)}'\n" for p in parts)
        ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
           os.path.join(raw_dir, f"{n:02d}.mp4"))


def cut(root):
    out_dir = os.path.join(root, "clips", "cut")
    os.makedirs(out_dir, exist_ok=True)
    for n, dur, start, speed in TIMELINE:
        src = find_raw(root, n)
        vf = CONFORM if speed == 1.0 else f"setpts=PTS/{speed},{CONFORM}"
        ff("-ss", str(start), "-t", str(dur * speed), "-i", src, "-vf", vf,
           "-t", str(dur), "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "14",
           os.path.join(out_dir, f"{n:02d}.mp4"))
    # Кадр 11: последний кадр кадра 10, растянутый в стоп-кадр.
    last = os.path.join(out_dir, "10_last.png")
    ff("-sseof", "-0.1", "-i", os.path.join(out_dir, "10.mp4"), "-frames:v", "1", "-update", "1", last)
    ff("-loop", "1", "-framerate", str(FPS), "-t", str(FREEZE_DUR), "-i", last,
       "-vf", CONFORM, "-c:v", "libx264", "-preset", "fast", "-crf", "14",
       os.path.join(out_dir, "11.mp4"))


def audio_graph(root, first_input):
    """Возвращает (входы ffmpeg, filter_complex для звука, метка выхода)."""
    a = os.path.join(root, "audio")
    inputs, chains, labels = [], [], []
    idx = first_input

    voice = os.path.join(a, "voiceover.wav")
    if os.path.exists(voice):
        inputs += ["-i", voice]
        chains.append(f"[{idx}:a]volume={VOICE_DB}dB,aresample=48000[vo]")
        labels.append("[vo]")
        idx += 1
    else:
        print("! нет audio/voiceover.wav, собираю без голоса")

    music = os.path.join(a, "music.mp3")
    if os.path.exists(music):
        inputs += ["-stream_loop", "-1", "-i", music]
        m0, m1 = MUSIC_MUTE
        chains.append(
            f"[{idx}:a]atrim=0:{TOTAL},aresample=48000,volume={MUSIC_DB}dB,"
            f"volume='if(between(t,{m0},{m1}),0,1)':eval=frame,"
            f"afade=t=out:st={FADE_START}:d={TOTAL - FADE_START}[mu]")
        labels.append("[mu]")
        idx += 1
    else:
        print("! нет audio/music.mp3, собираю без музыки")

    for i, (t, name, db) in enumerate(SFX):
        path = os.path.join(a, "sfx", name)
        if not os.path.exists(path):
            print(f"! нет audio/sfx/{name}, пропускаю звук на {t} с")
            continue
        inputs += ["-i", path]
        ms = int(t * 1000)
        chains.append(f"[{idx}:a]aresample=48000,volume={db}dB,adelay={ms}:all=1[s{i}]")
        labels.append(f"[s{i}]")
        idx += 1

    if not labels:
        inputs += ["-f", "lavfi", "-t", str(TOTAL), "-i", "anullsrc=r=48000:cl=stereo"]
        chains.append(f"[{idx}:a]anull[aout]")
        return inputs, ";".join(chains), "[aout]"

    chains.append(
        f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,"
        f"atrim=0:{TOTAL},alimiter=limit=0.95,"
        f"aformat=sample_rates=48000:channel_layouts=stereo[aout]")
    return inputs, ";".join(chains), "[aout]"


def build(root):
    cut_dir = os.path.join(root, "clips", "cut")
    parts = [os.path.join(cut_dir, f"{n:02d}.mp4") for n in range(1, 12)]
    missing = [p for p in parts if not os.path.exists(p)]
    if missing:
        sys.exit("Нет обрезанных клипов, сначала cut: " + ", ".join(missing))
    os.makedirs(os.path.join(root, "out"), exist_ok=True)
    concat_list = os.path.join(cut_dir, "concat.txt")
    with open(concat_list, "w") as f:
        f.writelines(f"file '{os.path.abspath(p)}'\n" for p in parts)

    a_inputs, a_graph, a_out = audio_graph(root, first_input=1)
    v_graph = (f"[0:v]{GRADE},fade=t=out:st={FADE_START}:d={FADE_DUR},"
               f"subtitles=subs/subs.ass:fontsdir=fonts,format=yuv420p[vout]")
    os.chdir(root)  # пути subtitles/fontsdir относительные, без экранирования
    ff("-f", "concat", "-safe", "0", "-i", concat_list, *a_inputs,
       "-filter_complex", f"{v_graph};{a_graph}",
       "-map", "[vout]", "-map", a_out, "-t", str(TOTAL),
       "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "18",
       "-r", str(FPS), "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
       "-movflags", "+faststart", "out/reel.mp4")


def check(root):
    """Кадр из середины каждого сегмента + линии безопасных зон (верх 10%, низ 20%)."""
    reel = os.path.join(root, "out", "reel.mp4")
    times, t = [], 0.0
    for _, dur, _, _ in TIMELINE:
        times.append(t + dur / 2)
        t += dur
    times.append(t + 0.5)
    sel = "+".join(f"between(t,{x:.2f},{x + 1 / FPS:.3f})" for x in times)
    zones = (f"drawbox=y={int(H * 0.10)}:w=iw:h=6:color=yellow@0.9:t=fill,"
             f"drawbox=y={int(H * 0.80)}:w=iw:h=6:color=yellow@0.9:t=fill")
    ff("-i", reel, "-vf",
       f"select='{sel}',{zones},scale=270:-1,tile=6x2:padding=8:color=white",
       "-frames:v", "1", "-update", "1", os.path.join(root, "out", "check.png"))
    run(["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_name,width,height,r_frame_rate,bit_rate",
         "-of", "compact", reel])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("step", choices=["stills", "cut", "build", "check", "all"])
    p.add_argument("--stills", help="папка с позами для шага stills (по умолчанию <root>/stills)")
    p.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = p.parse_args()
    root = os.path.abspath(args.root)
    if args.step == "stills":
        stills(root, os.path.abspath(args.stills or os.path.join(root, "stills")))
    if args.step in ("cut", "all"):
        cut(root)
    if args.step in ("build", "all"):
        build(root)
    if args.step in ("check", "all"):
        check(root)


if __name__ == "__main__":
    main()
