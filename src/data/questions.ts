import { Question, AssessmentType } from '@/types';

export const assessmentQuestions: Record<AssessmentType, Question[]> = {
  anxiety: [
    {
      id: 'anx_1',
      type: 'mcq',
      question: 'How often do you experience feelings of nervousness or anxiety?',
      description: 'Think about your typical week and how anxiety shows up in your daily life.',
      options: ['Rarely or never', 'Occasionally', 'Often', 'Almost daily', 'Multiple times daily'],
      hint: 'Be honest about your experience - there are no wrong answers.',
      environment: 'forest',
      required: true,
    },
    {
      id: 'anx_2',
      type: 'scale',
      question: 'When you feel anxious, how intense is the feeling?',
      description: 'Rate the intensity of your anxiety when it occurs.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Very mild', 'Overwhelming'],
      environment: 'forest',
      required: true,
    },
    {
      id: 'anx_3',
      type: 'mcq',
      question: 'Which physical symptoms do you experience during anxiety?',
      description: 'Select all that apply to your experience.',
      options: [
        'Rapid heartbeat',
        'Sweating',
        'Trembling or shaking',
        'Shortness of breath',
        'Muscle tension',
        'Nausea or stomach issues',
        'Dizziness',
        'None of these'
      ],
      environment: 'ocean',
      required: false,
    },
    {
      id: 'anx_4',
      type: 'open-ended',
      question: 'What situations or thoughts tend to trigger your anxiety?',
      description: 'Describe what usually happens before you start feeling anxious.',
      hint: 'Examples: public speaking, social situations, health concerns, work deadlines, etc.',
      example: 'I often feel anxious when I have to speak in meetings or when I think about upcoming deadlines.',
      environment: 'ocean',
      required: false,
    },
    {
      id: 'anx_5',
      type: 'mcq',
      question: 'How do you typically cope when feeling anxious?',
      description: 'Think about your usual response to anxiety.',
      options: [
        'Deep breathing or meditation',
        'Avoid the situation',
        'Talk to someone',
        'Exercise or physical activity',
        'Use distractions (TV, phone, etc.)',
        'Try to push through it',
        'Use alcohol or substances',
        'I don\'t have effective coping strategies'
      ],
      environment: 'mountains',
      required: false,
    },
    {
      id: 'anx_6',
      type: 'scale',
      question: 'How much does anxiety interfere with your daily activities?',
      description: 'Consider work, relationships, hobbies, and personal care.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Not at all', 'Completely prevents me'],
      environment: 'mountains',
      required: true,
    },
    {
      id: 'anx_7',
      type: 'open-ended',
      question: 'Describe a recent time when anxiety affected your life significantly.',
      description: 'Share as much or as little as you feel comfortable with.',
      hint: 'This helps us understand the real-world impact of your anxiety.',
      environment: 'garden',
      required: false,
    },
    {
      id: 'anx_8',
      type: 'mood',
      question: 'How are you feeling right now as you complete this assessment?',
      description: 'Check in with yourself in this moment.',
      environment: 'garden',
      required: false,
    }
  ],

  ocd: [
    {
      id: 'ocd_1',
      type: 'mcq',
      question: 'Do you experience repetitive, unwanted thoughts that cause distress?',
      description: 'These might be thoughts about contamination, harm, order, or other concerns.',
      options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Almost constantly'],
      hint: 'Intrusive thoughts are more common than you might think.',
      environment: 'room',
      required: true,
    },
    {
      id: 'ocd_2',
      type: 'open-ended',
      question: 'What types of thoughts tend to get stuck in your mind?',
      description: 'Describe the content of repetitive or distressing thoughts.',
      hint: 'Examples: worries about germs, fears of harm, need for symmetry, religious concerns, etc.',
      example: 'I keep thinking about whether I locked the door or turned off the stove.',
      environment: 'room',
      required: false,
    },
    {
      id: 'ocd_3',
      type: 'mcq',
      question: 'Do you feel compelled to perform certain actions repeatedly?',
      description: 'These might be physical actions or mental rituals.',
      options: [
        'No repetitive behaviors',
        'Some checking or organizing',
        'Regular repetitive actions',
        'Frequent compulsive behaviors',
        'Almost constant rituals'
      ],
      environment: 'lighthouse',
      required: true,
    },
    {
      id: 'ocd_4',
      type: 'mcq',
      question: 'Which behaviors do you find yourself repeating?',
      description: 'Select all that apply to your experience.',
      options: [
        'Checking (locks, appliances, etc.)',
        'Washing or cleaning',
        'Counting or arranging',
        'Seeking reassurance',
        'Mental reviewing or praying',
        'Avoiding certain places/things',
        'Hoarding or collecting',
        'None of these'
      ],
      environment: 'lighthouse',
      required: false,
    },
    {
      id: 'ocd_5',
      type: 'scale',
      question: 'How much time do these thoughts and behaviors take up each day?',
      description: 'Consider both the mental energy and actual time spent.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Almost none', 'Most of my day'],
      environment: 'sky',
      required: true,
    },
    {
      id: 'ocd_6',
      type: 'open-ended',
      question: 'How do these patterns affect your daily life and relationships?',
      description: 'Share the impact on work, family, friends, or personal activities.',
      hint: 'Consider both positive and negative effects these patterns might have.',
      environment: 'sky',
      required: false,
    },
    {
      id: 'ocd_7',
      type: 'scale',
      question: 'How distressing are these thoughts and urges for you?',
      description: 'Rate the emotional discomfort they cause.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Mildly bothersome', 'Extremely distressing'],
      environment: 'forest',
      required: true,
    },
    {
      id: 'ocd_8',
      type: 'mood',
      question: 'How are you feeling after reflecting on these patterns?',
      description: 'Take a moment to notice your current emotional state.',
      environment: 'garden',
      required: false,
    }
  ],

  anger: [
    {
      id: 'ang_1',
      type: 'scale',
      question: 'How often do you experience intense anger or irritability?',
      description: 'Think about episodes where anger felt difficult to control.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Very rarely', 'Daily'],
      environment: 'mountains',
      required: true,
    },
    {
      id: 'ang_2',
      type: 'mcq',
      question: 'What typically triggers your anger?',
      description: 'Select the most common triggers for you.',
      options: [
        'Feeling misunderstood or unheard',
        'Injustice or unfairness',
        'Being criticized or blamed',
        'Feeling rushed or pressured',
        'Technical problems or delays',
        'Other people\'s behavior',
        'Feeling out of control',
        'Physical discomfort or pain'
      ],
      environment: 'mountains',
      required: false,
    },
    {
      id: 'ang_3',
      type: 'mcq',
      question: 'How do you typically express anger?',
      description: 'Think about your most common responses.',
      options: [
        'Raise my voice or yell',
        'Withdraw or give silent treatment',
        'Express it calmly and directly',
        'Bottle it up inside',
        'Become sarcastic or passive-aggressive',
        'Physical actions (slam doors, etc.)',
        'Take it out on objects',
        'Leave the situation immediately'
      ],
      environment: 'ocean',
      required: false,
    },
    {
      id: 'ang_4',
      type: 'open-ended',
      question: 'Describe a recent situation where you felt very angry.',
      description: 'What happened, how did you respond, and how did you feel afterward?',
      hint: 'This helps us understand your anger patterns and their effects.',
      example: 'Last week when my colleague took credit for my work, I felt furious but didn\'t say anything...',
      environment: 'ocean',
      required: false,
    },
    {
      id: 'ang_5',
      type: 'scale',
      question: 'How quickly do you usually calm down after getting angry?',
      description: 'Consider how long the angry feelings typically last.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Very quickly (minutes)', 'Very slowly (days)'],
      environment: 'forest',
      required: true,
    },
    {
      id: 'ang_6',
      type: 'mcq',
      question: 'How has anger affected your relationships?',
      description: 'Consider the impact on family, friends, and colleagues.',
      options: [
        'No significant impact',
        'Occasional tension',
        'Some relationships have been strained',
        'Several relationships have been damaged',
        'Major problems in most relationships',
        'I prefer not to answer'
      ],
      environment: 'forest',
      required: false,
    },
    {
      id: 'ang_7',
      type: 'open-ended',
      question: 'What strategies have you tried to manage your anger?',
      description: 'Share what has worked, what hasn\'t, and what you\'d like to try.',
      hint: 'Examples: counting to 10, exercise, talking it out, meditation, therapy, etc.',
      environment: 'garden',
      required: false,
    },
    {
      id: 'ang_8',
      type: 'mood',
      question: 'How are you feeling as you complete this reflection on anger?',
      description: 'Notice any emotions that have come up during this assessment.',
      environment: 'lighthouse',
      required: false,
    }
  ],

  // CBT Family (continued)
  'behavioral-activation': [
    {
      id: 'ba_1',
      type: 'mcq',
      question: 'How often do you find yourself avoiding activities you used to enjoy?',
      description: 'Think about your engagement with previously pleasurable activities.',
      options: ['Rarely', 'Sometimes', 'Often', 'Most of the time', 'Always'],
      environment: 'garden',
      required: true,
    },
    {
      id: 'ba_2',
      type: 'open-ended',
      question: 'What activities used to bring you joy or satisfaction?',
      description: 'List activities that you enjoyed in the past but may have stopped doing.',
      hint: 'Examples: hobbies, social activities, exercise, creative pursuits',
      environment: 'garden',
      required: true,
    },
    {
      id: 'ba_3',
      type: 'scale',
      question: 'Rate your current motivation to engage in meaningful activities.',
      description: 'How motivated do you feel to participate in activities?',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['No motivation', 'Very motivated'],
      environment: 'garden',
      required: true,
    }
  ],

  'habit-reversal': [
    {
      id: 'hr_1',
      type: 'mcq',
      question: 'Do you have any habits you would like to change or reduce?',
      description: 'Consider habits that may be interfering with your daily life.',
      options: ['No habits to change', 'One habit', 'A few habits', 'Several habits', 'Many habits'],
      environment: 'forest',
      required: true,
    },
    {
      id: 'hr_2',
      type: 'open-ended',
      question: 'Describe a habit you would most like to change.',
      description: 'What habit would have the biggest positive impact if changed?',
      hint: 'Examples: nail biting, hair pulling, smoking, procrastination',
      environment: 'forest',
      required: false,
    },
    {
      id: 'hr_3',
      type: 'scale',
      question: 'How aware are you when engaging in this habit?',
      description: 'Rate your awareness level during the habit.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Completely unaware', 'Very aware'],
      environment: 'forest',
      required: true,
    }
  ],

  'problem-solving': [
    {
      id: 'ps_1',
      type: 'mcq',
      question: 'When facing a problem, what is your typical approach?',
      description: 'Think about how you usually handle challenges.',
      options: ['Avoid the problem', 'React emotionally', 'Think it through systematically', 'Ask others for help', 'Jump to solutions quickly'],
      environment: 'mountains',
      required: true,
    },
    {
      id: 'ps_2',
      type: 'scale',
      question: 'How confident are you in your problem-solving abilities?',
      description: 'Rate your confidence in handling life challenges.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Not confident', 'Very confident'],
      environment: 'mountains',
      required: true,
    }
  ],

  // Mindfulness & Acceptance
  mindfulness: [
    {
      id: 'mf_1',
      type: 'mcq',
      question: 'How often do you practice mindfulness or meditation?',
      description: 'Consider any form of mindful awareness or meditation practice.',
      options: ['Never', 'Rarely', 'Occasionally', 'Regularly', 'Daily'],
      environment: 'garden',
      required: true,
    },
    {
      id: 'mf_2',
      type: 'scale',
      question: 'How present and aware do you feel in your daily life?',
      description: 'Rate your general level of mindful awareness.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Always distracted', 'Very present'],
      environment: 'garden',
      required: true,
    }
  ],

  'acceptance-commitment': [
    {
      id: 'act_1',
      type: 'mcq',
      question: 'How do you typically respond to difficult thoughts or feelings?',
      description: 'Think about your reaction to uncomfortable internal experiences.',
      options: ['Try to suppress them', 'Get overwhelmed by them', 'Accept them as part of life', 'Distract myself', 'Fight against them'],
      environment: 'forest',
      required: true,
    },
    {
      id: 'act_2',
      type: 'open-ended',
      question: 'What values are most important to you in life?',
      description: 'List the principles or qualities that guide your decisions.',
      hint: 'Examples: family, creativity, honesty, growth, helping others',
      environment: 'forest',
      required: true,
    }
  ],

  'mindful-cognitive': [
    {
      id: 'mc_1',
      type: 'mcq',
      question: 'How often do you notice and observe your thoughts without judgment?',
      description: 'Consider your ability to watch thoughts come and go.',
      options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Almost always'],
      environment: 'ocean',
      required: true,
    }
  ],

  // Emotion Regulation & Interpersonal
  'emotion-regulation': [
    {
      id: 'er_1',
      type: 'mcq',
      question: 'How intense are your emotional experiences typically?',
      description: 'Think about the strength of your emotional reactions.',
      options: ['Very mild', 'Mild', 'Moderate', 'Intense', 'Overwhelming'],
      environment: 'ocean',
      required: true,
    },
    {
      id: 'er_2',
      type: 'scale',
      question: 'How well can you calm yourself when upset?',
      description: 'Rate your ability to self-soothe during emotional distress.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Cannot calm down', 'Excellent at self-soothing'],
      environment: 'ocean',
      required: true,
    }
  ],

  interpersonal: [
    {
      id: 'ip_1',
      type: 'mcq',
      question: 'How comfortable are you in social situations?',
      description: 'Consider your general comfort level with interpersonal interactions.',
      options: ['Very uncomfortable', 'Somewhat uncomfortable', 'Neutral', 'Comfortable', 'Very comfortable'],
      environment: 'garden',
      required: true,
    },
    {
      id: 'ip_2',
      type: 'open-ended',
      question: 'What challenges do you face in your relationships?',
      description: 'Describe any difficulties you experience with others.',
      hint: 'Examples: communication, conflict resolution, setting boundaries',
      environment: 'garden',
      required: false,
    }
  ],

  // Compassion & Self-Kindness
  'self-compassion': [
    {
      id: 'sc_1',
      type: 'mcq',
      question: 'How do you typically treat yourself when you make mistakes?',
      description: 'Think about your internal dialogue during difficult times.',
      options: ['Very harsh and critical', 'Somewhat critical', 'Neutral', 'Kind and understanding', 'Very compassionate'],
      environment: 'garden',
      required: true,
    },
    {
      id: 'sc_2',
      type: 'scale',
      question: 'How much do you practice self-forgiveness?',
      description: 'Rate your ability to forgive yourself for perceived failures.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Never forgive myself', 'Always forgive myself'],
      environment: 'garden',
      required: true,
    }
  ],

  'positive-psychology': [
    {
      id: 'pp_1',
      type: 'mcq',
      question: 'How often do you practice gratitude?',
      description: 'Consider your focus on positive aspects of life.',
      options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily'],
      environment: 'garden',
      required: true,
    },
    {
      id: 'pp_2',
      type: 'scale',
      question: 'Rate your overall life satisfaction.',
      description: 'How satisfied are you with your life currently?',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Very dissatisfied', 'Very satisfied'],
      environment: 'garden',
      required: true,
    }
  ],

  strengths: [
    {
      id: 'str_1',
      type: 'open-ended',
      question: 'What do you consider to be your greatest strengths?',
      description: 'List your personal qualities, skills, or talents.',
      hint: 'Examples: creativity, empathy, problem-solving, leadership',
      environment: 'mountains',
      required: true,
    },
    {
      id: 'str_2',
      type: 'mcq',
      question: 'How often do you use your strengths in daily life?',
      description: 'Consider how frequently you apply your best qualities.',
      options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Always'],
      environment: 'mountains',
      required: true,
    }
  ],

  // Lifestyle & Holistic
  sleep: [
    {
      id: 'sl_1',
      type: 'mcq',
      question: 'How would you rate your sleep quality?',
      description: 'Think about how rested you feel after sleeping.',
      options: ['Very poor', 'Poor', 'Fair', 'Good', 'Excellent'],
      environment: 'ocean',
      required: true,
    },
    {
      id: 'sl_2',
      type: 'scale',
      question: 'How many hours of sleep do you typically get per night?',
      description: 'Consider your average sleep duration.',
      scaleMin: 3,
      scaleMax: 12,
      scaleLabels: ['3 hours', '12 hours'],
      environment: 'ocean',
      required: true,
    }
  ],

  relaxation: [
    {
      id: 'rel_1',
      type: 'mcq',
      question: 'How often do you practice relaxation techniques?',
      description: 'Consider any form of intentional relaxation or stress relief.',
      options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily'],
      environment: 'ocean',
      required: true,
    },
    {
      id: 'rel_2',
      type: 'scale',
      question: 'Rate your current stress level.',
      description: 'How stressed do you feel in general?',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['No stress', 'Extremely stressed'],
      environment: 'ocean',
      required: true,
    }
  ],

  breathing: [
    {
      id: 'br_1',
      type: 'mcq',
      question: 'Are you aware of your breathing throughout the day?',
      description: 'Consider how conscious you are of your breath.',
      options: ['Never aware', 'Rarely aware', 'Sometimes aware', 'Often aware', 'Always aware'],
      environment: 'forest',
      required: true,
    },
    {
      id: 'br_2',
      type: 'mcq',
      question: 'Do you practice any breathing exercises?',
      description: 'Think about intentional breathing practices.',
      options: ['Never', 'Rarely', 'Sometimes', 'Regularly', 'Daily'],
      environment: 'forest',
      required: true,
    }
  ],

  exercise: [
    {
      id: 'ex_1',
      type: 'mcq',
      question: 'How often do you engage in physical exercise?',
      description: 'Consider any form of physical activity or movement.',
      options: ['Never', 'Rarely', 'Sometimes', 'Regularly', 'Daily'],
      environment: 'mountains',
      required: true,
    },
    {
      id: 'ex_2',
      type: 'scale',
      question: 'Rate how exercise affects your mood.',
      description: 'How much does physical activity improve your mental state?',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['No effect', 'Major improvement'],
      environment: 'mountains',
      required: true,
    }
  ],

  nutrition: [
    {
      id: 'nut_1',
      type: 'mcq',
      question: 'How would you describe your eating habits?',
      description: 'Consider the quality and patterns of your nutrition.',
      options: ['Very poor', 'Poor', 'Fair', 'Good', 'Excellent'],
      environment: 'garden',
      required: true,
    },
    {
      id: 'nut_2',
      type: 'mcq',
      question: 'Do you notice connections between food and your mood?',
      description: 'Think about how different foods affect how you feel.',
      options: ['Never notice', 'Rarely notice', 'Sometimes notice', 'Often notice', 'Always notice'],
      environment: 'garden',
      required: true,
    }
  ],

  // Specialized Therapies
  trauma: [
    {
      id: 'tr_1',
      type: 'mcq',
      question: 'Have you experienced any traumatic or highly distressing events?',
      description: 'Consider any experiences that significantly impacted you.',
      options: ['No', 'One event', 'A few events', 'Several events', 'Many events'],
      environment: 'forest',
      required: true,
    },
    {
      id: 'tr_2',
      type: 'scale',
      question: 'How much do past experiences affect your daily life?',
      description: 'Rate the impact of difficult past experiences on your current functioning.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['No impact', 'Major impact'],
      environment: 'forest',
      required: true,
    }
  ],

  schema: [
    {
      id: 'sch_1',
      type: 'mcq',
      question: 'Do you notice repeating patterns in your relationships?',
      description: 'Consider if similar issues arise across different relationships.',
      options: ['No patterns', 'Few patterns', 'Some patterns', 'Many patterns', 'Very clear patterns'],
      environment: 'mountains',
      required: true,
    },
    {
      id: 'sch_2',
      type: 'open-ended',
      question: 'What beliefs about yourself or others seem to guide your behavior?',
      description: 'Describe any core beliefs that influence how you interact with the world.',
      hint: 'Examples: "I must be perfect", "Others will abandon me", "I am not good enough"',
      environment: 'mountains',
      required: false,
    }
  ],

  narrative: [
    {
      id: 'nar_1',
      type: 'open-ended',
      question: 'How would you describe your life story in a few sentences?',
      description: 'Think about the main themes and narrative of your life.',
      hint: 'Focus on the story you tell yourself about who you are and your journey',
      environment: 'garden',
      required: true,
    },
    {
      id: 'nar_2',
      type: 'mcq',
      question: 'How empowered do you feel as the author of your own life?',
      description: 'Consider your sense of agency in shaping your story.',
      options: ['Not empowered', 'Slightly empowered', 'Moderately empowered', 'Very empowered', 'Completely empowered'],
      environment: 'garden',
      required: true,
    }
  ],

  motivation: [
    {
      id: 'mot_1',
      type: 'scale',
      question: 'Rate your motivation to make positive changes in your life.',
      description: 'How motivated are you to work on personal growth?',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['No motivation', 'Extremely motivated'],
      environment: 'mountains',
      required: true,
    },
    {
      id: 'mot_2',
      type: 'open-ended',
      question: 'What are your main reasons for wanting to change or grow?',
      description: 'Describe what drives your desire for personal development.',
      hint: 'Examples: family, career, health, relationships, personal values',
      environment: 'mountains',
      required: true,
    }
  ],

  'solution-focused': [
    {
      id: 'sf_1',
      type: 'open-ended',
      question: 'What is already working well in your life?',
      description: 'Identify current strengths and positive aspects of your situation.',
      hint: 'Think about relationships, skills, habits, or circumstances that are going well',
      environment: 'garden',
      required: true,
    },
    {
      id: 'sf_2',
      type: 'mcq',
      question: 'How confident are you that small changes can lead to big improvements?',
      description: 'Consider your belief in the power of incremental progress.',
      options: ['Not confident', 'Slightly confident', 'Moderately confident', 'Very confident', 'Extremely confident'],
      environment: 'garden',
      required: true,
    }
  ],

  general: [
    {
      id: 'gen_1',
      type: 'scale',
      question: 'How would you rate your overall mental wellbeing right now?',
      description: 'Consider your general mood, stress levels, and life satisfaction.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Very poor', 'Excellent'],
      environment: 'garden',
      required: true,
    },
    {
      id: 'gen_2',
      type: 'mcq',
      question: 'Which areas of your life are you most concerned about?',
      description: 'Select all that feel relevant to you right now.',
      options: [
        'Work or career stress',
        'Relationship difficulties',
        'Financial worries',
        'Health concerns',
        'Family issues',
        'Social connections',
        'Personal growth',
        'Life direction or purpose',
        'None of these'
      ],
      environment: 'garden',
      required: false,
    },
    {
      id: 'gen_3',
      type: 'scale',
      question: 'How well do you currently manage daily stress?',
      description: 'Think about your typical response to everyday challenges.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Very poorly', 'Very well'],
      environment: 'ocean',
      required: true,
    },
    {
      id: 'gen_4',
      type: 'open-ended',
      question: 'What does a good day look like for you?',
      description: 'Describe what makes you feel happy, fulfilled, or at peace.',
      hint: 'This helps us understand what supports your wellbeing.',
      example: 'A good day for me includes time in nature, connecting with friends, and feeling productive at work.',
      environment: 'ocean',
      required: false,
    },
    {
      id: 'gen_5',
      type: 'mcq',
      question: 'How often do you engage in activities that bring you joy?',
      description: 'Consider hobbies, social time, relaxation, or other fulfilling activities.',
      options: [
        'Daily',
        'Several times a week',
        'Once a week',
        'A few times a month',
        'Rarely',
        'I\'m not sure what brings me joy'
      ],
      environment: 'sky',
      required: false,
    },
    {
      id: 'gen_6',
      type: 'scale',
      question: 'How supported do you feel by the people in your life?',
      description: 'Consider family, friends, colleagues, and community.',
      scaleMin: 1,
      scaleMax: 10,
      scaleLabels: ['Very unsupported', 'Very supported'],
      environment: 'sky',
      required: true,
    },
    {
      id: 'gen_7',
      type: 'open-ended',
      question: 'What changes would most improve your quality of life?',
      description: 'Think about what you\'d like to be different in your life.',
      hint: 'Consider both internal changes (mindset, habits) and external changes (environment, relationships).',
      environment: 'lighthouse',
      required: false,
    },
    {
      id: 'gen_8',
      type: 'mood',
      question: 'How are you feeling after this reflection on your wellbeing?',
      description: 'Take a moment to check in with yourself.',
      environment: 'lighthouse',
      required: false,
    }
  ]
};

export const getQuestionsForAssessment = (type: AssessmentType): Question[] => {
  return assessmentQuestions[type] || [];
};

export const getTotalQuestions = (type: AssessmentType): number => {
  return assessmentQuestions[type]?.length || 0;
};
