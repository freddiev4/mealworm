"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { usePreferences } from "@/hooks/usePreferences";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { ArrowRight, ArrowLeft, Check } from "lucide-react";

type Step = 1 | 2 | 3 | 4;

export default function OnboardingPage() {
  const router = useRouter();
  const { updatePreferences } = usePreferences();
  const [step, setStep] = useState<Step>(1);
  const [loading, setLoading] = useState(false);

  // Step 1: Basic Requirements
  const [chickenDishes, setChickenDishes] = useState(1);
  const [fishDishes, setFishDishes] = useState(2);
  const [vegetablesRequired, setVegetablesRequired] = useState(true);
  const [leftoversForLunch, setLeftoversForLunch] = useState(true);

  // Step 2: Preferences
  const [likes, setLikes] = useState("");
  const [dislikes, setDislikes] = useState("olives, capers, pesto");
  const [cuisines, setCuisines] = useState("Asian, Latin, Italian, American");

  // Step 3: Dietary
  const [dietaryRestrictions, setDietaryRestrictions] = useState("");
  const [allergens, setAllergens] = useState("");
  const [avoidMealTypes, setAvoidMealTypes] = useState("stir fry");

  // Step 4: Additional
  const [saucePreference, setSaucePreference] = useState(
    "Every meal should have some kind of sauce on top. I don't like dry meals."
  );
  const [easyMealPreference, setEasyMealPreference] = useState(
    "I prefer one super easy meal where I can buy the ingredients mostly pre-made & frozen."
  );

  const nextStep = () => {
    if (step < 4) {
      setStep((step + 1) as Step);
    }
  };

  const prevStep = () => {
    if (step > 1) {
      setStep((step - 1) as Step);
    }
  };

  const handleFinish = async () => {
    setLoading(true);

    try {
      await updatePreferences({
        chicken_dishes_per_week: chickenDishes,
        fish_dishes_per_week: fishDishes,
        vegetables_required: vegetablesRequired,
        leftovers_for_lunch: leftoversForLunch,
        likes: likes.split(",").map((l) => l.trim()).filter(Boolean),
        dislikes: dislikes.split(",").map((d) => d.trim()).filter(Boolean),
        preferred_cuisines: cuisines.split(",").map((c) => c.trim()).filter(Boolean),
        dietary_restrictions: dietaryRestrictions.split(",").map((d) => d.trim()).filter(Boolean),
        allergens: allergens.split(",").map((a) => a.trim()).filter(Boolean),
        avoid_meal_types: avoidMealTypes.split(",").map((m) => m.trim()).filter(Boolean),
        sauce_preference: saucePreference,
        easy_meal_preference: easyMealPreference,
      });

      router.push("/dashboard");
    } catch (err) {
      console.error("Failed to save preferences:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-slate-900 dark:text-slate-50">
              Step {step} of 4
            </span>
            <span className="text-sm text-slate-500">
              {Math.round((step / 4) * 100)}% Complete
            </span>
          </div>
          <div className="h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-slate-900 dark:bg-slate-50 transition-all duration-300"
              style={{ width: `${(step / 4) * 100}%` }}
            />
          </div>
        </div>

        {/* Step 1: Basic Requirements */}
        {step === 1 && (
          <Card>
            <CardHeader>
              <CardTitle>Basic Meal Planning</CardTitle>
              <CardDescription>
                Let's start with your weekly meal planning basics
              </CardDescription>
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
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="vegetables"
                    checked={vegetablesRequired}
                    onChange={(e: any) => setVegetablesRequired(e.target.checked)}
                  />
                  <Label htmlFor="vegetables">I want vegetables in every meal</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="leftovers"
                    checked={leftoversForLunch}
                    onChange={(e: any) => setLeftoversForLunch(e.target.checked)}
                  />
                  <Label htmlFor="leftovers">I'll use leftovers for lunch</Label>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 2: Preferences */}
        {step === 2 && (
          <Card>
            <CardHeader>
              <CardTitle>Your Taste Preferences</CardTitle>
              <CardDescription>
                Tell us what you like and don't like
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="likes">Foods I like (comma-separated)</Label>
                <Input
                  id="likes"
                  placeholder="pasta, tacos, curry, grilled chicken"
                  value={likes}
                  onChange={(e) => setLikes(e.target.value)}
                />
                <p className="text-xs text-slate-500">Leave blank if you're open to anything</p>
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
            </CardContent>
          </Card>
        )}

        {/* Step 3: Dietary */}
        {step === 3 && (
          <Card>
            <CardHeader>
              <CardTitle>Dietary Restrictions</CardTitle>
              <CardDescription>
                Any dietary restrictions or allergies we should know about?
              </CardDescription>
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
                <p className="text-xs text-slate-500">Leave blank if none</p>
              </div>
              <div className="space-y-2">
                <Label htmlFor="allergens">Allergens (comma-separated)</Label>
                <Input
                  id="allergens"
                  placeholder="nuts, shellfish, soy"
                  value={allergens}
                  onChange={(e) => setAllergens(e.target.value)}
                />
                <p className="text-xs text-slate-500">Leave blank if none</p>
              </div>
              <div className="space-y-2">
                <Label htmlFor="avoid">Meal types to avoid (comma-separated)</Label>
                <Input
                  id="avoid"
                  placeholder="stir fry, casserole"
                  value={avoidMealTypes}
                  onChange={(e) => setAvoidMealTypes(e.target.value)}
                />
                <p className="text-xs text-slate-500">E.g., stir fry, soup, salad</p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 4: Additional Preferences */}
        {step === 4 && (
          <Card>
            <CardHeader>
              <CardTitle>Final Touches</CardTitle>
              <CardDescription>
                A few more preferences to make your meal plans perfect
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="sauce">How do you feel about sauces?</Label>
                <Textarea
                  id="sauce"
                  placeholder="Every meal should have some kind of sauce..."
                  value={saucePreference}
                  onChange={(e) => setSaucePreference(e.target.value)}
                  rows={3}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="easyMeal">Do you want any easy/quick meals?</Label>
                <Textarea
                  id="easyMeal"
                  placeholder="I prefer one super easy meal per week..."
                  value={easyMealPreference}
                  onChange={(e) => setEasyMealPreference(e.target.value)}
                  rows={4}
                />
              </div>
            </CardContent>
          </Card>
        )}

        {/* Navigation Buttons */}
        <div className="flex justify-between mt-6">
          <Button
            variant="outline"
            onClick={prevStep}
            disabled={step === 1}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Previous
          </Button>
          {step < 4 ? (
            <Button onClick={nextStep}>
              Next
              <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          ) : (
            <Button onClick={handleFinish} disabled={loading}>
              <Check className="h-4 w-4 mr-2" />
              {loading ? "Saving..." : "Finish & Start Planning"}
            </Button>
          )}
        </div>

        {/* Skip Link */}
        <div className="text-center mt-4">
          <button
            onClick={() => router.push("/dashboard")}
            className="text-sm text-slate-500 hover:text-slate-700 dark:hover:text-slate-300"
          >
            Skip for now
          </button>
        </div>
      </div>
    </div>
  );
}
