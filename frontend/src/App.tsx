import React, { useState, useRef } from 'react';
import { 
  FileText, 
  Upload, 
  Send, 
  Sparkles, 
  Image as ImageIcon, 
  Layers, 
  BookOpen, 
  Loader2
} from 'lucide-react';
import { useChat } from './hooks/useChat';
import { DocumentItem } from './services/api';

export default function App() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<DocumentItem | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [activeTab, setActiveTab] = useState<'text' | 'images' | 'metadata'>('text');
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { messages, isLoading, sendMessage } = useChat();
  const [inputVal, setInputVal] = useState('');

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const processFile = async (file: File) => {
    setIsUploading(true);
    try {
      const docId = Math.random().toString(36).substring(2, 9);
      const newDoc: DocumentItem = {
        id: docId,
        name: file.name,
        size: `${(file.size / 1024 / 1024).toFixed(2)} MB`,
        type: file.type || 'application/pdf',
        status: 'processing'
      };
      
      setDocuments(prev => [...prev, newDoc]);
      setSelectedDoc(newDoc);

      // Simulate API call and ingestion processing latency
      setTimeout(() => {
        setDocuments(prev => 
          prev.map(d => d.id === docId ? { ...d, status: 'ready' } : d)
        );
        setSelectedDoc(prev => 
          prev && prev.id === docId ? { ...prev, status: 'ready' } : prev
        );
      }, 3000);
      
    } catch (err) {
      console.error("Failed to upload document", err);
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      await processFile(e.target.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      await processFile(e.dataTransfer.files[0]);
    }
  };

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputVal.trim()) return;
    sendMessage(inputVal, selectedDoc?.id);
    setInputVal('');
  };

  return (
    <div className="app-container">
      {/* Decorative Glows */}
      <div className="bg-glow-radial" />
      <div className="bg-glow-radial-2" />

      {/* Header */}
      <header className="app-header">
        <div className="logo-container">
          <Sparkles className="logo-icon" size={24} />
          <span className="logo-text">Multimodal RAG Explorer</span>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            v1.0.0 (FastAPI + React)
          </span>
        </div>
      </header>

      {/* Main workspace */}
      <main className="app-main">
        {/* Left Panel - Documents & Ingestion */}
        <section className="panel">
          <div>
            <h3 className="section-title">Documents Ingestion</h3>
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleFileChange} 
              style={{ display: 'none' }}
              accept=".pdf,.png,.jpg,.jpeg"
            />
            <div 
              className={`upload-zone ${isDragging ? 'dragging' : ''}`} 
              onClick={handleUploadClick}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              {isUploading ? (
                <Loader2 className="upload-icon" size={32} style={{ animation: 'spin 1s linear infinite' }} />
              ) : (
                <Upload className="upload-icon" size={32} />
              )}
              <div>
                <p style={{ fontSize: '0.9rem', fontWeight: 600 }}>Drag PDF Here</p>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: '0.25rem 0' }}>or</p>
                <button style={{ 
                  background: 'rgba(168, 85, 247, 0.1)', 
                  border: '1px solid var(--primary)', 
                  color: 'var(--primary-light)', 
                  padding: '0.3rem 0.8rem', 
                  borderRadius: '6px', 
                  fontSize: '0.8rem', 
                  cursor: 'pointer',
                  fontWeight: 600
                }}>
                  Upload PDF
                </button>
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', flex: 1, overflow: 'hidden' }}>
            <h3 className="section-title">Uploaded Files</h3>
            <div className="doc-list" style={{ overflowY: 'auto', flex: 1 }}>
              {documents.length === 0 ? (
                <div className="empty-state" style={{ padding: '1rem 0' }}>
                  <FileText size={24} />
                  <p style={{ fontSize: '0.8rem' }}>No documents ingested yet</p>
                </div>
              ) : (
                documents.map(doc => (
                  <div 
                    key={doc.id} 
                    className="doc-item"
                    style={{
                      borderColor: selectedDoc?.id === doc.id ? 'var(--primary)' : 'var(--border-color)',
                      background: selectedDoc?.id === doc.id ? 'rgba(168, 85, 247, 0.08)' : 'rgba(255, 255, 255, 0.02)'
                    }}
                    onClick={() => setSelectedDoc(doc)}
                  >
                    <div className="doc-info" style={{ flex: 1 }}>
                      <FileText size={18} style={{ color: 'var(--primary)', flexShrink: 0 }} />
                      <div style={{ overflow: 'hidden', flex: 1 }}>
                        <p className="doc-name">{doc.name}</p>
                        <span className="doc-meta">{doc.size}</span>
                      </div>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      {doc.status === 'processing' ? (
                        <span className="status-badge status-processing">Processing...</span>
                      ) : (
                        <span className="status-badge status-ready">Ready</span>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </section>

        {/* Center Panel - Conversational RAG */}
        <section className="chat-container">
          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="empty-state" style={{ margin: 'auto' }}>
                <Sparkles size={48} style={{ color: 'var(--primary)', marginBottom: '0.5rem' }} />
                <h2>Explore with Multimodal RAG</h2>
                <p style={{ maxWidth: '400px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                  Upload a document, type your question, and visual sources will automatically be located.
                </p>
              </div>
            ) : (
              messages.map(msg => (
                <div 
                  key={msg.id} 
                  className={`chat-message ${msg.role === 'user' ? 'message-user' : 'message-assistant'}`}
                >
                  <div className="message-avatar">
                    {msg.role === 'user' ? 'U' : 'AI'}
                  </div>
                  <div>
                    <div className="message-bubble">
                      <p>{msg.content}</p>
                    </div>
                    <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.4rem', fontSize: '0.75rem', color: 'var(--text-muted)', justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start' }}>
                      <span>{msg.timestamp}</span>
                      {msg.pageReferences && msg.pageReferences.length > 0 && (
                        <span style={{ color: 'var(--secondary)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '2px' }}>
                          <BookOpen size={12} /> Ref Page {msg.pageReferences.join(', ')}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="chat-message message-assistant">
                <div className="message-avatar">AI</div>
                <div className="message-bubble" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Loader2 size={16} style={{ animation: 'spin 1s linear infinite' }} />
                  <span>Synthesizing response...</span>
                </div>
              </div>
            )}
          </div>

          <div className="chat-input-container">
            <form className="chat-form" onSubmit={handleFormSubmit}>
              <input 
                type="text" 
                className="chat-input"
                placeholder={selectedDoc ? "Ask about the document..." : "Upload a document on the left to start"}
                disabled={!selectedDoc || isLoading}
                value={inputVal}
                onChange={e => setInputVal(e.target.value)}
              />
              <button 
                type="submit" 
                className="btn-send"
                disabled={!selectedDoc || isLoading || !inputVal.trim()}
              >
                <Send size={18} />
              </button>
            </form>
          </div>
        </section>

        {/* Right Panel - Document Viewer & Source Reference */}
        <section className="panel panel-right">
          <div className="viewer-panel">
            <div className="viewer-header">
              <h3 className="section-title" style={{ margin: 0 }}>Document Inspector</h3>
              {selectedDoc && (
                <span style={{ fontSize: '0.75rem', background: 'rgba(255,255,255,0.05)', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>
                  Page 1 of 3
                </span>
              )}
            </div>

            {/* Navigation Tabs */}
            <div style={{ display: 'flex', borderBottom: '1px solid var(--border-color)', marginBottom: '1rem', gap: '1rem' }}>
              <button 
                style={{ 
                  background: 'none', 
                  border: 'none', 
                  color: activeTab === 'text' ? 'var(--primary)' : 'var(--text-muted)', 
                  borderBottom: activeTab === 'text' ? '2px solid var(--primary)' : '2px solid transparent',
                  padding: '0.5rem 0',
                  cursor: 'pointer',
                  fontWeight: 600,
                  fontSize: '0.85rem'
                }}
                onClick={() => setActiveTab('text')}
              >
                Document Text
              </button>
              <button 
                style={{ 
                  background: 'none', 
                  border: 'none', 
                  color: activeTab === 'images' ? 'var(--primary)' : 'var(--text-muted)', 
                  borderBottom: activeTab === 'images' ? '2px solid var(--primary)' : '2px solid transparent',
                  padding: '0.5rem 0',
                  cursor: 'pointer',
                  fontWeight: 600,
                  fontSize: '0.85rem'
                }}
                onClick={() => setActiveTab('images')}
              >
                Extracted Images
              </button>
            </div>

            <div className="viewer-content">
              {selectedDoc ? (
                selectedDoc.status === 'processing' ? (
                  <div className="empty-state">
                    <Loader2 size={32} style={{ animation: 'spin 1s linear infinite', color: 'var(--primary)' }} />
                    <p style={{ fontSize: '0.85rem', fontWeight: 600 }}>Processing PDF...</p>
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Parsing layout, texts, and extracting page images</p>
                  </div>
                ) : activeTab === 'text' ? (
                  <div className="pdf-viewer-container">
                    <div className="pdf-page-mock">
                      <div className="pdf-page-header">
                        <span>{selectedDoc.name}</span>
                        <span>Page 1 of 2</span>
                      </div>
                      <div className="pdf-page-body">
                        <h3 style={{ fontSize: '1rem', marginBottom: '1rem', fontWeight: 700 }}>LEASE AND LICENSE AGREEMENT</h3>
                        <p style={{ marginBottom: '1rem' }}>
                          This Lease and License Agreement is entered into on this 9th day of January, 2027 by and between the Licensor (hereinafter referred to as the party of the First Part) and the Licensee (hereinafter referred to as the party of the Second Part).
                        </p>
                        <p>
                          WHEREAS the Licensor is the absolute owner of the premises situated at Flat 303, Bhakti Rajarshi Heights, and wishes to lease the premises under the following terms...
                        </p>
                      </div>
                    </div>

                    <div className="pdf-page-mock">
                      <div className="pdf-page-header">
                        <span>{selectedDoc.name}</span>
                        <span>Page 2 of 2</span>
                      </div>
                      <div className="pdf-page-body">
                        <div className="pdf-highlight-zone">
                          <h4 style={{ fontSize: '0.9rem', color: 'var(--primary)', marginBottom: '0.5rem', fontWeight: 700 }}>
                            Section 4: Rent and Security Deposit
                          </h4>
                          <p>
                            The licensee shall pay a monthly license fee of ₹25,000 (Rupees Twenty-Five Thousand Only), payable in advance on or before the 5th day of every calendar month.
                          </p>
                        </div>
                        <p style={{ marginTop: '1rem' }}>
                          IN WITNESS WHEREOF the parties hereto have signed and executed this agreement on the day and year first above written.
                        </p>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="empty-state">
                    <ImageIcon size={32} />
                    <p style={{ fontSize: '0.8rem' }}>No visual assets detected on current page</p>
                  </div>
                )
              ) : (
                <div className="empty-state">
                  <Layers size={32} />
                  <p style={{ fontSize: '0.8rem' }}>Select a document to inspect contents</p>
                </div>
              )}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
