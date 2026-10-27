# Кадры в Gemini (бесплатный путь)

Видео не генерируем. Каждый кадр раскадровки собираем из 1–3 статичных поз.
Движение (наезды, тряска, склейки) делает `tools/make_reel.py`.

## Как генерировать

1. Один чат в Gemini на все кадры. Так персонажи меньше «плывут».
2. Первым сообщением прикрепи `refs/_draft/storyboard_3d.png` и вставь блок «Старт».
3. Дальше по одному промпту из списка. Каждый начинается с `Same characters and style.`
4. Если персонаж поменялся, напиши: `Keep characters exactly as in the reference sheet` и повтори промпт.
5. Брак выкидываем: появилось лицо, логотипы или полоски на обуви, лишние руки,
   цвета перепутались, неправильная техника.

## Куда класть

GitHub → `reels/boxer-vs-wrestler/stills/` → Add file → Upload files.
Имена: `01a.png`, `02a.png`, `02b.png` … как в списке ниже.
Через чат тоже можно, но картинки там сжимаются.

## Старт (первое сообщение, с картинкой)

```
Use the attached sheet as the character reference. Three characters, keep them identical in every image:
BOXER: faceless 3D mannequin, lean athletic build, light grey matte body, red boxing gloves, red shorts with white side stripe, plain black boxing shoes.
WRESTLER: faceless 3D mannequin, stocky powerful build, thick neck, broad shoulders, light grey matte body, blue wrestling singlet, plain blue wrestling shoes.
STREET GUY: faceless 3D mannequin, average build, dark charcoal body, black hoodie with hood up, black pants, plain dark sneakers.
Style for every image: stylized 3D render, faceless mannequins, smooth matte surface, no eyes no nose no mouth, realistic proportions, correct fighting technique.
Location for every image: simplified night city street, wet asphalt with soft reflections, a few street lamps with warm orange light, simple block buildings, a closed kiosk, light fog, cold blue night with warm lamp light. NOT a concrete room.
Shoes: plain, no logos, no stripes.
Frame: vertical 9:16. Characters in the middle of the frame. Keep the top 10% and bottom 25% free of important details (text will go there). Camera at waist or eye level.
No text, no watermark.
Reply "ok" and wait for my prompts.
```

## Список кадров

| Файл | Промпт |
|---|---|
| `00_bg.png` | `Same style. The empty street location only, no people, vertical 9:16.` |
| `01a.png` | `Same characters and style. Boxer (left) and wrestler (right) stand facing each other 3 meters apart, side view, tense. Boxer in boxing stance, gloves up. Wrestler in low wrestling stance: feet wider than shoulders and staggered, knees bent, hips low, back straight, head up, hands forward at chest level, elbows close to body.` |
| `02a.png` | `Same characters and style. Wrestler drops his level: deep penetration step, lead knee almost touching the asphalt, head up, hands reaching for the boxer's legs. Boxer still standing, gloves up. Side view.` |
| `02b.png` | `Same characters and style. Double-leg takedown: wrestler's head on the side of the boxer's chest, arms wrapped around both of boxer's thighs, driving forward. Boxer off balance. Side view.` |
| `03a.png` | `Same characters and style. Wrestler starts shooting in low. Boxer steps back with his rear foot, eyes on the wrestler, gloves up. Side view.` |
| `03b.png` | `Same characters and style. Boxer throws a straight right punch at the incoming wrestler's head. The glove is 20 cm from the head, no contact yet. Side view, dynamic.` |
| `04a.png` | `Same characters and style. Boxer alone, throws a sharp jab into the air, fully extended arm, rear glove guarding the chin. 3/4 view. Wrestler blurred in the background.` |
| `04b.png` | `Same, but a straight right cross: hips and rear foot rotated, arm fully extended.` |
| `04c.png` | `Same, but a left hook: elbow at shoulder height, arm bent at 90 degrees, body rotated.` |
| `05a.png` | `Same characters and style. Wrestler ties up the boxer in a tight clinch: underhooks, head on the boxer's chest, chest to chest. 3/4 view.` |
| `05b.png` | `Same characters and style. Wrestler pins the boxer against the closed kiosk shutter in a clinch. Boxer's arms are trapped, he cannot punch. 3/4 view.` |
| `06a.png` | `Same characters and style. Wrestler lifts the boxer off the ground from a body lock, hips under the boxer, boxer's feet in the air. Side view, motion blur.` |
| `06b.png` | `Same characters and style. Mid-air throw: boxer upside down above the asphalt, wrestler arching back. Boxer has NOT touched the ground yet. Low camera, motion blur.` |
| `07a.png` | `Same characters and style. Boxer moves lightly on the balls of his feet, side-stepping out of reach, gloves up. Wrestler in the background reaching for him and missing. 3/4 view.` |
| `07b.png` | `Same, different moment: boxer pivoting away in a circle, wrestler further from him.` |
| `08a.png` | `Same characters and style. Wrestler on his hands and knees on the wet asphalt, head down. Street guy in the black hoodie walks toward him from behind in the background, under a street lamp.` |
| `08b.png` | `Same, the street guy is now close, standing right behind the wrestler, fists clenched. Low camera from the ground.` |
| `09a.png` | `Same characters and style. Wrestler finishes a hip throw: the boxer lands on his back on the asphalt, the wrestler stays on his feet, knees bent. Side view.` |
| `09b.png` | `Same characters and style. Wrestler stands upright over the boxer lying on the ground, looking around, ready. 3/4 view.` |
| `10a.png` | `Same characters and style. Boxer (left) and wrestler (right) stand side by side, facing the camera, still, neutral pose. Full body, eye-level camera.` |

Итого 20 картинок. Если лимит Gemini на сегодня кончится, доделаем завтра.
Минимум, чтобы собрать черновик: `00_bg`, `01a`, `02b`, `03b`, `04b`, `05b`, `06b`, `07a`, `08a`, `09b`, `10a`.
