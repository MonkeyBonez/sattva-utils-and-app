export interface EmotionNode {
  id: string;
  label: string;
  color?: string;
  children?: EmotionNode[];
}

export const emotionData: EmotionNode[] = [
  {
    id: "sad",
    label: "Sad",
    color: "#5B6B7A",
    children: [
      {
        id: "sad_lonely",
        label: "Lonely",
        children: [
          { id: "sad_lonely_isolated", label: "Isolated" },
          { id: "sad_lonely_abandoned", label: "Abandoned" }
        ]
      },
      {
        id: "sad_vulnerable",
        label: "Vulnerable",
        children: [
          { id: "sad_vulnerable_fragile", label: "Fragile" },
          { id: "sad_vulnerable_victimized", label: "Victimized" }
        ]
      },
      {
        id: "sad_despaired",
        label: "Despair",
        children: [
          { id: "sad_despaired_powerless", label: "Powerless" },
          { id: "sad_despaired_grief", label: "Grief" }
        ]
      },
      {
        id: "sad_guilty",
        label: "Guilty",
        children: [
          { id: "sad_guilty_remorse", label: "Remorse" },
          { id: "sad_guilty_ashamed", label: "Ashamed" }
        ]
      },
      {
        id: "sad_depressed",
        label: "Depressed",
        children: [
          { id: "sad_depressed_empty", label: "Empty" },
          { id: "sad_depressed_inferior", label: "Inferior" }
        ]
      },
      {
        id: "sad_hurt",
        label: "Hurt",
        children: [
          { id: "sad_hurt_disappointed", label: "Disappointed" },
          { id: "sad_hurt_agonized", label: "Agonized" }
        ]
      }
    ]
  },
  {
    id: "mad",
    label: "Mad",
    color: "#B34747",
    children: [
      {
        id: "mad_critical",
        label: "Critical",
        children: [
          { id: "mad_critical_skeptical", label: "Skeptical" },
          { id: "mad_critical_judgmental", label: "Judgmental" }
        ]
      },
      {
        id: "mad_distant",
        label: "Distant",
        children: [
          { id: "mad_distant_withdrawn", label: "Withdrawn" },
          { id: "mad_distant_numb", label: "Numb" }
        ]
      },
      {
        id: "mad_frustrated",
        label: "Frustrated",
        children: [
          { id: "mad_frustrated_annoyed", label: "Annoyed" },
          { id: "mad_frustrated_bitter", label: "Bitter" }
        ]
      },
      {
        id: "mad_aggressive",
        label: "Aggressive",
        children: [
          { id: "mad_aggressive_hostile", label: "Hostile" },
          { id: "mad_aggressive_furious", label: "Furious" }
        ]
      },
      {
        id: "mad_hateful",
        label: "Hateful",
        children: [
          { id: "mad_hateful_rage", label: "Rage" },
          { id: "mad_hateful_violated", label: "Violated" }
        ]
      },
      {
        id: "mad_hurt",
        label: "Hurt",
        children: [
          { id: "mad_hurt_jealous", label: "Jealous" },
          { id: "mad_hurt_bashful", label: "Bashful" }
        ]
      }
    ]
  },
  {
    id: "scared",
    label: "Scared",
    color: "#6C7CB0",
    children: [
      {
        id: "scared_anxious",
        label: "Anxious",
        children: [
          { id: "scared_anxious_worried", label: "Worried" },
          { id: "scared_anxious_frightened", label: "Frightened" }
        ]
      },
      {
        id: "scared_insecure",
        label: "Insecure",
        children: [
          { id: "scared_insecure_inadequate", label: "Inadequate" },
          { id: "scared_insecure_inferior", label: "Inferior" }
        ]
      },
      {
        id: "scared_overwhelmed",
        label: "Overwhelmed",
        children: [
          { id: "scared_overwhelmed_helpless", label: "Helpless" },
          { id: "scared_overwhelmed_insignificant", label: "Insignificant" }
        ]
      },
      {
        id: "scared_rejected",
        label: "Rejected",
        children: [
          { id: "scared_rejected_weak", label: "Weak" },
          { id: "scared_rejected_submissive", label: "Submissive" }
        ]
      },
      {
        id: "scared_confused",
        label: "Confused",
        children: [
          { id: "scared_confused_bewildered", label: "Bewildered" },
          { id: "scared_confused_discouraged", label: "Discouraged" }
        ]
      },
      {
        id: "scared_embarrassed",
        label: "Embarrassed",
        children: [
          { id: "scared_embarrassed_foolish", label: "Foolish" },
          { id: "scared_embarrassed_selfconscious", label: "Self-conscious" }
        ]
      }
    ]
  },
  {
    id: "joyful",
    label: "Joyful",
    color: "#EFBF5B",
    children: [
      {
        id: "joyful_playful",
        label: "Playful",
        children: [
          { id: "joyful_playful_amused", label: "Amused" },
          { id: "joyful_playful_spirited", label: "Spirited" }
        ]
      },
      {
        id: "joyful_content",
        label: "Content",
        children: [
          { id: "joyful_content_peaceful", label: "Peaceful" },
          { id: "joyful_content_pleasant", label: "Pleasant" }
        ]
      },
      {
        id: "joyful_interested",
        label: "Interested",
        children: [
          { id: "joyful_interested_curious", label: "Curious" },
          { id: "joyful_interested_inquisitive", label: "Inquisitive" }
        ]
      },
      {
        id: "joyful_proud",
        label: "Proud",
        children: [
          { id: "joyful_proud_successful", label: "Successful" },
          { id: "joyful_proud_confident", label: "Confident" }
        ]
      },
      {
        id: "joyful_excited",
        label: "Excited",
        children: [
          { id: "joyful_excited_eager", label: "Eager" },
          { id: "joyful_excited_energetic", label: "Energetic" }
        ]
      },
      {
        id: "joyful_cheerful",
        label: "Cheerful",
        children: [
          { id: "joyful_cheerful_delightful", label: "Delightful" },
          { id: "joyful_cheerful_optimistic", label: "Optimistic" }
        ]
      }
    ]
  },
  {
    id: "powerful",
    label: "Powerful",
    color: "#65A665",
    children: [
      {
        id: "powerful_respected",
        label: "Respected",
        children: [
          { id: "powerful_respected_valued", label: "Valuable" },
          { id: "powerful_respected_appreciated", label: "Appreciated" }
        ]
      },
      {
        id: "powerful_courageous",
        label: "Courageous",
        children: [
          { id: "powerful_courageous_daring", label: "Daring" },
          { id: "powerful_courageous_bold", label: "Bold" }
        ]
      },
      {
        id: "powerful_proud",
        label: "Proud",
        children: [
          { id: "powerful_proud_successful", label: "Successful" },
          { id: "powerful_proud_important", label: "Important" }
        ]
      },
      {
        id: "powerful_creative",
        label: "Creative",
        children: [
          { id: "powerful_creative_ingenious", label: "Ingenious" },
          { id: "powerful_creative_resourceful", label: "Resourceful" }
        ]
      },
      {
        id: "powerful_aware",
        label: "Aware",
        children: [
          { id: "powerful_aware_present", label: "Present" },
          { id: "powerful_aware_focused", label: "Focused" }
        ]
      },
      {
        id: "powerful_confident",
        label: "Confident",
        children: [
          { id: "powerful_confident_valued", label: "Capable" },
          { id: "powerful_confident_secure", label: "Secure" }
        ]
      }
    ]
  },
  {
    id: "peaceful",
    label: "Peaceful",
    color: "#6CB3B9",
    children: [
      {
        id: "peaceful_thankful",
        label: "Thankful",
        children: [
          { id: "peaceful_thankful_grateful", label: "Grateful" },
          { id: "peaceful_thankful_blessed", label: "Blessed" }
        ]
      },
      {
        id: "peaceful_loving",
        label: "Loving",
        children: [
          { id: "peaceful_loving_affectionate", label: "Affectionate" },
          { id: "peaceful_loving_compassionate", label: "Compassionate" }
        ]
      },
      {
        id: "peaceful_trusting",
        label: "Trusting",
        children: [
          { id: "peaceful_trusting_receptive", label: "Receptive" },
          { id: "peaceful_trusting_patient", label: "Patient" }
        ]
      },
      {
        id: "peaceful_nurturing",
        label: "Nurturing",
        children: [
          { id: "peaceful_nurturing_supportive", label: "Supportive" },
          { id: "peaceful_nurturing_caring", label: "Caring" }
        ]
      },
      {
        id: "peaceful_serene",
        label: "Serene",
        children: [
          { id: "peaceful_serene_calm", label: "Calm" },
          { id: "peaceful_serene_content", label: "Content" }
        ]
      },
      {
        id: "peaceful_hopeful",
        label: "Hopeful",
        children: [
          { id: "peaceful_hopeful_optimistic", label: "Optimistic" },
          { id: "peaceful_hopeful_inspired", label: "Inspired" }
        ]
      }
    ]
  }
];