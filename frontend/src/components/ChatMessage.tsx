import React from 'react';
import { Bot, User, ExternalLink } from 'lucide-react';
import type { Message } from '../types/chat';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  
  return (
    <div className={`flex w-full mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 ${isUser ? 'ml-3' : 'mr-3'}`}>
          <div className={`
            w-8 h-8 rounded-full flex items-center justify-center
            ${isUser 
              ? 'bg-blue-500 text-white' 
              : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300'
            }
          `}>
            {isUser ? <User size={16} /> : <Bot size={16} />}
          </div>
        </div>

        {/* Message Content */}
        <div className={`
          rounded-2xl px-4 py-3 shadow-sm
          ${isUser 
            ? 'bg-blue-500 text-white' 
            : 'bg-white text-gray-800 dark:bg-gray-800 dark:text-gray-200 border border-gray-200 dark:border-gray-700'
          }
        `}>
          <div className="whitespace-pre-wrap break-words">
            {message.content}
          </div>
          
          {/* Sources for assistant messages */}
          {!isUser && message.sources && message.sources.length > 0 && (
            <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
              <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                Sources:
              </div>
              <div className="space-y-2">
                {message.sources.map((source, index) => (
                  <div 
                    key={index}
                    className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3 text-sm"
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <ExternalLink size={12} />
                      <span className="font-medium text-gray-700 dark:text-gray-300">
                        {source.source}
                      </span>
                    </div>
                    <div className="text-gray-600 dark:text-gray-400 text-xs line-clamp-2">
                      {source.content_preview}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* Timestamp */}
          <div className={`
            text-xs mt-2 
            ${isUser ? 'text-blue-100' : 'text-gray-500 dark:text-gray-400'}
          `}>
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;
