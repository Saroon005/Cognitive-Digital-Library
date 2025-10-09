import './ResultList.css';

function ResultList({ results }) {
    if (results.length === 0) {
        return (
            <div className="empty-results">
                <div className="empty-icon">🔍</div>
                <p>Enter a query to search documents</p>
            </div>
        );
    }

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    };

    const truncateContent = (text, maxLength = 300) => {
        if (!text) return '';
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    };

    return (
        <div className="results-container">
            <div className="results-header">
                <h3>Search Results ({results.length})</h3>
            </div>
            
            <div className="results-list">
                {results.map((result, index) => (
                    <div key={result._id || index} className="result-card">
                        <div className="result-header">
                            <div className="result-rank">#{index + 1}</div>
                            <div className="result-score">
                                <span className="score-label">Relevance:</span>
                                <span className="score-value">{(result.score * 100).toFixed(1)}%</span>
                            </div>
                        </div>

                        <h4 className="result-title">{result.title}</h4>

                        {result.authors && result.authors.length > 0 && (
                            <div className="result-meta">
                                <span className="meta-icon">👤</span>
                                <span className="meta-text">{result.authors.join(', ')}</span>
                            </div>
                        )}

                        {result.tags && result.tags.length > 0 && (
                            <div className="result-tags">
                                {result.tags.map((tag, idx) => (
                                    <span key={idx} className="tag">{tag}</span>
                                ))}
                            </div>
                        )}

                        <p className="result-content">{truncateContent(result.content)}</p>

                        <div className="result-footer">
                            {result.upload_date && (
                                <span className="result-date">📅 {formatDate(result.upload_date)}</span>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ResultList;
