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
  const [startDepthAnimation, setStartDepthAnimation] = useState(false);
  const [pendingAbsorptions, setPendingAbsorptions] = useState<string[]>([]);

  const handleStartAbsorption = (philosophyName: string) => {
    // Start the visual absorption animation
    setPendingAbsorptions(prev => [...prev, philosophyName]);
    
    // Wait for the animation to complete (0.8s) then log and update
    setTimeout(() => {
      setAbsorbedPhilosophies(prev => {
        const newList = [...prev, philosophyName];
        console.log(`📈 Absorbed ${philosophyName}, total: ${newList.length}/${philosophies.length}`);
        return newList;
      });
    }, 800); // Match the animation duration
  };

  // Calculate width based on absorbed philosophies - starts at 60, adds 25 per philosophy
  const spikeWidth = 60 + (absorbedPhilosophies.length * 25);

  // Trigger depth animation after all philosophies are absorbed
  useEffect(() => {
    if (absorbedPhilosophies.length === philosophies.length && !startDepthAnimation) {
      console.log("All philosophies absorbed, starting depth animation in 3 seconds...");
      // Wait longer to ensure all absorption animations are complete
      // The last philosophy (Upanishads) appears at 3s + waits 3s = 6s total
      // So we wait 2 additional seconds after that = 8s total
      setTimeout(() => {
        console.log("Triggering depth animation now!");
        setStartDepthAnimation(true);
      }, 5000); // Wait 5 seconds after the last philosophy is absorbed
    }
  }, [absorbedPhilosophies.length, startDepthAnimation]);

  return (
    <div className="w-full h-screen bg-black flex flex-col items-center justify-center">
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-white">Sattva</h1>
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
              onAbsorb={() => handleStartAbsorption(philosophy.name)}
              isAbsorbed={pendingAbsorptions.includes(philosophy.name)}
            />
          ))}
          
          {/* Sattva spike */}
          <SattvaSpike 
            height={spikeHeight}
            width={spikeWidth}
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
    </div>
  );
}