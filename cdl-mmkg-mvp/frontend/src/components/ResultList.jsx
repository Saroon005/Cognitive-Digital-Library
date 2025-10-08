function ResultList({ results }) {
    if (results.length === 0) {
        return <p>Enter a query to see results</p>;
    }

    return (
        <div>
            {results.map((result, index) => (
                <div key={index} style={{ marginBottom: '1rem', padding: '1rem', border: '1px solid #ccc', borderRadius: '4px' }}>
                    <p><strong>Text:</strong> {result.text}</p>
                    <p><strong>Score:</strong> {result.score.toFixed(4)}</p>
                </div>
            ))}
        </div>
    );
}

export default ResultList;
