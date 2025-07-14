import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { format } from 'date-fns';
import { styled, keyframes } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import SendIcon from '@mui/icons-material/Send';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import MicIcon from '@mui/icons-material/Mic';
import FlightIcon from '@mui/icons-material/FlightTakeoff';
import ReactMarkdown from 'react-markdown';

// Animation keyframes
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const pulse = keyframes`
  0% { transform: scale(0.9); opacity: 0.7; }
  50% { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(0.9); opacity: 0.7; }
`;

// Styled components
const StyledMessage = styled(Box, {
  shouldForwardProp: (prop) => prop !== 'isUser'
})(({ theme, isUser }) => ({
  maxWidth: '80%',
  padding: theme.spacing(1.5, 2),
  borderRadius: '18px',
  background: 'linear-gradient(135deg, #3f51b5, #6573c3)',
  color: '#fff',
  boxShadow: theme.shadows[1],
  animation: `${fadeIn} 0.3s ease-out`,
  position: 'relative',
  '&:hover': {
    boxShadow: theme.shadows[3],
  },
  '&:after': {
    content: '""',
    position: 'absolute',
    bottom: 0,
    width: '20px',
    height: '20px',
    backgroundColor: 'transparent',
    [isUser ? 'left' : 'right']: '-10px',
    [isUser ? 'borderBottomRightRadius' : 'borderBottomLeftRadius']: '15px',
    boxShadow: isUser ? '5px 5px 0 5px #3f51b5' : '5px 5px 0 5px #ffffff',
    transform: 'rotate(45deg)',
    zIndex: -1,
  },
}));

const StyledAvatar = styled(Avatar)(({ theme }) => ({
  width: 40,
  height: 40,
  margin: theme.spacing(0, 1.5),
  background: 'linear-gradient(45deg, #3f51b5, #5c6bc0)',
  boxShadow: theme.shadows[2],
  '&:hover': {
    transform: 'scale(1.1)',
    transition: 'transform 0.2s ease-in-out',
  },
}));

const StyledInput = styled(TextField)({
  '& .MuiInputBase-root': {
    borderRadius: '24px',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    padding: '8px 16px',
    color: '#ffffff',
    '&:hover': {
      backgroundColor: 'rgba(255, 255, 255, 0.15)',
    },
    '&.Mui-focused': {
      backgroundColor: 'rgba(255, 255, 255, 0.2)',
    },
  },
  '& .MuiInputBase-input': {
    color: '#ffffff',
    '&::placeholder': {
      color: 'rgba(255, 255, 255, 0.6)',
      opacity: 1,
    },
  },
});

const LoadingDots = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  gap: '4px',
  '& > div': {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    backgroundColor: theme.palette.primary.main,
    animation: `${pulse} 1.4s infinite ease-in-out`,
    '&:nth-of-type(1)': { animationDelay: '0s' },
    '&:nth-of-type(2)': { animationDelay: '0.2s' },
    '&:nth-of-type(3)': { animationDelay: '0.4s' },
  },
}));

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
    <Box 
      sx={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        width: '100%',
        height: '100vh',
        background: 'linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%)',
        p: 2,
      }}
    >
      <Paper 
        elevation={6} 
        sx={{ 
          width: '100%', 
          maxWidth: '900px',
          height: '90vh',
          display: 'flex', 
          flexDirection: 'column',
          borderRadius: 3,
          overflow: 'hidden',
          boxShadow: '0 10px 30px rgba(0, 0, 0, 0.3)',
        }}
      >
        {/* Header */}
        <Box 
          sx={{ 
            background: 'linear-gradient(90deg, #3f51b5 0%, #5c6bc0 100%)',
            color: 'white',
            p: 2,
            display: 'flex',
            alignItems: 'center',
            boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
          }}
        >
          <FlightIcon sx={{ mr: 1.5, fontSize: 28 }} />
          <Typography variant="h6" component="h1" sx={{ fontWeight: 600 }}>
            Flight Assistant
          </Typography>
          <Box sx={{ flex: 1 }} />
          <Box sx={{ 
            bgcolor: 'rgba(255, 255, 255, 0.2)', 
            px: 1.5, 
            py: 0.5, 
            borderRadius: 10,
            fontSize: 12,
            fontWeight: 500,
          }}>
            Online
          </Box>
        </Box>

        {/* Messages */}
        <Box 
          sx={{ 
            flex: 1, 
            p: 3, 
            overflowY: 'auto',
            background: 'linear-gradient(180deg, #f5f7ff 0%, #e8eaf6 100%)',
            '&::-webkit-scrollbar': {
              width: '6px',
            },
            '&::-webkit-scrollbar-track': {
              background: 'rgba(0, 0, 0, 0.05)',
            },
            '&::-webkit-scrollbar-thumb': {
              background: 'rgba(0, 0, 0, 0.1)',
              borderRadius: '3px',
              '&:hover': {
                background: 'rgba(0, 0, 0, 0.2)',
              },
            },
          }}
        >
          <Box sx={{ maxWidth: '800px', margin: '0 auto', width: '100%' }}>
            {messages.map((msg, index) => (
              <Box 
                key={index} 
                sx={{ 
                  display: 'flex',
                  justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                  mb: 2,
                  animation: `${fadeIn} 0.3s ease-out`,
                }}
              >
                {msg.sender === 'bot' && (
                  <StyledAvatar>🤖</StyledAvatar>
                )}
                <StyledMessage isUser={msg.sender === 'user'}>
                  <Box sx={{ 
                    fontSize: '0.9375rem', 
                    lineHeight: 1.5, 
                    color: msg.sender === 'user' ? '#ffffff' : 'inherit',
                    '& p': { 
                      margin: '0.5em 0',
                      color: msg.sender === 'user' ? '#ffffff' : 'inherit'
                    },
                    '& a': {
                      color: msg.sender === 'user' ? '#e3f2fd' : '#1e88e5',
                      textDecoration: 'none',
                      '&:hover': {
                        textDecoration: 'underline'
                      }
                    }
                  }}>
                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                  </Box>
                  <Box 
                    sx={{ 
                      fontSize: '0.6875rem', 
                      mt: 1, 
                      textAlign: 'right',
                      color: '#fff',
                    }}
                  >
                    {formatTime(msg.timestamp)}
                  </Box>
                </StyledMessage>
                {msg.sender === 'user' && (
                  <StyledAvatar>👤</StyledAvatar>
                )}
              </Box>
            ))}
            
            {isLoading && (
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <StyledAvatar>🤖</StyledAvatar>
                <Box 
                  sx={{ 
                    bgcolor: 'white', 
                    px: 2.5, 
                    py: 1.5, 
                    borderRadius: 4, 
                    boxShadow: 1,
                    ml: 1,
                  }}
                >
                  <LoadingDots>
                    <div />
                    <div />
                    <div />
                  </LoadingDots>
                </Box>
              </Box>
            )}
            <div ref={messagesEndRef} />
          </Box>
        </Box>

        {/* Input area */}
        <Box 
          component="form" 
          onSubmit={handleSubmit}
          sx={{ 
            p: 2, 
            borderTop: '1px solid rgba(0, 0, 0, 0.05)',
            background: '#fff',
            display: 'flex', 
            alignItems: 'center',
            gap: 1,
            boxShadow: '0 -2px 10px rgba(0, 0, 0, 0.03)',
          }}
        >
          <IconButton 
            color="primary" 
            size="medium"
            sx={{
              '&:hover': {
                backgroundColor: 'rgba(63, 81, 181, 0.08)',
              },
            }}
          >
            <AttachFileIcon />
          </IconButton>
          
          <StyledInput
            fullWidth
            variant="outlined"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            InputProps={{
              disableUnderline: true,
              sx: { 
                '& .MuiOutlinedInput-notchedOutline': {
                  border: 'none',
                },
                '&:hover .MuiOutlinedInput-notchedOutline': {
                  border: 'none',
                },
                '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                  border: 'none',
                  boxShadow: '0 0 0 2px rgba(63, 81, 181, 0.2)',
                },
              },
            }}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
            multiline
            maxRows={4}
          />
          
          <IconButton 
            color="primary" 
            size="medium"
            sx={{
              '&:hover': {
                backgroundColor: 'rgba(63, 81, 181, 0.08)',
              },
            }}
          >
            <MicIcon />
          </IconButton>
          
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={!input.trim() || isLoading}
            sx={{
              minWidth: '44px',
              minHeight: '44px',
              borderRadius: '50%',
              p: 0,
              '&:hover': {
                transform: 'scale(1.05)',
                boxShadow: '0 4px 12px rgba(63, 81, 181, 0.3)',
              },
              '&:active': {
                transform: 'scale(0.98)',
              },
              transition: 'all 0.2s ease',
            }}
          >
            <SendIcon />
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}

export default Chat;
