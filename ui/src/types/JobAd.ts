export interface JobAd {
    id: string;
    date_added: Date;
    description: string;
    website: string;
    is_qualified: boolean;
    is_not_qualified_reason: string;
    is_a_match: number;
    has_applied: boolean;
    resume_version: string;
    title: string;
    company: string;
    date_applied: Date;
    is_duplicate: boolean;
}