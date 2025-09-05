'use client';

import { motion } from 'framer-motion';
import { EnvironmentTheme } from '@/types';
import { getEnvironmentGradient } from '@/utils/helpers';

interface EnvironmentBackgroundProps {
  environment: EnvironmentTheme;
  userMood?: string;
  responseIntensity?: number; // 0-1 scale based on response severity
  isInteractive?: boolean;
}

export default function EnvironmentBackground({ 
  environment, 
  userMood = 'neutral', 
  responseIntensity = 0.5,
  isInteractive = false 
}: EnvironmentBackgroundProps) {
  const gradient = getEnvironmentGradient(environment);
  
  // Calculate animation intensity based on user's mood and responses
  const getAnimationIntensity = () => {
    let intensity = 0.5; // base intensity
    
    // Adjust based on mood
    switch (userMood) {
      case 'happy':
      case 'calm':
        intensity *= 1.3; // More active, positive animations
        break;
      case 'sad':
      case 'frustrated':
        intensity *= 0.7; // Slower, more subdued animations
        break;
      case 'anxious':
        intensity *= 1.5; // More intense, rapid animations
        break;
      case 'hopeful':
        intensity *= 1.1; // Slightly more active
        break;
      default:
        intensity *= 1.0; // neutral
    }
    
    // Factor in response intensity (how severe their answers were)
    intensity = intensity * (0.5 + responseIntensity * 0.5);
    
    return Math.max(0.3, Math.min(2.0, intensity)); // Clamp between 0.3 and 2.0
  };
  
  // Get mood-based colors
  const getMoodColors = () => {
    switch (userMood) {
      case 'happy':
        return { primary: 'yellow-400', secondary: 'orange-300', accent: 'pink-300' };
      case 'calm':
        return { primary: 'blue-400', secondary: 'green-300', accent: 'teal-300' };
      case 'sad':
        return { primary: 'gray-400', secondary: 'blue-300', accent: 'indigo-300' };
      case 'anxious':
        return { primary: 'red-400', secondary: 'orange-400', accent: 'yellow-400' };
      case 'frustrated':
        return { primary: 'orange-500', secondary: 'red-400', accent: 'yellow-500' };
      case 'hopeful':
        return { primary: 'green-400', secondary: 'blue-300', accent: 'purple-300' };
      default:
        return { primary: 'white', secondary: 'gray-300', accent: 'blue-300' };
    }
  };
  
  const animationIntensity = getAnimationIntensity();
  const moodColors = getMoodColors();

  const renderEnvironmentElements = () => {
    switch (environment) {
      case 'forest':
        return (
          <>
            {/* Trees */}
            {Array.from({ length: 8 }, (_, i) => (
              <motion.div
                key={`tree-${i}`}
                className="absolute bottom-0 w-4 bg-green-800 opacity-30"
                style={{
                  left: `${15 + i * 12}%`,
                  height: `${120 + Math.random() * 80}px`,
                }}
                initial={{ scaleY: 0 }}
                animate={{ scaleY: 1 }}
                transition={{ delay: i * 0.2, duration: 1 }}
              />
            ))}
            
            {/* Floating leaves - Interactive based on mood */}
            {Array.from({ length: isInteractive ? Math.floor(12 * animationIntensity) : 12 }, (_, i) => (
              <motion.div
                key={`leaf-${i}`}
                className={`absolute w-2 h-2 bg-${moodColors.primary} rounded-full opacity-60`}
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 60}%`,
                  boxShadow: isInteractive ? `0 0 10px rgba(${userMood === 'anxious' ? '255,0,0' : '0,255,0'}, 0.3)` : 'none'
                }}
                animate={{
                  y: [0, -20 * animationIntensity, 0],
                  x: [0, 10 * animationIntensity, -5 * animationIntensity, 0],
                  rotate: [0, 180 * animationIntensity, 360 * animationIntensity],
                  scale: isInteractive ? [1, 1.2, 1] : [1, 1, 1],
                }}
                transition={{
                  duration: (4 + Math.random() * 2) / animationIntensity,
                  repeat: Infinity,
                  delay: Math.random() * 2,
                  ease: userMood === 'anxious' ? 'easeInOut' : 'easeOut',
                }}
              />
            ))}
          </>
        );

      case 'ocean':
        return (
          <>
            {/* Waves */}
            {Array.from({ length: 3 }, (_, i) => (
              <motion.div
                key={`wave-${i}`}
                className="absolute bottom-0 w-full bg-blue-400 opacity-20 rounded-t-full"
                style={{
                  height: `${60 + i * 20}px`,
                  bottom: `${i * 15}px`,
                }}
                animate={{
                  scaleX: [1, 1.1, 1],
                  x: [-20, 20, -20],
                }}
                transition={{
                  duration: 3 + i,
                  repeat: Infinity,
                  ease: 'easeInOut',
                }}
              />
            ))}
            
            {/* Bubbles - Interactive based on mood */}
            {Array.from({ length: isInteractive ? Math.floor(15 * animationIntensity) : 15 }, (_, i) => (
              <motion.div
                key={`bubble-${i}`}
                className={`absolute rounded-full bg-${moodColors.secondary} opacity-40`}
                style={{
                  width: `${8 + Math.random() * 16 * animationIntensity}px`,
                  height: `${8 + Math.random() * 16 * animationIntensity}px`,
                  left: `${Math.random() * 100}%`,
                  bottom: `${Math.random() * 30}%`,
                  filter: isInteractive ? `blur(${userMood === 'sad' ? '2px' : '0px'})` : 'none'
                }}
                animate={{
                  y: [-20 * animationIntensity, -100 * animationIntensity],
                  opacity: [0.4, 0.8, 0],
                  scale: [1, 1.2 * animationIntensity, 0.8],
                }}
                transition={{
                  duration: (3 + Math.random() * 2) / animationIntensity,
                  repeat: Infinity,
                  delay: Math.random() * 3,
                  ease: userMood === 'calm' ? 'easeOut' : 'easeInOut',
                }}
              />
            ))}
          </>
        );

      case 'mountains':
        return (
          <>
            {/* Mountain silhouettes */}
            {Array.from({ length: 5 }, (_, i) => (
              <motion.div
                key={`mountain-${i}`}
                className="absolute bottom-0 bg-gray-700 opacity-30"
                style={{
                  left: `${i * 20}%`,
                  width: `${80 + Math.random() * 40}px`,
                  height: `${100 + Math.random() * 60}px`,
                  clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)',
                }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 0.3, y: 0 }}
                transition={{ delay: i * 0.3, duration: 1 }}
              />
            ))}
            
            {/* Clouds */}
            {Array.from({ length: 6 }, (_, i) => (
              <motion.div
                key={`cloud-${i}`}
                className="absolute bg-white opacity-20 rounded-full"
                style={{
                  width: `${40 + Math.random() * 60}px`,
                  height: `${20 + Math.random() * 30}px`,
                  left: `${Math.random() * 100}%`,
                  top: `${10 + Math.random() * 40}%`,
                }}
                animate={{
                  x: [0, 100, 0],
                }}
                transition={{
                  duration: 15 + Math.random() * 10,
                  repeat: Infinity,
                  ease: 'linear',
                }}
              />
            ))}
          </>
        );

      case 'garden':
        return (
          <>
            {/* Flowers */}
            {Array.from({ length: 10 }, (_, i) => (
              <motion.div
                key={`flower-${i}`}
                className="absolute bottom-4"
                style={{
                  left: `${10 + Math.random() * 80}%`,
                }}
              >
                <motion.div
                  className="w-6 h-6 bg-pink-400 rounded-full opacity-60"
                  animate={{
                    scale: [1, 1.2, 1],
                    rotate: [0, 5, -5, 0],
                  }}
                  transition={{
                    duration: 2 + Math.random(),
                    repeat: Infinity,
                    delay: Math.random() * 2,
                  }}
                />
                <div className="w-1 h-8 bg-green-500 mx-auto opacity-40" />
              </motion.div>
            ))}
            
            {/* Butterflies */}
            {Array.from({ length: 4 }, (_, i) => (
              <motion.div
                key={`butterfly-${i}`}
                className="absolute w-4 h-4 bg-yellow-400 opacity-50"
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${20 + Math.random() * 40}%`,
                  clipPath: 'polygon(50% 0%, 0% 50%, 50% 100%, 100% 50%)',
                }}
                animate={{
                  x: [0, 50, -30, 0],
                  y: [0, -30, 20, 0],
                  rotate: [0, 15, -15, 0],
                }}
                transition={{
                  duration: 6 + Math.random() * 2,
                  repeat: Infinity,
                  delay: Math.random() * 3,
                }}
              />
            ))}
          </>
        );

      case 'sky':
        return (
          <>
            {/* Stars */}
            {Array.from({ length: 20 }, (_, i) => (
              <motion.div
                key={`star-${i}`}
                className="absolute w-1 h-1 bg-white rounded-full"
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 70}%`,
                }}
                animate={{
                  opacity: [0.3, 1, 0.3],
                  scale: [1, 1.5, 1],
                }}
                transition={{
                  duration: 2 + Math.random() * 3,
                  repeat: Infinity,
                  delay: Math.random() * 2,
                }}
              />
            ))}
            
            {/* Shooting stars */}
            {Array.from({ length: 3 }, (_, i) => (
              <motion.div
                key={`shooting-star-${i}`}
                className="absolute w-20 h-0.5 bg-gradient-to-r from-white to-transparent opacity-0"
                style={{
                  left: `${Math.random() * 50}%`,
                  top: `${Math.random() * 50}%`,
                }}
                animate={{
                  x: [0, 200],
                  opacity: [0, 1, 0],
                }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  delay: 5 + Math.random() * 10,
                  repeatDelay: 8 + Math.random() * 12,
                }}
              />
            ))}
          </>
        );

      case 'lighthouse':
        return (
          <>
            {/* Lighthouse beam */}
            <motion.div
              className="absolute top-0 left-1/2 transform -translate-x-1/2 w-1 h-full bg-gradient-to-b from-yellow-300 to-transparent opacity-30"
              animate={{
                rotate: [0, 360],
                scaleX: [1, 3, 1],
              }}
              transition={{
                duration: 8,
                repeat: Infinity,
                ease: 'linear',
              }}
              style={{ transformOrigin: 'top center' }}
            />
            
            {/* Light rays */}
            {Array.from({ length: 8 }, (_, i) => (
              <motion.div
                key={`ray-${i}`}
                className="absolute top-0 left-1/2 transform -translate-x-1/2 w-0.5 h-32 bg-yellow-200 opacity-20"
                style={{
                  transformOrigin: 'top center',
                  rotate: `${i * 45}deg`,
                }}
                animate={{
                  opacity: [0.1, 0.4, 0.1],
                  scaleY: [1, 1.2, 1],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  delay: i * 0.25,
                }}
              />
            ))}
          </>
        );

      case 'room':
        return (
          <>
            {/* Window light */}
            <motion.div
              className="absolute top-8 right-8 w-32 h-24 bg-yellow-200 opacity-20 rounded-lg"
              animate={{
                opacity: [0.15, 0.25, 0.15],
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
            />
            
            {/* Dust particles */}
            {Array.from({ length: 8 }, (_, i) => (
              <motion.div
                key={`dust-${i}`}
                className="absolute w-1 h-1 bg-yellow-300 rounded-full opacity-30"
                style={{
                  right: `${40 + Math.random() * 30}%`,
                  top: `${20 + Math.random() * 40}%`,
                }}
                animate={{
                  y: [0, -40, 0],
                  x: [0, 10, -5, 0],
                  opacity: [0.1, 0.4, 0.1],
                }}
                transition={{
                  duration: 3 + Math.random() * 2,
                  repeat: Infinity,
                  delay: Math.random() * 3,
                }}
              />
            ))}
          </>
        );

      default:
        return null;
    }
  }

  return (
    <motion.div
      className={`fixed inset-0 bg-gradient-to-br ${gradient} z-0`}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1.5 }}
    >
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        {renderEnvironmentElements()}
      </div>
      
      {/* Overlay for better text readability */}
      <div className="absolute inset-0 bg-black/10" />
    </motion.div>
  );
}
