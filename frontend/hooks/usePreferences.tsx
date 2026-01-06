"use client";

import { useState, useEffect } from "react";
import { UserPreferences, UpdatePreferencesRequest } from "@/types/preferences";
import { preferencesApi, ApiError } from "@/lib/api";

export function usePreferences() {
  const [preferences, setPreferences] = useState<UserPreferences | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPreferences = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await preferencesApi.get();
      setPreferences(data);
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "Failed to fetch preferences";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const updatePreferences = async (data: UpdatePreferencesRequest) => {
    try {
      setLoading(true);
      setError(null);
      const updated = await preferencesApi.update(data);
      setPreferences(updated);
      return updated;
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "Failed to update preferences";
      setError(message);
      throw new Error(message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPreferences();
  }, []);

  return {
    preferences,
    loading,
    error,
    updatePreferences,
    refreshPreferences: fetchPreferences,
  };
}
