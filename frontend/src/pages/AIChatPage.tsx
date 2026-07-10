import { useState, useEffect, useRef } from 'react';
import { aiService } from '../services/aiService';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { Bot, User } from 'lucide-react';

export const AIChatPage = () => {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    aiService.getHistory().then(res => setMessages(res.data.reverse()));
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    const userMsg = { prompt: input };
    setMessages(prev => [...prev, { prompt: input, response: '...' }]);
    setInput('');
    try {
      const res = await aiService.chat(userMsg);
      setMessages(prev => [...prev.slice(0, -1), res.data]);
    } catch {
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 space-y-6">
      <h2 className="text-3xl font-bold text-gray-900">AI Assistant</h2>
      <Card className="h-[60vh] flex flex-col">
        <div className="flex-1 overflow-y-auto space-y-4 mb-4">
          {messages.map((m, i) => (
            <div key={i} className="space-y-2">
              <div className="flex items-start gap-2 justify-end">
                <div className="bg-indigo-100 p-3 rounded-lg text-sm">{m.prompt}</div>
                <User className="w-6 h-6 text-indigo-600" />
              </div>
              <div className="flex items-start gap-2">
                <Bot className="w-6 h-6 text-gray-600" />
                <div className="bg-gray-100 p-3 rounded-lg text-sm">{m.response}</div>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <div className="flex gap-2">
          <Input label="" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask about team activity..." />
          <Button onClick={handleSend} disabled={loading}>
            {loading ? <LoadingSpinner /> : 'Send'}
          </Button>
        </div>
      </Card>
    </div>
  );
};
