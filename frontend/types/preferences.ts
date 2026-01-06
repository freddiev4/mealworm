export interface UserPreferences {
  id: number;
  user_id: number;

  // Meal Plan Requirements
  chicken_dishes_per_week: number;
  fish_dishes_per_week: number;
  vegetables_required: boolean;
  eating_out_days: string[];
  leftovers_for_lunch: boolean;

  // Meal Preferences
  likes: string[];
  dislikes: string[];
  preferred_cuisines: string[];
  sauce_preference: string;
  easy_meal_preference: string;

  // Dietary Restrictions
  dietary_restrictions: string[];
  allergens: string[];

  // Avoid certain meal types
  avoid_meal_types: string[];

  // Shopping List Template
  other_items: string[];

  // Metadata
  created_at: string;
  updated_at: string;
}

export interface UpdatePreferencesRequest {
  chicken_dishes_per_week?: number;
  fish_dishes_per_week?: number;
  vegetables_required?: boolean;
  eating_out_days?: string[];
  leftovers_for_lunch?: boolean;
  likes?: string[];
  dislikes?: string[];
  preferred_cuisines?: string[];
  sauce_preference?: string;
  easy_meal_preference?: string;
  dietary_restrictions?: string[];
  allergens?: string[];
  avoid_meal_types?: string[];
  other_items?: string[];
}
