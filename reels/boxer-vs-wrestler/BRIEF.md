# Рилс: «Кто победит на улице: боксёр или борец?»

Исполнитель один: **Claude Code** через Kling.
Рефы персонажей вырезаются из 3D-листа автора (`refs/_draft/storyboard_3d.*`),
чистятся и увеличиваются через Kling image-to-image.
Локация через Kling text-to-image. Потом видео и монтаж (разделы 4–8).

Claude Code: читай этот файл целиком перед работой. Все решения сверяй с ним.

---

## 1. Концепция

Формат «аргумент, контраргумент». Каждый ход одного бойца ломается ответом другого.
Зритель каждые 3–4 секунды думает «всё, этот выиграл», и тут же получает контраргумент.

- Длина: 30–40 секунд
- Формат: вертикальный 9:16, 1080×1920, 30 fps
- Плашка сверху весь ролик: **«Кто победит на улице: боксёр или борец?»**
- Озвучка: живой голос автора (файл `audio/voiceover.wav`). Не ИИ-голос.
- Финал без однозначного ответа, вопрос в комментарии.

Тон: уверенно, быстро, без мата и без жестокости. Это разбор, а не избиение.

---

## 2. Стиль и персонажи (Kling image-to-image)

**Стиль: 3D-манекены без лиц.** Как обучающие анимации техники. Гладкие фигуры, голова без глаз, носа и рта. Бойцов различают только по цвету и экипировке.

Зачем так:
- нет лиц, значит нечему «плыть» между кадрами;
- выглядит как осознанный стиль, а не дешёвая попытка в реализм;
- зритель сразу видит, где кто.

### Общий стиль (добавлять в каждый промпт)
```
stylized 3D render, faceless mannequin figure, smooth matte surface,
no eyes no nose no mouth, clean anatomy, realistic human proportions,
soft studio lighting, subtle ambient occlusion, high quality 3D,
neutral grey background, character reference sheet
```

### Боксёр (цвет: красный)
```
Faceless 3D mannequin boxer, lean athletic build, light grey matte body,
red boxing gloves, red shorts with white stripe, black boxing shoes.
Reference sheet: front view, side view, back view, fighting stance.
```

### Борец (цвет: синий)
```
Faceless 3D mannequin wrestler, stocky powerful build, thick neck,
broad shoulders, light grey matte body, blue wrestling singlet,
blue wrestling shoes.
Reference sheet: front view, side view, back view, low wrestling stance.
Stance: feet wider than shoulders and staggered, knees bent, hips low,
back straight, head up, hands forward at chest level, elbows close to body.
```

### Второй противник (кадр 8)
```
Faceless 3D mannequin, average build, dark charcoal matte body,
black hoodie, black pants. Looks like a street guy, not a fighter.
Reference sheet: front view, side view, back view.
```

Источник: 3D-лист автора `refs/_draft/storyboard_3d.*`, нижний ряд (блоки персонажей).
Вырезать каждый блок через ffmpeg, увеличить в 2 раза (lanczos), прогнать через
Kling image-to-image: та же фигура и экипировка, чистый серый фон, 2k.
Что исправить при этом:
- «Низкая стойка» борца на листе неправильная (присед, руки на коленях).
  Стойку брать из промпта выше.
- Убрать три полоски на обуви (узнаваемый бренд). Обувь без логотипов.
- Фон листа это бетонная комната. Локация отдельно, по разделу 3 (ночная улица).

Сохранить: `refs/boxer.png`, `refs/wrestler.png`, `refs/thug.png`. Разрешение 2k.
Показать автору перед следующим шагом.

---

## 3. Локация (Kling text-to-image)

Улица в том же 3D-стиле, упрощённая, без мелких деталей.
```
stylized 3D render, simplified night city street, low detail,
wet asphalt with soft reflections, a few street lamps with warm orange light,
simple block buildings in background, a closed kiosk, light fog,
clean minimal look, no people, vertical 9:16 frame
```
Сохранить: `refs/location.png`

---

## 4. Раскадровка

Каждый кадр 3–4 секунды. Камера: плавная, уровень пояса или глаз.
**Контакт удара не показываем.** Склейка на моменте удара, дальше реакция или звук.

| # | Сек | Кадр | Озвучка | Субтитры |
|---|---|---|---|---|
| 1 | 0–3 | Оба бойца стоят друг напротив друга, медленный наезд камеры | — | — |
| 2 | 3–6 | Борец делает проход в ноги | «Борец может пройти в ноги и уронить» | БОРЕЦ ПРОХОДИТ В НОГИ |
| 3 | 6–10 | Боксёр отшагивает назад, бьёт навстречу. Склейка до контакта | «Но боксёр видит проход и встречает ударом» | НО ВСТРЕЧНЫЙ УДАР |
| 4 | 10–13 | Боксёр бьёт быструю серию в воздух | «Боксёр бьёт быстрее и сильнее» | СКОРОСТЬ И СИЛА |
| 5 | 13–16 | Борец входит в клинч, прижимает боксёра к киоску | «Но в клинче удары не работают» | В КЛИНЧЕ НЕ УДАРИШЬ |
| 6 | 16–19 | Бросок, слоумо, склейка до удара о землю | «А бросок на бетон это почти нокаут» | БЕТОН, НЕ КОВЁР |
| 7 | 19–22 | Боксёр на ногах, двигается, уходит по кругу | «Но боксёра ещё надо поймать» | ЕЩЁ ПОЙМАЙ |
| 8 | 22–26 | Борец на земле, сзади подходит второй | «А на улице их часто двое. Борец на земле беззащитен» | ИХ ДВОЕ |
| 9 | 26–29 | Борец бросает и сразу встаёт на ноги | «Хороший борец бросает и остаётся стоять» | БРОСИЛ И ВСТАЛ |
| 10 | 29–33 | Оба стоят, стоп-кадр | «Один на один чаще борец. Против толпы боксёр» | 1 НА 1: БОРЕЦ / ТОЛПА: БОКСЁР |
| 11 | 33–36 | Тот же стоп-кадр, затемнение | «А ты кого выберешь?» | КОГО ВЫБЕРЕШЬ? 👇 |

---

## 5. Промпты для Kling (image-to-video)

- Персонажи через Elements (`refs/*.png`), чтобы фигуры и цвета не менялись.
- Стартовый кадр собирать из `refs/location.png` + персонажи.
- Длина клипа 5 сек, потом обрезать.
- Негативный промпт для всех:
```
face, eyes, mouth, realistic skin, photorealistic human, morphing,
extra limbs, extra fingers, melting body, color change of gloves or singlet,
blurry, text, watermark
```

Шаблон промпта:
```
[действие кадра], stylized 3D faceless mannequins, red gloves boxer,
blue singlet wrestler, simplified night street, warm street lamps,
smooth realistic motion, correct fighting technique, cinematic camera,
vertical 9:16
```

Действия по кадрам:
1. `boxer and wrestler stand facing each other 3 meters apart, tense, slow camera push-in`
2. `wrestler drops level and shoots forward for a double-leg takedown`
3. `boxer steps back and throws a straight punch forward, side camera`
4. `boxer throws fast combination of punches into the air, sharp footwork`
5. `wrestler grabs boxer in a clinch and pushes him against a closed kiosk`
6. `wrestler lifts and throws boxer, slow motion, cut before impact`
7. `boxer moves lightly on his feet, circling, staying out of reach`
8. `wrestler kneeling on the ground, a dark mannequin in a hoodie approaches from behind`
9. `wrestler finishes a throw and immediately stands up, looking around`
10. `boxer and wrestler stand side by side, facing camera, still`
11. повтор кадра 10, затемнение делать в монтаже

Брак, который выкидываем: появилось лицо, перчатки сменили цвет, тело «потекло», лишние руки.

---

## 6. Звук

- `audio/voiceover.wav`, озвучка автора. Громкость −6 dB.
- Музыка: тёмный бит без слов, `audio/music.mp3`. −20 dB под голосом.
- **Музыка обрывается** на кадре 8, возвращается на кадре 9.
- Звуки, папка `audio/sfx/`:
  - свист удара (кадры 3, 4)
  - шорох и шаг (кадры 2, 5, 7)
  - глухой удар о землю (кадр 6, сразу после склейки)
  - короткий «вуш» на каждом «Но»
  - шаги второго (кадр 8)

---

## 7. Монтаж и оформление

- Плашка сверху: белый жирный шрифт (Montserrat ExtraBold или аналог), чёрная полупрозрачная подложка, весь ролик.
- Субтитры: нижняя треть, капсом, 2–4 слова, белые с чёрной обводкой. Синхронно с голосом.
- Слово «БОКСЁР» в субтитрах красным, «БОРЕЦ» синим. Цвета совпадают с персонажами.
- Безопасная зона Инсты: ничего важного в нижних 20% и верхних 10%.
- Цвет: холодная ночь, тёплые фонари. Зерно **не добавлять**, для 3D-стиля оно лишнее.
- Переходы: только резкие склейки. Кроме финального затемнения.

---

## 8. Пайплайн для Claude Code

Структура:
```
project/
  BRIEF.md            (этот файл)
  refs/               модельки из ChatGPT
  audio/              voiceover.wav, music.mp3, sfx/
  clips/raw/          клипы из Kling
  clips/cut/          обрезанные под тайминг
  subs/subs.ass       субтитры
  out/reel.mp4        готовый ролик
```

Шаги:
0. Проверить, что Kling MCP подключён (`who_am_i`). Если нет, остановиться и сказать.
1. Сделать 4 рефа по разделам 2–3, показать автору, перегенерировать брак.
2. Загрузить персонажей в Kling как Elements.
3. Сгенерировать клипы 1–10 по разделу 5 → `clips/raw/`.
4. Показать мне все клипы. Я отбираю, брак перегенерировать.
5. Обрезать под тайминги раздела 4 через ffmpeg → `clips/cut/`.
6. Склеить, 1080×1920, 30 fps.
7. Грейдинг по разделу 7.
8. Субтитры `subs.ass` и плашка сверху.
9. Свести звук по разделу 6.
10. Экспорт `out/reel.mp4`: H.264, 1080×1920, 30 fps, AAC 192 kbps.
11. Проверка: досмотреть целиком, синхрон субтитров, безопасные зоны.

Публикацию в Инстаграм делаю сам, вручную.

---

## 9. Правила против слопа

- Не показывать контакт удара. Склейка, звук, реакция.
- Клипы короткие, 3–4 сек.
- Фигуры и цвета одинаковые во всех кадрах.
- Техника должна быть правильной: стойки, проход, бросок. Кривая техника убивает доверие знающих людей.
- Живой голос, не ИИ.
- Любой кадр с браком из раздела 5 выкидывать.
