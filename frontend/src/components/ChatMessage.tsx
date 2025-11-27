import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";
import ReactMarkdown, { Components } from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp?: string;
  isThinking?: boolean;
  metadata?: {
    searchTerms?: string;
    arxivId?: string;
    stageTimes?: {
      stage1?: number;
      stage2?: number;
      stage3?: number;
      total?: number;
    };
  };
}

const ChatMessage = ({ message, isUser, timestamp, isThinking, metadata }: ChatMessageProps) => {
  const markdownComponents: Components = {
    a: (props) => {
      const { children, ...rest } = props;
      return <a {...rest} className="text-blue-600 hover:text-blue-700 underline font-medium" target="_blank" rel="noopener noreferrer">{children}</a>;
    },
    h1: (props) => {
      const { children, ...rest } = props;
      return <h1 {...rest} className="text-lg font-bold mt-4 mb-2 text-foreground">{children}</h1>;
    },
    h2: (props) => {
      const { children, ...rest } = props;
      return <h2 {...rest} className="text-base font-bold mt-3 mb-2 text-foreground">{children}</h2>;
    },
    h3: (props) => {
      const { children, ...rest } = props;
      return <h3 {...rest} className="text-sm font-bold mt-2 mb-1 text-foreground">{children}</h3>;
    },
    ul: (props) => {
      const { children, ...rest } = props;
      return <ul {...rest} className="list-disc pl-5 space-y-1 my-2">{children}</ul>;
    },
    ol: (props) => {
      const { children, ...rest } = props;
      return <ol {...rest} className="list-decimal pl-5 space-y-1 my-2">{children}</ol>;
    },
    li: (props) => {
      const { children, ...rest } = props;
      return <li {...rest} className="text-sm leading-relaxed">{children}</li>;
    },
    p: (props) => {
      const { children, ...rest } = props;
      return <p {...rest} className="text-sm mb-2 leading-relaxed">{children}</p>;
    },
    strong: (props) => {
      const { children, ...rest } = props;
      return <strong {...rest} className="font-bold text-foreground">{children}</strong>;
    },
    em: (props) => {
      const { children, ...rest } = props;
      return <em {...rest} className="italic">{children}</em>;
    },
    code: (props) => {
      const { children, ...rest } = props;
      return <code {...rest} className="bg-muted px-1 py-0.5 rounded text-xs font-mono">{children}</code>;
    },
    pre: (props) => {
      const { children, ...rest } = props;
      return <pre {...rest} className="bg-muted p-2 rounded my-2 overflow-x-auto text-xs font-mono">{children}</pre>;
    },
  };

  return (
    <div className={cn("flex gap-3 mb-4 animate-fade-in", isUser ? "justify-end" : "justify-start")}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-gradient-accent flex items-center justify-center flex-shrink-0">
          <Bot className={cn("w-5 h-5 text-primary-foreground", isThinking && "animate-spin")} />
        </div>
      )}

      <div className={cn(
        "max-w-[70%] rounded-2xl px-4 py-3 shadow-sm",
        isUser
          ? "bg-gradient-accent text-primary-foreground"
          : "bg-card border border-border"
      )}>
        {isUser ? (
          <p className="text-sm leading-relaxed text-primary-foreground">
            {message}
          </p>
        ) : (
          <div className="prose prose-sm dark:prose-invert max-w-none">
            {isThinking ? (
              <p className="text-sm leading-relaxed">
                <span className="animate-pulse">{message}</span>
              </p>
            ) : (
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={markdownComponents}
              >
                {message}
              </ReactMarkdown>
            )}
          </div>
        )}

        {metadata && (
          <div className="mt-3 pt-2 border-t border-border/50 text-xs text-muted-foreground space-y-1">
            {metadata.searchTerms && (
              <div>Search terms: <span className="font-mono">{metadata.searchTerms}</span></div>
            )}
            {metadata.arxivId && (
              <div>arXiv Paper: <span className="font-mono">{metadata.arxivId}</span></div>
            )}
            {metadata.stageTimes && (
              <div className="flex gap-3 flex-wrap">
                {metadata.stageTimes.stage1 && <span>Stage 1: {metadata.stageTimes.stage1}s</span>}
                {metadata.stageTimes.stage2 && <span>Stage 2: {metadata.stageTimes.stage2}s</span>}
                {metadata.stageTimes.stage3 && <span>Stage 3 (Paper): {metadata.stageTimes.stage3}s</span>}
                {metadata.stageTimes.total && <span className="font-semibold">Total: {metadata.stageTimes.total}s</span>}
              </div>
            )}
          </div>
        )}

        {timestamp && (
          <p className={cn(
            "text-xs mt-2",
            isUser ? "text-primary-foreground/70" : "text-muted-foreground"
          )}>
            {timestamp}
          </p>
        )}
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
          <User className="w-5 h-5 text-primary-foreground" />
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
