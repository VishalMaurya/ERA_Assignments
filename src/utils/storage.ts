import { Assessment, AssessmentReport, User } from '@/types';
import Cookies from 'js-cookie';

const STORAGE_KEYS = {
  USER: 'therapy_user',
  CURRENT_ASSESSMENT: 'current_assessment',
  ASSESSMENTS: 'user_assessments',
  REPORTS: 'user_reports',
  GEMINI_API_KEY: 'gemini_api_key',
  PROGRESS: 'assessment_progress'
};

export class StorageService {
  // User management
  static saveUser(user: User): void {
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
  }

  static getUser(): User | null {
    const userData = localStorage.getItem(STORAGE_KEYS.USER);
    return userData ? JSON.parse(userData) : null;
  }

  static removeUser(): void {
    localStorage.removeItem(STORAGE_KEYS.USER);
  }

  // Assessment management
  static saveCurrentAssessment(assessment: Assessment): void {
    localStorage.setItem(STORAGE_KEYS.CURRENT_ASSESSMENT, JSON.stringify(assessment));
  }

  static getCurrentAssessment(): Assessment | null {
    const assessmentData = localStorage.getItem(STORAGE_KEYS.CURRENT_ASSESSMENT);
    if (!assessmentData) return null;
    
    const assessment = JSON.parse(assessmentData);
    // Convert date strings back to Date objects
    return {
      ...assessment,
      startedAt: new Date(assessment.startedAt),
      completedAt: assessment.completedAt ? new Date(assessment.completedAt) : undefined,
      responses: assessment.responses.map((response: any) => ({
        ...response,
        timestamp: new Date(response.timestamp)
      }))
    };
  }

  static clearCurrentAssessment(): void {
    localStorage.removeItem(STORAGE_KEYS.CURRENT_ASSESSMENT);
  }

  // Completed assessments
  static saveAssessment(assessment: Assessment): void {
    const assessments = this.getAssessments();
    const existingIndex = assessments.findIndex(a => a.id === assessment.id);
    
    if (existingIndex >= 0) {
      assessments[existingIndex] = assessment;
    } else {
      assessments.push(assessment);
    }
    
    localStorage.setItem(STORAGE_KEYS.ASSESSMENTS, JSON.stringify(assessments));
  }

  static getAssessments(): Assessment[] {
    const assessmentsData = localStorage.getItem(STORAGE_KEYS.ASSESSMENTS);
    if (!assessmentsData) return [];
    
    const assessments = JSON.parse(assessmentsData);
    // Convert date strings back to Date objects
    return assessments.map((assessment: any) => ({
      ...assessment,
      startedAt: new Date(assessment.startedAt),
      completedAt: assessment.completedAt ? new Date(assessment.completedAt) : undefined,
      responses: assessment.responses.map((response: any) => ({
        ...response,
        timestamp: new Date(response.timestamp)
      }))
    }));
  }

  // Reports management
  static saveReport(report: AssessmentReport): void {
    const reports = this.getReports();
    const existingIndex = reports.findIndex(r => r.id === report.id);
    
    if (existingIndex >= 0) {
      reports[existingIndex] = report;
    } else {
      reports.push(report);
    }
    
    localStorage.setItem(STORAGE_KEYS.REPORTS, JSON.stringify(reports));
  }

  static getReports(): AssessmentReport[] {
    const reportsData = localStorage.getItem(STORAGE_KEYS.REPORTS);
    return reportsData ? JSON.parse(reportsData) : [];
  }

  static getReportByAssessmentId(assessmentId: string): AssessmentReport | null {
    const reports = this.getReports();
    return reports.find(r => r.assessmentId === assessmentId) || null;
  }

  // API Key management (stored securely in cookies with httpOnly-like behavior)
  static saveGeminiApiKey(apiKey: string): void {
    // Store in sessionStorage for security (cleared when browser closes)
    sessionStorage.setItem(STORAGE_KEYS.GEMINI_API_KEY, apiKey);
    // Also set a secure cookie
    Cookies.set(STORAGE_KEYS.GEMINI_API_KEY, apiKey, { 
      secure: true, 
      sameSite: 'strict',
      expires: 1/24 // 1 hour
    });
  }

  static getGeminiApiKey(): string | null {
    // First try sessionStorage, then cookies
    return sessionStorage.getItem(STORAGE_KEYS.GEMINI_API_KEY) || 
           Cookies.get(STORAGE_KEYS.GEMINI_API_KEY) || null;
  }

  static removeGeminiApiKey(): void {
    sessionStorage.removeItem(STORAGE_KEYS.GEMINI_API_KEY);
    Cookies.remove(STORAGE_KEYS.GEMINI_API_KEY);
  }

  // Progress tracking
  static saveProgress(data: any): void {
    localStorage.setItem(STORAGE_KEYS.PROGRESS, JSON.stringify(data));
  }

  static getProgress(): any {
    const progressData = localStorage.getItem(STORAGE_KEYS.PROGRESS);
    return progressData ? JSON.parse(progressData) : null;
  }

  // Clear all data
  static clearAllData(): void {
    Object.values(STORAGE_KEYS).forEach(key => {
      localStorage.removeItem(key);
      sessionStorage.removeItem(key);
      Cookies.remove(key);
    });
  }

  // Export data for user
  static exportUserData(): string {
    const userData = {
      user: this.getUser(),
      assessments: this.getAssessments(),
      reports: this.getReports(),
      exportedAt: new Date().toISOString()
    };
    
    return JSON.stringify(userData, null, 2);
  }

  // Import data for user
  static importUserData(jsonData: string): boolean {
    try {
      const data = JSON.parse(jsonData);
      
      if (data.user) this.saveUser(data.user);
      if (data.assessments) {
        data.assessments.forEach((assessment: Assessment) => {
          this.saveAssessment(assessment);
        });
      }
      if (data.reports) {
        data.reports.forEach((report: AssessmentReport) => {
          this.saveReport(report);
        });
      }
      
      return true;
    } catch (error) {
      console.error('Error importing user data:', error);
      return false;
    }
  }
}
