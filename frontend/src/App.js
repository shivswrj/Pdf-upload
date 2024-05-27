import React, { useState } from 'react';
import QuestionForm from './components/QuestionForm';
import FileUpload from './components/Fileupload';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { createTheme, ThemeProvider } from '@mui/material/styles';

import './App.css';

const theme = createTheme();

function App() {
    const [pdfId, setPdfId] = useState(null);

    const handleUpload = (pdfData) => {
        setPdfId(pdfData.id);
    };

    return (
        <ThemeProvider theme={theme}>
            <Container component="main" maxWidth="sm">
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Typography component="h1" variant="h4">
                        PDF Q&A
                    </Typography>
                    <FileUpload onUpload={handleUpload} />
                    {pdfId && <QuestionForm pdfId={pdfId} />}
                </Box>
            </Container>
        </ThemeProvider>
    );
}

export default App;
