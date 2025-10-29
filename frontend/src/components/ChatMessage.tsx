import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp?: string;
}

const ChatMessage = ({ message, isUser, timestamp }: ChatMessageProps) => {
  return (
    <div className={cn("flex gap-3 mb-4 animate-fade-in", isUser ? "justify-end" : "justify-start")}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-gradient-accent flex items-center justify-center flex-shrink-0">
          <Bot className="w-5 h-5 text-primary-foreground" />
        </div>
      )}
      
      <div className={cn(
        "max-w-[70%] rounded-2xl px-4 py-3 shadow-sm",
        isUser 
          ? "bg-gradient-accent text-primary-foreground" 
          : "bg-card border border-border"
      )}>
        <p className={cn(
          "text-sm leading-relaxed",
          isUser ? "text-primary-foreground" : "text-foreground"
        )}>
          {message}
        </p>
        {timestamp && (
          <p className={cn(
            "text-xs mt-1",
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
