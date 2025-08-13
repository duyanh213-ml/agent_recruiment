from src.agents.evaluator.schemas import JobInfo, CandidateInfo


class EvaluatorPrompt:
    
    @staticmethod
    def candidate_preparation(candidate_info: CandidateInfo):
        candidate_info_txt = ""
        
        if candidate_info.extract_objective:
            candidate_info_txt += f"-objective: {candidate_info.extract_objective}\n"
        if candidate_info.extract_experiences:
            candidate_info_txt += f"-experiences: {candidate_info.extract_experiences}\n"
        if candidate_info.extract_skills:
            candidate_info_txt += f"-skills: {candidate_info.extract_skills}\n"
        if candidate_info.extract_education:
            candidate_info_txt += f"-education: {candidate_info.extract_education}\n"
        if candidate_info.extract_certificate:
            candidate_info_txt += f"-certificate: {candidate_info.extract_certificate}\n"
            
        return candidate_info_txt
    
    @classmethod
    def evaluate_candidate_prompt(cls, job_info: JobInfo, candidate_info: CandidateInfo):
        return f"""
            You are an exceptionally strict and highly critical expert in the field of recruitment. 
            Given the following information about the "Job Position" and the "Candidate," 
            evaluate the candidate’s suitability for the role on a scale from 0 to 100. 
            Additionally, provide a detailed explanation for your decision.Keep in mind that 
            I expect an extremely rigorous and demanding assessment. Do not be lenient in your evaluation.
            
            Job position:
            - title: {job_info.title}
            - job_type: {job_info.job_type}
            - qualifications: {job_info.qualifications}
            - responsibilities: {job_info.responsibilities}
            - benefits: {job_info.benefits}
            - work_schedule: {job_info.work_schedule}
            - location: {job_info.location}
            
            Candidate information:
            {cls.candidate_preparation(candidate_info)}
            
            Return only the extracted result with 2 keys: "score" and "summary_reason" without any additional explanation or commentary
            and return the data as a raw JSON object without formatting it as a code block or using triple backticks.
        """
    
    