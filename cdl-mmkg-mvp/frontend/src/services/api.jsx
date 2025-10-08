import axios from 'axios';

export async function searchAPI(query) {
    try {
        const response = await axios.get('http://localhost:8000/search', {
            params: { q: query }
        });
        return response.data;
    } catch (error) {
        console.error('Search API error:', error);
        throw new Error('Failed to fetch search results');
    }
}
