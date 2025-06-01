import React from 'react'
import Chat from './components/Chat'
import './App.css'

import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

function App() {
  return (
    <Container maxWidth="md" sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <Paper elevation={8} sx={{ width: '100%', maxWidth: 900, minWidth: 600, borderRadius: 4, p: { xs: 3, sm: 4, md: 5 }, minHeight: 600, display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center', bgcolor: 'rgb(19, 32, 45)' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4, mb: 3, mt: 2, width: '100%' }}>
          <img src="/image.png" alt="Flight Icon" style={{ width: 160, height: 160 }} />
          <Box textAlign="center">
            <Typography variant="h4" fontWeight={700} sx={{ color: '#f5f5f5' }} gutterBottom>
              Flight Assistance App
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Your personal travel companion
            </Typography>
          </Box>
        </Box>
        <Chat />
      </Paper>
    </Container>
  );
}

export default App
