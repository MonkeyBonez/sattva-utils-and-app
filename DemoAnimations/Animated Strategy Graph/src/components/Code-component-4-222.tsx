import { motion } from 'motion/react';
import { useState, useEffect } from 'react';

interface SattvaSpikeProps {
  height: number;
  width: number;
  absorbedPhilosophies: string[];
  startDepthAnimation: boolean;
}

export function SattvaSpike({ height, width, absorbedPhilosophies, startDepthAnimation }: SattvaSpikeProps) {
  const [currentHeight, setCurrentHeight] = useState(100); // Start very short
  
  // When depth animation starts, dramatically increase height
  useEffect(() => {
    if (startDepthAnimation) {
      console.log("🚀 DEPTH ANIMATION STARTING!");
      setCurrentHeight(300); // Make it MUCH taller - very obvious change
    }
  }, [startDepthAnimation]);
  
  const spikePoints = `400,400 ${400 - width/2},400 400,${400 - currentHeight} ${400 + width/2},400`;
  
  return (
    <motion.g>
      {/* Main spike */}
      <motion.polygon
        points={spikePoints}
        fill="url(#sattvaGradient)"
        stroke="#8B5CF6"
        strokeWidth="3"
        className="drop-shadow-xl"
        initial={{ scaleY: 0.1 }}
        animate={{ 
          scaleY: 1,
          points: spikePoints
        }}
        transition={{ 
          scaleY: { duration: 1, type: "spring", stiffness: 80 },
          points: startDepthAnimation ? 
            { duration: 4, type: "spring", stiffness: 30, damping: 20 } : 
            { duration: 1.5, type: "spring", stiffness: 60 }
        }}
        style={{ transformOrigin: "400px 400px" }}
      />
      
      {/* Sattva label */}
      <motion.text
        x={400}
        y={430}
        textAnchor="middle"
        className="fill-white text-xl font-medium"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        SATTVA
      </motion.text>
      
      {/* Absorbed philosophies at the top */}
      {absorbedPhilosophies.map((philosophy, index) => (
        <motion.text
          key={philosophy}
          x={400}
          y={400 - currentHeight + 20 + (index * 15)}
          textAnchor="middle"
          className="fill-white text-xs font-medium"
          initial={{ opacity: 0, scale: 0 }}
          animate={{ 
            opacity: 1, 
            scale: 1,
            y: 400 - currentHeight + 20 + (index * 15)
          }}
          transition={{ 
            opacity: { delay: 1 + index * 0.3 },
            scale: { delay: 1 + index * 0.3 },
            y: startDepthAnimation ? 
              { duration: 4, type: "spring", stiffness: 30, damping: 20 } : 
              { duration: 0 }
          }}
        >
          {philosophy}
        </motion.text>
      ))}
      
      {/* Gradient definition */}
      <defs>
        <linearGradient id="sattvaGradient" x1="0%" y1="100%" x2="0%" y2="0%">
          <stop offset="0%" stopColor="#8B5CF6" />
          <stop offset="50%" stopColor="#A78BFA" />
          <stop offset="100%" stopColor="#C4B5FD" />
        </linearGradient>
      </defs>
    </motion.g>
  );
}