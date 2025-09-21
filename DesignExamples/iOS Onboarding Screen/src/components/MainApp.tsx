import React from 'react';
import exampleImage from 'figma:asset/20ad9fcd5b5bdb0dc4e89513759d8eddd071a76d.png';
import { Bookmark, Share } from 'lucide-react';

export function MainApp() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col">
      {/* iOS Status Bar */}
      <div className="flex justify-between items-center px-4 pt-2 pb-1 text-white text-sm">
        <span>2:15</span>
        <div className="flex items-center gap-1">
          <div className="flex gap-1">
            <div className="w-1 h-1 bg-white rounded-full"></div>
            <div className="w-1 h-1 bg-white rounded-full"></div>
            <div className="w-1 h-1 bg-white rounded-full"></div>
            <div className="w-1 h-1 bg-white rounded-full"></div>
          </div>
          <svg className="w-4 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2.5 8.5h15l-1.5-1.5H4L2.5 8.5zm0 3h15l-1.5 1.5H4L2.5 11.5z"/>
          </svg>
          <div className="w-6 h-3 border border-white rounded-sm">
            <div className="w-4 h-full bg-green-500 rounded-sm"></div>
          </div>
        </div>
      </div>

      {/* Header Icons */}
      <div className="flex justify-between items-center px-6 py-4">
        <div className="w-8 h-8 border border-white/30 rounded-lg flex items-center justify-center">
          <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
          </svg>
        </div>
        <div className="w-8 h-8 flex items-center justify-center">
          <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,10.84 21.79,9.69 21.39,8.61L19.79,10.21C19.93,10.8 20,11.4 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.6,4 13.2,4.07 13.79,4.21L15.39,2.61C14.31,2.21 13.16,2 12,2Z"/>
          </svg>
        </div>
      </div>

      {/* Main Quote Content */}
      <div className="flex-1 flex flex-col justify-center px-8 py-16">
        <div className="text-center">
          <p className="text-white text-xl leading-relaxed mb-12 max-w-sm mx-auto">
            Better indeed is knowledge than practice; better than knowledge is meditation; better than meditation is the renunciation of the fruits of actions; peace immediately follows renunciation.
          </p>
          
          <div className="space-y-2">
            <p className="text-white text-lg">Bhagavad Gita</p>
            <p className="text-white/70 text-base">12.12</p>
          </div>
        </div>
      </div>

      {/* Bottom Actions */}
      <div className="flex justify-between items-center px-8 pb-8">
        <button className="p-3">
          <Bookmark className="w-6 h-6 text-white" />
        </button>
        <button className="p-3">
          <Share className="w-6 h-6 text-white" />
        </button>
      </div>

      {/* Home Indicator */}
      <div className="flex justify-center pb-2">
        <div className="w-32 h-1 bg-white rounded-full"></div>
      </div>
    </div>
  );
}