import { EmotionWheel } from './components/EmotionWheel';

export default function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8 bg-background">
      <div className="text-center mb-8">
        <h1 className="mb-2">Emotion Wheel</h1>
        <p className="text-muted-foreground">
          Navigate through layers of emotions to find what you're truly feeling
        </p>
      </div>
      <EmotionWheel />
    </div>
  );
}