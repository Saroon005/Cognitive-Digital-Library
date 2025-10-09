import { useState } from 'react';
import './SearchBar.css';

function SearchBar({ onSearchSubmit }) {
    const [inputValue, setInputValue] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (inputValue.trim()) {
            onSearchSubmit(inputValue.trim());
        }
    };

    const handleClear = () => {
        setInputValue('');
    };

    return (
        <form onSubmit={handleSubmit} className="search-form">
            <div className="search-input-wrapper">
                <span className="search-icon">🔍</span>
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Search documents by content, title, tags..."
                    className="search-input"
                />
                {inputValue && (
                    <button
                        type="button"
                        onClick={handleClear}
                        className="clear-btn"
                        aria-label="Clear search"
                    >
                        ✕
                    </button>
                )}
            </div>
            <button type="submit" className="search-btn" disabled={!inputValue.trim()}>
                Search
            </button>
        </form>
    );
}

export default SearchBar;
