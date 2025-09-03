/**
 * TYPE DEFINITIONS FOR BHAGAVAD GITA VERSES
 * 
 * This file defines the data structure for Gita verses and provides
 * mock data for the bookmark app. The interface captures all necessary
 * information about each verse including translations and bookmark status.
 */

/**
 * GitaVerse Interface
 * 
 * Represents a single verse from the Bhagavad Gita with all its
 * textual content and metadata.
 */
export interface GitaVerse {
  chapter: number;        // Chapter number (1-18)
  verse: number;          // Verse number within the chapter
  sanskrit: string;       // Original Sanskrit text (not displayed in app)
  english: string;        // Romanized Sanskrit transliteration (not displayed)
  translation: string;    // English translation (main content displayed)
  isBookmarked: boolean;  // Whether user has bookmarked this verse
  id: string;            // Unique identifier in "chapter.verse" format
}

/**
 * MOCK BOOKMARK DATA
 * 
 * Sample verses used to demonstrate the bookmark list functionality.
 * These are some of the most well-known and inspirational verses
 * from the Bhagavad Gita, showcasing different chapters and themes.
 * 
 * Verses included:
 * - 2.47: Famous verse about duty without attachment to results
 * - 18.66: Surrender verse - Krishna's final instruction
 * - 4.7: Divine incarnation verse - when dharma declines
 * - 7.19: Rare soul verse - about true knowledge and surrender
 * - 15.7: Living entities verse - about the eternal soul
 */
export const mockBookmarkedVerses: GitaVerse[] = [
  // 2.47 - The most famous verse about selfless action and duty
  {
    id: "2.47",
    chapter: 2,
    verse: 47,
    sanskrit: "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन। मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥",
    english: "karmaṇy evādhikāras te mā phaleṣu kadācana mā karma-phala-hetur bhūr mā te saṅgo 'stv akarmaṇi",
    translation: "You have a right to perform your prescribed duty, but not to the fruits of action. Never consider yourself the cause of the results of your activities, and never be attached to not doing your duty.",
    isBookmarked: true
  },
  // 18.66 - The ultimate surrender verse, Krishna's final instruction
  {
    id: "18.66",
    chapter: 18,
    verse: 66,
    sanskrit: "सर्वधर्मान्परित्यज्य मामेकं शरणं व्रज। अहं त्वां सर्वपापेभ्यो मोक्षयिष्यामि मा शुचः॥",
    english: "sarva-dharmān parityajya mām ekaṁ śaraṇaṁ vraja ahaṁ tvāṁ sarva-pāpebhyo mokṣayiṣyāmi mā śucaḥ",
    translation: "Abandon all varieties of religion and just surrender unto Me. I shall deliver you from all sinful reactions. Do not fear.",
    isBookmarked: true
  },
  // 4.7 - Divine incarnation verse about when God appears on Earth
  {
    id: "4.7",
    chapter: 4,
    verse: 7,
    sanskrit: "यदा यदा हि धर्मस्य ग्लानिर्भवति भारत। अभ्युत्थानमधर्मस्य तदात्मानं सृजाम्यहम्॥",
    english: "yadā yadā hi dharmasya glānir bhavati bhārata abhyutthānam adharmasya tadātmānaṁ sṛjāmy aham",
    translation: "Whenever and wherever there is a decline in religious practice, O descendant of Bharata, and a predominant rise of irreligion—at that time I descend Myself.",
    isBookmarked: true
  },
  // 7.19 - About the rarity of a truly enlightened soul
  {
    id: "7.19",
    chapter: 7,
    verse: 19,
    sanskrit: "बहूनां जन्मनामन्ते ज्ञानवान्मां प्रपद्यते। वासुदेवः सर्वमिति स महात्मा सुदुर्लभः॥",
    english: "bahūnāṁ janmanām ante jñānavān māṁ prapadyate vāsudevaḥ sarvam iti sa mahātmā su-durlabhaḥ",
    translation: "After many births and deaths, he who is actually in knowledge surrenders unto Me, knowing Me to be the cause of all causes and all that is. Such a great soul is very rare.",
    isBookmarked: true
  },
  // 15.7 - About the eternal soul and its struggle in material world
  {
    id: "15.7",
    chapter: 15,
    verse: 7,
    sanskrit: "ममैवांशो जीवलोके जीवभूतः सनातनः। मनःषष्ठानीन्द्रियाणि प्रकृतिस्थानि कर्षति॥",
    english: "mamaivāṁśo jīva-loke jīva-bhūtaḥ sanātanaḥ manaḥ-ṣaṣṭhānīndriyāṇi prakṛti-sthāni karṣati",
    translation: "The living entities in this conditioned world are My eternal fragmental parts. Due to conditioned life, they are struggling very hard with the six senses, which include the mind.",
    isBookmarked: true
  }
];