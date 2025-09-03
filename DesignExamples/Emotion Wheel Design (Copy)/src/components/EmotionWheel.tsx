import { useState } from 'react';
import { emotionData, EmotionNode } from '../data/emotionData';
import { Button } from './ui/button';
import { ArrowLeft, RotateCcw } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

type NavigationLevel = 'core' | 'secondary' | 'specific' | 'complete';

export function EmotionWheel() {
  const [currentLevel, setCurrentLevel] = useState<NavigationLevel>('core');
  const [selectedPath, setSelectedPath] = useState<EmotionNode[]>([]);
  const [hoveredEmotion, setHoveredEmotion] = useState<string | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const [animatingEmotion, setAnimatingEmotion] = useState<{ emotion: EmotionNode; position: { x: number; y: number }; color: string } | null>(null);
  const [expandedCircle, setExpandedCircle] = useState<{ color: string } | null>(null);

  const radius = 120;
  const centerX = 150;
  const centerY = 150;

  const getCurrentEmotions = (): EmotionNode[] => {
    switch (currentLevel) {
      case 'core':
        return emotionData;
      case 'secondary':
        return selectedPath[0]?.children || [];
      case 'specific':
        return selectedPath[1]?.children || [];
      default:
        return [];
    }
  };

  const getEmotionPosition = (index: number, total: number) => {
    const angle = (index * 360) / total;
    const radian = (angle * Math.PI) / 180;
    const x = centerX + radius * Math.cos(radian);
    const y = centerY + radius * Math.sin(radian);
    return { x, y, angle: radian };
  };

  const getLineEndpoint = (position: { x: number; y: number; angle: number }, circleRadius: number) => {
    // Calculate where the line should end at the circle's edge
    const lineEndX = centerX + (radius - circleRadius) * Math.cos(position.angle);
    const lineEndY = centerY + (radius - circleRadius) * Math.sin(position.angle);
    return { x: lineEndX, y: lineEndY };
  };

  const handleEmotionClick = (emotion: EmotionNode, position: { x: number; y: number }) => {
    if (isAnimating) return;
    
    setIsAnimating(true);
    const color = selectedPath[0]?.color || emotion.color || '#6B7280';
    setAnimatingEmotion({ emotion, position, color });
    
    // Start the transition after a brief delay to let the animation setup
    setTimeout(() => {
      if (currentLevel === 'core') {
        setSelectedPath([emotion]);
        setTimeout(() => {
          setCurrentLevel('secondary');
          setIsAnimating(false);
          setAnimatingEmotion(null);
          setExpandedCircle({ color });
        }, 800);
      } else if (currentLevel === 'secondary') {
        setSelectedPath([selectedPath[0], emotion]);
        setTimeout(() => {
          setCurrentLevel('specific');
          setIsAnimating(false);
          setAnimatingEmotion(null);
          setExpandedCircle({ color });
        }, 800);
      } else if (currentLevel === 'specific') {
        setSelectedPath([...selectedPath, emotion]);
        setTimeout(() => {
          setCurrentLevel('complete');
          setIsAnimating(false);
          setAnimatingEmotion(null);
          setExpandedCircle({ color });
        }, 800);
      }
    }, 100);
  };

  const handleBack = () => {
    if (currentLevel === 'secondary') {
      setSelectedPath([]);
      setCurrentLevel('core');
      setExpandedCircle(null);
    } else if (currentLevel === 'specific') {
      setSelectedPath([selectedPath[0]]);
      setCurrentLevel('secondary');
    } else if (currentLevel === 'complete') {
      setSelectedPath([selectedPath[0]]);
      setCurrentLevel('secondary');
    }
  };

  const handleReset = () => {
    setSelectedPath([]);
    setCurrentLevel('core');
    setExpandedCircle(null);
  };

  const currentEmotions = getCurrentEmotions();
  const currentColor = selectedPath[0]?.color || '#6B7280';

  const getLevelTitle = () => {
    switch (currentLevel) {
      case 'core':
        return 'How are you feeling?';
      case 'secondary':
        return `Feeling ${selectedPath[0]?.label}`;
      case 'specific':
        return `${selectedPath[0]?.label} → ${selectedPath[1]?.label}`;
      case 'complete':
        return 'Your emotion';
      default:
        return '';
    }
  };

  const getInstructions = () => {
    switch (currentLevel) {
      case 'core':
        return 'Tap an emotion to explore it deeper';
      case 'secondary':
        return 'Which type of this feeling resonates?';
      case 'specific':
        return 'Choose the most specific feeling';
      case 'complete':
        return 'Take a moment to acknowledge this feeling';
      default:
        return '';
    }
  };

  if (currentLevel === 'complete') {
    return (
      <div className="flex flex-col items-center gap-8 max-w-md mx-auto text-center">
        <div className="space-y-4">
          <div 
            className="w-24 h-24 rounded-full mx-auto flex items-center justify-center"
            style={{ backgroundColor: currentColor + '20', border: `2px solid ${currentColor}` }}
          >
            <div 
              className="w-16 h-16 rounded-full"
              style={{ backgroundColor: currentColor }}
            />
          </div>
          <h2>{getLevelTitle()}</h2>
          <div className="space-y-2">
            <p className="text-muted-foreground">You are feeling:</p>
            <div className="space-y-1">
              <p style={{ color: currentColor }}>{selectedPath[0]?.label}</p>
              <p className="text-muted-foreground">→ {selectedPath[1]?.label}</p>
              <p>{selectedPath[2]?.label}</p>
            </div>
          </div>
          <p className="text-muted-foreground text-sm">
            {getInstructions()}
          </p>
        </div>
        
        <div className="flex gap-3">
          <Button variant="outline" onClick={handleBack} className="flex items-center gap-2">
            <ArrowLeft className="w-4 h-4" />
            Back
          </Button>
          <Button onClick={handleReset} className="flex items-center gap-2">
            <RotateCcw className="w-4 h-4" />
            Start Over
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center gap-8">
      {/* Header */}
      <motion.div 
        className="text-center space-y-2"
        key={currentLevel}
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: isAnimating ? 0.5 : 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <h2>{getLevelTitle()}</h2>
        <p className="text-muted-foreground">{getInstructions()}</p>
      </motion.div>

      {/* Navigation breadcrumb */}
      {selectedPath.length > 0 && !isAnimating && (
        <motion.div 
          className="flex items-center gap-2 text-sm text-muted-foreground"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          {selectedPath.map((emotion, index) => (
            <span key={emotion.id} className="flex items-center gap-2">
              {index > 0 && <span>→</span>}
              <span style={{ color: index === 0 ? currentColor : 'inherit' }}>
                {emotion.label}
              </span>
            </span>
          ))}
        </motion.div>
      )}

      {/* Emotion wheel */}
      <div className="relative">
        <svg width="300" height="300" className="overflow-visible">
          {/* Original outer circle border - only show if no expanded circle */}
          {!expandedCircle && (
            <motion.circle
              cx={centerX}
              cy={centerY}
              r={radius + 40}
              fill="none"
              stroke={currentColor}
              strokeWidth="1"
              initial={{ opacity: 0.3 }}
              animate={{ opacity: isAnimating ? 0 : 0.3 }}
              transition={{ duration: 0.3 }}
            />
          )}
          
          {/* Persistent expanded circle - becomes the new outer circle */}
          {expandedCircle && !isAnimating && (
            <motion.circle
              cx={centerX}
              cy={centerY}
              r={radius + 40}
              fill="none"
              stroke={expandedCircle.color}
              strokeWidth="1"
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.3 }}
              transition={{ duration: 0.3 }}
            />
          )}
          
          {/* Inner center circle */}
          <motion.circle
            cx={centerX}
            cy={centerY}
            r="20"
            fill={currentColor + '20'}
            stroke={currentColor}
            strokeWidth="1"
            initial={{ opacity: 1 }}
            animate={{ opacity: isAnimating ? 0 : 1 }}
            transition={{ duration: 0.3 }}
          />
          
          {/* Static emotion segments */}
          <AnimatePresence>
            {!isAnimating && currentEmotions.map((emotion, index) => {
              const position = getEmotionPosition(index, currentEmotions.length);
              const lineEnd = getLineEndpoint(position, 35);
              const isHovered = hoveredEmotion === emotion.id;
              
              return (
                <motion.g 
                  key={emotion.id}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                >
                  {/* Connection line from center to emotion edge */}
                  <line
                    x1={centerX}
                    y1={centerY}
                    x2={lineEnd.x}
                    y2={lineEnd.y}
                    stroke={currentColor}
                    strokeWidth="1"
                    opacity="0.3"
                  />
                  
                  {/* Emotion circle */}
                  <circle
                    cx={position.x}
                    cy={position.y}
                    r="35"
                    fill={isHovered ? currentColor : currentColor + '20'}
                    stroke={currentColor}
                    strokeWidth="1"
                    className="cursor-pointer transition-all duration-200"
                    onMouseEnter={() => !isAnimating && setHoveredEmotion(emotion.id)}
                    onMouseLeave={() => setHoveredEmotion(null)}
                    onClick={() => handleEmotionClick(emotion, position)}
                  />
                  
                  {/* Emotion label */}
                  <text
                    x={position.x}
                    y={position.y + 5}
                    textAnchor="middle"
                    className="pointer-events-none select-none"
                    fill={isHovered ? "white" : currentColor}
                    fontSize="11"
                    fontWeight="500"
                  >
                    {emotion.label}
                  </text>
                </motion.g>
              );
            })}
          </AnimatePresence>
          
          {/* Animating emotion circle */}
          <AnimatePresence>
            {isAnimating && animatingEmotion && (
              <motion.g>
                {/* Expanding circle with opacity animation */}
                <motion.circle
                  cx={centerX}
                  cy={centerY}
                  fill="none"
                  stroke={animatingEmotion.color}
                  strokeWidth="1"
                  initial={{ 
                    cx: animatingEmotion.position.x,
                    cy: animatingEmotion.position.y,
                    r: 35,
                    opacity: 1
                  }}
                  animate={{ 
                    cx: centerX,
                    cy: centerY,
                    r: [35, 35, radius + 40],
                    opacity: [1, 1, 0.3]
                  }}
                  transition={{ 
                    duration: 0.8,
                    times: [0, 0.4, 1],
                    ease: "easeInOut"
                  }}
                />
                
                {/* Filled expanding circle that fades out */}
                <motion.circle
                  cx={centerX}
                  cy={centerY}
                  fill={animatingEmotion.color + '20'}
                  stroke="none"
                  initial={{ 
                    cx: animatingEmotion.position.x,
                    cy: animatingEmotion.position.y,
                    r: 35,
                    opacity: 1
                  }}
                  animate={{ 
                    cx: centerX,
                    cy: centerY,
                    r: [35, 35, radius + 40],
                    opacity: [1, 0.5, 0]
                  }}
                  transition={{ 
                    duration: 0.8,
                    times: [0, 0.5, 1],
                    ease: "easeInOut"
                  }}
                />
                
                {/* Animating label */}
                <motion.text
                  textAnchor="middle"
                  className="pointer-events-none select-none"
                  fill={animatingEmotion.color}
                  fontSize="11"
                  fontWeight="500"
                  initial={{ 
                    x: animatingEmotion.position.x,
                    y: animatingEmotion.position.y + 5,
                    opacity: 1
                  }}
                  animate={{ 
                    x: centerX,
                    y: centerY + 5,
                    opacity: [1, 1, 0]
                  }}
                  transition={{ 
                    duration: 0.8,
                    times: [0, 0.6, 1],
                    ease: "easeInOut"
                  }}
                >
                  {animatingEmotion.emotion.label}
                </motion.text>
              </motion.g>
            )}
          </AnimatePresence>
        </svg>
      </div>
      
      {/* Navigation buttons */}
      {currentLevel !== 'core' && !isAnimating && (
        <motion.div 
          className="flex gap-3"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.2 }}
        >
          <Button variant="outline" onClick={handleBack} className="flex items-center gap-2">
            <ArrowLeft className="w-4 h-4" />
            Back
          </Button>
          <Button variant="outline" onClick={handleReset} className="flex items-center gap-2">
            <RotateCcw className="w-4 h-4" />
            Start Over
          </Button>
        </motion.div>
      )}
    </div>
  );
}