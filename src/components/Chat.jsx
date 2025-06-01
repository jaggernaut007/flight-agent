import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { format } from 'date-fns';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import MicIcon from '@mui/icons-material/Mic';
import ReactMarkdown from 'react-markdown';

// Base URL for the API
const API_BASE_URL = 'http://localhost:8000/api';

const Chat = () => {
  const [messages, setMessages] = useState([
    {
      text: "Hi there! I'm your AI travel assistant. I can help you find flights, hotels, and vacation packages. Ask me anything about travel!",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const [conversationContext, setConversationContext] = useState({});

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input on load
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userMessage = input.trim();
    if (!userMessage || isLoading) return;

    // Add user message to chat
    const userMessageObj = {
      text: userMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessageObj]);
    setInput('');
    setIsLoading(true);

    try {
      // Call our backend API
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message: userMessage,
        context: conversationContext
      });

      // Update conversation context with the one returned from the server
      if (response.data.context) {
        setConversationContext(response.data.context);
      }

      // Add bot response to chat
      const botMessage = {
        text: response.data.response,
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error calling chat API:', error);
      
      const errorMessage = {
        text: error.response?.data?.response || 'Sorry, there was an error processing your request. Please try again.',
        sender: 'bot',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }

  // Format timestamp
  const formatTime = (date) => {
    return format(new Date(date), 'h:mm a');
  };

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center" width="100%" minHeight="500px" height="100%">
      <Paper elevation={3} sx={{ width: '100%', maxWidth: 420, minHeight: 420, p: 0, display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', bgcolor: 'rgb(19, 32, 45)' }}>
        {/* Messages */}
        <Box flex={1} sx={{ overflowY: 'auto', p: 2, minHeight: 340, maxHeight: 400, display: 'flex', flexDirection: 'column', gap: 2 }}>
          {messages.map((msg, index) => (
            <Box key={index} display="flex" alignItems="flex-end" mb={1} justifyContent={msg.sender === 'user' ? 'flex-end' : 'flex-start'}>
              {msg.sender === 'bot' && (
                <Avatar sx={{ bgcolor: '#e3eafe', color: '#3b3f5c', width: 36, height: 36, mr: 1 }}>🤖</Avatar>
              )}
              <Box
                sx={{
                  maxWidth: 280,
                  px: 2,
                  py: 1.5,
                  borderRadius: 2.5,
                  bgcolor: '#fff',
                  color: '#fff',
                  boxShadow: 1,
                  borderBottomRightRadius: msg.sender === 'user' ? 6 : 20,
                  borderBottomLeftRadius: msg.sender === 'bot' ? 6 : 20,
                  ml: msg.sender === 'user' ? 1 : 0,
                  mr: msg.sender === 'bot' ? 1 : 0,
                }}
              >
                <Box fontSize={15} whiteSpace="pre-line" sx={{ color: '#fff' }}>
  <ReactMarkdown>{msg.text}</ReactMarkdown>
</Box>
                <Box fontSize={12} mt={0.5} sx={{ color: '#e0e0e0' }} textAlign="right">
                  {formatTime(msg.timestamp)}
                </Box>
              </Box>
              {msg.sender === 'user' && (
                <Avatar sx={{ bgcolor: '#e3eafe', color: '#2563eb', width: 36, height: 36, ml: 1 }}>🧑‍✈️</Avatar>
              )}
            </Box>
          ))}
          {isLoading && (
            <Box display="flex" alignItems="flex-end" mb={1} justifyContent="flex-start">
              <Avatar sx={{ bgcolor: '#e3eafe', color: '#3b3f5c', width: 36, height: 36, mr: 1 }}>🤖</Avatar>
              <Box sx={{ bgcolor: '#fff', color: '#222', px: 2, py: 1.5, borderRadius: 2.5, boxShadow: 1, borderBottomLeftRadius: 6, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Box sx={{ width: 8, height: 8, bgcolor: 'primary.light', borderRadius: '50%', animation: 'mui-bounce 1s infinite alternate' }} />
                <Box sx={{ width: 8, height: 8, bgcolor: 'primary.main', borderRadius: '50%', animation: 'mui-bounce 1s 0.2s infinite alternate' }} />
                <Box sx={{ width: 8, height: 8, bgcolor: 'primary.dark', borderRadius: '50%', animation: 'mui-bounce 1s 0.4s infinite alternate' }} />
                <Box ml={1} fontSize={12} color="primary.main">AI is typing...</Box>
              </Box>
            </Box>
          )}
          <div ref={messagesEndRef} />
        </Box>
        {/* Input area */}
        <Box component="form" onSubmit={handleSubmit} sx={{ p: 2, borderTop: '1px solid #232e6b', bgcolor: 'rgb(19, 32, 45)', display: 'flex', alignItems: 'flex-end', gap: 1 }}>
          <IconButton color="primary" component="span" size="large">
            <AttachFileIcon />
          </IconButton>
          <TextField
            fullWidth
            variant="standard"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            InputProps={{
              disableUnderline: true,
              sx: { fontSize: 16, color: '#f5f5f5', background: 'transparent' }
            }}
          />
          <IconButton color="primary" component="span" size="large">
            <MicIcon />
          </IconButton>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={!input.trim() || isLoading}
            sx={{ minWidth: 44, minHeight: 44, borderRadius: 2, boxShadow: 'none' }}
          >
            <SendIcon />
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}

export default Chat;
