import React, { useState } from 'react';
import { JobAd } from '../types/JobAd';
import { updateJob } from '../services/apiService';
import '../css/JobCard.css';
interface JobCardProps {
    job: JobAd;
}

const JobCard: React.FC<JobCardProps> = ({ job: Ad }) => {
    const [resumeVersion, setResumeVersion] = useState('');
    const [isQualified, setIsQualified] = useState(Ad.is_qualified);
    const [isNotQualifiedReason, setIsNotQualifiedReason] = useState('');
    const [dateApplied, setDateApplied] = useState<Date | null>(null);

    const handleUpdateJob = () => {
        setDateApplied(new Date());
        const updatedJob = {
            ...Ad,
            resume_version: resumeVersion,
            is_qualified: isQualified,
            has_applied: isQualified,
            date_applied: dateApplied!!,
            ...(isNotQualifiedReason && { is_not_qualified_reason: isNotQualifiedReason }),
        };
        updateJob(updatedJob);
    };

    return (
        <div className="ad-container">
            <h2 className="ad-title">{Ad.title}</h2>
            <p className="ad-date">Added on: {new Date(Ad.date_added).toLocaleDateString()}</p>       
                 <a className="ad-link" href={`https://www.indeed.com/viewjob?jk=${Ad.id}`} target="_blank" rel="noreferrer">Link to job</a>
            <div className="input-group">
                <input
                    className="input-text"
                    type="text"
                    value={resumeVersion}
                    onChange={(e) => setResumeVersion(e.target.value)}
                    placeholder="Resume Version"
                />
            </div>
            <label className="checkbox-label">
                <input
                    className="checkbox-input"
                    type="checkbox"
                    checked={isQualified}
                    onChange={(e) => setIsQualified(e.target.checked)}
                />
                Is Qualified
            </label>
            <div className="input-group">
                <input
                    className="input-text"
                    type="text"
                    value={isNotQualifiedReason}
                    onChange={(e) => setIsNotQualifiedReason(e.target.value)}
                    placeholder="Reason for not being qualified"
                />
            </div>
            <button className="update-button" onClick={handleUpdateJob}>Update Job</button>
            <p className="ad-description">{Ad.description}</p>
            </div>
    );
};

export default JobCard;