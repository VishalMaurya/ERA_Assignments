# Session 2 Assignment - Web Applications

This repository contains multiple web application projects built with FastAPI backend and modern frontend technologies.

## 🎮 **TECH QUEST ACADEMY** - **LATEST PROJECT**

A **gamified learning platform** for mastering AI/ML and DevOps concepts through interactive challenges and progression systems.

### 🎯 **Game Features:**
- **Character Progression:** Level up from Code Apprentice to Tech Master
- **Learning Paths:** Neural Networks, CNNs, LLMs, AI Agents, DevOps
- **Interactive Challenges:** Real coding exercises with instant feedback  
- **Achievement System:** Unlock badges and compete on leaderboards
- **XP & Leveling:** Earn experience points for completing modules
- **Visual Design:** Retro gaming aesthetic with animated backgrounds

### 🚀 **Quick Start:**
```bash
# Start the game
python run_tech_quest.py

# Visit: http://localhost:8000
```

### 📚 **Learning Paths Available:**
1. **🔧 Programming Foundations** (Level 1+)
2. **🧠 Neural Networks** (Level 5+) 
3. **👁️ Convolutional Neural Networks** (Level 10+)
4. **💬 Large Language Models** (Level 15+)
5. **🤖 AI Agents** (Level 20+)
6. **⚙️ DevOps & MLOps** (Level 12+)

---

## 📋 **All Projects in This Repository:**

### 🎮 Tech Quest Academy (`tech_quest_main.py`)
**Latest:** Gamified learning platform for AI/ML & DevOps
- Interactive coding challenges
- Character progression and achievements
- Multiple learning paths with unlockable content

### 🧠 The Consciousness Simulator (`consciousness_main.py`)
Psychological experiment in digital consciousness
- Real-time personality analysis
- WebSocket-powered collective feed
- Neural network visualization

### 🐾 Animal & File Upload App (`main.py`)
Simple demonstration app
- Animal selection with images
- File upload functionality

---

## 🛠️ **Setup Instructions**

### Prerequisites
- Python 3.12+ 
- `uv` package manager (ultra-fast Python installer)

### Quick Setup
```bash
# 1. Clone and navigate
git clone <repository>
cd Session2_Assignment

# 2. Activate virtual environment
source consciousness_env/bin/activate

# 3. Install dependencies
uv pip install -r requirements.txt

# 4. Run Tech Quest Academy
python run_tech_quest.py
```

### Manual Setup
```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv consciousness_env

# Activate environment
source consciousness_env/bin/activate  # macOS/Linux
# or consciousness_env\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt
```

---

## 📁 **File Structure**

```
Session2_Assignment/
├── 🎮 TECH QUEST ACADEMY
│   ├── tech_quest_main.py        # Game backend
│   ├── run_tech_quest.py         # Game runner
│   └── templates/tech_quest.html # Game frontend
├── 🧠 CONSCIOUSNESS SIMULATOR  
│   ├── consciousness_main.py     # Consciousness backend
│   ├── run_consciousness.py      # Consciousness runner
│   └── templates/consciousness.html # Consciousness frontend
├── 🐾 ANIMAL & FILE UPLOAD
│   ├── main.py                   # Simple app backend
│   ├── run.py                    # App runner
│   └── templates/index.html      # App frontend
├── 📁 SHARED RESOURCES
│   ├── requirements.txt          # Python dependencies
│   ├── README.md                 # This documentation
│   ├── .gitignore               # Git ignore patterns
│   ├── check_setup.py           # Setup verification
│   ├── youtube.md               # Video content
│   └── static/images/           # Image assets
└── 📁 ENVIRONMENT
    └── consciousness_env/        # Virtual environment
```

---

## 🎮 **Tech Quest Academy - Detailed Guide**

### Game Mechanics
- **XP System:** Earn 100+ XP per completed challenge
- **Leveling:** Each level requires 100 XP (Level 1: 0-99 XP, Level 2: 100-199 XP)
- **Unlocks:** Higher levels unlock advanced learning paths
- **Achievements:** Special badges for milestones and perfect scores

### Learning Paths

#### 🔧 **Programming Foundations** (Level 1+)
- Variables and data types
- Functions and control flow  
- Data structures
- Algorithm basics

#### 🧠 **Neural Networks** (Level 5+)
- Perceptron implementation
- Backpropagation algorithm
- Activation functions
- Training loops and optimization

#### 👁️ **Convolutional Neural Networks** (Level 10+)
- Convolution operations
- Pooling layers
- Filter design
- Image classification projects

#### 💬 **Large Language Models** (Level 15+)
- Transformer architecture
- Attention mechanisms
- Fine-tuning techniques
- Prompt engineering mastery

#### 🤖 **AI Agents** (Level 20+)
- Agent architectures
- Reasoning systems
- Tool integration
- Multi-agent coordination

#### ⚙️ **DevOps & MLOps** (Level 12+)
- Docker containerization
- CI/CD pipelines
- Model deployment
- Monitoring and logging

### Challenge Types
1. **Coding Challenges:** Implement algorithms and models
2. **Quiz Modules:** Test theoretical knowledge
3. **Project Builds:** Complete mini-projects
4. **Debug Missions:** Fix broken code

---

## 🎯 **API Endpoints**

### Tech Quest Academy
- `GET /` - Game homepage
- `POST /api/player/create` - Create new player
- `GET /api/player/{player_id}` - Get player progress
- `GET /api/learning-paths` - Available learning paths
- `GET /api/challenge/{path_id}/{module_id}` - Get challenge
- `POST /api/challenge/submit` - Submit solution
- `GET /api/leaderboard` - Top players
- `POST /api/quiz/submit` - Submit quiz answers

### Player Data Structure
```json
{
  "id": "player123",
  "name": "CodeMaster",
  "xp": 1250,
  "level": 13,
  "completed_modules": ["neural_networks_perceptron", ...],
  "achievements": ["first_steps", "code_warrior", ...],
  "stats": {
    "challenges_completed": 25,
    "quizzes_passed": 15,
    "perfect_scores": 5
  }
}
```

---

## 🔧 **Development**

### Running Different Projects
```bash
# Tech Quest Academy (recommended)
python run_tech_quest.py

# Consciousness Simulator
python run_consciousness.py

# Original Animal App
python run.py
```

### Adding New Learning Content
1. Update `LEARNING_PATHS` in `tech_quest_main.py`
2. Add challenges to `CHALLENGES` dictionary
3. Create challenge templates with solutions
4. Test with different difficulty levels

### Customization
- **Styling:** Modify CSS in template files
- **Game Balance:** Adjust XP rewards and level requirements
- **Content:** Add new learning paths and challenges
- **Achievements:** Create custom achievement conditions

---

## 🌟 **Why Tech Quest Academy?**

### Educational Benefits
- **Hands-on Learning:** Write real code, not just read theory
- **Progressive Difficulty:** Unlock advanced topics as you improve
- **Immediate Feedback:** Get instant results and suggestions
- **Gamified Motivation:** Achievements and leaderboards drive engagement

### Technical Innovation
- **Modern Stack:** FastAPI + HTML5/CSS3/JavaScript
- **Real-time Updates:** Dynamic XP and progress tracking
- **Responsive Design:** Works on desktop and mobile
- **Extensible Architecture:** Easy to add new content

### Unique Features
- **Character Evolution:** Visual progression from apprentice to master
- **Code Execution:** Submit and test real Python code
- **Social Elements:** Leaderboards and achievement sharing
- **Comprehensive Coverage:** From basics to advanced AI/DevOps

---

## 🤝 **Contributing**

Want to add new challenges or learning paths?

1. Fork the repository
2. Create a feature branch
3. Add your content to the appropriate sections
4. Test with different skill levels
5. Submit a pull request

---

## 📜 **License & Credits**

Built for educational purposes as part of ERA Session 2 Assignment.

**Technologies Used:**
- FastAPI (Python web framework)
- HTML5/CSS3/JavaScript (Frontend)
- uv (Package management)
- Git (Version control)

---

🎮 **Ready to level up your AI/ML and DevOps skills? Start your quest today!**