import React from 'react';
import JobList from './components/JobList';

const App: React.FC = () => {
    return (
        <div className="App">
            <h1 style={{ textAlign: 'center' }}>Qualifed Jobs</h1>
            <JobList />
        </div>
    );
}

export default App;