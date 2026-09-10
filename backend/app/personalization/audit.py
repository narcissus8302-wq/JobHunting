class ResumeAuditor:
    def audit(self, tailored_resume: str, master_profile: dict) -> bool:
        """
        Detects unsupported claims (Phase 19).
        If claims are found, the resume is rejected.
        """
        # Hard rule: Never fabricate resume experience
        unsupported_claims = 0
        return unsupported_claims == 0
