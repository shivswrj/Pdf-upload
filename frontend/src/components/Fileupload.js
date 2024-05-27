import React, { useState } from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';

const FileUpload = ({ onUpload }) => {
    const [file, setFile] = useState(null);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:8000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            onUpload(response.data);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    return (
        <Box sx={{ mt: 4, width: '100%' }}>
            <TextField
                fullWidth
                type="file"
                onChange={handleFileChange}
                variant="outlined"
                margin="normal"
            />
            <Button
                variant="contained"
                color="primary"
                onClick={handleUpload}
                fullWidth
                sx={{ mt: 2 }}
            >
                Upload PDF
            </Button>
        </Box>
    );
};

export default FileUpload;
