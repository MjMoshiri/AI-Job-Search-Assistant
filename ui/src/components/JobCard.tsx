import React, { useState, useRef } from 'react';
import { JobAd } from '../types/JobAd';
import { Reason } from '../types/Reason'; // Ensure Reason is correctly imported as an array or adjust accordingly
import { updateJob } from '../services/apiService';
import '../css/JobCard.css';

interface JobCardProps {
    job: JobAd;
    onRemove: (jobId: string) => void;
}

const JobCard: React.FC<JobCardProps> = ({ job: Ad , onRemove }) => {
    const [resumeVersion, setResumeVersion] = useState('');
    const [isQualified, setIsQualified] = useState(Ad.is_qualified);
    const [selectedReasons, setSelectedReasons] = useState<string[]>(Ad.is_not_qualified_reason ? Ad.is_not_qualified_reason.split(', ') : []);
    const [dateApplied, setDateApplied] = useState<Date | null>(null);
    const [isCollapsed, setIsCollapsed] = useState(true);
    const accordionTitleRef = useRef<HTMLHeadingElement>(null);

    const handleUpdateJob = () => {
        setDateApplied(new Date());
        const updatedJob = {
            ...Ad,
            resume_version: resumeVersion,
            is_qualified: isQualified,
            has_applied: isQualified && selectedReasons.length === 0,
            date_applied: dateApplied!,
            is_not_qualified_reason: selectedReasons.join(', ')
        };
        updateJob(updatedJob);
        toggleCollapse();
        onRemove(Ad.id);
    };

    const handleReasonChange = (reason: string, checked: boolean) => {
        if (checked) {
            setSelectedReasons(prev => [...prev, reason]);
        } else {
            setSelectedReasons(prev => prev.filter(r => r !== reason));
        }
    };

    const toggleCollapse = () => {
        accordionTitleRef.current?.classList.toggle('collapsed');
        setIsCollapsed(!isCollapsed);
    };

    return (
        <div className="ad-container">
            <h2 ref={accordionTitleRef} className="ad-title accordion-title" onClick={toggleCollapse}>{Ad.title}, {Ad.company}</h2>
            {!isCollapsed && (
                <>
                    <p className="ad-date">Added on: {new Date(Ad.date_added).toLocaleDateString()}</p>
                    <a className="ad-link" href={Ad.link} target="_blank" rel="noreferrer">Link to job</a>
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
                        Qualified
                    </label><br />
                    <div className="checkbox-container">
                        Rejected for: 
                        {Reason.map((reason) => (
                            <label key={reason} className="checkbox-label">
                                <input
                                    type="checkbox"
                                    checked={selectedReasons.includes(reason)}
                                    onChange={(e) => handleReasonChange(reason, e.target.checked)}
                                />
                                {reason}
                            </label>
                        ))}
                    </div>
                    <br />
                    <button className="update-button" onClick={handleUpdateJob}>Process</button>
                    <p className="ad-description">{Ad.description}</p>
                </>
            )}
        </div>
    );
};

export default JobCard;
