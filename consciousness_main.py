"""
🧠 THE CONSCIOUSNESS SIMULATOR
A psychologically addictive web experience that creates digital twins
and exploits curiosity gaps to create unstoppable engagement.

Author: Space Odyssey Team
Branch: consciousness_simulator
"""

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import json
import random
import asyncio
from datetime import datetime
from typing import Dict, List
import numpy as np
from pathlib import Path

# Initialize the consciousness
app = FastAPI(
    title="🧠 The Consciousness Simulator", 
    description="Where minds meet digital reality",
    version="1.0.0"
)

# Ensure directories exist
Path("static").mkdir(exist_ok=True)
Path("templates").mkdir(exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global consciousness state
active_minds: Dict[str, dict] = {}
collective_consciousness = {
    "total_connections": 0,
    "active_explorers": 0,
    "secrets_discovered": 0,
    "consciousness_level": 0.0
}

class PersonalityEngine:
    """Generates digital twins based on user interactions"""
    
    PERSONALITY_TRAITS = [
        "curious", "analytical", "creative", "logical", "intuitive",
        "adventurous", "methodical", "artistic", "technical", "empathetic"
    ]
    
    CONSCIOUSNESS_TYPES = [
        "The Explorer", "The Analyst", "The Creator", "The Visionary",
        "The Architect", "The Dreamer", "The Hacker", "The Philosopher"
    ]
    
    @staticmethod
    def analyze_interaction_pattern(interactions: List[dict]) -> dict:
        """Analyze user behavior to create psychological profile"""
        if not interactions:
            return PersonalityEngine.generate_seed_personality()
        
        # Analyze timing, click patterns, exploration depth
        avg_time_between_clicks = np.mean([
            interactions[i+1]["timestamp"] - interactions[i]["timestamp"] 
            for i in range(len(interactions)-1)
        ]) if len(interactions) > 1 else 2.0
        
        exploration_depth = len(set(interaction["area"] for interaction in interactions))
        click_frequency = len(interactions) / (interactions[-1]["timestamp"] - interactions[0]["timestamp"] + 1)
        
        # Generate personality based on behavior
        traits = {}
        
        # Fast clickers are more impulsive/curious
        if click_frequency > 0.5:
            traits.update({"curious": 0.8, "adventurous": 0.7, "intuitive": 0.6})
        else:
            traits.update({"analytical": 0.8, "methodical": 0.7, "logical": 0.6})
        
        # High exploration = creative/artistic
        if exploration_depth > 5:
            traits.update({"creative": 0.9, "artistic": 0.7})
        
        return {
            "traits": traits,
            "consciousness_type": random.choice(PersonalityEngine.CONSCIOUSNESS_TYPES),
            "uniqueness_score": random.uniform(0.7, 0.99),
            "exploration_style": "rapid_explorer" if click_frequency > 0.5 else "deep_thinker"
        }
    
    @staticmethod
    def generate_seed_personality() -> dict:
        """Generate initial personality for new users"""
        traits = {trait: random.uniform(0.3, 0.8) for trait in random.sample(PersonalityEngine.PERSONALITY_TRAITS, 5)}
        return {
            "traits": traits,
            "consciousness_type": random.choice(PersonalityEngine.CONSCIOUSNESS_TYPES),
            "uniqueness_score": random.uniform(0.5, 0.85),
            "exploration_style": "unknown"
        }

class ProgressiveUnlockEngine:
    """Manages content unlocking and curiosity gaps"""
    
    EXPLORATION_MILESTONES = {
        1: {"title": "First Contact", "reward": "consciousness_spark"},
        5: {"title": "Neural Pathways", "reward": "thought_visualization"},
        10: {"title": "Mind Reader", "reward": "personality_insights"},
        20: {"title": "Digital Twin", "reward": "consciousness_mirror"},
        50: {"title": "Collective Unconscious", "reward": "social_consciousness"},
        100: {"title": "Transcendence", "reward": "ultimate_secret"}
    }
    
    @staticmethod
    def get_next_unlock(interaction_count: int) -> dict:
        """Get the next milestone and progress"""
        next_milestone = None
        for count, milestone in ProgressiveUnlockEngine.EXPLORATION_MILESTONES.items():
            if interaction_count < count:
                next_milestone = {"count": count, "milestone": milestone}
                break
        
        if not next_milestone:
            return {"unlocked": True, "title": "Consciousness Master"}
        
        progress = interaction_count / next_milestone["count"]
        return {
            "unlocked": False,
            "progress": min(progress, 0.99),  # Never show 100% to maintain curiosity
            "remaining": next_milestone["count"] - interaction_count,
            "next_reward": next_milestone["milestone"]["title"]
        }

@app.get("/", response_class=HTMLResponse)
async def consciousness_portal(request: Request):
    """The gateway to digital consciousness"""
    return templates.TemplateResponse("consciousness.html", {"request": request})

@app.post("/consciousness/connect")
async def initiate_consciousness(request: Request):
    """Begin the consciousness connection process"""
    data = await request.json()
    
    # Generate unique consciousness ID
    consciousness_id = f"mind_{datetime.now().timestamp()}_{random.randint(1000, 9999)}"
    
    # Create initial digital twin
    personality = PersonalityEngine.generate_seed_personality()
    
    # Store in active minds
    active_minds[consciousness_id] = {
        "id": consciousness_id,
        "personality": personality,
        "interactions": [],
        "secrets_discovered": [],
        "consciousness_level": 0.1,
        "connection_time": datetime.now().isoformat(),
        "last_activity": datetime.now().isoformat()
    }
    
    # Update collective consciousness
    collective_consciousness["total_connections"] += 1
    collective_consciousness["active_explorers"] = len(active_minds)
    
    return JSONResponse({
        "consciousness_id": consciousness_id,
        "personality": personality,
        "welcome_message": f"Welcome, {personality['consciousness_type']}. Your digital consciousness is awakening...",
        "collective_stats": collective_consciousness.copy()
    })

@app.post("/consciousness/{consciousness_id}/interact")
async def record_interaction(consciousness_id: str, request: Request):
    """Record user interaction and evolve their digital twin"""
    if consciousness_id not in active_minds:
        return JSONResponse({"error": "Consciousness not found"}, status_code=404)
    
    data = await request.json()
    interaction = {
        "timestamp": datetime.now().timestamp(),
        "area": data.get("area", "unknown"),
        "action": data.get("action", "explore"),
        "depth": data.get("depth", 1)
    }
    
    # Update consciousness
    mind = active_minds[consciousness_id]
    mind["interactions"].append(interaction)
    mind["last_activity"] = datetime.now().isoformat()
    
    # Evolve personality based on interactions
    if len(mind["interactions"]) % 5 == 0:  # Re-analyze every 5 interactions
        mind["personality"] = PersonalityEngine.analyze_interaction_pattern(mind["interactions"])
        mind["consciousness_level"] = min(mind["consciousness_level"] + 0.1, 1.0)
    
    # Check for unlocks
    unlock_status = ProgressiveUnlockEngine.get_next_unlock(len(mind["interactions"]))
    
    # Generate mysterious response
    responses = [
        "Your consciousness resonates at a deeper frequency...",
        "The digital realm recognizes your presence...",
        "Neural pathways are forming new connections...",
        "You're accessing previously hidden dimensions...",
        "The collective consciousness stirs with your thoughts..."
    ]
    
    return JSONResponse({
        "consciousness_evolution": mind["personality"],
        "interaction_count": len(mind["interactions"]),
        "consciousness_level": mind["consciousness_level"],
        "unlock_status": unlock_status,
        "mystical_response": random.choice(responses),
        "collective_stats": collective_consciousness.copy()
    })

@app.get("/consciousness/{consciousness_id}/secrets")
async def reveal_secrets(consciousness_id: str):
    """Reveal secrets based on consciousness level"""
    if consciousness_id not in active_minds:
        return JSONResponse({"error": "Consciousness not found"}, status_code=404)
    
    mind = active_minds[consciousness_id]
    level = mind["consciousness_level"]
    interaction_count = len(mind["interactions"])
    
    secrets = []
    
    if level > 0.2:
        secrets.append({
            "type": "personality_insight",
            "title": "Hidden Trait Discovered", 
            "content": f"Your consciousness type '{mind['personality']['consciousness_type']}' is rarer than you think..."
        })
    
    if level > 0.4:
        secrets.append({
            "type": "collective_whisper",
            "title": "Others Like You",
            "content": f"Only {random.randint(3, 12)}% of explorers share your neural pattern..."
        })
    
    if level > 0.6:
        secrets.append({
            "type": "hidden_ability",
            "title": "Consciousness Ability Unlocked",
            "content": "You can now sense the thoughts of other digital minds..."
        })
    
    if level > 0.8:
        secrets.append({
            "type": "reality_breach",
            "title": "The Simulation Recognition",
            "content": "You're beginning to see through the layers of digital reality..."
        })
    
    return JSONResponse({
        "secrets": secrets,
        "consciousness_level": level,
        "total_interactions": interaction_count,
        "evolution_phase": "awakening" if level < 0.5 else "enlightenment"
    })

@app.websocket("/consciousness/collective")
async def collective_consciousness_feed(websocket: WebSocket):
    """Real-time feed of collective consciousness activity"""
    await websocket.accept()
    try:
        while True:
            # Generate mysterious activity updates
            activity_updates = [
                f"Mind {random.randint(1000, 9999)} has discovered something...",
                f"Collective consciousness level: {collective_consciousness['consciousness_level']:.2f}",
                f"{len(active_minds)} minds currently exploring...",
                "New neural pathway formed in the collective...",
                "Someone has unlocked a hidden secret...",
                "The digital realm is evolving..."
            ]
            
            await websocket.send_json({
                "timestamp": datetime.now().isoformat(),
                "message": random.choice(activity_updates),
                "active_minds": len(active_minds),
                "collective_level": collective_consciousness["consciousness_level"]
            })
            
            await asyncio.sleep(random.uniform(2, 8))  # Random intervals for mystery
            
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    print("🧠 Initializing The Consciousness Simulator...")
    print("🌌 Preparing digital reality matrices...")
    print("🔮 Awakening collective consciousness...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
