import { TherapyExercise, AssessmentType } from '@/types';

export const therapyExercises: Record<AssessmentType, TherapyExercise[]> = {
  // CBT Family
  anxiety: [
    {
      id: 'thought_record_basic',
      name: 'Thought Record',
      type: 'cognitive',
      therapyType: 'anxiety',
      difficulty: 'beginner',
      estimatedDuration: 10,
      description: 'Learn to identify and challenge anxious thoughts using a structured thought record.',
      instructions: [
        'Think of a recent situation that made you anxious',
        'Write down what went through your mind',
        'Rate your anxiety level (0-10)',
        'Look for evidence for and against this thought',
        'Create a more balanced perspective'
      ],
      requiredInputs: [
        { id: 'situation', type: 'text', label: 'Describe the situation', required: true },
        { id: 'automatic_thought', type: 'text', label: 'What thought went through your mind?', required: true },
        { id: 'anxiety_level', type: 'scale', label: 'Anxiety level (0-10)', required: true },
        { id: 'evidence_for', type: 'text', label: 'Evidence supporting this thought', required: false },
        { id: 'evidence_against', type: 'text', label: 'Evidence against this thought', required: false },
        { id: 'balanced_thought', type: 'text', label: 'More balanced perspective', required: true }
      ],
      learningObjectives: [
        'Identify automatic negative thoughts',
        'Examine evidence objectively',
        'Develop balanced thinking patterns',
        'Reduce anxiety through cognitive restructuring'
      ],
      evidenceBase: 'CBT thought records: Beck et al. (1979), effect size d = 0.68-0.84'
    },
    {
      id: 'exposure_hierarchy',
      name: 'Build Your Exposure Ladder',
      type: 'behavioral',
      therapyType: 'anxiety',
      difficulty: 'intermediate',
      estimatedDuration: 15,
      description: 'Create a step-by-step plan to gradually face your fears.',
      instructions: [
        'List situations that make you anxious',
        'Rate each situation from 0-100 (anxiety level)',
        'Arrange them from lowest to highest anxiety',
        'Start with the lowest rated item',
        'Plan specific exposure exercises'
      ],
      requiredInputs: [
        { id: 'fear_situations', type: 'text', label: 'List 5-10 anxiety-provoking situations', required: true },
        { id: 'anxiety_ratings', type: 'text', label: 'Rate each situation (0-100)', required: true },
        { id: 'first_exposure', type: 'choice', label: 'Which will you try first?', required: true },
        { id: 'timeline', type: 'text', label: 'When will you do this exposure?', required: true }
      ],
      learningObjectives: [
        'Understand exposure therapy principles',
        'Create personalized exposure hierarchy',
        'Plan systematic desensitization',
        'Build confidence through gradual exposure'
      ],
      evidenceBase: 'Exposure therapy: Wolpe (1958), Foa & Kozak (1986)'
    }
  ],

  ocd: [
    {
      id: 'erp_planning',
      name: 'ERP Exercise Planner',
      type: 'behavioral',
      therapyType: 'ocd',
      difficulty: 'intermediate',
      estimatedDuration: 20,
      description: 'Plan and track Exposure and Response Prevention exercises.',
      instructions: [
        'Identify a specific obsession and compulsion',
        'Rate anxiety level when resisting compulsion',
        'Plan exposure without performing compulsion',
        'Track anxiety changes over time',
        'Record insights and progress'
      ],
      requiredInputs: [
        { id: 'obsession', type: 'text', label: 'Describe the obsessive thought', required: true },
        { id: 'compulsion', type: 'text', label: 'Describe the compulsive behavior', required: true },
        { id: 'initial_anxiety', type: 'scale', label: 'Initial anxiety (0-100)', required: true },
        { id: 'exposure_plan', type: 'text', label: 'Describe your exposure plan', required: true },
        { id: 'duration', type: 'choice', label: 'How long will you resist the compulsion?', required: true }
      ],
      learningObjectives: [
        'Understand ERP principles',
        'Plan systematic exposures',
        'Learn to tolerate uncertainty',
        'Break obsession-compulsion cycles'
      ],
      evidenceBase: 'ERP for OCD: Foa et al. (2005), 60-85% response rate'
    }
  ],

  'behavioral-activation': [
    {
      id: 'activity_scheduler',
      name: 'Activity Scheduling',
      type: 'behavioral',
      therapyType: 'behavioral-activation',
      difficulty: 'beginner',
      estimatedDuration: 15,
      description: 'Plan meaningful activities to improve mood and motivation.',
      instructions: [
        'List activities you used to enjoy',
        'Rate potential mood impact (1-10)',
        'Schedule specific times for activities',
        'Start with easier activities',
        'Track mood before and after'
      ],
      requiredInputs: [
        { id: 'past_activities', type: 'text', label: 'Activities you used to enjoy', required: true },
        { id: 'mood_prediction', type: 'scale', label: 'Predicted mood impact (1-10)', required: true },
        { id: 'scheduled_time', type: 'text', label: 'When will you do this?', required: true },
        { id: 'barriers', type: 'text', label: 'What might prevent you?', required: false },
        { id: 'solutions', type: 'text', label: 'How will you overcome barriers?', required: false }
      ],
      learningObjectives: [
        'Identify meaningful activities',
        'Plan behavioral experiments',
        'Increase activity engagement',
        'Improve mood through action'
      ],
      evidenceBase: 'Behavioral Activation: Martell et al. (2001), comparable to CBT for depression'
    }
  ],

  'habit-reversal': [
    {
      id: 'habit_tracker',
      name: 'Habit Awareness Training',
      type: 'behavioral',
      therapyType: 'habit-reversal',
      difficulty: 'beginner',
      estimatedDuration: 10,
      description: 'Increase awareness of habit triggers and patterns.',
      instructions: [
        'Identify the specific habit you want to change',
        'Track when and where it occurs',
        'Notice physical sensations before the habit',
        'Identify emotional triggers',
        'Plan competing responses'
      ],
      requiredInputs: [
        { id: 'habit_description', type: 'text', label: 'Describe the habit', required: true },
        { id: 'trigger_situations', type: 'text', label: 'When does it usually happen?', required: true },
        { id: 'warning_signs', type: 'text', label: 'What do you notice before it happens?', required: true },
        { id: 'competing_response', type: 'text', label: 'What could you do instead?', required: true }
      ],
      learningObjectives: [
        'Increase habit awareness',
        'Identify trigger patterns',
        'Develop competing responses',
        'Build self-control skills'
      ],
      evidenceBase: 'HRT: Azrin & Nunn (1973), 80% reduction in tic frequency'
    }
  ],

  'problem-solving': [
    {
      id: 'problem_solver_5step',
      name: '5-Step Problem Solver',
      type: 'cognitive',
      therapyType: 'problem-solving',
      difficulty: 'beginner',
      estimatedDuration: 20,
      description: 'Use a systematic approach to solve problems effectively.',
      instructions: [
        'Define the problem clearly',
        'Set a specific, achievable goal',
        'Brainstorm multiple solutions',
        'Evaluate pros and cons',
        'Create an action plan'
      ],
      requiredInputs: [
        { id: 'problem_definition', type: 'text', label: 'Define the problem clearly', required: true },
        { id: 'goal_statement', type: 'text', label: 'What is your goal?', required: true },
        { id: 'solutions_list', type: 'text', label: 'List possible solutions', required: true },
        { id: 'chosen_solution', type: 'text', label: 'Which solution will you try?', required: true },
        { id: 'action_steps', type: 'text', label: 'What are the specific steps?', required: true }
      ],
      learningObjectives: [
        'Structure problem-solving approach',
        'Generate creative solutions',
        'Evaluate options systematically',
        'Develop action planning skills'
      ],
      evidenceBase: 'PST: D\'Zurilla & Nezu (2007), effective for anxiety and depression'
    }
  ],

  // Mindfulness & Acceptance
  mindfulness: [
    {
      id: 'body_scan_meditation',
      name: 'Body Scan Meditation',
      type: 'interactive',
      therapyType: 'mindfulness',
      difficulty: 'beginner',
      estimatedDuration: 10,
      description: 'Practice mindful awareness of physical sensations.',
      instructions: [
        'Find a comfortable position',
        'Start with your toes and work upward',
        'Notice sensations without judgment',
        'Breathe naturally throughout',
        'Return attention when mind wanders'
      ],
      requiredInputs: [
        { id: 'comfort_level', type: 'scale', label: 'Comfort level (1-10)', required: true },
        { id: 'mind_wandering', type: 'scale', label: 'How often did your mind wander?', required: true },
        { id: 'relaxation_after', type: 'scale', label: 'Relaxation level after (1-10)', required: true },
        { id: 'insights', type: 'text', label: 'Any insights or observations?', required: false }
      ],
      learningObjectives: [
        'Develop body awareness',
        'Practice non-judgmental attention',
        'Learn to anchor in present moment',
        'Build mindfulness skills'
      ],
      evidenceBase: 'MBSR: Kabat-Zinn (1994), moderate to large effect sizes'
    },
    {
      id: 'mindful_breathing',
      name: 'Mindful Breathing',
      type: 'interactive',
      therapyType: 'mindfulness',
      difficulty: 'beginner',
      estimatedDuration: 5,
      description: 'Focus attention on the breath to cultivate present-moment awareness.',
      instructions: [
        'Sit comfortably with eyes closed or soft gaze',
        'Notice your natural breathing rhythm',
        'Focus on sensations of breathing',
        'When mind wanders, gently return to breath',
        'End with a few deep breaths'
      ],
      requiredInputs: [
        { id: 'focus_quality', type: 'scale', label: 'How focused were you? (1-10)', required: true },
        { id: 'calmness_before', type: 'scale', label: 'Calmness before (1-10)', required: true },
        { id: 'calmness_after', type: 'scale', label: 'Calmness after (1-10)', required: true },
        { id: 'distractions', type: 'text', label: 'What distracted you?', required: false }
      ],
      learningObjectives: [
        'Anchor attention in the present',
        'Develop concentration skills',
        'Learn to observe without reacting',
        'Build foundation for mindfulness practice'
      ]
    }
  ],

  'acceptance-commitment': [
    {
      id: 'values_clarification',
      name: 'Values Compass',
      type: 'reflection',
      therapyType: 'acceptance-commitment',
      difficulty: 'beginner',
      estimatedDuration: 15,
      description: 'Clarify your core values to guide meaningful action.',
      instructions: [
        'Reflect on what matters most to you',
        'Consider different life domains',
        'Choose your top 5 values',
        'Define what each value means to you',
        'Identify actions aligned with values'
      ],
      requiredInputs: [
        { id: 'top_values', type: 'text', label: 'List your top 5 values', required: true },
        { id: 'value_definitions', type: 'text', label: 'Define what each value means to you', required: true },
        { id: 'current_alignment', type: 'scale', label: 'How well are you living your values? (1-10)', required: true },
        { id: 'action_steps', type: 'text', label: 'What actions would align with your values?', required: true }
      ],
      learningObjectives: [
        'Clarify personal values',
        'Understand values vs. goals',
        'Increase values-based action',
        'Build psychological flexibility'
      ],
      evidenceBase: 'ACT: Hayes et al. (2006), large effect sizes for behavioral change'
    },
    {
      id: 'defusion_exercise',
      name: 'Cognitive Defusion Practice',
      type: 'cognitive',
      therapyType: 'acceptance-commitment',
      difficulty: 'intermediate',
      estimatedDuration: 10,
      description: 'Learn to step back from difficult thoughts and see them as mental events.',
      instructions: [
        'Identify a troubling thought',
        'Notice it as a mental event, not truth',
        'Try "I\'m having the thought that..."',
        'Imagine the thought on a leaf floating by',
        'Practice observing without believing'
      ],
      requiredInputs: [
        { id: 'difficult_thought', type: 'text', label: 'What thought troubles you?', required: true },
        { id: 'thought_power_before', type: 'scale', label: 'How powerful is this thought? (1-10)', required: true },
        { id: 'defusion_technique', type: 'choice', label: 'Which technique helped most?', required: true },
        { id: 'thought_power_after', type: 'scale', label: 'How powerful is it now? (1-10)', required: true }
      ],
      learningObjectives: [
        'Develop psychological distance from thoughts',
        'Learn defusion techniques',
        'Reduce thought-behavior fusion',
        'Increase psychological flexibility'
      ]
    }
  ],

  'mindful-cognitive': [
    {
      id: 'mindful_mood_check',
      name: 'Mindful Mood Check-in',
      type: 'reflection',
      therapyType: 'mindful-cognitive',
      difficulty: 'beginner',
      estimatedDuration: 8,
      description: 'Combine mindfulness with cognitive awareness to monitor mood patterns.',
      instructions: [
        'Pause and take three mindful breaths',
        'Notice your current mood without judgment',
        'Observe any thoughts contributing to this mood',
        'Practice accepting the mood as temporary',
        'Choose a mindful response if needed'
      ],
      requiredInputs: [
        { id: 'current_mood', type: 'scale', label: 'Current mood (1-10, low=difficult)', required: true },
        { id: 'mood_thoughts', type: 'text', label: 'What thoughts accompany this mood?', required: true },
        { id: 'acceptance_level', type: 'scale', label: 'How accepting are you of this mood? (1-10)', required: true },
        { id: 'mindful_response', type: 'text', label: 'What would be a mindful response?', required: false }
      ],
      learningObjectives: [
        'Develop mood awareness',
        'Combine mindfulness with cognitive skills',
        'Practice acceptance of difficult emotions',
        'Choose skillful responses to mood changes'
      ]
    }
  ],

  // Emotion Regulation & Interpersonal
  anger: [
    {
      id: 'anger_diary',
      name: 'Anger Trigger Diary',
      type: 'reflection',
      therapyType: 'anger',
      difficulty: 'beginner',
      estimatedDuration: 10,
      description: 'Track anger episodes to identify patterns and triggers.',
      instructions: [
        'Describe the situation that triggered anger',
        'Rate anger intensity (0-10)',
        'Identify physical warning signs',
        'Note thoughts during the episode',
        'Reflect on alternative responses'
      ],
      requiredInputs: [
        { id: 'trigger_situation', type: 'text', label: 'What triggered your anger?', required: true },
        { id: 'anger_intensity', type: 'scale', label: 'Anger intensity (0-10)', required: true },
        { id: 'physical_signs', type: 'text', label: 'Physical sensations you noticed', required: true },
        { id: 'angry_thoughts', type: 'text', label: 'What thoughts went through your mind?', required: true },
        { id: 'alternative_response', type: 'text', label: 'What could you do differently next time?', required: true }
      ],
      learningObjectives: [
        'Increase anger awareness',
        'Identify personal triggers',
        'Recognize early warning signs',
        'Develop alternative responses'
      ],
      evidenceBase: 'Anger management: Kassinove & Tafrate (2002)'
    }
  ],

  'emotion-regulation': [
    {
      id: 'dbt_stop_skill',
      name: 'STOP Skill Practice',
      type: 'behavioral',
      therapyType: 'emotion-regulation',
      difficulty: 'beginner',
      estimatedDuration: 5,
      description: 'Use the STOP skill to manage intense emotions in the moment.',
      instructions: [
        'STOP: Pause whatever you\'re doing',
        'Take a step back: Create physical/mental space',
        'Observe: Notice thoughts, feelings, body sensations',
        'Proceed: Choose a helpful response',
        'Practice regularly for best results'
      ],
      requiredInputs: [
        { id: 'emotion_intensity', type: 'scale', label: 'Emotion intensity before STOP (1-10)', required: true },
        { id: 'what_observed', type: 'text', label: 'What did you observe?', required: true },
        { id: 'chosen_response', type: 'text', label: 'How did you proceed?', required: true },
        { id: 'emotion_after', type: 'scale', label: 'Emotion intensity after (1-10)', required: true }
      ],
      learningObjectives: [
        'Interrupt emotional reactivity',
        'Develop emotional awareness',
        'Choose skillful responses',
        'Build distress tolerance'
      ],
      evidenceBase: 'DBT skills: Linehan (2014), large effect sizes for emotion regulation'
    }
  ],

  interpersonal: [
    {
      id: 'communication_practice',
      name: 'DEAR MAN Communication',
      type: 'behavioral',
      therapyType: 'interpersonal',
      difficulty: 'intermediate',
      estimatedDuration: 15,
      description: 'Practice assertive communication using the DEAR MAN framework.',
      instructions: [
        'Describe the situation factually',
        'Express your feelings and opinions',
        'Assert your needs clearly',
        'Reinforce benefits of compliance',
        'Stay Mindful, Appear confident, Negotiate'
      ],
      requiredInputs: [
        { id: 'situation_description', type: 'text', label: 'Describe the situation', required: true },
        { id: 'feelings_expressed', type: 'text', label: 'Express your feelings', required: true },
        { id: 'request_assertion', type: 'text', label: 'What are you asking for?', required: true },
        { id: 'reinforcement', type: 'text', label: 'Why would they want to agree?', required: true },
        { id: 'confidence_level', type: 'scale', label: 'How confident do you feel? (1-10)', required: true }
      ],
      learningObjectives: [
        'Practice assertive communication',
        'Improve relationship skills',
        'Set healthy boundaries',
        'Increase interpersonal effectiveness'
      ]
    }
  ],

  // Compassion & Self-Kindness
  'self-compassion': [
    {
      id: 'self_compassion_letter',
      name: 'Self-Compassion Letter',
      type: 'reflection',
      therapyType: 'self-compassion',
      difficulty: 'beginner',
      estimatedDuration: 20,
      description: 'Write a kind, understanding letter to yourself about a difficulty.',
      instructions: [
        'Think of a situation you\'re struggling with',
        'Acknowledge your suffering with kindness',
        'Remember that struggle is part of human experience',
        'Write as you would to a good friend',
        'Focus on understanding rather than judgment'
      ],
      requiredInputs: [
        { id: 'struggle_description', type: 'text', label: 'What are you struggling with?', required: true },
        { id: 'self_criticism', type: 'text', label: 'How do you usually talk to yourself about this?', required: true },
        { id: 'compassionate_letter', type: 'text', label: 'Write your self-compassion letter', required: true },
        { id: 'kindness_level', type: 'scale', label: 'How kind was your letter? (1-10)', required: true }
      ],
      learningObjectives: [
        'Develop self-kindness',
        'Reduce self-criticism',
        'Practice common humanity',
        'Build emotional resilience'
      ],
      evidenceBase: 'Self-compassion: Neff (2003), associated with wellbeing and resilience'
    }
  ],

  'positive-psychology': [
    {
      id: 'gratitude_practice',
      name: 'Three Good Things',
      type: 'reflection',
      therapyType: 'positive-psychology',
      difficulty: 'beginner',
      estimatedDuration: 10,
      description: 'Identify and savor three good things that happened today.',
      instructions: [
        'Think of three good things from today',
        'Write down what happened',
        'Explain why this was good for you',
        'Consider your role in making it happen',
        'Savor the positive feelings'
      ],
      requiredInputs: [
        { id: 'good_thing_1', type: 'text', label: 'First good thing', required: true },
        { id: 'why_good_1', type: 'text', label: 'Why was this good?', required: true },
        { id: 'good_thing_2', type: 'text', label: 'Second good thing', required: true },
        { id: 'why_good_2', type: 'text', label: 'Why was this good?', required: true },
        { id: 'good_thing_3', type: 'text', label: 'Third good thing', required: true },
        { id: 'why_good_3', type: 'text', label: 'Why was this good?', required: true },
        { id: 'mood_impact', type: 'scale', label: 'How did this exercise affect your mood? (1-10)', required: true }
      ],
      learningObjectives: [
        'Increase gratitude awareness',
        'Build positive emotions',
        'Develop optimistic thinking',
        'Enhance life satisfaction'
      ],
      evidenceBase: 'Gratitude interventions: Seligman et al. (2005), increased happiness'
    }
  ],

  strengths: [
    {
      id: 'strengths_spotting',
      name: 'Daily Strengths Spotting',
      type: 'reflection',
      therapyType: 'strengths',
      difficulty: 'beginner',
      estimatedDuration: 8,
      description: 'Identify how you used your character strengths today.',
      instructions: [
        'Review your top character strengths',
        'Think about your day so far',
        'Identify moments you used these strengths',
        'Notice how it felt to use them',
        'Plan to use strengths more intentionally'
      ],
      requiredInputs: [
        { id: 'top_strengths', type: 'text', label: 'What are your top 3 strengths?', required: true },
        { id: 'strength_usage', type: 'text', label: 'How did you use them today?', required: true },
        { id: 'felt_good', type: 'scale', label: 'How good did it feel to use your strengths? (1-10)', required: true },
        { id: 'tomorrow_plan', type: 'text', label: 'How will you use your strengths tomorrow?', required: false }
      ],
      learningObjectives: [
        'Recognize personal strengths',
        'Increase strengths usage',
        'Build self-efficacy',
        'Enhance wellbeing through strengths'
      ]
    }
  ],

  // Lifestyle & Holistic
  sleep: [
    {
      id: 'sleep_hygiene_audit',
      name: 'Sleep Environment Audit',
      type: 'behavioral',
      therapyType: 'sleep',
      difficulty: 'beginner',
      estimatedDuration: 10,
      description: 'Evaluate and optimize your sleep environment and habits.',
      instructions: [
        'Assess your bedroom environment',
        'Review your bedtime routine',
        'Identify sleep disruptors',
        'Plan specific improvements',
        'Set goals for better sleep hygiene'
      ],
      requiredInputs: [
        { id: 'sleep_quality', type: 'scale', label: 'Current sleep quality (1-10)', required: true },
        { id: 'bedtime_routine', type: 'text', label: 'Describe your bedtime routine', required: true },
        { id: 'sleep_disruptors', type: 'text', label: 'What disrupts your sleep?', required: true },
        { id: 'environment_issues', type: 'text', label: 'Any bedroom environment issues?', required: false },
        { id: 'improvement_plan', type: 'text', label: 'What will you change?', required: true }
      ],
      learningObjectives: [
        'Assess sleep environment',
        'Identify sleep hygiene issues',
        'Create improvement plan',
        'Build healthy sleep habits'
      ]
    }
  ],

  relaxation: [
    {
      id: 'progressive_muscle_relaxation',
      name: 'Progressive Muscle Relaxation',
      type: 'interactive',
      therapyType: 'relaxation',
      difficulty: 'beginner',
      estimatedDuration: 15,
      description: 'Learn to release physical tension through systematic muscle relaxation.',
      instructions: [
        'Find a comfortable position',
        'Tense each muscle group for 5 seconds',
        'Release tension and notice the contrast',
        'Work from feet to head systematically',
        'End with whole-body relaxation'
      ],
      requiredInputs: [
        { id: 'tension_before', type: 'scale', label: 'Physical tension before (1-10)', required: true },
        { id: 'completed_sequence', type: 'choice', label: 'Did you complete the full sequence?', required: true },
        { id: 'tension_after', type: 'scale', label: 'Physical tension after (1-10)', required: true },
        { id: 'most_tense_area', type: 'text', label: 'Which area held the most tension?', required: false }
      ],
      learningObjectives: [
        'Learn muscle relaxation technique',
        'Develop body awareness',
        'Reduce physical tension',
        'Create relaxation response'
      ]
    }
  ],

  breathing: [
    {
      id: 'box_breathing',
      name: 'Box Breathing Technique',
      type: 'interactive',
      therapyType: 'breathing',
      difficulty: 'beginner',
      estimatedDuration: 5,
      description: 'Practice box breathing (4-4-4-4) to calm the nervous system.',
      instructions: [
        'Inhale for 4 counts',
        'Hold breath for 4 counts',
        'Exhale for 4 counts',
        'Hold empty lungs for 4 counts',
        'Repeat for 10 cycles'
      ],
      requiredInputs: [
        { id: 'stress_before', type: 'scale', label: 'Stress level before (1-10)', required: true },
        { id: 'completed_cycles', type: 'scale', label: 'How many cycles did you complete?', required: true },
        { id: 'stress_after', type: 'scale', label: 'Stress level after (1-10)', required: true },
        { id: 'found_rhythm', type: 'choice', label: 'Did you find a comfortable rhythm?', required: true }
      ],
      learningObjectives: [
        'Learn structured breathing technique',
        'Activate parasympathetic nervous system',
        'Develop breath awareness',
        'Create portable calming tool'
      ]
    }
  ],

  exercise: [
    {
      id: 'mood_movement_tracker',
      name: 'Movement for Mood',
      type: 'behavioral',
      therapyType: 'exercise',
      difficulty: 'beginner',
      estimatedDuration: 25,
      description: 'Track how different types of movement affect your mood and energy.',
      instructions: [
        'Choose any form of movement you enjoy',
        'Rate mood and energy before activity',
        'Engage in 15-20 minutes of movement',
        'Rate mood and energy after activity',
        'Reflect on the connection'
      ],
      requiredInputs: [
        { id: 'activity_type', type: 'text', label: 'What movement did you choose?', required: true },
        { id: 'mood_before', type: 'scale', label: 'Mood before movement (1-10)', required: true },
        { id: 'energy_before', type: 'scale', label: 'Energy before movement (1-10)', required: true },
        { id: 'duration', type: 'scale', label: 'How many minutes did you move?', required: true },
        { id: 'mood_after', type: 'scale', label: 'Mood after movement (1-10)', required: true },
        { id: 'energy_after', type: 'scale', label: 'Energy after movement (1-10)', required: true }
      ],
      learningObjectives: [
        'Understand exercise-mood connection',
        'Find enjoyable movement activities',
        'Build exercise motivation',
        'Create sustainable movement habits'
      ]
    }
  ],

  nutrition: [
    {
      id: 'food_mood_diary',
      name: 'Food-Mood Connection Tracker',
      type: 'reflection',
      therapyType: 'nutrition',
      difficulty: 'beginner',
      estimatedDuration: 5,
      description: 'Track how different foods affect your mood and energy levels.',
      instructions: [
        'Log what you eat and when',
        'Rate mood before and after eating',
        'Note energy levels throughout the day',
        'Identify foods that boost or drain energy',
        'Plan mood-supporting meals'
      ],
      requiredInputs: [
        { id: 'meal_description', type: 'text', label: 'Describe what you ate', required: true },
        { id: 'mood_before_eating', type: 'scale', label: 'Mood before eating (1-10)', required: true },
        { id: 'mood_after_eating', type: 'scale', label: 'Mood 1 hour after eating (1-10)', required: true },
        { id: 'energy_impact', type: 'scale', label: 'Energy level 2 hours later (1-10)', required: true },
        { id: 'food_mood_connection', type: 'text', label: 'What did you notice about this food?', required: false }
      ],
      learningObjectives: [
        'Understand food-mood connections',
        'Identify mood-supporting foods',
        'Develop mindful eating habits',
        'Build nutritional awareness'
      ]
    }
  ],

  // Specialized Therapies
  trauma: [
    {
      id: 'safe_place_visualization',
      name: 'Safe Place Visualization',
      type: 'interactive',
      therapyType: 'trauma',
      difficulty: 'beginner',
      estimatedDuration: 10,
      description: 'Create and strengthen a mental safe place for emotional regulation.',
      instructions: [
        'Imagine a place where you feel completely safe',
        'Engage all your senses in this image',
        'Notice colors, sounds, smells, textures',
        'Practice returning to this place when stressed',
        'Strengthen the image with regular practice'
      ],
      requiredInputs: [
        { id: 'safe_place_description', type: 'text', label: 'Describe your safe place', required: true },
        { id: 'safety_feeling', type: 'scale', label: 'How safe does this place feel? (1-10)', required: true },
        { id: 'sensory_details', type: 'text', label: 'What sensory details make it vivid?', required: true },
        { id: 'access_ease', type: 'scale', label: 'How easily can you access this image? (1-10)', required: true }
      ],
      learningObjectives: [
        'Create internal safety resource',
        'Develop self-soothing skills',
        'Build emotional regulation capacity',
        'Prepare for trauma processing work'
      ],
      evidenceBase: 'Safe place: Van der Kolk (2014), foundational trauma stabilization'
    }
  ],

  schema: [
    {
      id: 'schema_pattern_recognition',
      name: 'Life Pattern Recognition',
      type: 'reflection',
      therapyType: 'schema',
      difficulty: 'intermediate',
      estimatedDuration: 20,
      description: 'Identify recurring patterns in relationships and life experiences.',
      instructions: [
        'Think about recurring themes in your relationships',
        'Notice patterns in your emotional reactions',
        'Identify beliefs about yourself and others',
        'Connect patterns to early experiences',
        'Recognize when patterns are activated'
      ],
      requiredInputs: [
        { id: 'relationship_patterns', type: 'text', label: 'What patterns do you notice in relationships?', required: true },
        { id: 'emotional_patterns', type: 'text', label: 'What emotional reactions repeat?', required: true },
        { id: 'core_beliefs', type: 'text', label: 'What beliefs about yourself seem central?', required: true },
        { id: 'early_connections', type: 'text', label: 'How might these connect to early experiences?', required: false },
        { id: 'trigger_awareness', type: 'scale', label: 'How aware are you when patterns activate? (1-10)', required: true }
      ],
      learningObjectives: [
        'Identify life patterns and schemas',
        'Connect present to past experiences',
        'Develop pattern awareness',
        'Begin schema healing process'
      ]
    }
  ],

  narrative: [
    {
      id: 'story_reauthoring',
      name: 'Reauthoring Your Story',
      type: 'reflection',
      therapyType: 'narrative',
      difficulty: 'intermediate',
      estimatedDuration: 25,
      description: 'Reframe your life story to emphasize agency, growth, and resilience.',
      instructions: [
        'Write your story from a problem-saturated perspective',
        'Identify unique outcomes - times when problems didn\'t dominate',
        'Rewrite focusing on your agency and resilience',
        'Highlight growth, learning, and strength',
        'Consider what this new story says about who you are'
      ],
      requiredInputs: [
        { id: 'problem_story', type: 'text', label: 'How might you tell your story focusing on problems?', required: true },
        { id: 'unique_outcomes', type: 'text', label: 'When have you overcome or resisted these problems?', required: true },
        { id: 'preferred_story', type: 'text', label: 'Rewrite your story emphasizing your agency and growth', required: true },
        { id: 'identity_reflection', type: 'text', label: 'What does this new story say about who you are?', required: true },
        { id: 'story_preference', type: 'scale', label: 'Which story feels more true to you? (1=problem, 10=preferred)', required: true }
      ],
      learningObjectives: [
        'Deconstruct problem-saturated narratives',
        'Identify unique outcomes and agency',
        'Develop preferred identity stories',
        'Increase sense of personal agency'
      ]
    }
  ],

  motivation: [
    {
      id: 'change_motivation_explorer',
      name: 'Motivation for Change Explorer',
      type: 'reflection',
      therapyType: 'motivation',
      difficulty: 'beginner',
      estimatedDuration: 15,
      description: 'Explore and enhance your motivation for making positive changes.',
      instructions: [
        'Identify something you want to change',
        'Explore reasons for and against change',
        'Rate importance and confidence for change',
        'Identify what would increase your motivation',
        'Plan small steps toward change'
      ],
      requiredInputs: [
        { id: 'change_goal', type: 'text', label: 'What would you like to change?', required: true },
        { id: 'reasons_for_change', type: 'text', label: 'Why do you want to make this change?', required: true },
        { id: 'reasons_against', type: 'text', label: 'What keeps you from changing?', required: true },
        { id: 'importance_rating', type: 'scale', label: 'How important is this change? (1-10)', required: true },
        { id: 'confidence_rating', type: 'scale', label: 'How confident are you that you can change? (1-10)', required: true },
        { id: 'next_steps', type: 'text', label: 'What small step could you take?', required: true }
      ],
      learningObjectives: [
        'Explore change ambivalence',
        'Clarify motivation for change',
        'Build confidence in ability to change',
        'Plan concrete action steps'
      ]
    }
  ],

  'solution-focused': [
    {
      id: 'miracle_question',
      name: 'The Miracle Question',
      type: 'reflection',
      therapyType: 'solution-focused',
      difficulty: 'beginner',
      estimatedDuration: 15,
      description: 'Envision your preferred future to identify solutions and goals.',
      instructions: [
        'Imagine waking up and your problems are solved',
        'Describe in detail what would be different',
        'How would others notice the change?',
        'What would you be doing differently?',
        'Identify small signs of this miracle happening now'
      ],
      requiredInputs: [
        { id: 'miracle_description', type: 'text', label: 'If a miracle happened overnight, what would be different?', required: true },
        { id: 'others_notice', type: 'text', label: 'How would others notice this change?', required: true },
        { id: 'different_actions', type: 'text', label: 'What would you be doing differently?', required: true },
        { id: 'current_signs', type: 'text', label: 'Are any small signs of this miracle already happening?', required: true },
        { id: 'hope_level', type: 'scale', label: 'How hopeful does this vision make you feel? (1-10)', required: true }
      ],
      learningObjectives: [
        'Envision preferred future',
        'Identify solution-focused goals',
        'Notice existing progress',
        'Build hope and motivation'
      ]
    }
  ],

  // General
  general: [
    {
      id: 'daily_mood_check',
      name: 'Daily Mood Check-in',
      type: 'reflection',
      therapyType: 'general',
      difficulty: 'beginner',
      estimatedDuration: 5,
      description: 'Regular mood monitoring to build self-awareness and track patterns.',
      instructions: [
        'Rate your overall mood today',
        'Identify what influenced your mood',
        'Notice any patterns or triggers',
        'Set an intention for mood support',
        'Choose one self-care action'
      ],
      requiredInputs: [
        { id: 'mood_rating', type: 'scale', label: 'Overall mood today (1-10)', required: true },
        { id: 'mood_influences', type: 'text', label: 'What influenced your mood today?', required: true },
        { id: 'energy_level', type: 'scale', label: 'Energy level (1-10)', required: true },
        { id: 'stress_level', type: 'scale', label: 'Stress level (1-10)', required: true },
        { id: 'self_care_plan', type: 'text', label: 'What self-care will you do today?', required: false }
      ],
      learningObjectives: [
        'Build emotional awareness',
        'Track mood patterns',
        'Identify mood influences',
        'Plan supportive actions'
      ]
    }
  ]
};

// Default exercises that appear for all assessment types
export const universalExercises: TherapyExercise[] = [
  {
    id: 'gratitude_moment',
    name: 'Gratitude Moment',
    type: 'reflection',
    therapyType: 'general',
    difficulty: 'beginner',
    estimatedDuration: 3,
    description: 'Quick gratitude practice to shift perspective and boost mood.',
    instructions: [
      'Take a deep breath',
      'Think of something you\'re grateful for right now',
      'Notice how this feels in your body',
      'Hold this feeling for a moment',
      'Carry this appreciation with you'
    ],
    requiredInputs: [
      { id: 'gratitude_item', type: 'text', label: 'What are you grateful for?', required: true },
      { id: 'body_sensation', type: 'text', label: 'How does gratitude feel in your body?', required: false },
      { id: 'mood_shift', type: 'scale', label: 'Did this shift your mood? (1-10)', required: true }
    ],
    learningObjectives: [
      'Practice quick mood regulation',
      'Build gratitude awareness',
      'Develop positive emotion skills',
      'Create portable wellbeing tool'
    ]
  }
];
