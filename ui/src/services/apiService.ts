import { JobAd } from '../types/JobAd';

const API_URL = "/qualified";

export const fetchJobs = async (page: number, pageSize: number) => {
    try {
        const response = await fetch(`${API_URL}/${page}/${pageSize}`, {
            method: 'GET'
        });
        if (!response.ok) {
            console.error(await response.text());
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching job applications', error);
        throw error;
    }
};

export const fetchCount = async () => {
    try {
        const response = await fetch('/qualified/count');
        if (!response.ok) {
            console.error(await response.text());
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching job count', error);
        throw error;
    }
};

const UPDATE_URL = "/job"
export const updateJob = async (job: JobAd) => {
    try {
        const url = `${UPDATE_URL}/${job.id}`;
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(job)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error updating job application', error);
        throw error;
    }
};