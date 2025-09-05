import { Assessment, QuestionResponse, AssessmentType, TherapyRecommendation } from '@/types';
import { therapyExercises } from '@/data/exercises';

interface PatternAnalysis {
  cognitivePatterns: string[];
  emotionalPatterns: string[];
  behavioralPatterns: string[];
  severityLevel: 'mild' | 'moderate' | 'severe';
  confidenceScore: number;
}

interface TherapyMatch {
  therapyType: AssessmentType;
  score: number;
  reasoning: string[];
  evidenceLevel: 'strong' | 'moderate' | 'emerging';
}

export class TherapyRecommendationEngine {
  private analysisCache: Map<string, PatternAnalysis> = new Map();

  /**
   * Generate comprehensive therapy recommendations based on assessment results
   */
  async generateRecommendations(assessment: Assessment): Promise<TherapyRecommendation[]> {
    const patternAnalysis = this.analyzePatterns(assessment);
    const therapyMatches = this.matchToTherapies(patternAnalysis, assessment.type);
    const recommendations = this.buildRecommendations(therapyMatches, patternAnalysis);

    return recommendations.sort((a, b) => b.confidence - a.confidence);
  }

  /**
   * Analyze response patterns to identify cognitive, emotional, and behavioral patterns
   */
  private analyzePatterns(assessment: Assessment): PatternAnalysis {
    const cacheKey = this.generateCacheKey(assessment);
    
    if (this.analysisCache.has(cacheKey)) {
      return this.analysisCache.get(cacheKey)!;
    }

    const cognitivePatterns: string[] = [];
    const emotionalPatterns: string[] = [];
    const behavioralPatterns: string[] = [];
    let totalSeverity = 0;
    let severityCount = 0;

    // Analyze each response for patterns
    assessment.responses.forEach(response => {
      const patterns = this.identifyResponsePatterns(response, assessment.type);
      cognitivePatterns.push(...patterns.cognitive);
      emotionalPatterns.push(...patterns.emotional);
      behavioralPatterns.push(...patterns.behavioral);
      
      if (patterns.severity > 0) {
        totalSeverity += patterns.severity;
        severityCount++;
      }
    });

    // Calculate overall severity
    const averageSeverity = severityCount > 0 ? totalSeverity / severityCount : 0;
    const severityLevel: 'mild' | 'moderate' | 'severe' = 
      averageSeverity >= 7 ? 'severe' : averageSeverity >= 4 ? 'moderate' : 'mild';

    // Calculate confidence based on response completeness and consistency
    const confidenceScore = this.calculateConfidence(assessment);

    const analysis: PatternAnalysis = {
      cognitivePatterns: Array.from(new Set(cognitivePatterns)),
      emotionalPatterns: Array.from(new Set(emotionalPatterns)),
      behavioralPatterns: Array.from(new Set(behavioralPatterns)),
      severityLevel,
      confidenceScore
    };

    this.analysisCache.set(cacheKey, analysis);
    return analysis;
  }

  /**
   * Identify patterns from individual response
   */
  private identifyResponsePatterns(response: QuestionResponse, assessmentType: AssessmentType): {
    cognitive: string[];
    emotional: string[];
    behavioral: string[];
    severity: number;
  } {
    const cognitive: string[] = [];
    const emotional: string[] = [];
    const behavioral: string[] = [];
    let severity = 0;

    // Analyze based on response value and question context
    if (typeof response.answer === 'string') {
      // Text analysis for open-ended responses
      const text = response.answer.toLowerCase();
      
      // Cognitive patterns
      if (text.includes('always') || text.includes('never') || text.includes('everyone') || text.includes('no one')) {
        cognitive.push('all-or-nothing thinking');
      }
      if (text.includes('terrible') || text.includes('disaster') || text.includes('worst')) {
        cognitive.push('catastrophizing');
      }
      if (text.includes('should') || text.includes('must') || text.includes('have to')) {
        cognitive.push('should statements');
      }
      if (text.includes('my fault') || text.includes('blame myself')) {
        cognitive.push('self-blame');
      }

      // Emotional patterns
      if (text.includes('overwhelmed') || text.includes('can\'t cope')) {
        emotional.push('emotional overwhelm');
      }
      if (text.includes('numb') || text.includes('empty') || text.includes('nothing')) {
        emotional.push('emotional numbing');
      }
      if (text.includes('angry') || text.includes('rage') || text.includes('furious')) {
        emotional.push('anger reactivity');
      }

      // Behavioral patterns
      if (text.includes('avoid') || text.includes('escape') || text.includes('stay away')) {
        behavioral.push('avoidance');
      }
      if (text.includes('check') || text.includes('repeat') || text.includes('ritual')) {
        behavioral.push('compulsive behavior');
      }
      if (text.includes('isolate') || text.includes('withdraw') || text.includes('alone')) {
        behavioral.push('social withdrawal');
      }

    } else if (typeof response.answer === 'number') {
      // Scale analysis for numerical responses
      if (response.answer >= 8) {
        severity = 8;
        if (assessmentType === 'anxiety') {
          emotional.push('high anxiety');
        } else if (assessmentType === 'anger') {
          emotional.push('intense anger');
        }
      } else if (response.answer >= 6) {
        severity = 6;
        emotional.push('moderate distress');
      } else if (response.answer >= 4) {
        severity = 4;
        emotional.push('mild distress');
      }
    }

    return { cognitive, emotional, behavioral, severity };
  }

  /**
   * Match identified patterns to appropriate therapies
   */
  private matchToTherapies(analysis: PatternAnalysis, primaryType: AssessmentType): TherapyMatch[] {
    const matches: TherapyMatch[] = [];

    // Primary therapy (from assessment type)
    matches.push({
      therapyType: primaryType,
      score: 1.0,
      reasoning: [`Primary assessment focus: ${primaryType}`],
      evidenceLevel: 'strong'
    });

    // CBT for cognitive patterns
    if (analysis.cognitivePatterns.length > 0) {
      matches.push({
        therapyType: 'anxiety', // CBT techniques
        score: 0.9,
        reasoning: [`Identified cognitive patterns: ${analysis.cognitivePatterns.join(', ')}`],
        evidenceLevel: 'strong'
      });
    }

    // DBT for emotional regulation issues
    if (analysis.emotionalPatterns.includes('emotional overwhelm') || 
        analysis.emotionalPatterns.includes('anger reactivity')) {
      matches.push({
        therapyType: 'emotion-regulation',
        score: 0.85,
        reasoning: ['Emotional regulation challenges identified'],
        evidenceLevel: 'strong'
      });
    }

    // Behavioral Activation for avoidance patterns
    if (analysis.behavioralPatterns.includes('avoidance') || 
        analysis.behavioralPatterns.includes('social withdrawal')) {
      matches.push({
        therapyType: 'behavioral-activation',
        score: 0.8,
        reasoning: ['Avoidance and withdrawal patterns suggest behavioral activation'],
        evidenceLevel: 'strong'
      });
    }

    // Mindfulness for high severity or emotional numbing
    if (analysis.severityLevel === 'severe' || 
        analysis.emotionalPatterns.includes('emotional numbing')) {
      matches.push({
        therapyType: 'mindfulness',
        score: 0.75,
        reasoning: ['Mindfulness supports emotional awareness and regulation'],
        evidenceLevel: 'strong'
      });
    }

    // ACT for multiple pattern types (psychological flexibility)
    if (analysis.cognitivePatterns.length > 2 && analysis.behavioralPatterns.length > 1) {
      matches.push({
        therapyType: 'acceptance-commitment',
        score: 0.7,
        reasoning: ['Multiple patterns suggest need for psychological flexibility'],
        evidenceLevel: 'strong'
      });
    }

    // Self-compassion for self-blame patterns
    if (analysis.cognitivePatterns.includes('self-blame')) {
      matches.push({
        therapyType: 'self-compassion',
        score: 0.65,
        reasoning: ['Self-criticism patterns identified'],
        evidenceLevel: 'moderate'
      });
    }

    // ERP for compulsive behaviors
    if (analysis.behavioralPatterns.includes('compulsive behavior')) {
      matches.push({
        therapyType: 'ocd',
        score: 0.9,
        reasoning: ['Compulsive behavior patterns suggest ERP approach'],
        evidenceLevel: 'strong'
      });
    }

    return matches;
  }

  /**
   * Build structured recommendations from therapy matches
   */
  private buildRecommendations(matches: TherapyMatch[], analysis: PatternAnalysis): TherapyRecommendation[] {
    const recommendations: TherapyRecommendation[] = [];

    matches.forEach((match, index) => {
      const priority: 'primary' | 'secondary' | 'supplementary' = 
        index === 0 ? 'primary' : index < 3 ? 'secondary' : 'supplementary';

      const availableExercises = therapyExercises[match.therapyType] || [];
      const suggestedExercises = this.selectExercises(availableExercises, analysis);

      const recommendation: TherapyRecommendation = {
        therapyType: match.therapyType,
        priority,
        confidence: match.score * analysis.confidenceScore,
        reasoning: match.reasoning,
        suggestedExercises: suggestedExercises.map(ex => ex.id),
        estimatedDuration: this.estimateDuration(analysis.severityLevel),
        successPredictors: this.getSuccessPredictors(match.therapyType, analysis),
        potentialBarriers: this.getBarriers(match.therapyType, analysis)
      };

      recommendations.push(recommendation);
    });

    return recommendations;
  }

  /**
   * Select appropriate exercises based on difficulty and patterns
   */
  private selectExercises(exercises: any[], analysis: PatternAnalysis): any[] {
    const difficultyLevel = analysis.severityLevel === 'mild' ? 'beginner' : 
                           analysis.severityLevel === 'moderate' ? 'intermediate' : 'beginner';

    return exercises
      .filter(ex => ex.difficulty === difficultyLevel || ex.difficulty === 'beginner')
      .slice(0, 3); // Top 3 exercises
  }

  /**
   * Estimate therapy duration based on severity
   */
  private estimateDuration(severity: 'mild' | 'moderate' | 'severe'): string {
    switch (severity) {
      case 'mild': return '2-4 weeks';
      case 'moderate': return '4-8 weeks';
      case 'severe': return '8-12 weeks';
    }
  }

  /**
   * Get success predictors for therapy type
   */
  private getSuccessPredictors(therapyType: AssessmentType, analysis: PatternAnalysis): string[] {
    const general = [
      'Regular practice and engagement',
      'Willingness to try new approaches'
    ];

    const specific: Record<string, string[]> = {
      'anxiety': ['Motivated to reduce avoidance', 'Open to exposure exercises'],
      'ocd': ['Willing to resist compulsions', 'Understanding of ERP principles'],
      'mindfulness': ['Interest in present-moment awareness', 'Patience with practice'],
      'behavioral-activation': ['Motivation to increase activities', 'Social support available'],
      'emotion-regulation': ['Recognition of emotional patterns', 'Commitment to skill practice']
    };

    return [...general, ...(specific[therapyType] || [])];
  }

  /**
   * Get potential barriers for therapy type
   */
  private getBarriers(therapyType: AssessmentType, analysis: PatternAnalysis): string[] {
    const barriers: string[] = [];

    if (analysis.severityLevel === 'severe') {
      barriers.push('High symptom severity may slow initial progress');
    }

    if (analysis.cognitivePatterns.includes('all-or-nothing thinking')) {
      barriers.push('Perfectionist thinking may interfere with practice');
    }

    if (analysis.behavioralPatterns.includes('avoidance')) {
      barriers.push('Avoidance patterns may resist exposure exercises');
    }

    const specificBarriers: Record<string, string[]> = {
      'anxiety': ['Fear of anxiety sensations', 'Overprotective behaviors'],
      'ocd': ['Fear of not performing compulsions', 'Doubt about ERP safety'],
      'mindfulness': ['Restless mind', 'Impatience with slow progress'],
      'behavioral-activation': ['Low energy levels', 'Lack of social support']
    };

    barriers.push(...(specificBarriers[therapyType] || []));

    return barriers;
  }

  /**
   * Calculate confidence score based on assessment quality
   */
  private calculateConfidence(assessment: Assessment): number {
    const totalQuestions = assessment.responses.length;
    const completedQuestions = assessment.responses.filter(r => r.answer !== '').length;
    const completionRate = completedQuestions / totalQuestions;

    // Factor in response quality (longer text responses get higher scores)
    const qualityScore = assessment.responses.reduce((acc, response) => {
      if (typeof response.answer === 'string' && response.answer.length > 10) {
        return acc + 0.1;
      }
      return acc;
    }, 0) / totalQuestions;

    return Math.min(1.0, completionRate * 0.7 + qualityScore * 0.3);
  }

  /**
   * Generate cache key for analysis
   */
  private generateCacheKey(assessment: Assessment): string {
    const responseHash = assessment.responses
      .map(r => `${r.questionId}:${r.answer}`)
      .join('|');
    
    return `${assessment.type}:${responseHash}`;
  }

  /**
   * Get exercise recommendations for a specific therapy type
   */
  getExerciseRecommendations(therapyType: AssessmentType, difficulty: 'beginner' | 'intermediate' | 'advanced' = 'beginner'): any[] {
    const exercises = therapyExercises[therapyType] || [];
    return exercises.filter(ex => ex.difficulty === difficulty).slice(0, 5);
  }

  /**
   * Track exercise completion and update recommendations
   */
  updateRecommendationsBasedOnProgress(
    userId: string, 
    completedExercises: string[], 
    currentRecommendations: TherapyRecommendation[]
  ): TherapyRecommendation[] {
    // This would integrate with progress tracking to refine recommendations
    // For now, return current recommendations
    return currentRecommendations;
  }
}

// Export singleton instance
export const therapyEngine = new TherapyRecommendationEngine();
