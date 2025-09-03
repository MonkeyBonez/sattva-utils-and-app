/**
 * BookmarkList Component
 * 
 * Displays a static list of bookmarked Bhagavad Gita verses in an iOS-inspired design.
 * This is the main interface component that shows saved verses with their chapter.verse
 * references and English translations.
 * 
 * Design Features:
 * - Dark green theme with sophisticated dark teal backgrounds
 * - iOS-style press interactions (scale, shadow, background changes)
 * - Minimal design without Sanskrit text, heart icons, or click indicators
 * - Clean typography hierarchy with proper spacing
 * - Empty state with encouraging messaging
 */

import React from 'react';
import { GitaVerse } from '../types/verse';
import { BookOpen } from 'lucide-react';

// Component props interface
interface BookmarkListProps {
  verses: GitaVerse[]; // Array of bookmarked verse objects
}

export function BookmarkList({ verses }: BookmarkListProps) {
  return (
    <div className="bg-background min-h-screen">
      {/* Header Section - Contains title and verse count */}
      <div className="px-6 pt-16 pb-6">
        <h1 className="text-white text-2xl font-medium mb-2">Bookmarks</h1>
        <p className="text-white/60 text-base">
          {verses.length} saved verse{verses.length !== 1 ? 's' : ''}
        </p>
      </div>

      {/* Content Section - Main scrollable area */}
      <div className="px-6 pb-8">
        {/* Empty State - Displayed when no verses are bookmarked */}
        {verses.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            {/* Empty state icon */}
            <div className="p-4 bg-white/10 rounded-full mb-6">
              <BookOpen className="w-8 h-8 text-white/60" />
            </div>
            <h3 className="text-white text-xl font-medium mb-3">No bookmarks yet</h3>
            <p className="text-white/60 text-base max-w-xs leading-relaxed">
              Start exploring the Gita and bookmark verses that inspire you
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {verses.map((verse) => (
              <div
                key={verse.id}
                className="bg-white/5 border border-white/10 rounded-2xl p-4 active:scale-[0.98] active:shadow-card-pressed active:bg-white/8 transition-all duration-150 shadow-card"
              >
                {/* Chapter.Verse Header - Badge showing the verse reference */}
                <div className="flex items-center gap-3 mb-3">
                  <div className="px-2.5 py-1 bg-white/10 rounded-full shadow-sm shadow-black/10">
                    <span className="text-white text-sm font-medium">
                      {verse.chapter}.{verse.verse}
                    </span>
                  </div>
                </div>

                {/* Translation Preview - English translation with line clamping */}
                <div>
                  <p className="text-white text-base leading-relaxed line-clamp-3">
                    {verse.translation}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}