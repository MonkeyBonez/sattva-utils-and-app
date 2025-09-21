import { motion } from 'motion/react';

interface SattvaSpikeProps {
  height: number;
  width: number;
  absorbedPhilosophies: string[];
}

export function SattvaSpike({ height, width, absorbedPhilosophies }: SattvaSpikeProps) {
  console.log(`🔍 SattvaSpike render: width=${width}, height=${height}, absorbed=${absorbedPhilosophies.length}`);
  
  const spikePoints = `400,450 ${400 - width/2},450 400,${450 - height} ${400 + width/2},450`;
  
  return (
    <motion.g>
      {/* Main spike */}
      <motion.polygon
        points={spikePoints}
        fill="url(#sattvaGradient)"
        stroke="#8B5CF6"
        strokeWidth="3"
        className="drop-shadow-xl"
        initial={{ points: spikePoints }}
        animate={{ points: spikePoints }}
        transition={{ points: { duration: 1.2, type: "spring", stiffness: 60, damping: 18 } }}
        style={{ transformOrigin: "400px 450px" }}
      />
      
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