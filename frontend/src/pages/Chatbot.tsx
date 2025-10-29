import { useState } from "react";
import Navbar from "@/components/Navbar";
import ChatMessage from "@/components/ChatMessage";
import ModelTree from "@/components/ModelTree";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Send, Sparkles } from "lucide-react";
import { toast } from "sonner";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: string;
}

const exampleQueries = [
  "Which models were trained on LAION-5B?",
  "Show me the lineage of LLaVA v1.6",
  "Are there any risks with using Vicuna-13B and PLIP?",
  "What datasets does GPT-OSS-120B use?",
];

const Chatbot = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "Hello! I'm DataDetox AI. Ask me about model lineages, training datasets, or potential risks in AI models.",
      isUser: false,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [inputValue, setInputValue] = useState("");

  const handleSend = () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      isUser: true,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Based on my analysis of the model tree, I found several interesting connections. The model you're asking about has dependencies on multiple upstream models, some of which have been trained on datasets with known risks. Let me show you the lineage tree visualization below.",
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, aiMessage]);
      toast.success("Model lineage analysis complete");
    }, 1000);
  };

  const handleExampleClick = (query: string) => {
    setInputValue(query);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <div className="container mx-auto px-6 pt-24 pb-12">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-3">
              AI Model Lineage
              <span className="bg-gradient-accent bg-clip-text text-transparent"> Explorer</span>
            </h1>
            <p className="text-muted-foreground">
              Ask questions about model dependencies, training data, and potential risks
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-6">
            {/* Chat Section */}
            <div className="lg:col-span-2">
              <Card className="bg-card border-border shadow-lg h-[700px] flex flex-col">
                <CardHeader className="border-b border-border">
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-secondary" />
                    Chat with DataDetox AI
                  </CardTitle>
                </CardHeader>
                
                <CardContent className="flex-1 overflow-y-auto p-6 space-y-4">
                  {messages.map((message) => (
                    <ChatMessage
                      key={message.id}
                      message={message.text}
                      isUser={message.isUser}
                      timestamp={message.timestamp}
                    />
                  ))}
                </CardContent>

                <div className="p-4 border-t border-border">
                  <div className="flex gap-2">
                    <Input
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      onKeyPress={(e) => e.key === "Enter" && handleSend()}
                      placeholder="Ask about model lineage, datasets, or risks..."
                      className="flex-1"
                    />
                    <Button 
                      onClick={handleSend}
                      className="bg-gradient-accent hover:opacity-90 transition-opacity"
                    >
                      <Send className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </Card>
            </div>

            {/* Sidebar Section */}
            <div className="space-y-6">
              {/* Example Queries */}
              <Card className="bg-card border-border shadow-md">
                <CardHeader>
                  <CardTitle className="text-lg">Example Queries</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  {exampleQueries.map((query, index) => (
                    <button
                      key={index}
                      onClick={() => handleExampleClick(query)}
                      className="w-full text-left text-sm p-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors border border-border"
                    >
                      {query}
                    </button>
                  ))}
                </CardContent>
              </Card>

              {/* Model Tree Visualization */}
              <ModelTree />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
