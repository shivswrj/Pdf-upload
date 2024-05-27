import React, { useState } from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

const QuestionForm = ({ pdfId }) => {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');

    const handleQuestionChange = (event) => {
        setQuestion(event.target.value);
    };

    const handleAskQuestion = async () => {
        if (!question) return;

        try {
            const response = await axios.post('http://localhost:8000/ask', {
                pdf_id: pdfId,
                question: question,
            });
            setAnswer(response.data.answer);
        } catch (error) {
            console.error('Error asking question:', error);
        }
    };

    return (
        <Box sx={{ mt: 4, width: '100%' }}>
            <TextField
                fullWidth
                label="Ask a question"
                value={question}
                onChange={handleQuestionChange}
                variant="outlined"
                margin="normal"
            />
            <Button
                variant="contained"
                color="primary"
                onClick={handleAskQuestion}
                fullWidth
                sx={{ mt: 2 }}
            >
                Ask Question
            </Button>
            {answer && (
                <Typography variant="body1" sx={{ mt: 4 }}>
                    <strong>Answer:</strong> {answer}
                </Typography>
            )}
        </Box>
    );
};

export default QuestionForm;
