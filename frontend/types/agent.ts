export interface RunRequest {
  message: string;
  stream?: boolean;
  model?: string;
  user_id?: string;
  session_id?: string;
}

export interface AgentRunResponse {
  content: string;
}

export enum AgentType {
  MEAL_PLANNING_AGENT = "meal_planning_agent"
}

export enum Model {
  CLAUDE_OPUS_4_5 = "claude-opus-4-5",
  CLAUDE_SONNET_4_5 = "claude-sonnet-4-5",
  CLAUDE_SONNET_4_0 = "claude-sonnet-4-0",
  CLAUDE_OPUS_4_1 = "claude-opus-4-1",
  CLAUDE_HAIKU_4_5 = "claude-haiku-4-5",
  GPT_5_MINI = "gpt-5-mini",
  GPT_5_2 = "gpt-5.2-2025-12-11",
  GPT_4 = "gpt-4"
}
