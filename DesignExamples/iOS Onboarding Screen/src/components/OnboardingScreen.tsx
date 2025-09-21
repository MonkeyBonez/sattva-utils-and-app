import React, { useState } from "react";
import { Button } from "./ui/button";

import appIcon from "figma:asset/504c24a61a4b80f6ce992fcb5bb88103a7d9b01a.png";
import homeScreenWidget from "figma:asset/3fc58376df1af3888caa005c7cc7a08bde84fe85.png";
import lockScreenWidget from "figma:asset/ae80b5ed7ca40c5e54302f05b4b9639e65c7f96d.png";

interface OnboardingStep {
  id: number;
  title: string;
  description: string;
  buttonText: string;
}

const onboardingSteps: OnboardingStep[] = [
  {
    id: 1,
    title: "Live aligned with the Bhagavad Gita",
    description:
      "Let's quickly set you up for weekly lessons and personalized guidance.",
    buttonText: "Get Started",
  },
  {
    id: 2,
    title: "Lesson Reminders",
    description:
      "We’ll remind you to review each week’s lesson — at the right time.",
    buttonText: "Enable Notifications",
  },
  {
    id: 3,
    title: "Lessons — where you're at",
    description:
      "Immerse yourself in the learnings of the Bhagavad Gita. Add lesson of the week widgets to your lock or home screen.",
    buttonText: "Enter App",
  },
];

interface OnboardingScreenProps {
  onComplete: () => void;
}

export function OnboardingScreen({
  onComplete,
}: OnboardingScreenProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [selectedWidget, setSelectedWidget] = useState<'home' | 'lock' | null>(null);

  const handleNext = () => {
    if (currentStep < onboardingSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      onComplete();
    }
  };

  const currentStepData = onboardingSteps[currentStep];

  return (
    <div
      className="min-h-screen flex flex-col relative"
      style={{
        background:
          "linear-gradient(to bottom, rgb(16, 34, 30), rgb(16, 34, 34))",
      }}
    >
      {/* iOS Status Bar */}
      <div className="flex justify-between items-center px-4 pt-2 pb-1 text-white text-sm">
        <span>9:41</span>
        <div className="flex items-center gap-1">
          <div className="flex gap-1">
            <div className="w-1 h-1 bg-white rounded-full"></div>
            <div className="w-1 h-1 bg-white rounded-full"></div>
            <div className="w-1 h-1 bg-white/50 rounded-full"></div>
            <div className="w-1 h-1 bg-white/50 rounded-full"></div>
          </div>
          <svg
            className="w-4 h-3 text-white"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path d="M2.5 8.5h15l-1.5-1.5H4L2.5 8.5zm0 3h15l-1.5 1.5H4L2.5 11.5z" />
          </svg>
          <div className="w-6 h-3 border border-white rounded-sm">
            <div className="w-4 h-full bg-green-500 rounded-sm"></div>
          </div>
        </div>
      </div>

      {/* Icon at the very top */}
      <div className="flex justify-center pt-8 pb-3">
        <div className="w-24 h-24 flex items-center justify-center">
          <img
            src={appIcon}
            alt="App Icon"
            className="w-full h-full object-contain"
          />
        </div>
      </div>

      {/* Hero Section - Clustered Title and Description */}
      <div className="text-center px-8 pt-2 pb-16">
        {/* Title */}
        <h1
          className="text-2xl font-semibold leading-relaxed mx-4 max-w-sm mb-3"
          style={{ color: "rgb(238, 231, 210)" }}
        >
          {currentStepData.title}
        </h1>

        {/* Description - clustered close to title */}
        <p
          className="text-base leading-loose mx-4 max-w-md"
          style={{ color: "rgb(238, 231, 210)" }}
        >
          {currentStepData.description}
        </p>
      </div>

      {/* Middle Space Content */}
      <div className="flex-1 flex items-center justify-center relative">
        {currentStep === onboardingSteps.length - 1 ? (
          /* Widget Options for Final Step - Extra Large Mockups */
          <div className="flex justify-center items-center space-x-4 px-1">
            {/* Home Screen Widget Option */}
            <button
              onClick={() => setSelectedWidget('home')}
              className={`transition-all ${
                selectedWidget === 'home' ? 'opacity-100 scale-105' : 'opacity-80'
              }`}
            >
              <img 
                src={homeScreenWidget} 
                alt="Home Screen Widget" 
                className="w-48 h-80 object-contain"
              />
            </button>

            {/* Lock Screen Widget Option */}
            <button
              onClick={() => setSelectedWidget('lock')}
              className={`transition-all ${
                selectedWidget === 'lock' ? 'opacity-100 scale-105' : 'opacity-80'
              }`}
            >
              <img 
                src={lockScreenWidget} 
                alt="Lock Screen Widget" 
                className="w-48 h-80 object-contain"
              />
            </button>
          </div>
        ) : (
          /* Mandala for Other Steps */
          <div className="absolute inset-0 flex items-center justify-center opacity-10">
            <svg
              className="w-48 h-48"
              viewBox="0 0 200 200"
              fill="none"
              style={{ color: "rgb(238, 231, 210)" }}
            >
              {/* Outer ring */}
              <circle
                cx="100"
                cy="100"
                r="90"
                stroke="currentColor"
                strokeWidth="0.5"
                fill="none"
              />
              <circle
                cx="100"
                cy="100"
                r="75"
                stroke="currentColor"
                strokeWidth="0.3"
                fill="none"
              />

              {/* Petal pattern */}
              {Array.from({ length: 8 }).map((_, i) => {
                const angle = i * 45 * (Math.PI / 180);
                const x1 = 100 + Math.cos(angle) * 50;
                const y1 = 100 + Math.sin(angle) * 50;
                const x2 = 100 + Math.cos(angle) * 70;
                const y2 = 100 + Math.sin(angle) * 70;

                return (
                  <g key={i}>
                    <circle
                      cx={x1}
                      cy={y1}
                      r="8"
                      stroke="currentColor"
                      strokeWidth="0.3"
                      fill="none"
                    />
                    <line
                      x1="100"
                      y1="100"
                      x2={x2}
                      y2={y2}
                      stroke="currentColor"
                      strokeWidth="0.2"
                    />
                  </g>
                );
              })}

              {/* Inner geometric pattern */}
              <circle
                cx="100"
                cy="100"
                r="30"
                stroke="currentColor"
                strokeWidth="0.4"
                fill="none"
              />
              <circle
                cx="100"
                cy="100"
                r="15"
                stroke="currentColor"
                strokeWidth="0.3"
                fill="none"
              />

              {/* Center lotus */}
              {Array.from({ length: 6 }).map((_, i) => {
                const angle = i * 60 * (Math.PI / 180);
                const x = 100 + Math.cos(angle) * 20;
                const y = 100 + Math.sin(angle) * 20;

                return (
                  <circle
                    key={i}
                    cx={x}
                    cy={y}
                    r="3"
                    stroke="currentColor"
                    strokeWidth="0.2"
                    fill="none"
                  />
                );
              })}
            </svg>
          </div>
        )}
      </div>

      {/* Bottom Actions */}
      <div className="px-6 pb-8">
        <Button
          onClick={handleNext}
          className="w-full py-6 text-lg rounded-2xl transition-colors"
          style={{
            backgroundColor: "rgb(238, 231, 210)",
            color: "rgb(16, 34, 30)",
          }}
        >
          {currentStepData.buttonText}
        </Button>
      </div>
    </div>
  );
}