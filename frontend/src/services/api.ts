export interface DocumentItem {
  id: string;
  name: string;
  size: string;
  type: string;
  status: 'processing' | 'ready' | 'error';
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  pageReferences?: number[];
  imageReferences?: string[];
}

export const apiService = {
  async uploadDocument(file: File): Promise<DocumentItem> {
    // Stub for backend implementation. Connects to FastAPI `/api/ingest`
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      // In production/integration, this would fetch:
      // const response = await fetch('/api/ingest', { method: 'POST', body: formData });
      // return await response.json();
      
      // Return a simulated document item for visual preview:
      return {
        id: Math.random().toString(36).substring(2, 9),
        name: file.name,
        size: `${(file.size / 1024 / 1024).toFixed(2)} MB`,
        type: file.type || 'application/pdf',
        status: 'ready'
      };
    } catch (error) {
      console.error("Upload error:", error);
      throw error;
    }
  },

  async queryRAG(_query: string, _documentId?: string): Promise<ChatMessage> {
    try {
      // Simulated delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Simulated response
      return {
        id: Math.random().toString(36).substring(2, 9),
        role: 'assistant',
        content: `Based on the active document, the requested detail was located on Page 2. The text content outlines the registered Lease & License agreement information, specifically highlighting Section 4 which describes the rent schedules and security deposits.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        pageReferences: [2],
      };
    } catch (error) {
      console.error("Query error:", error);
      throw error;
    }
  }
};
