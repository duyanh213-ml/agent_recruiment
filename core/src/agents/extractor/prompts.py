from src.settings.settings import GeneralCoreSettings


class ExtractorPrompt:

    @classmethod
    def paragraph_correction_prompt(cls, paragraph: str):
        return f"""
            The following text is written in either English or Vietnamese and may contain 
            spelling or grammatical errors. Please restore and correct any mistakes, returning only the fully corrected text. 
            Do not provide any additional information:
            ```
            {paragraph}
            ```
        """

    @classmethod
    def extraction_prompt(cls, paragraph: str):
        return f"""
            Given the following text, which is a CV/resume of a candidate (in either Vietnamese or English), 
            extract the information into a dictionary with the following five fields: "{GeneralCoreSettings.EXTRACT_OBJECTIVE}", 
            "{GeneralCoreSettings.EXTRACT_EXPERIENCES}", "{GeneralCoreSettings.EXTRACT_SKILLS}", 
            "{GeneralCoreSettings.EXTRACT_EDUCATION}", and "{GeneralCoreSettings.EXTRACT_CERTIFICATE}".
            Each extracted value should be formatted as a well-structured string for readability.
            If a field has no relevant information, return 0.
            Return only the extracted result without any additional explanation or commentary
            and return the data as a raw JSON object without formatting it as a code block or using triple backticks.
            
            Here is the text:
            ```
            {paragraph}
            ```
        """
