import React, { useState } from 'react';
import { OnboardingScreen } from './components/OnboardingScreen';
import { MainApp } from './components/MainApp';

export default function App() {
  const [hasCompletedOnboarding, setHasCompletedOnboarding] = useState(false);

  const handleOnboardingComplete = () => {
    setHasCompletedOnboarding(true);
  };

  if (!hasCompletedOnboarding) {
    return <OnboardingScreen onComplete={handleOnboardingComplete} />;
  }

  return <MainApp />;
}