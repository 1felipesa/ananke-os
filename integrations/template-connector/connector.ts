/**
 * Template de Conector Resiliente de API
 * Demonstra boas práticas de autenticação, timeout e exponential backoff.
 */

export interface ConnectorConfig {
  apiKey: string;
  baseUrl?: string;
  timeoutMs?: number;
  maxRetries?: number;
}

export class ServiceConnector {
  private apiKey: string;
  private baseUrl: string;
  private timeoutMs: number;
  private maxRetries: number;

  constructor(config: ConnectorConfig) {
    if (!config.apiKey) {
      throw new Error("Erro de Configuração: apiKey é obrigatória.");
    }
    this.apiKey = config.apiKey;
    this.baseUrl = config.baseUrl || "https://api.exemplo.com/v1";
    this.timeoutMs = config.timeoutMs || 10000;
    this.maxRetries = config.maxRetries || 3;
  }

  /**
   * Executa uma requisição segura com retentativa exponencial (Backoff)
   */
  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint.startsWith("/") ? "" : "/"}${endpoint}`;
    let attempt = 0;

    while (attempt < this.maxRetries) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeoutMs);

        const response = await fetch(url, {
          ...options,
          signal: controller.signal,
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${this.apiKey}`,
            ...(options.headers || {}),
          },
        });

        clearTimeout(timeoutId);

        // Se bater no limite de taxa (429) ou erro de servidor (5xx), tenta novamente com backoff
        if (response.status === 429 || (response.status >= 500 && response.status < 600)) {
          attempt++;
          if (attempt >= this.maxRetries) {
            throw new Error(`Serviço temporariamente indisponível. Status: ${response.status}`);
          }
          const delay = Math.pow(2, attempt) * 1000 + Math.random() * 500;
          await new Promise((resolve) => setTimeout(resolve, delay));
          continue;
        }

        if (!response.ok) {
          const errorBody = await response.text();
          throw new Error(`Falha na API [${response.status}]: ${errorBody}`);
        }

        return (await response.json()) as T;
      } catch (err: any) {
        if (err.name === "AbortError") {
          throw new Error(`Timeout de conexão após ${this.timeoutMs}ms.`);
        }
        if (attempt >= this.maxRetries - 1) {
          throw err;
        }
        attempt++;
        const delay = Math.pow(2, attempt) * 1000;
        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }

    throw new Error("Falha desconhecida na requisição.");
  }

  /**
   * Healthcheck da conexão (Ping leve)
   */
  async ping(): Promise<{ ok: boolean; status: number; message: string }> {
    try {
      // Exemplo de endpoint leve de ping/me
      const data = await this.request<{ status?: string }>("/health");
      return { ok: true, status: 200, message: "Conexão ativa e autenticada." };
    } catch (err: any) {
      return { ok: false, status: 500, message: err.message || "Falha no healthcheck." };
    }
  }
}
