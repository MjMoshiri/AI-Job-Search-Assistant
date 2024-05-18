import React, { useEffect, useState } from 'react';
import { fetchJobs , fetchCount} from '../services/apiService';
import { JobAd } from '../types/JobAd';
import JobCard from './JobCard';

const JobList: React.FC = () => {
    const [jobs, setJobs] = useState<JobAd[]>([]);
    const [loading, setLoading] = useState(false);
    const [page, setPage] = useState(1);
    const [count, setCount] = useState(0);
    useEffect(() => {
        const loadJobs = async () => {
            setLoading(true);
            try {
                const data = await fetchJobs(page, 20);
                setJobs(data);
            } catch (error) {
                console.error('Failed to load jobs', error);
            } finally {
                setLoading(false);
            }
        };
        loadJobs();
    }, [page]);
    useEffect(() => {
        const loadCount = async () => {
            try {
                const data = await fetchCount();
                setCount(Math.ceil(data / 20));
            } catch (error) {
                console.error('Failed to load job count', error);
            }
        };
        loadCount();
    }, []);
    if (loading) return <p>Loading...</p>;

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginBottom: '20px' }}>
                <button onClick={() => setPage(old => Math.max(old - 1, 1))}>Previous</button>
                <span style={{ margin: '0 10px' }}>Page: {page} / {count}</span>
                <button onClick={() => setPage(old => old + 1)}>Next</button>
            </div>
            {jobs.map(job => <JobCard key={job.id} job={job} />)}
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginBottom: '20px' }}>
                <button onClick={() => setPage(old => Math.max(old - 1, 1))}>Previous</button>
                <span style={{ margin: '0 10px' }}>Page: {page} / {count}</span>
                <button onClick={() => setPage(old => old + 1)}>Next</button>
            </div>
        </div>
    );
}

export default JobList;