import { motion } from 'motion/react';
import { useState, useEffect } from 'react';

interface PhilosophyNodeProps {
  name: string;
  x: number;
  y: number;
  color: string;
  delay: number;
  onAbsorb: () => void;
  isAbsorbed: boolean;
}

export function PhilosophyNode({ name, x, y, color, delay, onAbsorb, isAbsorbed }: PhilosophyNodeProps) {
  const [hasAppeared, setHasAppeared] = useState(false);

  // Auto-trigger absorption after 3 seconds of being visible
  useEffect(() => {
    if (hasAppeared && !isAbsorbed) {
      const timer = setTimeout(() => {
        // This will trigger the absorption animation
        onAbsorb();
      }, 3000);
      
      return () => clearTimeout(timer);
    }
  }, [hasAppeared, isAbsorbed, onAbsorb]);

  return (
    <motion.g
      initial={{ opacity: 0, scale: 0 }}
      animate={{ 
        opacity: isAbsorbed ? 0 : 1, 
        scale: isAbsorbed ? 0 : 1,
        x: isAbsorbed ? 400 : x,
        y: isAbsorbed ? 100 : y
      }}
      transition={{ 
        duration: 0.8, 
        delay: delay,
        type: "spring",
        stiffness: 100
      }}
      onAnimationComplete={() => {
        if (!hasAppeared && !isAbsorbed) {
          // Philosophy just appeared
          setHasAppeared(true);
        } else if (isAbsorbed) {
          // Absorption animation completed - this is handled by parent now
          console.log(`✅ ${name} absorption animation completed`);
        }
      }}
    >
      <circle
        cx={0}
        cy={0}
        r="25"
        fill={color}
        stroke="#fff"
        strokeWidth="3"
        className="drop-shadow-lg"
      />
      <text
        x={0}
        y={-35}
        textAnchor="middle"
        className="fill-white text-sm font-medium"
        style={{ textShadow: '1px 1px 2px rgba(0,0,0,0.8)' }}
      >
        {name}
      </text>
    </motion.g>
  );
}