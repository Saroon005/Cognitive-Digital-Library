import { useState } from 'react';

function SearchBar({ onSearchSubmit }) {
    const [inputValue, setInputValue] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSearchSubmit(inputValue);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Enter your search query..."
            />
            <button type="submit">Search</button>
        </form>
    );
}

export default SearchBar;
