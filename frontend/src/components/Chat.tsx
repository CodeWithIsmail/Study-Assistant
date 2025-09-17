import React, { useState, useEffect, useRef } from 'react';
import { BookOpen, AlertCircle, Wifi, WifiOff } from 'lucide-react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import chatService from '../services/api';
import type { Message, ChatState } from '../types/chat';

const Chat: React.FC = () => {
  const [chatState, setChatState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    error: null,
  });
  const [isConnected, setIsConnected] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Check backend connection on mount
  useEffect(() => {
    const checkConnection = async () => {
      const connected = await chatService.checkHealth();
      setIsConnected(connected);
    };
    checkConnection();
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatState.messages]);

  // Add welcome message on first load
  useEffect(() => {
    if (chatState.messages.length === 0) {
      const welcomeMessage: Message = {
        id: 'welcome',
        content: "Hello! I'm your Study Assistant. I can help you find information from your uploaded documents. What would you like to know?",
        sender: 'assistant',
        timestamp: new Date(),
      };
      setChatState(prev => ({
        ...prev,
        messages: [welcomeMessage]
      }));
    }
  }, [chatState.messages.length]);

  const handleSendMessage = async (content: string) => {
    if (!isConnected) {
      setChatState(prev => ({
        ...prev,
        error: 'Not connected to the backend server. Please make sure the server is running.'
      }));
      return;
    }

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      sender: 'user',
      timestamp: new Date(),
    };

    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: null,
    }));

    try {
      // Call backend API
      const response = await chatService.askQuestion(content);
      
      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.answer,
        sender: 'assistant',
        timestamp: new Date(),
        sources: response.sources,
      };

      setChatState(prev => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        isLoading: false,
      }));
    } catch (error) {
      console.error('Error sending message:', error);
      
      let errorMessage = 'Sorry, I encountered an error while processing your question.';
      
      if (error instanceof Error) {
        if (error.message.includes('400')) {
          errorMessage = 'No knowledge base found. Please make sure documents are uploaded to the system first.';
        } else if (error.message.includes('500')) {
          errorMessage = 'Server error occurred. Please try again in a moment.';
        } else if (error.message.includes('timeout')) {
          errorMessage = 'Request timed out. The question might be too complex or the server is busy.';
        }
      }

      setChatState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
    }
  };

  const clearError = () => {
    setChatState(prev => ({ ...prev, error: null }));
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
              <BookOpen size={20} className="text-white" />
            </div>
            <div>
              <h1 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                Study Assistant
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                AI-powered document chat
              </p>
            </div>
          </div>
          
          {/* Connection Status */}
          <div className="flex items-center space-x-2">
            {isConnected ? (
              <div className="flex items-center space-x-1 text-green-600 dark:text-green-400">
                <Wifi size={16} />
                <span className="text-sm">Connected</span>
              </div>
            ) : (
              <div className="flex items-center space-x-1 text-red-600 dark:text-red-400">
                <WifiOff size={16} />
                <span className="text-sm">Disconnected</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Error Banner */}
      {chatState.error && (
        <div className="bg-red-50 dark:bg-red-900/20 border-b border-red-200 dark:border-red-800 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <AlertCircle size={16} className="text-red-500" />
              <span className="text-red-700 dark:text-red-300 text-sm">
                {chatState.error}
              </span>
            </div>
            <button
              onClick={clearError}
              className="text-red-500 hover:text-red-700 dark:hover:text-red-300"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {chatState.messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        
        {/* Loading indicator */}
        {chatState.isLoading && (
          <div className="flex justify-start mb-6">
            <div className="flex items-center space-x-2 bg-white dark:bg-gray-800 rounded-2xl px-4 py-3 shadow-sm border border-gray-200 dark:border-gray-700">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
              <span className="text-gray-500 dark:text-gray-400 text-sm">Thinking...</span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput
        onSendMessage={handleSendMessage}
        isLoading={chatState.isLoading}
        disabled={!isConnected}
      />
    </div>
  );
};

export default Chat;
