/**
 * VerseFullscreen Component
 * 
 * NOTE: This component is currently not used in the app since we removed navigation.
 * It was designed to display individual verses in fullscreen reading mode.
 * 
 * Original Purpose:
 * - Fullscreen verse reading experience
 * - iOS-style navigation with back button
 * - Share and bookmark functionality
 * - Centered, readable typography
 * - Fixed bottom action buttons
 * 
 * This component demonstrates how the app could be extended to include
 * detailed verse viewing if navigation were re-added in the future.
 */

import React from 'react';
import { GitaVerse } from '../types/verse';
import { ArrowLeft, Share, Bookmark } from 'lucide-react';

// Component props interface
interface VerseFullscreenProps {
  verse: GitaVerse;    // The verse object to display
  onBack: () => void;  // Callback function to return to list view
}

export function VerseFullscreen({ verse, onBack }: VerseFullscreenProps) {
  return (
    // Fullscreen container with dark background
    <div className="bg-background min-h-screen">
      
      {/* HEADER NAVIGATION */}
      {/* Top bar with back button and action buttons */}
      <div className="px-6 pt-16 pb-4">
        <div className="flex items-center justify-between">
          
          {/* Back button - iOS-style with arrow */}
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-white hover:text-white/80 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          
          {/* Right side actions */}
          <div className="flex items-center gap-4">
            {/* Share button */}
            <button className="p-2 hover:bg-white/10 rounded-lg transition-colors">
              <Share className="w-5 h-5 text-white" />
            </button>
          </div>
        </div>
      </div>

      {/* MAIN CONTENT AREA */}
      {/* Centered content with proper spacing and typography */}
      <div className="px-6 py-8 flex flex-col justify-center min-h-[calc(100vh-120px)]">
        
        {/* VERSE CONTENT CONTAINER */}
        {/* Centered layout for optimal reading experience */}
        <div className="text-center space-y-8">
          
          {/* TRANSLATION TEXT */}
          {/* Main verse content with readable typography */}
          <div className="max-w-md mx-auto">
            <p className="text-white text-lg leading-relaxed font-normal">
              {verse.translation}
            </p>
          </div>

          {/* SOURCE ATTRIBUTION */}
          {/* Shows the source and verse reference */}
          <div className="space-y-2">
            {/* Source title */}
            <p className="text-white font-medium">
              Bhagavad Gita
            </p>
            
            {/* Chapter and verse number */}
            <p className="text-white/60 text-base">
              {verse.chapter}.{verse.verse}
            </p>
          </div>
        </div>

        {/* BOTTOM ACTION BUTTONS */}
        {/* Fixed bottom bar with bookmark and share actions */}
        <div className="fixed bottom-8 left-6 right-6 flex items-center justify-between">
          
          {/* Bookmark toggle button */}
          <button className="p-3 hover:bg-white/10 rounded-lg transition-colors">
            <Bookmark className="w-6 h-6 text-white" />
          </button>
          
          {/* Share button (duplicate for easy access) */}
          <button className="p-3 hover:bg-white/10 rounded-lg transition-colors">
            <Share className="w-6 h-6 text-white" />
          </button>
        </div>
      </div>
    </div>
  );
}