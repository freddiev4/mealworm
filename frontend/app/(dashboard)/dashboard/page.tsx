"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { agentApi } from "@/lib/api";
import { AgentType, Model } from "@/types/agent";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { LogOut, Settings, Sparkles, Copy, Check } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout } = useAuth();
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  const handleGenerateMealPlan = async () => {
    if (!message.trim()) {
      setError("Please enter a message for the meal planner");
      return;
    }

    setLoading(true);
    setError("");
    setResponse("");

    try {
      await agentApi.runStream(
        AgentType.MEAL_PLANNING_AGENT,
        {
          message,
          stream: true,
          model: Model.CLAUDE_SONNET_4_0,
        },
        (chunk) => {
          setResponse((prev) => prev + chunk);
        }
      );
    } catch (err: any) {
      setError(err.message || "Failed to generate meal plan");
    } finally {
      setLoading(false);
    }
  };

  const handleQuickGenerate = () => {
    setMessage("Generate me a meal plan for next week");
    setTimeout(() => {
      const button = document.getElementById("generate-button");
      button?.click();
    }, 100);
  };

  const handleCopyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(response);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      {/* Header */}
      <header className="bg-white dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-50">
                Mealworm
              </h1>
              <p className="text-sm text-slate-500">
                Welcome back, {user?.email}
              </p>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => router.push("/preferences")}
              >
                <Settings className="h-4 w-4 mr-2" />
                Preferences
              </Button>
              <Button variant="ghost" size="sm" onClick={logout}>
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="h-5 w-5" />
                Generate Meal Plan
              </CardTitle>
              <CardDescription>
                Ask the AI to create a personalized meal plan based on your preferences
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Textarea
                  placeholder="E.g., 'Generate me a meal plan for next week' or 'Create a meal plan with more Asian dishes'"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  rows={4}
                  disabled={loading}
                />
              </div>
              {error && (
                <div className="text-sm text-red-600 bg-red-50 dark:bg-red-900/20 p-3 rounded-md">
                  {error}
                </div>
              )}
              <div className="flex gap-2">
                <Button
                  id="generate-button"
                  onClick={handleGenerateMealPlan}
                  disabled={loading}
                  className="flex-1"
                >
                  {loading ? "Generating..." : "Generate"}
                </Button>
                <Button
                  variant="outline"
                  onClick={handleQuickGenerate}
                  disabled={loading}
                >
                  Quick Generate
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Response Section */}
          <Card>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle>Your Meal Plan</CardTitle>
                  <CardDescription>
                    AI-generated meal plan with shopping list
                  </CardDescription>
                </div>
                {response && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleCopyToClipboard}
                    className="ml-4"
                  >
                    {copied ? (
                      <>
                        <Check className="h-4 w-4 mr-2" />
                        Copied!
                      </>
                    ) : (
                      <>
                        <Copy className="h-4 w-4 mr-2" />
                        Copy
                      </>
                    )}
                  </Button>
                )}
              </div>
            </CardHeader>
            <CardContent>
              {loading && !response && (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-slate-900 dark:border-slate-50"></div>
                </div>
              )}
              {response && (
                <div className="prose prose-slate dark:prose-invert max-w-none overflow-auto max-h-[600px] p-4">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      h1: ({node, ...props}) => <h1 className="text-3xl font-bold mb-4 mt-6" {...props} />,
                      h2: ({node, ...props}) => <h2 className="text-2xl font-semibold mb-3 mt-5" {...props} />,
                      h3: ({node, ...props}) => <h3 className="text-xl font-semibold mb-2 mt-4" {...props} />,
                      ul: ({node, ...props}) => <ul className="list-disc pl-6 mb-4 space-y-1" {...props} />,
                      ol: ({node, ...props}) => <ol className="list-decimal pl-6 mb-4 space-y-1" {...props} />,
                      p: ({node, ...props}) => <p className="mb-3" {...props} />,
                      a: ({node, ...props}) => <a className="text-blue-600 hover:underline" {...props} />,
                    }}
                  >
                    {response}
                  </ReactMarkdown>
                </div>
              )}
              {!loading && !response && (
                <div className="text-center py-12 text-slate-500">
                  <Sparkles className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>Your meal plan will appear here</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Quick Tips */}
        <Card className="mt-6">
          <CardHeader>
            <CardTitle className="text-lg">Tips for Better Meal Plans</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li>• Be specific about dietary needs or cuisine preferences</li>
              <li>• Mention if you want easy meals or more elaborate dishes</li>
              <li>• Update your preferences to get more personalized results</li>
              <li>• Ask for variations: "more vegetables" or "less cooking time"</li>
            </ul>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
