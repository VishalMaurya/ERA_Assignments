# Psychological Journey - AI-Powered Self Assessment v1.1.0

An immersive psychological self-assessment website that provides personalized insights through AI-powered analysis. This application offers guided journeys across 28 different assessment types with floating navigation, enhanced dashboard analytics, and robust error handling.

## ✨ Features

### 🆕 Latest in v1.1.0
- **🎯 Floating Navigation**: Always-visible "Begin Journey" button that adapts to your selection
- **🛡️ Enhanced Error Handling**: Robust dashboard with comprehensive error boundaries
- **📊 Advanced Analytics**: Never shows "N/A" - comprehensive time tracking and insights
- **📱 Improved Mobile UX**: Better responsive design with touch-optimized interactions
- **🎨 28 Assessment Types**: Expanded from 4 to 28 different psychological assessments

### 🚀 Core Features
- **🧠 AI-Powered Reports**: Personalized insights generated using Google's Gemini 2.0 Flash
- **🎨 Immersive Environments**: Beautiful animated backgrounds that change with each question
- **📊 Comprehensive Assessment**: Multiple question types including MCQ, scales, open-ended, and mood tracking
- **🎯 Evidence-Based Recommendations**: Therapeutic approaches like CBT, DBT, ACT, ERP, and mindfulness
- **📈 Progress Tracking**: Visual journey with milestone indicators and precise timing
- **💾 Data Privacy**: All data stored locally in your browser with secure API key management
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **🔄 Auto-Refresh**: Dashboard automatically updates when you return to the tab

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd psychological-journey
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000` (or `http://localhost:3001` if port 3000 is in use)

### Setting up Gemini AI

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. When prompted in the application, enter your API key

**Note**: Your API key is stored securely in your browser's local storage and is never sent to our servers.

## 🎮 How to Use

1. **Choose Your Journey**: Select from Anxiety, OCD, Anger Management, or General Wellbeing assessments
2. **Navigate the Experience**: Answer questions in beautiful animated environments
3. **Track Progress**: Watch your journey unfold with visual progress indicators
4. **Skip or Go Back**: Complete freedom to skip questions or revisit previous ones
5. **Generate Report**: Get your personalized AI-powered insights and recommendations
6. **Download & Save**: Export your reports and track progress over time

## 🏗️ Project Structure

```
src/
├── app/                    # Next.js 14 App Router
│   ├── assessment/[type]/  # Dynamic assessment routes
│   ├── report/[id]/        # Dynamic report routes
│   └── page.tsx           # Landing page
├── components/
│   ├── assessment/        # Assessment-related components
│   ├── report/           # Report generation & display
│   └── ui/               # Reusable UI components
├── data/                 # Assessment questions and configurations
├── lib/                  # External service integrations (Gemini AI)
├── types/               # TypeScript type definitions
└── utils/               # Helper functions and utilities
```

## 🧠 Assessment Types (28 Categories)

### 🧠 Cognitive Behavioral Therapy (CBT) - 5 Assessments
- **Anxiety**: Patterns, triggers, and coping mechanisms
- **OCD**: Obsessive thoughts and compulsive behaviors
- **Behavioral Activation**: Overcoming avoidance patterns
- **Habit Reversal**: Identifying and replacing unwanted habits
- **Problem Solving**: Structured approaches to life challenges

### 🧘 Mindfulness & Acceptance - 3 Assessments
- **Mindfulness**: Present-moment awareness practices
- **Acceptance & Commitment**: Value-driven actions despite difficult thoughts
- **Mindful Cognitive**: Blending mindfulness with cognitive strategies

### ❤️ Emotion Regulation & Interpersonal - 3 Assessments
- **Anger Management**: Triggers, expression, and healthy coping
- **Emotion Regulation**: Managing intense emotions and mood fluctuations
- **Interpersonal Skills**: Communication and relationship enhancement

### 💝 Self-Compassion & Strengths - 3 Assessments
- **Self-Compassion**: Developing kindness toward yourself
- **Positive Psychology**: Strengths, gratitude, and optimistic thinking
- **Personal Strengths**: Identifying and leveraging your unique abilities

### 🌱 Lifestyle & Wellness - 5 Assessments
- **Sleep Health**: Quality sleep and healthy bedtime routines
- **Relaxation & Stress Relief**: Effective stress management techniques
- **Breathing & Mindfulness**: Breathing techniques for calm and focus
- **Exercise & Movement**: Physical activity for mental health benefits
- **Nutrition & Wellness**: Connection between nutrition and emotional wellbeing

### 🎯 Specialized Therapies - 5 Assessments
- **Trauma Recovery**: Processing difficult experiences safely
- **Schema Therapy**: Healing deep-rooted relationship patterns
- **Narrative Therapy**: Reframing your life story for empowerment
- **Motivational Enhancement**: Exploring and enhancing motivation for change
- **Solution-Focused**: Building on what works to create positive change

### 🌟 General Wellbeing - 1 Assessment
- **General**: Overall mental health and life satisfaction assessment

> **📋 Total**: 28 evidence-based assessments covering the full spectrum of psychological wellbeing

## 🎨 Design Philosophy

- **Calming**: Soft colors and gentle animations create a therapeutic environment
- **Non-Clinical**: Warm, supportive language instead of medical terminology  
- **Empowering**: Focus on growth and self-compassion
- **Accessible**: Clear navigation with skip options and hints
- **Beautiful**: Immersive environments that make assessment feel like a journey

## 🔒 Privacy & Security

- **Local Storage**: All your data stays on your device
- **No Tracking**: We don't collect personal information
- **API Key Security**: Your Gemini API key is stored locally and encrypted
- **Data Export**: Full control over your data with export functionality

## 🛠️ Built With

- **Frontend**: Next.js 14 (App Router), TypeScript, TailwindCSS
- **Animations**: Framer Motion with GPU acceleration
- **Charts**: Recharts for analytics visualization
- **Icons**: Lucide React (clean, consistent icon library)
- **AI**: Google Gemini 2.0 Flash API with performance tracking
- **Storage**: Browser Local/Session Storage with secure API key management
- **State**: React Hooks with localStorage persistence
- **Error Handling**: Comprehensive error boundaries and recovery mechanisms

## 📦 Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

## 🤝 Contributing

This is a therapeutic tool designed to help people explore their mental health. Contributions should focus on:

- Improving accessibility
- Adding evidence-based therapeutic content
- Enhancing user experience
- Strengthening privacy protections

## ⚠️ Important Disclaimers

- **Not Medical Advice**: This tool is for self-reflection and educational purposes only
- **Not a Substitute**: Cannot replace professional mental health care
- **Emergency Support**: If experiencing crisis, contact emergency services or crisis hotlines
- **Professional Help**: Severe symptoms require consultation with qualified healthcare providers

## 🛠️ Technical Support

Having trouble with the application?
- **📋 Architecture**: See our [Solution Architecture Guide](./SOLUTION_ARCHITECTURE.md) for technical details
- **🔧 Troubleshooting**: Check our [Troubleshooting Guide](./TROUBLESHOOTING.md) for common solutions
- **🔑 API Key Problems**: Ensure your Gemini API key is valid and properly configured
- **🌐 Browser Issues**: Check the browser console for detailed error messages
- **📡 Connection Problems**: Verify your internet connection for API calls
- **📊 Dashboard Issues**: The dashboard automatically handles errors and provides fallback states

## 📞 Support

If you're experiencing mental health difficulties:
- **Crisis**: Call 988 (Suicide & Crisis Lifeline) or emergency services
- **Support**: Contact a licensed mental health professional
- **Resources**: Visit SAMHSA National Helpline: 1-800-662-4357

## 📄 License

MIT License - see LICENSE file for details

---

**Remember**: Taking care of your mental health is brave. You're not alone in this journey. 💙
