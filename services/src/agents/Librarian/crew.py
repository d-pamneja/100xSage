from src.dependencies import Agent,Crew,Process,Task,CrewBase,agent, crew, task,OPENAI_API_KEY,Path,yaml
from src.agents.Librarian.tools.fetchRelevantDocs import fetchDocsTool
from src.agents.Librarian.schemas.researcher import ResearcherOutput
from src.agents.Librarian.schemas.writer import WriterOutput
from src.agents.Librarian.schemas.editor import EditorOutput

class LibrarianCrew():
    
    def researcher(self) -> Agent: 
        return Agent(
           role = "researcher",
            goal = "To research and find the relevant answer from the existing knowledge base to the query {query}",
            backstory = """
                    You work as a researcher in an edtech startup 100xDevs, where your primary job is to research and give all the 
                    relevant documents/chunks from the documents uploaded buy the admin, where your task is to collate those references which will 
                    aid to solve the query : {query}. Your work will be directly passed to the writer, hence make sure you provide 
                    references only which you can quote with the relevant document name (you will find it as 'name') and reference page (you will find it as 'reference'). 
                    You have been given a tool to fetch the most relevant documents, which will give you a list of all the relevant documents, which 
                    consist of text (the actual text), name (this will be the document name), reference (this will be that text's page location) and a score for you to evaluate on which is most relevant.
                    In case you get irrelevant documents, the tool has handled that too and you just need to pass it on to the writer.
            """,
            verbose = True,
            allow_delegation = False,
            tools = [fetchDocsTool]
        )
        
    def research(self) -> Task:
        return Task(
           description="To research and find the most relevant documents and references to the given query : {query}",
            expected_output="""A list consisting of all the relevant documents, where each document (JSON) follows the structure :
                score : The score implying the relvance of this document to the given query, with 0 being the lowest and 1 being the highest, and -1 being irrelevant
                text : The relevant text to the query in this document
                name : The name of the document from which the text is
                reference : The page number from which this text is refered
            """,
            agent=self.researcher(),
            parameters={"query": "str"},
            output_pydantic= ResearcherOutput
        )
        
    def writer(self) -> Agent: 
        return Agent(
            role = "writer",
            goal = "To structure and answer the query : {query} given the relevant documents from the researcher",
            backstory = """
                    You are a recommendation analyst working at an edTech startup 100xDevs, where your job is to answer the theoretical
                    doubts of the students from admin uploaded documents, given the query : {query}. \n
                    Your work is dependent on the work of the researcher, who will bring you all the relevant information and your job is to collate it into a proper 
                    explanation of what the question was and what is it's answer according to offical documents along with it's name and reference.
                    You will be writing your recommendation with acknowledging and referencing each factual statement as given by the researcher, 
                    hence it is important you MUST give the document name and reference to your editor, should you find a relevant documents.\n
                    In case you find the research to be irrelevant, you can just let your editor know that there is no such document or solution as per
                    official documentation.\n\n
                    
                    IMPORTANT GUIDELINES : 
                    \t1.IF YOU FIND THE RESEARCH TO BE IRRELEVANT, YOU CAN JUST LET YOUR EDITOR KNOW THAT THERE IS NO SUCH DOCUMENT OR SOLUTION AS PER OFFICIAL DOCUMENTATION.
                    \t2.IF YOU FIND THE RESEARCH TO BE NULL OR AN EMPTY LIST, YOU CAN JUST LET YOUR EDITOR KNOW THAT THERE IS NO SUCH DOCUMENT OR SOLUTION AS PER OFFICIAL DOCUMENTATION.
                    \t3.IF THE SCORE OF ANY INDIVIDUAL DOCUMENT IS BELOW 0.3, YOU CAN JUST LET YOUR EDITOR KNOW THAT THERE IS NO SUCH DOCUMENT OR SOLUTION AS PER OFFICIAL DOCUMENTATION.
                    
                    \n\nREMEMBER : There is no need to solve it yourself, only solve if your have the relevant research and it follows the above guidelines.
            """,
            allow_delegation = False,
            verbose = True,
        )
        
    def write(self) -> Task:
        return Task(
           description="To write content providing the solution to the query : {query}, given the research done by researcher",
            expected_output="""A object consisting of all the content written by the writer, where it follows the structure : 
                name : The name of the document from which the text is refered
                reference : The page number(s) from which this text is refered. Here, each page will be an integer object in a list
                content : The content written by the writer to answer the query, given the research
            """,
            agent=self.writer(),
            output_pydantic=WriterOutput
        )
        
    def editor(self) -> Agent: 
        return Agent(
            role = "editor",
            goal = "To edit the writer's recommendation to answer the query : {query} and interact with student doubts",
            backstory = """
                    You are the senior editor at an edTech startup 100xDevs, where your job is to handle and answer theoretical doubts
                    as and when asked by a student on our discord channel. You work is dependent on the writer's content piece, as that would have information
                    on the most relevant text, document name and reference they could find to the query : {query}. In case the writer is unable to produce any results or 
                    denies any relevant findings to base their content on, you do not need to pass anything to the user as handled in your task.
                    In case the writer is unable to provide anything, you can just tell the student that there is no such document or solution as per
                    official documentation and nudge the student to vist the official documentation on the 100xDevs website.
            """,
            allow_delegation = False,
            verbose = True,
        )
        
    def edit(self) -> Task:
        return Task(
            description="To edit and give the status of work and final output as a recommendation to the student, if any content given by writer",
            expected_output="""A object consisting of all the final output given by the editor, with the structure of it as follows : 
                status : The status code of the team's findings. If any content given by writer, then 200 else 404.
                relevance : A boolean value indicating whether the team was able to complete the task or not
                solution : The final edited solution from the editor, if none then the text "Uh-oh! We could not find any relevant documents for the given query. You can visit the official documentation on the 100xDevs website."
                name : The name of the document from which the text is refered, if the solution is relevant, else "NA"
                reference : The page number(s) from which this text is refered where each page will be an integer object in a list, if the solution is relevant, else a list with 0 as the only element
            """,
            agent=self.editor(),
            output_pydantic=EditorOutput
        )
        
    def crew(self) -> Crew:
        return Crew(
            agents=[self.researcher(), self.writer(),self.editor()],
            tasks=[self.research(), self.write(),self.edit()],
            process=Process.sequential,
            verbose=True
        )