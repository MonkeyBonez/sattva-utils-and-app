/**
 * Main App Component
 *
 * This is the root component of the Bhagavad Gita bookmark app.
 * It renders a simple, static list view of bookmarked verses with iOS-inspired design.
 *
 * Features:
 * - Static bookmark list display (no navigation)
 * - Dark green theme with sophisticated styling
 * - iOS-style press interactions
 * - Minimal, clean design without Sanskrit text or extra icons
 */

import { BookmarkList } from "./components/BookmarkList";
import { mockBookmarkedVerses } from "./types/verse";

export default function App() {
  return (
    // Main container: full screen with dark background
    // - w-full h-screen: Takes full viewport width and height
    // - overflow-hidden: Prevents scrollbars on the main container
    // - bg-background: Uses the custom dark green background color (#1a2e2a)
    <div className="w-full h-screen overflow-hidden bg-background">
      {/* Render the bookmark list with mock data */}
      <BookmarkList verses={mockBookmarkedVerses} />
    </div>
  );
}