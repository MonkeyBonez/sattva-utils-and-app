# Query Template Comparison: Emotion Wheel

**72 emotions x 4 templates = 288 queries**

## Templates Tested

| ID | Description | Example (Sad > Lonely > Isolated) |
|----|-------------|-----------------------------------|
| Current | Current – iOS app format: I feel X because I feel Y, because I feel Z. | `I feel Sad because I feel Lonely, because I feel Isolated` |
| Option_A | Option A – Bridge to solution: I feel X and Y, how do I find peace and overcome Z. | `I feel isolated and lonely, how do I find peace and overcome sad` |
| Option_B | Option B – Drop 'I feel': solution phrase only (overcome X and Y). | `overcome lonely and isolated` |
| Option_C | Option C – Category-aware: negative → overcome/cope, positive → cultivate/deepen. | `overcome lonely and isolated, cope with sad` |

---

## Category Summary: Avg Top CE Score by Template

Higher (less negative) = better match confidence.

| Category | Current | Option_A | Option_B | Option_C | Best |
|----------|------|------|------|------|------|
| **Sad** | -7.15 | -3.64 | -3.63 | -4.02 | **Option_B** |
| **Mad** | -8.04 | -5.28 | -4.09 | -5.83 | **Option_B** |
| **Scared** | -7.25 | -4.43 | -4.94 | -4.88 | **Option_A** |
| **Joyful** | -3.75 | -0.12 | -4.53 | 4.14 | **Option_C** |
| **Powerful** | -3.97 | -1.00 | -3.30 | 0.41 | **Option_C** |
| **Peaceful** | -2.95 | -0.53 | -3.34 | 3.49 | **Option_C** |
| **OVERALL** | -5.52 | -2.50 | -3.97 | -1.12 | **Option_C** |
| **NEG ONLY** | -7.48 | -4.45 | -4.22 | -4.91 | **Option_B** |

---

## Differentiation: Duplicate Top-Lesson Count per Template

Lower = more variety across emotions.

| Template | Unique Top Lessons | Duplicate Pairs |
|----------|-------------------|----------------|
| Current | 31 | 41 |
| Option_A | 13 | 59 |
| Option_B | 17 | 55 |
| Option_C | 20 | 52 |

---

## Template Agreement: Same Top Lesson

For each emotion, how often do templates pick the same #1 lesson? Rows = emotions; checkmarks = template pair agrees.

**Emotions where all 4 templates share the same top lesson:** 0 / 72

| Template A | Template B | Same top lesson (count) |
|------------|------------|--------------------------|
| Current | Option_A | 3 |
| Current | Option_B | 8 |
| Current | Option_C | 25 |
| Option_A | Option_B | 9 |
| Option_A | Option_C | 7 |
| Option_B | Option_C | 20 |

---

## Side-by-Side: All Emotions (Top CE Score per Template)

| Emotion | Current | Option_A | Option_B | Option_C | Best |
|---------|--------|--------|--------|--------|------|
| Sad > Lonely > Isolated | -5.93 | -3.82 | -5.62 | -6.01 | **Option_A** |
| Sad > Lonely > Abandoned | -5.80 | +0.27 | -3.93 | -4.34 | **Option_A** |
| Sad > Vulnerable > Fragile | -8.33 | -3.28 | -3.88 | -5.77 | **Option_A** |
| Sad > Vulnerable > Victimized | -8.22 | -4.27 | -4.27 | -4.76 | **Option_B** |
| Sad > Despair > Powerless | -8.14 | -3.82 | -5.00 | -5.11 | **Option_A** |
| Sad > Despair > Grief | -3.73 | -1.23 | +4.95 | +2.52 | **Option_B** |
| Sad > Guilty > Remorse | -7.42 | -4.52 | -4.83 | -6.27 | **Option_A** |
| Sad > Guilty > Ashamed | -8.62 | -4.52 | -6.50 | -6.93 | **Option_A** |
| Sad > Depressed > Empty | -8.38 | -5.11 | -5.28 | -6.14 | **Option_A** |
| Sad > Depressed > Inferior | -7.76 | -5.51 | -4.55 | -4.67 | **Option_B** |
| Sad > Hurt > Let down | -6.19 | -3.46 | -4.94 | +0.35 | **Option_C** |
| Sad > Hurt > Agonized | -7.27 | -4.34 | +0.33 | -1.12 | **Option_B** |
| Mad > Critical > Skeptical | -6.13 | -4.21 | -2.44 | -6.09 | **Option_B** |
| Mad > Critical > Judging | -8.00 | -4.39 | -5.33 | -6.75 | **Option_A** |
| Mad > Distant > Withdrawn | -9.38 | -5.94 | -5.25 | -7.99 | **Option_B** |
| Mad > Distant > Numb | -9.48 | -4.50 | -7.21 | -8.74 | **Option_A** |
| Mad > Frustrated > Annoyed | -7.97 | -6.17 | -3.34 | -5.08 | **Option_B** |
| Mad > Frustrated > Bitter | -9.14 | -7.25 | -5.25 | -6.33 | **Option_B** |
| Mad > Aggressive > Hostile | -7.37 | -4.59 | -3.34 | -5.34 | **Option_B** |
| Mad > Aggressive > Furious | -7.77 | -6.36 | -4.54 | -5.64 | **Option_B** |
| Mad > Hateful > Rage | -6.53 | -3.57 | +0.44 | -1.97 | **Option_B** |
| Mad > Hateful > Violated | -7.77 | -5.70 | -2.52 | -3.85 | **Option_B** |
| Mad > Hurt > Jealous | -7.95 | -5.59 | -5.21 | -6.35 | **Option_B** |
| Mad > Hurt > Bashful | -9.02 | -5.12 | -5.10 | -5.81 | **Option_B** |
| Scared > Anxious > Worried | -3.56 | -2.77 | -4.45 | -2.31 | **Option_C** |
| Scared > Anxious > Afraid | -2.68 | -2.44 | -3.18 | -1.95 | **Option_C** |
| Scared > Insecure > Inadequate | -8.01 | -5.52 | -5.53 | -6.51 | **Option_A** |
| Scared > Insecure > Inferior | -9.20 | -6.38 | -6.64 | -6.66 | **Option_A** |
| Scared > Swamped > Helpless | -7.53 | -3.52 | -6.67 | -5.80 | **Option_A** |
| Scared > Swamped > Small | -8.64 | -5.03 | -7.61 | -6.52 | **Option_A** |
| Scared > Rejected > Weak | -8.39 | -2.17 | -2.66 | -3.09 | **Option_A** |
| Scared > Rejected > Submissive | -7.24 | -1.62 | -3.64 | -3.68 | **Option_A** |
| Scared > Confused > Baffled | -9.37 | -6.37 | -4.11 | -7.74 | **Option_B** |
| Scared > Confused > Discouraged | -8.88 | -3.81 | -4.13 | -4.97 | **Option_A** |
| Scared > Embarrassed > Foolish | -7.39 | -8.16 | -4.96 | -5.04 | **Option_B** |
| Scared > Embarrassed > Shy | -6.17 | -5.38 | -5.67 | -4.33 | **Option_C** |
| Joyful > Playful > Amused | -2.86 | -0.66 | -5.36 | +3.77 | **Option_C** |
| Joyful > Playful > Spirited | -3.92 | -1.60 | -5.41 | +2.59 | **Option_C** |
| Joyful > Content > Peaceful | -2.68 | +1.45 | +0.41 | +4.87 | **Option_C** |
| Joyful > Content > Pleasant | -3.29 | +0.45 | -6.15 | +5.14 | **Option_C** |
| Joyful > Interested > Curious | -4.58 | -0.50 | -2.32 | +3.46 | **Option_C** |
| Joyful > Interested > Inquisitive | -4.14 | -0.48 | -5.03 | +4.41 | **Option_C** |
| Joyful > Proud > Achieved | -4.41 | +0.31 | -2.82 | +4.71 | **Option_C** |
| Joyful > Proud > Confident | -3.64 | +0.54 | -3.62 | +4.77 | **Option_C** |
| Joyful > Excited > Eager | -5.56 | -1.35 | -6.23 | +3.47 | **Option_C** |
| Joyful > Excited > Energetic | -3.64 | -0.59 | -6.70 | +3.74 | **Option_C** |
| Joyful > Cheerful > Delightful | -2.47 | +0.56 | -5.23 | +4.53 | **Option_C** |
| Joyful > Cheerful > Optimistic | -3.81 | +0.47 | -5.87 | +4.17 | **Option_C** |
| Powerful > Respected > Valuable | -1.13 | -1.50 | -3.57 | +0.12 | **Option_C** |
| Powerful > Respected > Valued | -0.63 | -1.77 | -3.87 | +0.36 | **Option_C** |
| Powerful > Courageous > Daring | -1.72 | -1.41 | -1.27 | +2.82 | **Option_C** |
| Powerful > Courageous > Bold | -2.99 | -1.52 | -2.87 | +2.11 | **Option_C** |
| Powerful > Proud > Achieved | -5.37 | +0.52 | -2.82 | +0.00 | **Option_A** |
| Powerful > Proud > Important | -6.17 | -1.12 | -3.78 | -1.47 | **Option_A** |
| Powerful > Creative > Ingenious | -7.17 | -1.97 | -5.91 | -2.89 | **Option_A** |
| Powerful > Creative > Versatile | -8.13 | -2.07 | -5.80 | -2.63 | **Option_A** |
| Powerful > Aware > Present | -6.82 | -1.37 | -2.81 | +2.38 | **Option_C** |
| Powerful > Aware > Focused | -1.49 | +1.88 | -1.75 | +2.79 | **Option_C** |
| Powerful > Confident > Capable | -2.77 | -1.02 | -1.53 | +0.69 | **Option_C** |
| Powerful > Confident > Secure | -3.22 | -0.61 | -3.60 | +0.59 | **Option_C** |
| Peaceful > Thankful > Grateful | -3.06 | +0.12 | -1.52 | +3.42 | **Option_C** |
| Peaceful > Thankful > Blessed | -2.64 | +0.78 | -1.80 | +3.50 | **Option_C** |
| Peaceful > Loving > Tender | -3.47 | -0.79 | -3.59 | +3.16 | **Option_C** |
| Peaceful > Loving > Empathic | -3.70 | -1.19 | -4.21 | +3.31 | **Option_C** |
| Peaceful > Trusting > Receptive | -3.75 | -1.19 | -4.76 | +4.11 | **Option_C** |
| Peaceful > Trusting > Patient | -3.86 | -1.31 | -4.30 | +3.04 | **Option_C** |
| Peaceful > Nurturing > Supportive | -2.90 | +0.72 | -4.81 | +3.66 | **Option_C** |
| Peaceful > Nurturing > Caring | -3.61 | +0.01 | -5.44 | +2.77 | **Option_C** |
| Peaceful > Serene > Calm | +0.40 | -1.98 | +1.38 | +4.84 | **Option_C** |
| Peaceful > Serene > Content | -2.69 | -1.07 | -3.95 | +3.40 | **Option_C** |
| Peaceful > Hopeful > Optimistic | -3.36 | -0.54 | -3.85 | +3.11 | **Option_C** |
| Peaceful > Hopeful > Inspired | -2.71 | +0.10 | -3.19 | +3.58 | **Option_C** |

---

## Head-to-Head: Negative Emotions (Top Lesson per Template)

Showing the #1 CE-ranked lesson for each template, for all Sad/Mad/Scared emotions.

### Sad > Lonely > Isolated

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -5.93 | `I feel Sad because I feel Lonely, because I feel Isolated` | Maintain a steady mind through solitude and self-control. |
| Option_A | -3.82 | `I feel isolated and lonely, how do I find peace and overcome` | Restrain the restless mind to find inner peace. |
| Option_B | -5.62 | `overcome lonely and isolated` | Recognize and overcome attachment to find freedom. |
| Option_C | -6.01 | `overcome lonely and isolated, cope with sad` | Cultivate calmness to overcome restlessness and longing. |

### Sad > Lonely > Abandoned

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -5.80 | `I feel Sad because I feel Lonely, because I feel Abandoned` | Abandon ego and desire to find peace. |
| Option_A | +0.27 | `I feel abandoned and lonely, how do I find peace and overcom` | Abandon ego and desire to find peace. |
| Option_B | -3.93 | `overcome lonely and abandoned` | Cultivate calmness to overcome restlessness and longing. |
| Option_C | -4.34 | `overcome lonely and abandoned, cope with sad` | Cultivate calmness to overcome restlessness and longing. |

### Sad > Vulnerable > Fragile

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -8.33 | `I feel Sad because I feel Vulnerable, because I feel Fragile` | Focus your mind and seek inner refuge. |
| Option_A | -3.28 | `I feel fragile and vulnerable, how do I find peace and overc` | Focus on the tangible to find peace. |
| Option_B | -3.88 | `overcome vulnerable and fragile` | Overcome attachment to achieve lasting peace. |
| Option_C | -5.77 | `overcome vulnerable and fragile, cope with sad` | Overcome attachment to achieve lasting peace. |

### Sad > Vulnerable > Victimized

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -8.22 | `I feel Sad because I feel Vulnerable, because I feel Victimi` | Seek joy through practice to overcome suffering. |
| Option_A | -4.27 | `I feel victimized and vulnerable, how do I find peace and ov` | Overcome attachment to achieve lasting peace. |
| Option_B | -4.27 | `overcome vulnerable and victimized` | Seek joy through practice to overcome suffering. |
| Option_C | -4.76 | `overcome vulnerable and victimized, cope with sad` | Seek joy through practice to overcome suffering. |

### Sad > Despair > Powerless

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -8.14 | `I feel Sad because I feel Despair, because I feel Powerless` | Seek joy through practice to overcome suffering. |
| Option_A | -3.82 | `I feel powerless and despair, how do I find peace and overco` | Overcome attachment to achieve lasting peace. |
| Option_B | -5.00 | `overcome despair and powerless` | Seek joy through practice to overcome suffering. |
| Option_C | -5.11 | `overcome despair and powerless, cope with sad` | Seek joy through practice to overcome suffering. |

### Sad > Despair > Grief

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -3.73 | `I feel Sad because I feel Despair, because I feel Grief` | Maintain equanimity in joy and sorrow. |
| Option_A | -1.23 | `I feel grief and despair, how do I find peace and overcome s` | Embrace the eternal nature of existence to overcome grief. |
| Option_B | +4.95 | `overcome despair and grief` | Embrace the eternal nature of existence to overcome grief. |
| Option_C | +2.52 | `overcome despair and grief, cope with sad` | Embrace the eternal nature of existence to overcome grief. |

### Sad > Guilty > Remorse

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -7.42 | `I feel Sad because I feel Guilty, because I feel Remorse` | Seek forgiveness to restore inner peace. |
| Option_A | -4.52 | `I feel remorse and guilty, how do I find peace and overcome ` | Overcome attachment to achieve lasting peace. |
| Option_B | -4.83 | `overcome guilty and remorse` | Overcome attachment to achieve lasting peace. |
| Option_C | -6.27 | `overcome guilty and remorse, cope with sad` | Overcome attachment to achieve lasting peace. |

### Sad > Guilty > Ashamed

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -8.62 | `I feel Sad because I feel Guilty, because I feel Ashamed` | Detach from qualities to transcend pleasure and pain. |
| Option_A | -4.52 | `I feel ashamed and guilty, how do I find peace and overcome ` | Overcome attachment to achieve lasting peace. |
| Option_B | -6.50 | `overcome guilty and ashamed` | Recognize and overcome desire and anger to find clarity. |
| Option_C | -6.93 | `overcome guilty and ashamed, cope with sad` | Overcome attachment to achieve lasting peace. |

### Sad > Depressed > Empty

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -8.38 | `I feel Sad because I feel Depressed, because I feel Empty` | Focus your mind and seek inner refuge. |
| Option_A | -5.11 | `I feel empty and depressed, how do I find peace and overcome` | Overcome attachment to achieve lasting peace. |
| Option_B | -5.28 | `overcome depressed and empty` | Cultivate calmness to overcome restlessness and longing. |
| Option_C | -6.14 | `overcome depressed and empty, cope with sad` | Cultivate calmness to overcome restlessness and longing. |

### Sad > Depressed > Inferior

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -7.76 | `I feel Sad because I feel Depressed, because I feel Inferior` | Cultivate humility to overcome negative emotions. |
| Option_A | -5.51 | `I feel inferior and depressed, how do I find peace and overc` | Overcome attachment to achieve lasting peace. |
| Option_B | -4.55 | `overcome depressed and inferior` | Cultivate humility to overcome negative emotions. |
| Option_C | -4.67 | `overcome depressed and inferior, cope with sad` | Cultivate humility to overcome negative emotions. |

### Sad > Hurt > Let down

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -6.19 | `I feel Sad because I feel Hurt, because I feel Let down` | Detach from qualities to transcend pleasure and pain. |
| Option_A | -3.46 | `I feel let down and hurt, how do I find peace and overcome s` | Cultivate tranquility to overcome pain. |
| Option_B | -4.94 | `overcome hurt and let down` | Recognize and overcome desire and anger as obstacles. |
| Option_C | +0.35 | `overcome hurt and let down, cope with sad` | Cultivate tranquility to overcome pain. |

### Sad > Hurt > Agonized

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -7.27 | `I feel Sad because I feel Hurt, because I feel Agonized` | Detach from qualities to transcend pleasure and pain. |
| Option_A | -4.34 | `I feel agonized and hurt, how do I find peace and overcome s` | Cultivate tranquility to overcome pain. |
| Option_B | +0.33 | `overcome hurt and agonized` | Cultivate tranquility to overcome pain. |
| Option_C | -1.12 | `overcome hurt and agonized, cope with sad` | Cultivate tranquility to overcome pain. |

### Mad > Critical > Skeptical

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -6.13 | `I feel Mad because I feel Critical, because I feel Skeptical` | Seek clarity to overcome doubt. |
| Option_A | -4.21 | `I feel skeptical and critical, how do I find peace and overc` | Focus on the tangible to find peace. |
| Option_B | -2.44 | `overcome critical and skeptical` | Seek clarity to overcome doubt. |
| Option_C | -6.09 | `overcome critical and skeptical, cope with mad` | Seek clarity to overcome doubt. |

### Mad > Critical > Judging

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -8.00 | `I feel Mad because I feel Critical, because I feel Judging` | Recognize the influence of your mental state on your actions. |
| Option_A | -4.39 | `I feel judging and critical, how do I find peace and overcom` | Focus on the tangible to find peace. |
| Option_B | -5.33 | `overcome critical and judging` | Recognize and overcome desire and anger to find clarity. |
| Option_C | -6.75 | `overcome critical and judging, cope with mad` | Recognize and overcome desire and anger to find clarity. |

### Mad > Distant > Withdrawn

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -9.38 | `I feel Mad because I feel Distant, because I feel Withdrawn` | Focus your mind and seek inner refuge. |
| Option_A | -5.94 | `I feel withdrawn and distant, how do I find peace and overco` | Overcome attachment to achieve lasting peace. |
| Option_B | -5.25 | `overcome distant and withdrawn` | Overcome obstacles by letting go of ego. |
| Option_C | -7.99 | `overcome distant and withdrawn, cope with mad` | Recognize and overcome desire and anger as obstacles. |

### Mad > Distant > Numb

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -9.48 | `I feel Mad because I feel Distant, because I feel Numb` | Focus your mind and seek inner refuge. |
| Option_A | -4.50 | `I feel numb and distant, how do I find peace and overcome ma` | Restrain the restless mind to find inner peace. |
| Option_B | -7.21 | `overcome distant and numb` | Overcome attachment to achieve lasting peace. |
| Option_C | -8.74 | `overcome distant and numb, cope with mad` | Recognize and overcome desire and anger as obstacles. |

### Mad > Frustrated > Annoyed

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -7.97 | `I feel Mad because I feel Frustrated, because I feel Annoyed` | Recognize and overcome desire and anger as obstacles. |
| Option_A | -6.17 | `I feel annoyed and frustrated, how do I find peace and overc` | Recognize and overcome desire and anger to find clarity. |
| Option_B | -3.34 | `overcome frustrated and annoyed` | Recognize and overcome desire and anger as obstacles. |
| Option_C | -5.08 | `overcome frustrated and annoyed, cope with mad` | Recognize and overcome desire and anger as obstacles. |

### Mad > Frustrated > Bitter

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -9.14 | `I feel Mad because I feel Frustrated, because I feel Bitter` | Resist the sway of desire and anger. |
| Option_A | -7.25 | `I feel bitter and frustrated, how do I find peace and overco` | Recognize and overcome desire and anger to find clarity. |
| Option_B | -5.25 | `overcome frustrated and bitter` | Recognize and overcome desire and anger as obstacles. |
| Option_C | -6.33 | `overcome frustrated and bitter, cope with mad` | Recognize and overcome desire and anger as obstacles. |

### Mad > Aggressive > Hostile

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -7.37 | `I feel Mad because I feel Aggressive, because I feel Hostile` | Recognize and overcome desire and anger as obstacles. |
| Option_A | -4.59 | `I feel hostile and aggressive, how do I find peace and overc` | Restrain the restless mind to find inner peace. |
| Option_B | -3.34 | `overcome aggressive and hostile` | Recognize and overcome desire and anger as obstacles. |
| Option_C | -5.34 | `overcome aggressive and hostile, cope with mad` | Recognize and overcome desire and anger as obstacles. |

### Mad > Aggressive > Furious

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -7.77 | `I feel Mad because I feel Aggressive, because I feel Furious` | Recognize the influence of your mental state on your actions. |
| Option_A | -6.36 | `I feel furious and aggressive, how do I find peace and overc` | Recognize and overcome desire and anger to find clarity. |
| Option_B | -4.54 | `overcome aggressive and furious` | Recognize and overcome desire and anger as obstacles. |
| Option_C | -5.64 | `overcome aggressive and furious, cope with mad` | Recognize and overcome desire and anger as obstacles. |

### Mad > Hateful > Rage

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -6.53 | `I feel Mad because I feel Hateful, because I feel Rage` | Recognize and overcome desire and anger as obstacles. |
| Option_A | -3.57 | `I feel rage and hateful, how do I find peace and overcome ma` | Recognize and overcome desire and anger to find clarity. |
| Option_B | +0.44 | `overcome hateful and rage` | Recognize and overcome desire and anger as obstacles. |
| Option_C | -1.97 | `overcome hateful and rage, cope with mad` | Recognize and overcome desire and anger as obstacles. |

### Mad > Hateful > Violated

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -7.77 | `I feel Mad because I feel Hateful, because I feel Violated` | Resist the sway of desire and anger. |
| Option_A | -5.70 | `I feel violated and hateful, how do I find peace and overcom` | Recognize and overcome desire and anger to find clarity. |
| Option_B | -2.52 | `overcome hateful and violated` | Recognize and overcome desire and anger as obstacles. |
| Option_C | -3.85 | `overcome hateful and violated, cope with mad` | Recognize and overcome desire and anger as obstacles. |

### Mad > Hurt > Jealous

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -7.95 | `I feel Mad because I feel Hurt, because I feel Jealous` | Detach from qualities to transcend pleasure and pain. |
| Option_A | -5.59 | `I feel jealous and hurt, how do I find peace and overcome ma` | Overcome attachment to achieve lasting peace. |
| Option_B | -5.21 | `overcome hurt and jealous` | Recognize and overcome desire and anger as obstacles. |
| Option_C | -6.35 | `overcome hurt and jealous, cope with mad` | Recognize and overcome desire and anger as obstacles. |

### Mad > Hurt > Bashful

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -9.02 | `I feel Mad because I feel Hurt, because I feel Bashful` | Resist the sway of desire and anger. |
| Option_A | -5.12 | `I feel bashful and hurt, how do I find peace and overcome ma` | Overcome attachment to achieve lasting peace. |
| Option_B | -5.10 | `overcome hurt and bashful` | Seek joy through practice to overcome suffering. |
| Option_C | -5.81 | `overcome hurt and bashful, cope with mad` | Recognize and overcome desire and anger as obstacles. |

### Scared > Anxious > Worried

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -3.56 | `I feel Scared because I feel Anxious, because I feel Worried` | Act with courage in the face of fear. |
| Option_A | -2.77 | `I feel worried and anxious, how do I find peace and overcome` | Restrain the restless mind to find inner peace. |
| Option_B | -4.45 | `overcome anxious and worried` | Recognize and overcome desire and anger as obstacles. |
| Option_C | -2.31 | `overcome anxious and worried, cope with scared` | Act with courage in the face of fear. |

### Scared > Anxious > Afraid

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -2.68 | `I feel Scared because I feel Anxious, because I feel Afraid` | Act with courage in the face of fear. |
| Option_A | -2.44 | `I feel afraid and anxious, how do I find peace and overcome ` | Restrain the restless mind to find inner peace. |
| Option_B | -3.18 | `overcome anxious and afraid` | Recognize and overcome desire and anger as obstacles. |
| Option_C | -1.95 | `overcome anxious and afraid, cope with scared` | Act with courage in the face of fear. |

### Scared > Insecure > Inadequate

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -8.01 | `I feel Scared because I feel Insecure, because I feel Inadeq` | Focus your mind and seek inner refuge. |
| Option_A | -5.52 | `I feel inadequate and insecure, how do I find peace and over` | Rise above desires to find inner peace. |
| Option_B | -5.53 | `overcome insecure and inadequate` | Recognize and overcome desire and anger as obstacles. |
| Option_C | -6.51 | `overcome insecure and inadequate, cope with scared` | Recognize and overcome desire and anger as obstacles. |

### Scared > Insecure > Inferior

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -9.20 | `I feel Scared because I feel Insecure, because I feel Inferi` | Focus your mind and seek inner refuge. |
| Option_A | -6.38 | `I feel inferior and insecure, how do I find peace and overco` | Rise above desires to find inner peace. |
| Option_B | -6.64 | `overcome insecure and inferior` | Cultivate humility to overcome delusion and ego. |
| Option_C | -6.66 | `overcome insecure and inferior, cope with scared` | Recognize and overcome desire and anger as obstacles. |

### Scared > Swamped > Helpless

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -7.53 | `I feel Scared because I feel Swamped, because I feel Helples` | Act with courage in the face of fear. |
| Option_A | -3.52 | `I feel helpless and swamped, how do I find peace and overcom` | Recognize and overcome attachment to find freedom. |
| Option_B | -6.67 | `overcome swamped and helpless` | Recognize and overcome attachment to find freedom. |
| Option_C | -5.80 | `overcome swamped and helpless, cope with scared` | Act with courage in the face of fear. |

### Scared > Swamped > Small

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -8.64 | `I feel Scared because I feel Swamped, because I feel Small` | Focus your mind and seek inner refuge. |
| Option_A | -5.03 | `I feel small and swamped, how do I find peace and overcome s` | Recognize and overcome attachment to find freedom. |
| Option_B | -7.61 | `overcome swamped and small` | Recognize and overcome attachment to find freedom. |
| Option_C | -6.52 | `overcome swamped and small, cope with scared` | Act with courage in the face of fear. |

### Scared > Rejected > Weak

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -8.39 | `I feel Scared because I feel Rejected, because I feel Weak` | Recognize and overcome desire and anger as obstacles. |
| Option_A | -2.17 | `I feel weak and rejected, how do I find peace and overcome s` | Abandon ego and desire to find peace. |
| Option_B | -2.66 | `overcome rejected and weak` | Overcome obstacles by letting go of ego. |
| Option_C | -3.09 | `overcome rejected and weak, cope with scared` | Act with courage in the face of fear. |

### Scared > Rejected > Submissive

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -7.24 | `I feel Scared because I feel Rejected, because I feel Submis` | Act without attachment or desire for reward. |
| Option_A | -1.62 | `I feel submissive and rejected, how do I find peace and over` | Abandon ego and desire to find peace. |
| Option_B | -3.64 | `overcome rejected and submissive` | Recognize and overcome desire and anger as obstacles. |
| Option_C | -3.68 | `overcome rejected and submissive, cope with scared` | Act with courage in the face of fear. |

### Scared > Confused > Baffled

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -9.37 | `I feel Scared because I feel Confused, because I feel Baffle` | Control your senses to gain wisdom and clarity. |
| Option_A | -6.37 | `I feel baffled and confused, how do I find peace and overcom` | Let go of attachment to find inner peace. |
| Option_B | -4.11 | `overcome confused and baffled` | Overcome ignorance to free yourself from delusion. |
| Option_C | -7.74 | `overcome confused and baffled, cope with scared` | Recognize and overcome desire and anger as obstacles. |

### Scared > Confused > Discouraged

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -8.88 | `I feel Scared because I feel Confused, because I feel Discou` | Seek guidance to clarify your duty. |
| Option_A | -3.81 | `I feel discouraged and confused, how do I find peace and ove` | Restrain the restless mind to find inner peace. |
| Option_B | -4.13 | `overcome confused and discouraged` | Recognize and overcome desire and anger as obstacles. |
| Option_C | -4.97 | `overcome confused and discouraged, cope with scared` | Recognize and overcome desire and anger as obstacles. |

### Scared > Embarrassed > Foolish

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -7.39 | `I feel Scared because I feel Embarrassed, because I feel Foo` | Seek knowledge to overcome ignorance and heedlessness. |
| Option_A | -8.16 | `I feel foolish and embarrassed, how do I find peace and over` | Seek knowledge to overcome ignorance and heedlessness. |
| Option_B | -4.96 | `overcome embarrassed and foolish` | Seek knowledge to overcome ignorance and heedlessness. |
| Option_C | -5.04 | `overcome embarrassed and foolish, cope with scared` | Act with courage in the face of fear. |

### Scared > Embarrassed > Shy

| Template | CE Score | Query | Top Lesson |
|----------|---------|-------|------------|
| Current | -6.17 | `I feel Scared because I feel Embarrassed, because I feel Shy` | Act with courage in the face of fear. |
| Option_A | -5.38 | `I feel shy and embarrassed, how do I find peace and overcome` | Overcome attachment to achieve lasting peace. |
| Option_B | -5.67 | `overcome embarrassed and shy` | Recognize and overcome desire and anger as obstacles. |
| Option_C | -4.33 | `overcome embarrassed and shy, cope with scared` | Act with courage in the face of fear. |

---

## Recommendation

Compare the avg CE scores above to decide which template to ship.
Key questions:
1. Which template has the best **negative emotion** scores (Sad/Mad/Scared)?
2. Does the winning template hurt positive emotion scores?
3. Does the winning template produce more differentiated (unique) top lessons?
4. Do the actual top lessons for negative emotions feel more relevant?
