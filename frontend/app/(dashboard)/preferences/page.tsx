"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { usePreferences } from "@/hooks/usePreferences";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { ArrowLeft, Save } from "lucide-react";

export default function PreferencesPage() {
  const router = useRouter();
  const { logout } = useAuth();
  const { preferences, loading, updatePreferences } = usePreferences();

  // Form state
  const [chickenDishes, setChickenDishes] = useState(1);
  const [fishDishes, setFishDishes] = useState(2);
  const [vegetablesRequired, setVegetablesRequired] = useState(true);
  const [leftoversForLunch, setLeftoversForLunch] = useState(true);
  const [eatingOutDays, setEatingOutDays] = useState("Friday, Saturday");
  const [likes, setLikes] = useState("");
  const [dislikes, setDislikes] = useState("");
  const [cuisines, setCuisines] = useState("");
  const [saucePreference, setSaucePreference] = useState("");
  const [easyMealPreference, setEasyMealPreference] = useState("");
  const [dietaryRestrictions, setDietaryRestrictions] = useState("");
  const [allergens, setAllergens] = useState("");
  const [avoidMealTypes, setAvoidMealTypes] = useState("");
  const [otherItems, setOtherItems] = useState("");
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Load preferences into form
  useEffect(() => {
    if (preferences) {
      setChickenDishes(preferences.chicken_dishes_per_week);
      setFishDishes(preferences.fish_dishes_per_week);
      setVegetablesRequired(preferences.vegetables_required);
      setLeftoversForLunch(preferences.leftovers_for_lunch);
      setEatingOutDays(preferences.eating_out_days.join(", "));
      setLikes(preferences.likes.join(", "));
      setDislikes(preferences.dislikes.join(", "));
      setCuisines(preferences.preferred_cuisines.join(", "));
      setSaucePreference(preferences.sauce_preference);
      setEasyMealPreference(preferences.easy_meal_preference);
      setDietaryRestrictions(preferences.dietary_restrictions.join(", "));
      setAllergens(preferences.allergens.join(", "));
      setAvoidMealTypes(preferences.avoid_meal_types.join(", "));
      setOtherItems(preferences.other_items.join("\n"));
    }
  }, [preferences]);

  const handleSave = async () => {
    setSaving(true);
    setSaveSuccess(false);

    try {
      await updatePreferences({
        chicken_dishes_per_week: chickenDishes,
        fish_dishes_per_week: fishDishes,
        vegetables_required: vegetablesRequired,
        leftovers_for_lunch: leftoversForLunch,
        eating_out_days: eatingOutDays.split(",").map((d) => d.trim()).filter(Boolean),
        likes: likes.split(",").map((l) => l.trim()).filter(Boolean),
        dislikes: dislikes.split(",").map((d) => d.trim()).filter(Boolean),
        preferred_cuisines: cuisines.split(",").map((c) => c.trim()).filter(Boolean),
        sauce_preference: saucePreference,
        easy_meal_preference: easyMealPreference,
        dietary_restrictions: dietaryRestrictions.split(",").map((d) => d.trim()).filter(Boolean),
        allergens: allergens.split(",").map((a) => a.trim()).filter(Boolean),
        avoid_meal_types: avoidMealTypes.split(",").map((m) => m.trim()).filter(Boolean),
        other_items: otherItems.split("\n").map((i) => i.trim()).filter(Boolean),
      });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      console.error("Failed to save preferences:", err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-900"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      {/* Header */}
      <header className="bg-white dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <Button variant="ghost" size="sm" onClick={() => router.push("/dashboard")}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
            <Button variant="ghost" size="sm" onClick={logout}>
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-50">
            Meal Planning Preferences
          </h1>
          <p className="text-slate-500 mt-2">
            Customize your meal planning experience
          </p>
        </div>

        <div className="space-y-6">
          {/* Meal Plan Requirements */}
          <Card>
            <CardHeader>
              <CardTitle>Meal Plan Requirements</CardTitle>
              <CardDescription>Set your weekly meal planning rules</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="chicken">Chicken dishes per week</Label>
                  <Input
                    id="chicken"
                    type="number"
                    min="0"
                    max="7"
                    value={chickenDishes}
                    onChange={(e) => setChickenDishes(parseInt(e.target.value) || 0)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="fish">Fish dishes per week</Label>
                  <Input
                    id="fish"
                    type="number"
                    min="0"
                    max="7"
                    value={fishDishes}
                    onChange={(e) => setFishDishes(parseInt(e.target.value) || 0)}
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="eatingOut">Eating out days (comma-separated)</Label>
                <Input
                  id="eatingOut"
                  placeholder="Friday, Saturday"
                  value={eatingOutDays}
                  onChange={(e) => setEatingOutDays(e.target.value)}
                />
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="vegetables"
                  checked={vegetablesRequired}
                  onChange={(e: any) => setVegetablesRequired(e.target.checked)}
                />
                <Label htmlFor="vegetables">Vegetables required in every meal</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="leftovers"
                  checked={leftoversForLunch}
                  onChange={(e: any) => setLeftoversForLunch(e.target.checked)}
                />
                <Label htmlFor="leftovers">Use leftovers for lunch</Label>
              </div>
            </CardContent>
          </Card>

          {/* Meal Preferences */}
          <Card>
            <CardHeader>
              <CardTitle>Meal Preferences</CardTitle>
              <CardDescription>Your taste and cuisine preferences</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="likes">Foods I like (comma-separated)</Label>
                <Input
                  id="likes"
                  placeholder="pasta, tacos, curry"
                  value={likes}
                  onChange={(e) => setLikes(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="dislikes">Foods I dislike (comma-separated)</Label>
                <Input
                  id="dislikes"
                  placeholder="olives, capers, pesto"
                  value={dislikes}
                  onChange={(e) => setDislikes(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="cuisines">Preferred cuisines (comma-separated)</Label>
                <Input
                  id="cuisines"
                  placeholder="Asian, Latin, Italian, American"
                  value={cuisines}
                  onChange={(e) => setCuisines(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="sauce">Sauce preference</Label>
                <Textarea
                  id="sauce"
                  placeholder="Every meal should have some kind of sauce..."
                  value={saucePreference}
                  onChange={(e) => setSaucePreference(e.target.value)}
                  rows={2}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="easyMeal">Easy meal preference</Label>
                <Textarea
                  id="easyMeal"
                  placeholder="I prefer one super easy meal..."
                  value={easyMealPreference}
                  onChange={(e) => setEasyMealPreference(e.target.value)}
                  rows={3}
                />
              </div>
            </CardContent>
          </Card>

          {/* Dietary Restrictions */}
          <Card>
            <CardHeader>
              <CardTitle>Dietary Restrictions</CardTitle>
              <CardDescription>Health and allergy considerations</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="restrictions">Dietary restrictions (comma-separated)</Label>
                <Input
                  id="restrictions"
                  placeholder="vegetarian, gluten-free, dairy-free"
                  value={dietaryRestrictions}
                  onChange={(e) => setDietaryRestrictions(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="allergens">Allergens (comma-separated)</Label>
                <Input
                  id="allergens"
                  placeholder="nuts, shellfish, soy"
                  value={allergens}
                  onChange={(e) => setAllergens(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="avoid">Meal types to avoid (comma-separated)</Label>
                <Input
                  id="avoid"
                  placeholder="stir fry, casserole"
                  value={avoidMealTypes}
                  onChange={(e) => setAvoidMealTypes(e.target.value)}
                />
              </div>
            </CardContent>
          </Card>

          {/* Shopping List */}
          <Card>
            <CardHeader>
              <CardTitle>Shopping List Template</CardTitle>
              <CardDescription>Standard items to include in every shopping list</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <Label htmlFor="otherItems">Other items (one per line)</Label>
                <Textarea
                  id="otherItems"
                  placeholder="Almond milk&#10;Eggs&#10;Bread"
                  value={otherItems}
                  onChange={(e) => setOtherItems(e.target.value)}
                  rows={10}
                />
              </div>
            </CardContent>
          </Card>

          {/* Save Button */}
          <div className="flex justify-end gap-4">
            {saveSuccess && (
              <p className="text-green-600 flex items-center">
                Preferences saved successfully!
              </p>
            )}
            <Button onClick={handleSave} disabled={saving} size="lg">
              <Save className="h-4 w-4 mr-2" />
              {saving ? "Saving..." : "Save Preferences"}
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}
