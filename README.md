# Psychological Journey - AI-Powered Self Assessment

An immersive psychological self-assessment website that provides personalized insights through AI-powered analysis. This application offers guided journeys for anxiety, OCD, anger management, and general wellbeing.

## ✨ Features

- **🧠 AI-Powered Reports**: Personalized insights generated using Google's Gemini AI
- **🎨 Immersive Environments**: Beautiful animated backgrounds that change with each question
- **📊 Comprehensive Assessment**: Multiple question types including MCQ, scales, open-ended, and mood tracking
- **🎯 Evidence-Based Recommendations**: Therapeutic approaches like CBT, DBT, ACT, ERP, and mindfulness
- **📈 Progress Tracking**: Visual journey with milestone indicators
- **💾 Data Privacy**: All data stored locally in your browser
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

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
   Navigate to `http://localhost:3000`

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

## 🧠 Assessment Types

### Anxiety Assessment
- **Focus**: Anxiety patterns, triggers, and coping mechanisms
- **Therapies**: CBT, ACT, MBSR, Mindfulness, Behavioral Activation
- **Questions**: 8 interactive questions with mood tracking

### OCD Assessment  
- **Focus**: Obsessive thoughts and compulsive behaviors
- **Therapies**: ERP, HRT, ACT, CBT
- **Questions**: 8 questions exploring thought patterns and rituals

### Anger Management
- **Focus**: Anger triggers, expression, and impact
- **Therapies**: DBT skills, Anger Management, Mindfulness
- **Questions**: 8 questions about triggers and coping strategies

### General Wellbeing
- **Focus**: Overall mental health and life satisfaction
- **Therapies**: Mindfulness, Relaxation, Behavioral Activation, Self-care
- **Questions**: 8 holistic wellbeing questions

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

- **Frontend**: Next.js 14, TypeScript, TailwindCSS
- **Animations**: Framer Motion
- **Charts**: Recharts  
- **Icons**: FontAwesome (Free Solid & Regular Icons)
- **AI**: Google Gemini 2.0 Flash API
- **Storage**: Browser Local Storage

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
- **Report Generation Issues**: Check our [Troubleshooting Guide](./TROUBLESHOOTING.md) for common solutions
- **API Key Problems**: Ensure your Gemini API key is valid and properly configured
- **Browser Issues**: Check the browser console for detailed error messages
- **Connection Problems**: Verify your internet connection for API calls

## 📞 Support

If you're experiencing mental health difficulties:
- **Crisis**: Call 988 (Suicide & Crisis Lifeline) or emergency services
- **Support**: Contact a licensed mental health professional
- **Resources**: Visit SAMHSA National Helpline: 1-800-662-4357

## 📄 License

MIT License - see LICENSE file for details

---

**Remember**: Taking care of your mental health is brave. You're not alone in this journey. 💙
