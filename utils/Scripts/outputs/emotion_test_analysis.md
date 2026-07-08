# Emotion Wheel → Lesson Search: Test Results

**Config:** E5 top-10 retrieval → CE rerank top-5

**Models:** `intfloat/e5-small-v2` (retrieval) + `cross-encoder/ms-marco-MiniLM-L-6-v2` (rerank)

**Corpus:** 396 lesson texts

---

## Category Summary

| Category | Avg Top Cosine | Avg Top CE | Min CE | Max CE | Count |
|----------|---------------|-----------|--------|--------|-------|
| Sad | 0.8110 | -7.1481 | -8.6185 | -3.7258 | 12 |
| Mad | 0.8157 | -8.0443 | -9.4771 | -6.1342 | 12 |
| Scared | 0.8005 | -7.2540 | -9.3705 | -2.6772 | 12 |
| Joyful | 0.8275 | -3.7490 | -5.5592 | -2.4654 | 12 |
| Powerful | 0.8376 | -3.9669 | -8.1269 | -0.6332 | 12 |
| Peaceful | 0.8454 | -2.9458 | -3.8622 | 0.3993 | 12 |

---

## Per-Emotion Results

### SAD

#### Sad > Lonely > Isolated
**Query:** `I feel Sad because I feel Lonely, because I feel Isolated`

**Top cosine:** 0.8049  |  **Top CE:** -5.9267

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -5.9267 | 0.8013 | Maintain a steady mind through solitude and self-control. | 6:10-10 |
| 2 | -7.8495 | 0.8049 | Focus your mind and seek inner refuge. | 7:1-1 |
| 3 | -8.4354 | 0.7972 | Let go of attachment to find inner peace. | 5:12-12, 5:11-18, 6:4-4, 13:9-17, 15:3-3 |
| 4 | -8.5625 | 0.8015 | Cultivate devotion through solitude and self-reflection. | 13:11-11 |
| 5 | -8.9898 | 0.7991 | Let go of longing to find true fulfillment. | 2:59-59 |

#### Sad > Lonely > Abandoned
**Query:** `I feel Sad because I feel Lonely, because I feel Abandoned`

**Top cosine:** 0.828  |  **Top CE:** -5.7986

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -5.7986 | 0.8105 | Abandon ego and desire to find peace. | 18:53-53, 18:53-56 |
| 2 | -7.4076 | 0.8086 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |
| 3 | -7.8421 | 0.8030 | Focus your mind and seek inner refuge. | 7:1-1 |
| 4 | -8.0820 | 0.8041 | Let go of attachment to find inner peace. | 5:12-12, 5:11-18, 6:4-4, 13:9-17, 15:3-3 |
| 5 | -8.4896 | 0.8280 | Let go of longing to find true fulfillment. | 2:59-59 |

#### Sad > Vulnerable > Fragile
**Query:** `I feel Sad because I feel Vulnerable, because I feel Fragile`

**Top cosine:** 0.8083  |  **Top CE:** -8.3347

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -8.3347 | 0.8083 | Focus your mind and seek inner refuge. | 7:1-1 |
| 2 | -8.5029 | 0.7926 | Let go of attachment to find inner peace. | 5:12-12, 5:11-18, 6:4-4, 13:9-17, 15:3-3 |
| 3 | -9.1722 | 0.7938 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |
| 4 | -9.1787 | 0.7918 | Let go of longing to find true fulfillment. | 2:59-59 |
| 5 | -9.4486 | 0.7951 | Act with clarity and free yourself from attachment. | 3:30-30, 3:28-34 |

#### Sad > Vulnerable > Victimized
**Query:** `I feel Sad because I feel Vulnerable, because I feel Victimized`

**Top cosine:** 0.8099  |  **Top CE:** -8.2183

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -8.2183 | 0.7954 | Seek joy through practice to overcome suffering. | 18:36-36 |
| 2 | -8.5547 | 0.8099 | Focus your mind and seek inner refuge. | 7:1-1 |
| 3 | -8.5564 | 0.7983 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |
| 4 | -8.8169 | 0.7994 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 5 | -9.4126 | 0.7941 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |

#### Sad > Despair > Powerless
**Query:** `I feel Sad because I feel Despair, because I feel Powerless`

**Top cosine:** 0.7996  |  **Top CE:** -8.1359

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -8.1359 | 0.7920 | Seek joy through practice to overcome suffering. | 18:36-36 |
| 2 | -8.1827 | 0.7989 | Control your mind and senses to achieve liberation. | 5:28-28 |
| 3 | -8.2518 | 0.7982 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |
| 4 | -8.3112 | 0.7996 | Focus your mind and seek inner refuge. | 7:1-1 |
| 5 | -8.9614 | 0.7930 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |

#### Sad > Despair > Grief
**Query:** `I feel Sad because I feel Despair, because I feel Grief`

**Top cosine:** 0.8131  |  **Top CE:** -3.7258

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.7258 | 0.8131 | Maintain equanimity in joy and sorrow. | 5:20-20 |
| 2 | -5.4891 | 0.8040 | Cultivate serenity to transcend grief and desire. | 18:54-54 |
| 3 | -7.3680 | 0.8034 | Seek joy through practice to overcome suffering. | 18:36-36 |
| 4 | -8.2578 | 0.8043 | Let go of longing to find true fulfillment. | 2:59-59 |
| 5 | -8.4635 | 0.8011 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |

#### Sad > Guilty > Remorse
**Query:** `I feel Sad because I feel Guilty, because I feel Remorse`

**Top cosine:** 0.8105  |  **Top CE:** -7.4191

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -7.4191 | 0.8105 | Seek forgiveness to restore inner peace. | 11:44-44, 11:44-51 |
| 2 | -8.0655 | 0.8036 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 3 | -8.2721 | 0.8007 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |
| 4 | -8.2802 | 0.8011 | Focus your mind and seek inner refuge. | 7:1-1 |
| 5 | -8.9950 | 0.7993 | Control your mind and senses to achieve liberation. | 5:28-28 |

#### Sad > Guilty > Ashamed
**Query:** `I feel Sad because I feel Guilty, because I feel Ashamed`

**Top cosine:** 0.8022  |  **Top CE:** -8.6185

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -8.6185 | 0.8022 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |
| 2 | -8.8248 | 0.7981 | Focus your mind and seek inner refuge. | 7:1-1 |
| 3 | -8.8867 | 0.8011 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |
| 4 | -9.2189 | 0.7978 | Let go of longing to find true fulfillment. | 2:59-59 |
| 5 | -9.5341 | 0.7960 | Control your mind and senses to achieve liberation. | 5:28-28 |

#### Sad > Depressed > Empty
**Query:** `I feel Sad because I feel Depressed, because I feel Empty`

**Top cosine:** 0.8156  |  **Top CE:** -8.3795

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -8.3795 | 0.8031 | Focus your mind and seek inner refuge. | 7:1-1 |
| 2 | -8.6299 | 0.8001 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |
| 3 | -8.8225 | 0.8156 | Let go of longing to find true fulfillment. | 2:59-59 |
| 4 | -9.1032 | 0.7986 | Cultivate calmness to overcome restlessness and longing. | 14:12-12, 14:12-15 |
| 5 | -9.3625 | 0.7987 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |

#### Sad > Depressed > Inferior
**Query:** `I feel Sad because I feel Depressed, because I feel Inferior`

**Top cosine:** 0.8053  |  **Top CE:** -7.763

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -7.7630 | 0.7881 | Cultivate humility to overcome negative emotions. | 16:18-18 |
| 2 | -7.8326 | 0.7906 | Cultivate firmness to overcome negative emotions. | 18:35-35 |
| 3 | -9.1543 | 0.8053 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |
| 4 | -9.4044 | 0.7940 | Focus your mind and seek inner refuge. | 7:1-1 |
| 5 | -9.8942 | 0.7913 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |

#### Sad > Hurt > Let down
**Query:** `I feel Sad because I feel Hurt, because I feel Let down`

**Top cosine:** 0.8326  |  **Top CE:** -6.1871

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -6.1871 | 0.8195 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |
| 2 | -7.4622 | 0.8101 | Let go of attachment to find inner peace. | 5:12-12, 5:11-18, 6:4-4, 13:9-17, 15:3-3 |
| 3 | -8.2428 | 0.8326 | Let go of longing to find true fulfillment. | 2:59-59 |
| 4 | -8.9385 | 0.7956 | Focus your mind and seek inner refuge. | 7:1-1 |
| 5 | -9.4689 | 0.7987 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |

#### Sad > Hurt > Agonized
**Query:** `I feel Sad because I feel Hurt, because I feel Agonized`

**Top cosine:** 0.8021  |  **Top CE:** -7.2702

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -7.2702 | 0.8021 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |
| 2 | -9.4456 | 0.7947 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 3 | -9.4609 | 0.7857 | Seek joy through practice to overcome suffering. | 18:36-36 |
| 4 | -9.7901 | 0.7856 | Find happiness within by controlling desires and anger. | 5:21-21, 5:21-28 |
| 5 | -9.8122 | 0.7932 | Focus your mind and seek inner refuge. | 7:1-1 |

### MAD

#### Mad > Critical > Skeptical
**Query:** `I feel Mad because I feel Critical, because I feel Skeptical`

**Top cosine:** 0.8208  |  **Top CE:** -6.1342

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -6.1342 | 0.8208 | Seek clarity to overcome doubt. | 6:39-39 |
| 2 | -9.2582 | 0.7928 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 3 | -9.3620 | 0.7975 | Seek clarity to avoid the traps of delusion. | 16:16-16 |
| 4 | -9.6672 | 0.7968 | Seek self-awareness to perceive deeper truths. | 15:11-11 |
| 5 | -10.0453 | 0.7965 | Seek guidance to clarify your duty. | 2:7-7 |

#### Mad > Critical > Judging
**Query:** `I feel Mad because I feel Critical, because I feel Judging`

**Top cosine:** 0.8114  |  **Top CE:** -8.003

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -8.0030 | 0.8041 | Recognize the influence of your mental state on your actions. | 14:6-6, 14:6-9 |
| 2 | -8.4869 | 0.7999 | Your character reflects your beliefs. | 17:3-3 |
| 3 | -8.6027 | 0.8114 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 4 | -9.2222 | 0.7971 | Understand the nature of your actions. | 4:17-17 |
| 5 | -9.7954 | 0.7999 | Seek guidance to clarify your duty. | 2:7-7 |

#### Mad > Distant > Withdrawn
**Query:** `I feel Mad because I feel Distant, because I feel Withdrawn`

**Top cosine:** 0.819  |  **Top CE:** -9.3828

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -9.3828 | 0.8153 | Focus your mind and seek inner refuge. | 7:1-1 |
| 2 | -9.7044 | 0.8098 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 3 | -9.8966 | 0.8109 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |
| 4 | -9.9247 | 0.8190 | Let go of longing to find true fulfillment. | 2:59-59 |
| 5 | -10.1164 | 0.8128 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |

#### Mad > Distant > Numb
**Query:** `I feel Mad because I feel Distant, because I feel Numb`

**Top cosine:** 0.8086  |  **Top CE:** -9.4771

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -9.4771 | 0.8053 | Focus your mind and seek inner refuge. | 7:1-1 |
| 2 | -9.6552 | 0.8045 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |
| 3 | -10.0012 | 0.8051 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 4 | -10.0222 | 0.8086 | Resist the sway of desire and anger. | 3:34-34, 3:36-37 |
| 5 | -10.4113 | 0.8065 | Cultivate calmness to overcome restlessness and longing. | 14:12-12, 14:12-15 |

#### Mad > Frustrated > Annoyed
**Query:** `I feel Mad because I feel Frustrated, because I feel Annoyed`

**Top cosine:** 0.809  |  **Top CE:** -7.9716

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -7.9716 | 0.8064 | Recognize and overcome desire and anger as obstacles. | 3:37-37 |
| 2 | -8.3003 | 0.8090 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 3 | -8.3178 | 0.8084 | Resist the sway of desire and anger. | 3:34-34, 3:36-37 |
| 4 | -8.8971 | 0.7957 | Find happiness within by controlling desires and anger. | 5:21-21, 5:21-28 |
| 5 | -9.5825 | 0.7936 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |

#### Mad > Frustrated > Bitter
**Query:** `I feel Mad because I feel Frustrated, because I feel Bitter`

**Top cosine:** 0.8133  |  **Top CE:** -9.1394

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -9.1394 | 0.8051 | Resist the sway of desire and anger. | 3:34-34, 3:36-37 |
| 2 | -9.2317 | 0.8039 | Recognize and overcome desire and anger as obstacles. | 3:37-37 |
| 3 | -9.4133 | 0.8133 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 4 | -10.1460 | 0.8058 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |
| 5 | -10.1632 | 0.7987 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |

#### Mad > Aggressive > Hostile
**Query:** `I feel Mad because I feel Aggressive, because I feel Hostile`

**Top cosine:** 0.8209  |  **Top CE:** -7.3741

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -7.3741 | 0.8149 | Recognize and overcome desire and anger as obstacles. | 3:37-37 |
| 2 | -7.5177 | 0.8209 | Resist the sway of desire and anger. | 3:34-34, 3:36-37 |
| 3 | -7.9220 | 0.8169 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 4 | -8.8238 | 0.8020 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |
| 5 | -8.9683 | 0.8131 | Find happiness within by controlling desires and anger. | 5:21-21, 5:21-28 |

#### Mad > Aggressive > Furious
**Query:** `I feel Mad because I feel Aggressive, because I feel Furious`

**Top cosine:** 0.8246  |  **Top CE:** -7.7665

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -7.7665 | 0.7945 | Recognize the influence of your mental state on your actions. | 14:6-6, 14:6-9 |
| 2 | -8.1830 | 0.8150 | Recognize and overcome desire and anger as obstacles. | 3:37-37 |
| 3 | -8.2339 | 0.8246 | Resist the sway of desire and anger. | 3:34-34, 3:36-37 |
| 4 | -8.3821 | 0.8236 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 5 | -9.0198 | 0.8216 | Find happiness within by controlling desires and anger. | 5:21-21, 5:21-28 |

#### Mad > Hateful > Rage
**Query:** `I feel Mad because I feel Hateful, because I feel Rage`

**Top cosine:** 0.8227  |  **Top CE:** -6.5317

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -6.5317 | 0.8145 | Recognize and overcome desire and anger as obstacles. | 3:37-37 |
| 2 | -6.5888 | 0.8222 | Resist the sway of desire and anger. | 3:34-34, 3:36-37 |
| 3 | -7.0493 | 0.8227 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 4 | -7.7853 | 0.8104 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |
| 5 | -8.1694 | 0.8218 | Find happiness within by controlling desires and anger. | 5:21-21, 5:21-28 |

#### Mad > Hateful > Violated
**Query:** `I feel Mad because I feel Hateful, because I feel Violated`

**Top cosine:** 0.8162  |  **Top CE:** -7.7729

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -7.7729 | 0.8162 | Resist the sway of desire and anger. | 3:34-34, 3:36-37 |
| 2 | -8.0323 | 0.8107 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 3 | -8.9636 | 0.8111 | Find happiness within by controlling desires and anger. | 5:21-21, 5:21-28 |
| 4 | -9.0611 | 0.8089 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |
| 5 | -9.9890 | 0.7996 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |

#### Mad > Hurt > Jealous
**Query:** `I feel Mad because I feel Hurt, because I feel Jealous`

**Top cosine:** 0.8069  |  **Top CE:** -7.9533

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -7.9533 | 0.8069 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |
| 2 | -8.9102 | 0.8003 | Resist the sway of desire and anger. | 3:34-34, 3:36-37 |
| 3 | -9.3192 | 0.7975 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 4 | -9.4217 | 0.8009 | Find happiness within by controlling desires and anger. | 5:21-21, 5:21-28 |
| 5 | -9.8439 | 0.8048 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |

#### Mad > Hurt > Bashful
**Query:** `I feel Mad because I feel Hurt, because I feel Bashful`

**Top cosine:** 0.8151  |  **Top CE:** -9.0246

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -9.0246 | 0.8078 | Resist the sway of desire and anger. | 3:34-34, 3:36-37 |
| 2 | -9.1888 | 0.8058 | Recognize and overcome desire and anger as obstacles. | 3:37-37 |
| 3 | -9.3517 | 0.8151 | Recognize and overcome desire and anger to find clarity. | 3:37-37, 3:37-40 |
| 4 | -9.9048 | 0.8058 | Find happiness within by controlling desires and anger. | 5:21-21, 5:21-28 |
| 5 | -10.0505 | 0.8075 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |

### SCARED

#### Scared > Anxious > Worried
**Query:** `I feel Scared because I feel Anxious, because I feel Worried`

**Top cosine:** 0.7923  |  **Top CE:** -3.5641

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.5641 | 0.7918 | Act with courage in the face of fear. | 11:34-34 |
| 2 | -7.2780 | 0.7824 | Recognize the influence of your mental state on your actions. | 14:6-6, 14:6-9 |
| 3 | -7.7414 | 0.7923 | Focus your mind and seek inner refuge. | 7:1-1 |
| 4 | -8.7365 | 0.7807 | Cultivate calmness to overcome restlessness and longing. | 14:12-12, 14:12-15 |
| 5 | -8.7714 | 0.7894 | Control your mind and senses to achieve liberation. | 5:28-28 |

#### Scared > Anxious > Afraid
**Query:** `I feel Scared because I feel Anxious, because I feel Afraid`

**Top cosine:** 0.8053  |  **Top CE:** -2.6772

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -2.6772 | 0.8053 | Act with courage in the face of fear. | 11:34-34 |
| 2 | -6.6014 | 0.7884 | Recognize the influence of your mental state on your actions. | 14:6-6, 14:6-9 |
| 3 | -6.8551 | 0.7942 | Focus your mind and seek inner refuge. | 7:1-1 |
| 4 | -7.0128 | 0.7864 | Recognize and overcome desire and anger as obstacles. | 3:37-37 |
| 5 | -7.9448 | 0.7940 | Control your mind and senses to achieve liberation. | 5:28-28 |

#### Scared > Insecure > Inadequate
**Query:** `I feel Scared because I feel Insecure, because I feel Inadequate`

**Top cosine:** 0.792  |  **Top CE:** -8.0108

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -8.0108 | 0.7920 | Focus your mind and seek inner refuge. | 7:1-1 |
| 2 | -8.0841 | 0.7819 | Overcome ignorance to free yourself from delusion. | 14:8-8 |
| 3 | -9.1302 | 0.7811 | Let go of longing to find true fulfillment. | 2:59-59 |
| 4 | -9.1779 | 0.7853 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |
| 5 | -9.2772 | 0.7845 | Practice humility and self-control for inner strength. | 4:26-26, 4:26-27, 13:8-15 |

#### Scared > Insecure > Inferior
**Query:** `I feel Scared because I feel Insecure, because I feel Inferior`

**Top cosine:** 0.7911  |  **Top CE:** -9.1988

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -9.1988 | 0.7911 | Focus your mind and seek inner refuge. | 7:1-1 |
| 2 | -9.3312 | 0.7904 | Overcome ignorance to free yourself from delusion. | 14:8-8 |
| 3 | -9.8779 | 0.7908 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |
| 4 | -9.9026 | 0.7890 | Detach from qualities to transcend pleasure and pain. | 13:20-20, 13:15-22 |
| 5 | -10.2213 | 0.7875 | Practice humility and self-control for inner strength. | 4:26-26, 4:26-27, 13:8-15 |

#### Scared > Swamped > Helpless
**Query:** `I feel Scared because I feel Swamped, because I feel Helpless`

**Top cosine:** 0.807  |  **Top CE:** -7.5272

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -7.5272 | 0.7840 | Act with courage in the face of fear. | 11:34-34 |
| 2 | -9.2487 | 0.8070 | Focus your mind and seek inner refuge. | 7:1-1 |
| 3 | -9.9480 | 0.7857 | Resist the pull of attachment and aversion. | 3:31-31, 3:31-34, 3:36-38 |
| 4 | -10.0229 | 0.7925 | Freed from attachment, seek refuge in knowledge. | 4:3-3, 4:3-11 |
| 5 | -10.2505 | 0.7896 | Free yourself from attachment to pleasure and power. | 2:43-43, 2:43-46 |

#### Scared > Swamped > Small
**Query:** `I feel Scared because I feel Swamped, because I feel Small`

**Top cosine:** 0.8062  |  **Top CE:** -8.6351

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -8.6351 | 0.8062 | Focus your mind and seek inner refuge. | 7:1-1 |
| 2 | -9.4995 | 0.7860 | Act with clarity and free yourself from attachment. | 3:30-30, 3:28-34 |
| 3 | -9.5714 | 0.7880 | Freed from attachment, seek refuge in knowledge. | 4:3-3, 4:3-11 |
| 4 | -9.6336 | 0.7870 | Free yourself from attachment to pleasure and power. | 2:43-43, 2:43-46 |
| 5 | -10.2784 | 0.7876 | Practice self-discipline to purify your actions. | 4:30-30 |

#### Scared > Rejected > Weak
**Query:** `I feel Scared because I feel Rejected, because I feel Weak`

**Top cosine:** 0.7984  |  **Top CE:** -8.3875

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -8.3875 | 0.7966 | Recognize and overcome desire and anger as obstacles. | 3:37-37 |
| 2 | -9.2155 | 0.7934 | Act without attachment or desire for reward. | 18:23-23, 18:23-24 |
| 3 | -9.3530 | 0.7938 | Focus your mind and seek inner refuge. | 7:1-1 |
| 4 | -9.5101 | 0.7984 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |
| 5 | -9.9232 | 0.7945 | Let go of longing to find true fulfillment. | 2:59-59 |

#### Scared > Rejected > Submissive
**Query:** `I feel Scared because I feel Rejected, because I feel Submissive`

**Top cosine:** 0.8074  |  **Top CE:** -7.2368

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -7.2368 | 0.8006 | Act without attachment or desire for reward. | 18:23-23, 18:23-24 |
| 2 | -7.8447 | 0.8056 | Abandon lust, anger, and greed for liberation. | 16:21-21, 16:19-24 |
| 3 | -8.0443 | 0.8024 | Resist the pull of attachment and aversion. | 3:31-31, 3:31-34, 3:36-38 |
| 4 | -8.2304 | 0.8074 | Free yourself from attachment to pleasure and power. | 2:43-43, 2:43-46 |
| 5 | -8.9381 | 0.7996 | Let go of longing to find true fulfillment. | 2:59-59 |

#### Scared > Confused > Baffled
**Query:** `I feel Scared because I feel Confused, because I feel Baffled`

**Top cosine:** 0.801  |  **Top CE:** -9.3705

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -9.3705 | 0.7884 | Control your senses to gain wisdom and clarity. | 2:58-58, 2:58-63, 3:34-34, 3:36-42 |
| 2 | -9.5982 | 0.7992 | Seek guidance to clarify your duty. | 2:7-7 |
| 3 | -9.7669 | 0.7913 | Focus your mind and seek inner refuge. | 7:1-1 |
| 4 | -10.0800 | 0.7882 | Control your mind and senses to achieve liberation. | 5:28-28 |
| 5 | -10.5821 | 0.8010 | Seek understanding through meditation, knowledge, or action. | 13:23-23, 13:23-26 |

#### Scared > Confused > Discouraged
**Query:** `I feel Scared because I feel Confused, because I feel Discouraged`

**Top cosine:** 0.8088  |  **Top CE:** -8.8791

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -8.8791 | 0.8088 | Seek guidance to clarify your duty. | 2:7-7 |
| 2 | -9.0685 | 0.7955 | Focus your mind and seek inner refuge. | 7:1-1 |
| 3 | -9.7157 | 0.7957 | Freed from attachment, seek refuge in knowledge. | 4:3-3, 4:3-11 |
| 4 | -9.8499 | 0.7996 | Let go of longing to find true fulfillment. | 2:59-59 |
| 5 | -10.0378 | 0.8027 | Seek understanding through meditation, knowledge, or action. | 13:23-23, 13:23-26 |

#### Scared > Embarrassed > Foolish
**Query:** `I feel Scared because I feel Embarrassed, because I feel Foolish`

**Top cosine:** 0.8017  |  **Top CE:** -7.3882

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -7.3882 | 0.7972 | Seek knowledge to overcome ignorance and heedlessness. | 5:15-15, 10:8-11, 14:8-11 |
| 2 | -7.8973 | 0.8017 | Overcome ignorance to free yourself from delusion. | 14:8-8 |
| 3 | -8.5382 | 0.7928 | Recognize the influence of your mental state on your actions. | 14:6-6, 14:6-9 |
| 4 | -8.9547 | 0.7955 | Control your senses to gain wisdom and clarity. | 2:58-58, 2:58-63, 3:34-34, 3:36-42 |
| 5 | -9.5198 | 0.7930 | Practice self-discipline to purify your actions. | 4:30-30 |

#### Scared > Embarrassed > Shy
**Query:** `I feel Scared because I feel Embarrassed, because I feel Shy`

**Top cosine:** 0.7949  |  **Top CE:** -6.1723

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -6.1723 | 0.7949 | Act with courage in the face of fear. | 11:34-34 |
| 2 | -8.6357 | 0.7898 | Act without attachment or desire for reward. | 18:23-23, 18:23-24 |
| 3 | -8.6534 | 0.7903 | Recognize the influence of your mental state on your actions. | 14:6-6, 14:6-9 |
| 4 | -8.9444 | 0.7868 | Free yourself from attachment to pleasure and power. | 2:43-43, 2:43-46 |
| 5 | -9.4230 | 0.7927 | Control your mind and senses to achieve liberation. | 5:28-28 |

### JOYFUL

#### Joyful > Playful > Amused
**Query:** `I feel Joyful because I feel Playful, because I feel Amused`

**Top cosine:** 0.8172  |  **Top CE:** -2.8627

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -2.8627 | 0.8069 | Cultivate joy through mindful remembrance. | 18:77-77 |
| 2 | -4.6368 | 0.8114 | Seek lasting joy through self-realization, not fleeting pleasures. | 5:22-22, 18:35-41 |
| 3 | -5.2055 | 0.8172 | Find happiness and illumination within yourself. | 5:24-24 |
| 4 | -5.2987 | 0.8085 | Seek joy through practice to overcome suffering. | 18:36-36 |
| 5 | -5.7999 | 0.8066 | Act with purpose, not merely for pleasure. | 2:43-43 |

#### Joyful > Playful > Spirited
**Query:** `I feel Joyful because I feel Playful, because I feel Spirited`

**Top cosine:** 0.8234  |  **Top CE:** -3.9201

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.9201 | 0.8173 | Cultivate joy through mindful remembrance. | 18:77-77 |
| 2 | -5.3408 | 0.8234 | Seek lasting joy through self-realization, not fleeting pleasures. | 5:22-22, 18:35-41 |
| 3 | -5.7562 | 0.8176 | Seek joy through practice to overcome suffering. | 18:36-36 |
| 4 | -6.3505 | 0.8233 | Find happiness and illumination within yourself. | 5:24-24 |
| 5 | -8.1834 | 0.8170 | Act in harmony with your true nature. | 3:32-32, 3:32-34, 3:36-36 |

#### Joyful > Content > Peaceful
**Query:** `I feel Joyful because I feel Content, because I feel Peaceful`

**Top cosine:** 0.8432  |  **Top CE:** -2.6771

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -2.6771 | 0.8281 | Find contentment within yourself. | 3:17-17 |
| 2 | -2.8347 | 0.8413 | Cultivate steadiness to find peace and happiness. | 2:66-66, 2:66-69 |
| 3 | -3.1782 | 0.8432 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 4 | -3.8657 | 0.8270 | Seek lasting joy through self-realization, not fleeting pleasures. | 5:22-22, 18:35-41 |
| 5 | -5.3077 | 0.8264 | Find happiness and illumination within yourself. | 5:24-24 |

#### Joyful > Content > Pleasant
**Query:** `I feel Joyful because I feel Content, because I feel Pleasant`

**Top cosine:** 0.836  |  **Top CE:** -3.2888

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.2888 | 0.8329 | Find contentment within yourself. | 3:17-17 |
| 2 | -3.8301 | 0.8360 | Seek lasting joy through self-realization, not fleeting pleasures. | 5:22-22, 18:35-41 |
| 3 | -4.8083 | 0.8357 | Find happiness and illumination within yourself. | 5:24-24 |
| 4 | -8.5596 | 0.8249 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 5 | -8.5994 | 0.8269 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |

#### Joyful > Interested > Curious
**Query:** `I feel Joyful because I feel Interested, because I feel Curious`

**Top cosine:** 0.8222  |  **Top CE:** -4.5832

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -4.5832 | 0.8208 | Seek lasting joy through self-realization, not fleeting pleasures. | 5:22-22, 18:35-41 |
| 2 | -6.3103 | 0.8176 | Find happiness and illumination within yourself. | 5:24-24 |
| 3 | -8.6899 | 0.8204 | Seek understanding to connect with a greater existence. | 13:19-19 |
| 4 | -8.8502 | 0.8222 | Restrain desire to uncover true wisdom. | 3:39-39 |
| 5 | -9.7766 | 0.8211 | Seek understanding through meditation, knowledge, or action. | 13:23-23, 13:23-26 |

#### Joyful > Interested > Inquisitive
**Query:** `I feel Joyful because I feel Interested, because I feel Inquisitive`

**Top cosine:** 0.8235  |  **Top CE:** -4.1363

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -4.1363 | 0.8219 | Seek lasting joy through self-realization, not fleeting pleasures. | 5:22-22, 18:35-41 |
| 2 | -6.2995 | 0.8235 | Find happiness and illumination within yourself. | 5:24-24 |
| 3 | -9.1882 | 0.8139 | Seek understanding to connect with a greater existence. | 13:19-19 |
| 4 | -9.8481 | 0.8194 | Find contentment within yourself. | 3:17-17 |
| 5 | -10.5941 | 0.8134 | Find contentment within yourself to transcend external actions. | 3:16-16, 3:15-18 |

#### Joyful > Proud > Achieved
**Query:** `I feel Joyful because I feel Proud, because I feel Achieved`

**Top cosine:** 0.8248  |  **Top CE:** -4.4106

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -4.4106 | 0.8189 | Act with intention to achieve success. | 4:12-12 |
| 2 | -5.5904 | 0.8202 | Find happiness and illumination within yourself. | 5:24-24 |
| 3 | -7.1832 | 0.8248 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |
| 4 | -7.6137 | 0.8164 | Cultivate steadfastness to realize your true self. | 7:17-17, 7:17-20 |
| 5 | -8.7847 | 0.8146 | Strive diligently for personal growth and purification. | 6:45-45 |

#### Joyful > Proud > Confident
**Query:** `I feel Joyful because I feel Proud, because I feel Confident`

**Top cosine:** 0.8291  |  **Top CE:** -3.6353

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.6353 | 0.8291 | Act with clarity and confidence. | 18:73-73 |
| 2 | -4.9513 | 0.8175 | Find happiness and illumination within yourself. | 5:24-24 |
| 3 | -6.4674 | 0.8251 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |
| 4 | -6.7089 | 0.8181 | Practice with determination and a positive mindset. | 6:23-23 |
| 5 | -9.3148 | 0.8161 | Act with steadiness, free from attachment to results. | 2:47-47, 2:47-48 |

#### Joyful > Excited > Eager
**Query:** `I feel Joyful because I feel Excited, because I feel Eager`

**Top cosine:** 0.8178  |  **Top CE:** -5.5592

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -5.5592 | 0.8070 | Seek lasting joy through self-realization, not fleeting pleasures. | 5:22-22, 18:35-41 |
| 2 | -6.8098 | 0.8178 | Find happiness and illumination within yourself. | 5:24-24 |
| 3 | -8.5404 | 0.8041 | Embrace challenges for deeper happiness and self-realization. | 18:37-37 |
| 4 | -9.2599 | 0.8018 | Act with intention to fulfill your desires. | 3:10-10 |
| 5 | -9.6435 | 0.8072 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |

#### Joyful > Excited > Energetic
**Query:** `I feel Joyful because I feel Excited, because I feel Energetic`

**Top cosine:** 0.821  |  **Top CE:** -3.6381

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.6381 | 0.8032 | Cultivate joy through mindful remembrance. | 18:77-77 |
| 2 | -5.6490 | 0.8148 | Seek lasting joy through self-realization, not fleeting pleasures. | 5:22-22, 18:35-41 |
| 3 | -5.9730 | 0.8210 | Find happiness and illumination within yourself. | 5:24-24 |
| 4 | -6.5913 | 0.8018 | Find happiness within by controlling desires and anger. | 5:21-21, 5:21-28 |
| 5 | -9.0717 | 0.8056 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |

#### Joyful > Cheerful > Delightful
**Query:** `I feel Joyful because I feel Cheerful, because I feel Delightful`

**Top cosine:** 0.8406  |  **Top CE:** -2.4654

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -2.4654 | 0.8185 | Cultivate joy through mindful remembrance. | 18:77-77 |
| 2 | -3.6671 | 0.8178 | Seek lasting joy through self-realization, not fleeting pleasures. | 5:22-22, 18:35-41 |
| 3 | -4.4382 | 0.8406 | Find happiness and illumination within yourself. | 5:24-24 |
| 4 | -5.6371 | 0.8208 | Cultivate steadiness to find peace and happiness. | 2:66-66, 2:66-69 |
| 5 | -8.3129 | 0.8198 | Find contentment within yourself. | 3:17-17 |

#### Joyful > Cheerful > Optimistic
**Query:** `I feel Joyful because I feel Cheerful, because I feel Optimistic`

**Top cosine:** 0.8311  |  **Top CE:** -3.8116

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.8116 | 0.8311 | Find happiness and illumination within yourself. | 5:24-24 |
| 2 | -3.8522 | 0.8137 | Seek lasting joy through self-realization, not fleeting pleasures. | 5:22-22, 18:35-41 |
| 3 | -5.0340 | 0.8128 | Embrace challenges for deeper happiness and self-realization. | 18:37-37 |
| 4 | -5.0405 | 0.8212 | Cultivate steadiness to find peace and happiness. | 2:66-66, 2:66-69 |
| 5 | -6.5208 | 0.8181 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |

### POWERFUL

#### Powerful > Respected > Valuable
**Query:** `I feel Powerful because I feel Respected, because I feel Valuable`

**Top cosine:** 0.8507  |  **Top CE:** -1.1288

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -1.1288 | 0.8437 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |
| 2 | -5.7816 | 0.8367 | Value steadfastness and devotion for deeper connection. | 7:17-17 |
| 3 | -7.4997 | 0.8357 | Worship with steadfast devotion to cultivate inner strength. | 7:28-28, 9:11-19 |
| 4 | -8.3162 | 0.8507 | Recognize and transcend the qualities that bind you. | 14:5-5, 14:5-8 |
| 5 | -9.0766 | 0.8297 | Recognize and cultivate the qualities of clarity and balance. | 14:10-10, 14:10-13 |

#### Powerful > Respected > Valued
**Query:** `I feel Powerful because I feel Respected, because I feel Valued`

**Top cosine:** 0.8529  |  **Top CE:** -0.6332

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -0.6332 | 0.8414 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |
| 2 | -3.4726 | 0.8358 | Value steadfastness and devotion for deeper connection. | 7:17-17 |
| 3 | -7.7761 | 0.8352 | Worship with steadfast devotion to cultivate inner strength. | 7:28-28, 9:11-19 |
| 4 | -8.5213 | 0.8529 | Recognize and transcend the qualities that bind you. | 14:5-5, 14:5-8 |
| 5 | -9.0919 | 0.8313 | Recognize and cultivate the qualities of clarity and balance. | 14:10-10, 14:10-13 |

#### Powerful > Courageous > Daring
**Query:** `I feel Powerful because I feel Courageous, because I feel Daring`

**Top cosine:** 0.8427  |  **Top CE:** -1.7202

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -1.7202 | 0.8401 | Stand firm in your convictions and face challenges with courage. | 2:3-3, 2:3-6 |
| 2 | -2.1170 | 0.8390 | Act with courage in the face of fear. | 11:34-34 |
| 3 | -2.7110 | 0.8427 | Endure challenges with courage and equanimity. | 2:9-9, 2:9-20 |
| 4 | -4.2248 | 0.8365 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |
| 5 | -7.7159 | 0.8386 | Your character reflects your beliefs. | 17:3-3 |

#### Powerful > Courageous > Bold
**Query:** `I feel Powerful because I feel Courageous, because I feel Bold`

**Top cosine:** 0.8421  |  **Top CE:** -2.9913

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -2.9913 | 0.8354 | Fulfill your own responsibilities with courage. | 3:35-35, 13:25-25 |
| 2 | -3.0717 | 0.8404 | Stand firm in your convictions and face challenges with courage. | 2:3-3, 2:3-6 |
| 3 | -3.1885 | 0.8389 | Act with courage in the face of fear. | 11:34-34 |
| 4 | -3.8516 | 0.8378 | Endure challenges with courage and equanimity. | 2:9-9, 2:9-20 |
| 5 | -7.8783 | 0.8421 | Your character reflects your beliefs. | 17:3-3 |

#### Powerful > Proud > Achieved
**Query:** `I feel Powerful because I feel Proud, because I feel Achieved`

**Top cosine:** 0.833  |  **Top CE:** -5.3684

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -5.3684 | 0.8276 | Elevate yourself through self-mastery and awareness. | 6:5-5, 6:2-12 |
| 2 | -6.5501 | 0.8330 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |
| 3 | -7.6001 | 0.8242 | Cultivate steadfastness to realize your true self. | 7:17-17, 7:17-20 |
| 4 | -8.7441 | 0.8277 | Worship with steadfast devotion to cultivate inner strength. | 7:28-28, 9:11-19 |
| 5 | -9.4501 | 0.8263 | Recognize and transcend the qualities that bind you. | 14:5-5, 14:5-8 |

#### Powerful > Proud > Important
**Query:** `I feel Powerful because I feel Proud, because I feel Important`

**Top cosine:** 0.8306  |  **Top CE:** -6.1682

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -6.1682 | 0.8306 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |
| 2 | -8.7269 | 0.8262 | Worship with steadfast devotion to cultivate inner strength. | 7:28-28, 9:11-19 |
| 3 | -8.7295 | 0.8198 | Your character reflects your beliefs. | 17:3-3 |
| 4 | -8.8217 | 0.8269 | Value steadfastness and devotion for deeper connection. | 7:17-17 |
| 5 | -8.9989 | 0.8171 | Recognize and transcend the qualities that bind you. | 14:5-5, 14:5-8 |

#### Powerful > Creative > Ingenious
**Query:** `I feel Powerful because I feel Creative, because I feel Ingenious`

**Top cosine:** 0.8237  |  **Top CE:** -7.1699

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -7.1699 | 0.8108 | Elevate yourself through self-mastery and awareness. | 6:5-5, 6:2-12 |
| 2 | -8.3676 | 0.8237 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |
| 3 | -8.7488 | 0.8130 | Focus your mind on your purpose. | 8:7-7 |
| 4 | -9.2973 | 0.8126 | Recognize and transcend the qualities that bind you. | 14:5-5, 14:5-8 |
| 5 | -10.1113 | 0.8114 | Worship with steadfast devotion to cultivate inner strength. | 7:28-28, 9:11-19 |

#### Powerful > Creative > Versatile
**Query:** `I feel Powerful because I feel Creative, because I feel Versatile`

**Top cosine:** 0.825  |  **Top CE:** -8.1269

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -8.1269 | 0.8250 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |
| 2 | -8.5219 | 0.8122 | Control your senses to gain wisdom and clarity. | 2:58-58, 2:58-63, 3:34-34, 3:36-42 |
| 3 | -8.8671 | 0.8147 | Recognize and transcend the qualities that bind you. | 14:5-5, 14:5-8 |
| 4 | -9.8204 | 0.8168 | Value steadfastness and devotion for deeper connection. | 7:17-17 |
| 5 | -9.8473 | 0.8135 | Serve with unwavering devotion to transcend dualities. | 14:26-26 |

#### Powerful > Aware > Present
**Query:** `I feel Powerful because I feel Aware, because I feel Present`

**Top cosine:** 0.8362  |  **Top CE:** -6.8151

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -6.8151 | 0.8362 | Control your senses to gain wisdom and clarity. | 2:58-58, 2:58-63, 3:34-34, 3:36-42 |
| 2 | -7.8985 | 0.8244 | Control your mind and senses to achieve liberation. | 5:28-28 |
| 3 | -8.6655 | 0.8260 | Recognize the influence of your mental state on your actions. | 14:6-6, 14:6-9 |
| 4 | -9.6268 | 0.8296 | Recognize and transcend the qualities that bind you. | 14:5-5, 14:5-8 |
| 5 | -9.8781 | 0.8296 | Recognize the Self within to transcend attachment. | 13:22-22, 13:22-25 |

#### Powerful > Aware > Focused
**Query:** `I feel Powerful because I feel Aware, because I feel Focused`

**Top cosine:** 0.8349  |  **Top CE:** -1.4869

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -1.4869 | 0.8345 | Focus your mind on your purpose. | 8:7-7 |
| 2 | -6.2413 | 0.8349 | Control your senses to gain wisdom and clarity. | 2:58-58, 2:58-63, 3:34-34, 3:36-42 |
| 3 | -7.7997 | 0.8261 | Recognize the influence of your mental state on your actions. | 14:6-6, 14:6-9 |
| 4 | -8.2513 | 0.8241 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |
| 5 | -9.3925 | 0.8251 | Worship with steadfast devotion to cultivate inner strength. | 7:28-28, 9:11-19 |

#### Powerful > Confident > Capable
**Query:** `I feel Powerful because I feel Confident, because I feel Capable`

**Top cosine:** 0.841  |  **Top CE:** -2.7686

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -2.7686 | 0.8410 | Act with clarity and confidence. | 18:73-73 |
| 2 | -3.8188 | 0.8325 | Elevate yourself through self-mastery and awareness. | 6:5-5, 6:2-12 |
| 3 | -4.8532 | 0.8315 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |
| 4 | -8.0336 | 0.8334 | Recognize and transcend the qualities that bind you. | 14:5-5, 14:5-8 |
| 5 | -8.0775 | 0.8267 | Worship with steadfast devotion to cultivate inner strength. | 7:28-28, 9:11-19 |

#### Powerful > Confident > Secure
**Query:** `I feel Powerful because I feel Confident, because I feel Secure`

**Top cosine:** 0.8387  |  **Top CE:** -3.2249

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.2249 | 0.8387 | Act with clarity and confidence. | 18:73-73 |
| 2 | -4.5061 | 0.8238 | Act with clarity and confidence in your decisions. | 18:73-73, 18:73-76 |
| 3 | -6.1878 | 0.8258 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |
| 4 | -7.7616 | 0.8216 | Recognize and transcend the qualities that bind you. | 14:5-5, 14:5-8 |
| 5 | -8.9112 | 0.8291 | Worship with steadfast devotion to cultivate inner strength. | 7:28-28, 9:11-19 |

### PEACEFUL

#### Peaceful > Thankful > Grateful
**Query:** `I feel Peaceful because I feel Thankful, because I feel Grateful`

**Top cosine:** 0.842  |  **Top CE:** -3.0567

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.0567 | 0.8351 | Cultivate steadiness to find peace and happiness. | 2:66-66, 2:66-69 |
| 2 | -3.3516 | 0.8420 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 3 | -4.8853 | 0.8257 | Seek understanding to attain inner peace. | 3:2-2, 4:10-13, 5:29-29 |
| 4 | -8.3296 | 0.8233 | Endure life's fluctuations with courage and steadiness. | 2:7-7, 2:7-16 |
| 5 | -9.0841 | 0.8231 | Practice self-control for a pure and serene mind. | 17:9-9, 17:9-13, 17:16-19 |

#### Peaceful > Thankful > Blessed
**Query:** `I feel Peaceful because I feel Thankful, because I feel Blessed`

**Top cosine:** 0.8494  |  **Top CE:** -2.6405

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -2.6405 | 0.8494 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 2 | -3.3309 | 0.8421 | Cultivate steadiness to find peace and happiness. | 2:66-66, 2:66-69 |
| 3 | -5.3113 | 0.8305 | Seek understanding to attain inner peace. | 3:2-2, 4:10-13, 5:29-29 |
| 4 | -7.0567 | 0.8300 | Embrace compassion and truth for a liberated life. | 16:2-2, 16:2-9 |
| 5 | -9.2828 | 0.8283 | Practice self-control for a pure and serene mind. | 17:9-9, 17:9-13, 17:16-19 |

#### Peaceful > Loving > Tender
**Query:** `I feel Peaceful because I feel Loving, because I feel Tender`

**Top cosine:** 0.8419  |  **Top CE:** -3.4667

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.4667 | 0.8419 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 2 | -4.5645 | 0.8322 | Cultivate steadiness to find peace and happiness. | 2:66-66, 2:66-69 |
| 3 | -5.7082 | 0.8309 | Seek understanding to attain inner peace. | 3:2-2, 4:10-13, 5:29-29 |
| 4 | -6.2240 | 0.8318 | Rise above desires to find inner peace. | 2:42-42, 2:42-45 |
| 5 | -7.7288 | 0.8315 | Recognize the roots of attachment to cultivate inner peace. | 2:62-62 |

#### Peaceful > Loving > Empathic
**Query:** `I feel Peaceful because I feel Loving, because I feel Empathic`

**Top cosine:** 0.8388  |  **Top CE:** -3.6988

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.6988 | 0.8388 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 2 | -5.0644 | 0.8309 | Cultivate steadiness to find peace and happiness. | 2:66-66, 2:66-69 |
| 3 | -6.0096 | 0.8322 | Seek understanding to attain inner peace. | 3:2-2, 4:10-13, 5:29-29 |
| 4 | -6.4434 | 0.8263 | Rise above desires to find inner peace. | 2:42-42, 2:42-45 |
| 5 | -7.6428 | 0.8330 | Recognize the roots of attachment to cultivate inner peace. | 2:62-62 |

#### Peaceful > Trusting > Receptive
**Query:** `I feel Peaceful because I feel Trusting, because I feel Receptive`

**Top cosine:** 0.8375  |  **Top CE:** -3.7523

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.7523 | 0.8375 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 2 | -5.9755 | 0.8240 | Cultivate calm to maintain clarity and discernment. | 2:63-63 |
| 3 | -6.2764 | 0.8324 | Seek understanding to attain inner peace. | 3:2-2, 4:10-13, 5:29-29 |
| 4 | -6.7303 | 0.8269 | Act with clarity and confidence. | 18:73-73 |
| 5 | -8.4940 | 0.8244 | Recognize the roots of attachment to cultivate inner peace. | 2:62-62 |

#### Peaceful > Trusting > Patient
**Query:** `I feel Peaceful because I feel Trusting, because I feel Patient`

**Top cosine:** 0.837  |  **Top CE:** -3.8622

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.8622 | 0.8370 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 2 | -5.5465 | 0.8288 | Cultivate steadiness to find peace and happiness. | 2:66-66, 2:66-69 |
| 3 | -5.7023 | 0.8281 | Cultivate calm to maintain clarity and discernment. | 2:63-63 |
| 4 | -5.9730 | 0.8296 | Act with clarity and confidence. | 18:73-73 |
| 5 | -7.9818 | 0.8251 | Recognize the roots of attachment to cultivate inner peace. | 2:62-62 |

#### Peaceful > Nurturing > Supportive
**Query:** `I feel Peaceful because I feel Nurturing, because I feel Supportive`

**Top cosine:** 0.8452  |  **Top CE:** -2.8979

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -2.8979 | 0.8452 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 2 | -4.0913 | 0.8408 | Cultivate steadiness to find peace and happiness. | 2:66-66, 2:66-69 |
| 3 | -4.8639 | 0.8316 | Seek understanding to attain inner peace. | 3:2-2, 4:10-13, 5:29-29 |
| 4 | -5.6886 | 0.8301 | Embrace compassion and truth for a liberated life. | 16:2-2, 16:2-9 |
| 5 | -6.9165 | 0.8421 | Recognize the roots of attachment to cultivate inner peace. | 2:62-62 |

#### Peaceful > Nurturing > Caring
**Query:** `I feel Peaceful because I feel Nurturing, because I feel Caring`

**Top cosine:** 0.8486  |  **Top CE:** -3.6135

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.6135 | 0.8486 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 2 | -5.1343 | 0.8362 | Cultivate steadiness to find peace and happiness. | 2:66-66, 2:66-69 |
| 3 | -5.9306 | 0.8335 | Seek understanding to attain inner peace. | 3:2-2, 4:10-13, 5:29-29 |
| 4 | -7.9417 | 0.8404 | Recognize the roots of attachment to cultivate inner peace. | 2:62-62 |
| 5 | -8.8350 | 0.8305 | Practice self-control for a pure and serene mind. | 17:9-9, 17:9-13, 17:16-19 |

#### Peaceful > Serene > Calm
**Query:** `I feel Peaceful because I feel Serene, because I feel Calm`

**Top cosine:** 0.854  |  **Top CE:** 0.3993

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | +0.3993 | 0.8453 | Practice self-control for a pure and serene mind. | 17:9-9, 17:9-13, 17:16-19 |
| 2 | -1.1823 | 0.8540 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 3 | -4.3482 | 0.8373 | Practice mindfulness to achieve inner peace. | 6:12-12, 6:12-15 |
| 4 | -4.6969 | 0.8396 | Seek understanding to attain inner peace. | 3:2-2, 4:10-13, 5:29-29 |
| 5 | -5.2508 | 0.8374 | Rise above desires to find inner peace. | 2:42-42, 2:42-45 |

#### Peaceful > Serene > Content
**Query:** `I feel Peaceful because I feel Serene, because I feel Content`

**Top cosine:** 0.8528  |  **Top CE:** -2.6893

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -2.6893 | 0.8528 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 2 | -3.8574 | 0.8455 | Find contentment within yourself. | 3:17-17 |
| 3 | -5.1827 | 0.8453 | Cultivate steadiness to find peace and happiness. | 2:66-66, 2:66-69 |
| 4 | -7.0698 | 0.8377 | Recognize the value of inner stillness amidst activity. | 4:18-18 |
| 5 | -8.9238 | 0.8425 | Value wisdom and steadfastness in your pursuits. | 7:15-15, 7:15-18 |

#### Peaceful > Hopeful > Optimistic
**Query:** `I feel Peaceful because I feel Hopeful, because I feel Optimistic`

**Top cosine:** 0.85  |  **Top CE:** -3.3639

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -3.3639 | 0.8500 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 2 | -4.1086 | 0.8429 | Cultivate steadiness to find peace and happiness. | 2:66-66, 2:66-69 |
| 3 | -5.1967 | 0.8338 | Seek understanding to attain inner peace. | 3:2-2, 4:10-13, 5:29-29 |
| 4 | -5.7957 | 0.8309 | Rise above desires to find inner peace. | 2:42-42, 2:42-45 |
| 5 | -8.5958 | 0.8279 | Endure life's fluctuations with courage and steadiness. | 2:7-7, 2:7-16 |

#### Peaceful > Hopeful > Inspired
**Query:** `I feel Peaceful because I feel Hopeful, because I feel Inspired`

**Top cosine:** 0.8476  |  **Top CE:** -2.7071

| Rank (CE) | CE Score | Cosine | Lesson | Verses |
|-----------|---------|--------|--------|--------|
| 1 | -2.7071 | 0.8476 | Cultivate a peaceful mind to attain true bliss. | 6:24-24, 6:24-25, 6:27-30 |
| 2 | -4.7927 | 0.8322 | Cultivate steadiness to find peace and happiness. | 2:66-66, 2:66-69 |
| 3 | -5.4225 | 0.8337 | Seek understanding to attain inner peace. | 3:2-2, 4:10-13, 5:29-29 |
| 4 | -5.4943 | 0.8310 | Focus on the tangible to find peace. | 12:5-5 |
| 5 | -6.6776 | 0.8312 | Rise above desires to find inner peace. | 2:42-42, 2:42-45 |

---

## Differentiation Analysis

Emotion pairs where the #1 CE-ranked lesson is identical:

| Emotion A | Emotion B | Shared Lesson ID | Lesson Text |
|-----------|-----------|-----------------|-------------|
| Sad > Vulnerable > Victimized | Sad > Despair > Powerless | 369 | Seek joy through practice to overcome suffering. |
| Sad > Vulnerable > Fragile | Sad > Depressed > Empty | 198 | Focus your mind and seek inner refuge. |
| Sad > Guilty > Ashamed | Sad > Hurt > Let down | 290 | Detach from qualities to transcend pleasure and pain. |
| Sad > Guilty > Ashamed | Sad > Hurt > Agonized | 290 | Detach from qualities to transcend pleasure and pain. |
| Sad > Vulnerable > Fragile | Mad > Distant > Withdrawn | 198 | Focus your mind and seek inner refuge. |
| Sad > Vulnerable > Fragile | Mad > Distant > Numb | 198 | Focus your mind and seek inner refuge. |
| Mad > Frustrated > Annoyed | Mad > Aggressive > Hostile | 95 | Recognize and overcome desire and anger as obstacles. |
| Mad > Critical > Judging | Mad > Aggressive > Furious | 301 | Recognize the influence of your mental state on your actions |
| Mad > Frustrated > Annoyed | Mad > Hateful > Rage | 95 | Recognize and overcome desire and anger as obstacles. |
| Mad > Frustrated > Bitter | Mad > Hateful > Violated | 104 | Resist the sway of desire and anger. |
| Sad > Guilty > Ashamed | Mad > Hurt > Jealous | 290 | Detach from qualities to transcend pleasure and pain. |
| Mad > Frustrated > Bitter | Mad > Hurt > Bashful | 104 | Resist the sway of desire and anger. |
| Scared > Anxious > Worried | Scared > Anxious > Afraid | 261 | Act with courage in the face of fear. |
| Sad > Vulnerable > Fragile | Scared > Insecure > Inadequate | 198 | Focus your mind and seek inner refuge. |
| Sad > Vulnerable > Fragile | Scared > Insecure > Inferior | 198 | Focus your mind and seek inner refuge. |
| Scared > Anxious > Worried | Scared > Swamped > Helpless | 261 | Act with courage in the face of fear. |
| Sad > Vulnerable > Fragile | Scared > Swamped > Small | 198 | Focus your mind and seek inner refuge. |
| Mad > Frustrated > Annoyed | Scared > Rejected > Weak | 95 | Recognize and overcome desire and anger as obstacles. |
| Scared > Anxious > Worried | Scared > Embarrassed > Shy | 261 | Act with courage in the face of fear. |
| Joyful > Playful > Amused | Joyful > Playful > Spirited | 388 | Cultivate joy through mindful remembrance. |
| Joyful > Content > Peaceful | Joyful > Content > Pleasant | 80 | Find contentment within yourself. |
| Joyful > Interested > Curious | Joyful > Interested > Inquisitive | 145 | Seek lasting joy through self-realization, not fleeting plea |
| Joyful > Interested > Curious | Joyful > Excited > Eager | 145 | Seek lasting joy through self-realization, not fleeting plea |
| Joyful > Playful > Amused | Joyful > Excited > Energetic | 388 | Cultivate joy through mindful remembrance. |
| Joyful > Playful > Amused | Joyful > Cheerful > Delightful | 388 | Cultivate joy through mindful remembrance. |
| Powerful > Respected > Valuable | Powerful > Respected > Valued | 213 | Value wisdom and steadfastness in your pursuits. |
| Powerful > Respected > Valuable | Powerful > Proud > Important | 213 | Value wisdom and steadfastness in your pursuits. |
| Powerful > Proud > Achieved | Powerful > Creative > Ingenious | 160 | Elevate yourself through self-mastery and awareness. |
| Powerful > Respected > Valuable | Powerful > Creative > Versatile | 213 | Value wisdom and steadfastness in your pursuits. |
| Scared > Confused > Baffled | Powerful > Aware > Present | 28 | Control your senses to gain wisdom and clarity. |
| Joyful > Proud > Confident | Powerful > Confident > Capable | 56 | Act with clarity and confidence. |
| Joyful > Proud > Confident | Powerful > Confident > Secure | 56 | Act with clarity and confidence. |
| Peaceful > Thankful > Blessed | Peaceful > Loving > Tender | 175 | Cultivate a peaceful mind to attain true bliss. |
| Peaceful > Thankful > Blessed | Peaceful > Loving > Empathic | 175 | Cultivate a peaceful mind to attain true bliss. |
| Peaceful > Thankful > Blessed | Peaceful > Trusting > Receptive | 175 | Cultivate a peaceful mind to attain true bliss. |
| Peaceful > Thankful > Blessed | Peaceful > Trusting > Patient | 175 | Cultivate a peaceful mind to attain true bliss. |
| Peaceful > Thankful > Blessed | Peaceful > Nurturing > Supportive | 175 | Cultivate a peaceful mind to attain true bliss. |
| Peaceful > Thankful > Blessed | Peaceful > Nurturing > Caring | 175 | Cultivate a peaceful mind to attain true bliss. |
| Peaceful > Thankful > Blessed | Peaceful > Serene > Content | 175 | Cultivate a peaceful mind to attain true bliss. |
| Peaceful > Thankful > Blessed | Peaceful > Hopeful > Optimistic | 175 | Cultivate a peaceful mind to attain true bliss. |
| Peaceful > Thankful > Blessed | Peaceful > Hopeful > Inspired | 175 | Cultivate a peaceful mind to attain true bliss. |

---

## Notes for LLM Analysis

When reviewing these results, consider:
1. **Relevance:** Does the top lesson make sense for someone feeling this emotion?
2. **Differentiation:** Do similar emotions (e.g., Isolated vs Abandoned) get meaningfully different lessons?
3. **Positive vs Negative:** Do positive emotions (Joyful, Peaceful) get affirming lessons vs corrective ones?
4. **Score gaps:** Large CE score drops from #1 to #2 suggest strong matches; flat scores suggest ambiguity.
5. **Query format:** The query is `I feel X because I feel Y, because I feel Z` — consider if this phrasing helps or hurts semantic matching.
