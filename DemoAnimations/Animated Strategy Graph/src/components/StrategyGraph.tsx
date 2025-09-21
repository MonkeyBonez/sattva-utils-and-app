import React, { useState, useEffect } from 'react';
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
  const [completedPhilosophies, setCompletedPhilosophies] = useState<string[]>([]);
  const [spikeHeight, setSpikeHeight] = useState(150); // Fixed height initially
  const [spikeWidth, setSpikeWidth] = useState(60);
  const [startDepthAnimation, setStartDepthAnimation] = useState(false);

  const handleAbsorb = (philosophyName: string) => {
    setAbsorbedPhilosophies(prev => [...prev, philosophyName]);
  };

  // Trigger depth animation after all philosophies have COMPLETED absorption
  useEffect(() => {
    if (completedPhilosophies.length === philosophies.length && !startDepthAnimation) {
      console.log("All philosophies absorbed (completed), starting depth animation in 3 seconds...");
      setTimeout(() => {
        console.log("Triggering depth animation now!");
        setStartDepthAnimation(true);
      }, 3000); // Wait 3 seconds after the last philosophy is absorbed
    }
  }, [completedPhilosophies.length, startDepthAnimation]);

  // Option A: animate spike height (depth) once the depth animation starts
  useEffect(() => {
    if (!startDepthAnimation) return;
    const targetHeight = 320; // final depth height
    const step = 8;
    const intervalMs = 50;

    const intervalId = setInterval(() => {
      setSpikeHeight((current) => {
        if (current >= targetHeight) {
          clearInterval(intervalId);
          return current;
        }
        const next = current + step;
        return next >= targetHeight ? targetHeight : next;
      });
    }, intervalMs);

    return () => clearInterval(intervalId);
  }, [startDepthAnimation]);

  return (
    <div className="w-full h-screen flex flex-col items-center justify-center" style={{ backgroundColor: '#10221E' }}>
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold mb-4" style={{ color: '#EEE7D2' }}>The Future of Sattva</h1>
        <p className="text-lg max-w-2xl" style={{ color: '#EEE7D2' }}>
          Drawing from all kinds of value sets, surfacing the right lessons at the right time
        </p>
      </div>
      
      <div className="relative">
        <svg width="800" height="500" viewBox="0 0 800 500" className="border border-gray-700 rounded-lg shadow-lg" style={{ backgroundColor: '#10221E' }}>
          {/* Grid lines */}
          <defs>
            <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
              <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#EEE7D2" strokeOpacity="0.15" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
          
          {/* Axes */}
          <motion.line
            x1="50" y1="450" x2="750" y2="450"
            stroke="#EEE7D2" strokeWidth="2"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 1 }}
          />
          <motion.line
            x1="50" y1="450" x2="50" y2="50"
            stroke="#EEE7D2" strokeWidth="2"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 1, delay: 0.5 }}
          />
          
          {/* Axis labels */}
          <motion.text
            x="400" y="480"
            textAnchor="middle"
            fill="#EEE7D2"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
          >
            Breadth (Philosophical Traditions)
          </motion.text>
          <motion.text
            x="25" y="250"
            textAnchor="middle"
            fill="#EEE7D2"
            transform="rotate(-90 25 250)"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
          >
            Depth (Relevance & Timing)
          </motion.text>
          
          {/* Philosophy nodes */}
          {philosophies.map((philosophy) => (
            <React.Fragment key={philosophy.name}>
              <PhilosophyNode
                name={philosophy.name}
                x={philosophy.x}
                y={philosophy.y}
                color={philosophy.color}
                delay={philosophy.delay}
                onAbsorb={() => handleAbsorb(philosophy.name)}
                onAbsorbComplete={() => {
                  setCompletedPhilosophies((prev) => {
                    if (prev.includes(philosophy.name)) return prev;
                    const next = [...prev, philosophy.name];
                    console.log(`📈 Absorbed ${philosophy.name}, total: ${next.length}/${philosophies.length}`);
                    return next;
                  });
                }}
                isAbsorbed={absorbedPhilosophies.includes(philosophy.name)}
              />
            </React.Fragment>
          ))}
          
          {/* Sattva spike */}
          <SattvaSpike 
            height={spikeHeight}
            width={spikeWidth + completedPhilosophies.length * 40}
            absorbedPhilosophies={absorbedPhilosophies}
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