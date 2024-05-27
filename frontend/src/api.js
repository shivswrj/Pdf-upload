import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const uploadPDF = (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return axios.post(`${API_URL}/upload`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
};

export const askQuestion = (pdfId, question) => {
    return axios.post(`${API_URL}/ask`, { pdf_id: pdfId, question });
};
