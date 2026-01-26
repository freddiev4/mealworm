import { User, LoginRequest, RegisterRequest, AuthResponse } from "@/types/auth";
import { UserPreferences, UpdatePreferencesRequest } from "@/types/preferences";
import { RunRequest } from "@/types/agent";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const TOKEN_KEY = "access_token";

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

// Token management
function getToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem(TOKEN_KEY);
  }
  return null;
}

function setToken(token: string): void {
  if (typeof window !== "undefined") {
    localStorage.setItem(TOKEN_KEY, token);
  }
}

function removeToken(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem(TOKEN_KEY);
  }
}

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${endpoint}`;
  const token = getToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(url, {
    ...options,
    credentials: "include", // Still include for cookie fallback
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "An error occurred" }));
    throw new ApiError(response.status, error.detail || "An error occurred");
  }

  return response.json();
}

// Auth API
export const authApi = {
  register: async (data: RegisterRequest): Promise<User> => {
    const response = await fetchApi<AuthResponse>("/v1/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    });
    setToken(response.access_token);
    return response.user;
  },

  login: async (data: LoginRequest): Promise<User> => {
    const response = await fetchApi<AuthResponse>("/v1/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    });
    setToken(response.access_token);
    return response.user;
  },

  logout: async (): Promise<{ message: string }> => {
    const result = await fetchApi<{ message: string }>("/v1/auth/logout", {
      method: "POST",
    });
    removeToken();
    return result;
  },

  me: () => fetchApi<User>("/v1/auth/me"),
};

// Preferences API
export const preferencesApi = {
  get: () => fetchApi<UserPreferences>("/v1/preferences"),

  update: (data: UpdatePreferencesRequest) =>
    fetchApi<UserPreferences>("/v1/preferences", {
      method: "PUT",
      body: JSON.stringify(data),
    }),
};

// Agent API
export const agentApi = {
  list: () => fetchApi<string[]>("/v1/agents"),

  run: async (agentId: string, data: RunRequest): Promise<string> => {
    if (data.stream) {
      // Handle streaming response
      const token = getToken();
      const headers: HeadersInit = {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
      };

      const response = await fetch(`${API_URL}/v1/agents/${agentId}/runs`, {
        method: "POST",
        credentials: "include",
        headers,
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "An error occurred" }));
        throw new ApiError(response.status, error.detail || "An error occurred");
      }

      return response.body ? await streamToString(response.body) : "";
    } else {
      // Handle non-streaming response
      const result = await fetchApi<{ content: string }>(
        `/v1/agents/${agentId}/runs`,
        {
          method: "POST",
          body: JSON.stringify(data),
        }
      );
      return result.content;
    }
  },

  runStream: async (
    agentId: string,
    data: RunRequest,
    onChunk: (chunk: string) => void
  ): Promise<void> => {
    const token = getToken();
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    };

    const response = await fetch(`${API_URL}/v1/agents/${agentId}/runs`, {
      method: "POST",
      credentials: "include",
      headers,
      body: JSON.stringify({ ...data, stream: true }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "An error occurred" }));
      throw new ApiError(response.status, error.detail || "An error occurred");
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) return;

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        onChunk(chunk);
      }
    } finally {
      reader.releaseLock();
    }
  },
};

async function streamToString(stream: ReadableStream<Uint8Array>): Promise<string> {
  const reader = stream.getReader();
  const decoder = new TextDecoder();
  let result = "";

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      result += decoder.decode(value, { stream: true });
    }
  } finally {
    reader.releaseLock();
  }

  return result;
}

export { ApiError };
