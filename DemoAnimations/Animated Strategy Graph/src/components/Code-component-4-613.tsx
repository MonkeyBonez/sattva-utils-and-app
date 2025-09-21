import { motion } from 'motion/react';

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
        if (!isAbsorbed) {
          // Wait for philosophy to be fully visible, then wait additional time before absorption
          setTimeout(() => onAbsorb(), 3000); // Fixed 3 second wait after becoming visible
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