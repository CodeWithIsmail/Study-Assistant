import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import { Bot, User, ExternalLink } from 'lucide-react';
import type { Message } from '../types/chat';

// Import highlight.js CSS for code syntax highlighting
import 'highlight.js/styles/github-dark.css';

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
            {isUser ? (
              message.content
            ) : (
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeHighlight]}
                components={{
                  // Custom styling for markdown elements
                  code: ({ className, children, ...props }: React.HTMLProps<HTMLElement>) => {
                    const match = /language-(\w+)/.exec(className || '');
                    const isInline = !match;
                    
                    if (isInline) {
                      return (
                        <code
                          className="bg-gray-200 dark:bg-gray-600 text-red-600 dark:text-red-400 px-1 py-0.5 rounded text-sm font-mono"
                          {...props}
                        >
                          {children}
                        </code>
                      );
                    }
                    return (
                      <pre className="bg-gray-900 text-gray-100 p-3 rounded-lg overflow-x-auto my-2 text-sm">
                        <code className={className} {...props}>
                          {children}
                        </code>
                      </pre>
                    );
                  },
                  p: ({ children }) => (
                    <p className="mb-2 last:mb-0 leading-relaxed">{children}</p>
                  ),
                  strong: ({ children }) => (
                    <strong className="font-semibold">{children}</strong>
                  ),
                  em: ({ children }) => (
                    <em className="italic">{children}</em>
                  ),
                  ul: ({ children }) => (
                    <ul className="list-disc list-inside mb-2 space-y-1 ml-2">{children}</ul>
                  ),
                  ol: ({ children }) => (
                    <ol className="list-decimal list-inside mb-2 space-y-1 ml-2">{children}</ol>
                  ),
                  li: ({ children }) => (
                    <li className="text-inherit">{children}</li>
                  ),
                  blockquote: ({ children }) => (
                    <blockquote className="border-l-4 border-blue-400 pl-3 italic my-2 opacity-80">
                      {children}
                    </blockquote>
                  ),
                  h1: ({ children }) => (
                    <h1 className="text-lg font-bold mb-2 mt-3 first:mt-0">{children}</h1>
                  ),
                  h2: ({ children }) => (
                    <h2 className="text-base font-semibold mb-2 mt-3 first:mt-0">{children}</h2>
                  ),
                  h3: ({ children }) => (
                    <h3 className="text-sm font-semibold mb-1 mt-2 first:mt-0">{children}</h3>
                  ),
                  table: ({ children }) => (
                    <div className="overflow-x-auto my-2">
                      <table className="min-w-full border border-gray-300 dark:border-gray-600 text-sm">{children}</table>
                    </div>
                  ),
                  th: ({ children }) => (
                    <th className="border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-700 px-2 py-1 text-left font-semibold text-xs">
                      {children}
                    </th>
                  ),
                  td: ({ children }) => (
                    <td className="border border-gray-300 dark:border-gray-600 px-2 py-1 text-xs">{children}</td>
                  ),
                }}
              >
                {message.content}
              </ReactMarkdown>
            )}
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
