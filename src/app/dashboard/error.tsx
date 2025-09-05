'use client';

import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

interface ErrorPageProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function DashboardError({ error, reset }: ErrorPageProps) {
  useEffect(() => {
    // Log the error to the console for debugging
    console.error('Dashboard error:', error);
  }, [error]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-calm-50 to-primary-50 flex items-center justify-center p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-md w-full bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 text-center"
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
          className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6"
        >
          <AlertTriangle className="w-8 h-8 text-red-600" />
        </motion.div>

        <h1 className="text-2xl font-bold text-calm-800 mb-4">
          Dashboard Error
        </h1>
        
        <p className="text-calm-600 mb-6">
          Something went wrong while loading your dashboard. This might be due to browser storage issues or corrupted data.
        </p>

        <div className="text-xs text-calm-500 mb-6 p-3 bg-gray-50 rounded-lg text-left">
          <strong>Error details:</strong>
          <br />
          {error.message || 'Unknown error occurred'}
          {error.digest && (
            <>
              <br />
              <strong>Error ID:</strong> {error.digest}
            </>
          )}
        </div>

        <div className="space-y-3">
          <motion.button
            onClick={reset}
            className="w-full bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-xl transition-colors duration-200 flex items-center justify-center space-x-2"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <RefreshCw className="w-4 h-4" />
            <span>Try Again</span>
          </motion.button>

          <motion.button
            onClick={() => window.location.href = '/'}
            className="w-full bg-calm-200 hover:bg-calm-300 text-calm-700 font-semibold py-3 px-6 rounded-xl transition-colors duration-200 flex items-center justify-center space-x-2"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Home className="w-4 h-4" />
            <span>Go Home</span>
          </motion.button>
        </div>

        <p className="text-xs text-calm-500 mt-6">
          If this error persists, try clearing your browser data or contact support.
        </p>
      </motion.div>
    </div>
  );
}
