# Рилс «Боксёр vs борец»

ТЗ: `BRIEF.md`. Монтаж: `tools/make_reel.py` (нужен только ffmpeg и python3).

```
python3 tools/make_reel.py all   # cut + build + check
```

- Клипы класть в `clips/raw/01.mp4 … 10.mp4` (после отбора).
- Точки входа и скорость клипов: `TIMELINE` в `tools/make_reel.py`.
- Тайминги звуков: `SFX` там же. Ожидаемые файлы: `audio/sfx/step.wav, whoosh.wav, punch_swish.wav, thud.wav, footsteps.wav`.
- Субтитры и плашка: `subs/subs.ass`. После записи голоса подогнать тайминги.
- Результат: `out/reel.mp4`, контакт-лист с безопасными зонами: `out/check.png`.

`clips/`, `audio/`, `out/` не коммитятся (репозиторий публикуется на GitHub Pages).
`refs/_draft/` это вырезки из 2D-раскадровки, не финальные рефы (см. BRIEF.md, раздел 2).
