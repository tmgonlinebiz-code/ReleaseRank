"""Custom hook for workflow analysis"""

import { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

interface WorkflowResult {
  winner: any;
  ranked: any[];
  total_files: number;
}

export const useWorkflow = () => {
  const [results, setResults] = useState<WorkflowResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeAndRank = async (fileIds: string[]) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/workflow/analyze-and-rank`, {
        file_ids: fileIds,
      });

      setResults(response.data);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Analysis failed';
      setError(errorMessage);
      console.error('Workflow error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    analyzeAndRank,
    results,
    isLoading,
    error,
  };
};
