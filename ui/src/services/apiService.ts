import axios from 'axios';
import { JobAd } from '../types/JobAd';

const API_URL = "/qualified";

export const fetchJobs = async (page: number, pageSize: number) => {
    try {
        const response = await axios.get(`${API_URL}/${page}/${pageSize}` );
        if (response.status !== 200) {
            console.error(response.data);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.data;
    } catch (error) {
        console.error('Error fetching job applications', error);
        throw error;
    }
};

const UPDATE_URL = "/job";
export const updateJob = async (job: JobAd) => {
    try {
        const url = `${UPDATE_URL}/${job.id}`;
        const response = await axios.put(url, job);
        if (response.status !== 200) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.data;
    } catch (error) {
        console.error('Error updating job application', error);
        throw error;
    }
};