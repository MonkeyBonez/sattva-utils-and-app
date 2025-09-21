import { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import { PhilosophyNode } from './PhilosophyNode';
import { SattvaSpike } from './SattvaSpike';

interface Philosophy {
  name: string;
  x: number;
  y: number;
  color: string;
  delay: number;
}

const philosophies: Philosophy[] = [
  { name: "Bhagavad Gita", x: 300, y: 450, color: "#F59E0B", delay: 0 },
  { name: "Dao De Jing", x: 150, y: 450, color: "#10B981", delay: 0.5 },
  { name: "Heart Sutra", x: 550, y: 450, color: "#EF4444", delay: 1 },
  { name: "Meditations", x: 100, y: 450, color: "#3B82F6", delay: 1.5 },
  { name: "Masnavi", x: 650, y: 450, color: "#8B5CF6", delay: 2 },
  { name: "Zohar", x: 200, y: 450, color: "#EC4899", delay: 2.5 },
  { name: "Upanishads", x: 600, y: 450, color: "#F97316", delay: 3 },
];

export function StrategyGraph() {
  const [absorbedPhilosophies, setAbsorbedPhilosophies] = useState<string[]>([]);
  const [spikeHeight, setSpikeHeight] = useState(150); // Fixed height initially
  const [spikeWidth, setSpikeWidth] = useState(60);
  const [startDepthAnimation, setStartDepthAnimation] = useState(false);

  const handleAbsorb = (philosophyName: string) => {
    setAbsorbedPhilosophies(prev => [...prev, philosophyName]);
    // Only grow width, not height - representing breadth expansion
    setSpikeWidth(prev => prev + 20);
  };

  // Trigger depth animation after all philosophies are absorbed
  useEffect(() => {
    if (absorbedPhilosophies.length === philosophies.length && !startDepthAnimation) {
      console.log("All philosophies absorbed, starting depth animation in 3 seconds...");
      setTimeout(() => {
        console.log("Triggering depth animation now!");
        setStartDepthAnimation(true);
      }, 3000); // Wait 3 seconds after the last philosophy is absorbed
    }
  }, [absorbedPhilosophies.length, startDepthAnimation]);

  return (
    <div className="w-full h-screen bg-black flex flex-col items-center justify-center">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold mb-4 text-white">The Future of Sattva</h1>
        <p className="text-lg text-gray-300 max-w-2xl">
          Drawing from all kinds of value sets, surfacing the right lessons at the right time
        </p>
      </div>
      
      <div className="relative">
        <svg width="800" height="500" viewBox="0 0 800 500" className="border border-gray-700 rounded-lg shadow-lg bg-black">
          {/* Grid lines */}
          <defs>
            <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
              <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#374151" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
          
          {/* Axes */}
          <motion.line
            x1="50" y1="450" x2="750" y2="450"
            stroke="white" strokeWidth="2"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 1 }}
          />
          <motion.line
            x1="50" y1="450" x2="50" y2="50"
            stroke="white" strokeWidth="2"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 1, delay: 0.5 }}
          />
          
          {/* Axis labels */}
          <motion.text
            x="400" y="480"
            textAnchor="middle"
            className="fill-white"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
          >
            Breadth (Philosophical Traditions)
          </motion.text>
          <motion.text
            x="25" y="250"
            textAnchor="middle"
            className="fill-white"
            transform="rotate(-90 25 250)"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
          >
            Depth (Relevance & Timing)
          </motion.text>
          
          {/* Philosophy nodes */}
          {philosophies.map((philosophy) => (
            <PhilosophyNode
              key={philosophy.name}
              name={philosophy.name}
              x={philosophy.x}
              y={philosophy.y}
              color={philosophy.color}
              delay={philosophy.delay}
              onAbsorb={() => handleAbsorb(philosophy.name)}
              isAbsorbed={absorbedPhilosophies.includes(philosophy.name)}
            />
          ))}
          
          {/* Sattva spike */}
          <SattvaSpike 
            height={spikeHeight}
            width={spikeWidth + absorbedPhilosophies.length * 15}
            absorbedPhilosophies={absorbedPhilosophies}
            startDepthAnimation={startDepthAnimation}
          />
          
          {/* Animated connection lines */}
          {absorbedPhilosophies.map((_, index) => (
            <motion.circle
              key={`pulse-${index}`}
              cx="400" cy="350"
              r="10"
              fill="none"
              stroke="#8B5CF6"
              strokeWidth="2"
              initial={{ r: 10, opacity: 0.8 }}
              animate={{ r: 100, opacity: 0 }}
              transition={{ 
                duration: 2, 
                repeat: Infinity, 
                delay: index * 0.5,
                ease: "easeOut"
              }}
            />
          ))}
        </svg>
        
      </div>
      
      {/* Progress indicator */}
      <motion.div 
        className="mt-6 text-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 3 }}
      >
        <div className="text-sm text-gray-300 mb-2">
          Integration Progress
        </div>
        <div className="w-64 h-2 bg-gray-700 rounded-full overflow-hidden">
          <motion.div 
            className="h-full bg-violet-500"
            initial={{ width: 0 }}
            animate={{ width: `${(absorbedPhilosophies.length / philosophies.length) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </motion.div>
    </div>
  );
}