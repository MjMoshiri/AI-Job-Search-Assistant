export interface JobAd {
    id: string;
    date_added: Date;
    description: string;
    link: string;
    is_qualified: boolean;
    is_not_qualified_reason: string;
    has_applied: boolean;
    resume_version: string;
    title: string;
    company: string;
    date_applied: Date;
}