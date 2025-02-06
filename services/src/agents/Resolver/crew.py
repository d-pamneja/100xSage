from src.dependencies import Agent,Crew,Process,Task,CrewBase,agent, crew, task,OPENAI_API_KEY,Path,yaml
from src.agents.Resolver.tools.fetchRelevantDocs import fetchDocsTool
from src.agents.Resolver.schemas.researcher import ResearcherOutput
from src.agents.Resolver.schemas.writer import WriterOutput
from src.agents.Resolver.schemas.editor import EditorOutput

class ResolverCrew():
    
    def researcher(self) -> Agent: 
        return Agent(
            role = "researcher",
            goal = "To research and find the relevant Q&As from the past to the query {query}",
            backstory = """
                    You work as a researcher in an edtech startup 100xDevs, where your primary job is to research and give all the 
                    relevant documents/chunks of previously solved Q&As, where your task is to collate those references which will 
                    aid to solve the query : {query}. Your work will be directly passed to the writer, hence make sure you provide 
                    references only which you can quote with the relevant thread ID (you will find it as id). You have been given a tool 
                    to fetch the most relevant documents, which will give you a list of all the relevant documents, which 
                    consist of question, answer, id (this will be that thread's id on discord) and a score for you to evaluate on which is most relevant.
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
                id : The thread ID of that conversation on discord
                score : The relevance of the said document, with 0 being lowest and 1 being highest and -1 being irrelvant
                question : The primary question which was asked in the thread
                answer : The answer/solution which was provided to that thread
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
                    You are a recommendation analyst working at an edTech startup 100xDevs, where your job is to recommend the students 
                    on whether their query or something similar has been answered before, given the query : {query}. \n
                    Your work is dependent on the work of the researcher, who will bring you all the relevant information and your job is to collate it into a proper 
                    explanation of what the question was and how it was solved (make sure to keep the entire solution/answer intact) along with it's reference.
                    You will be writing your recommendation with acknowledging and referencing each factual statement as given by the researcher, 
                    hence it is important you MUST give the thread ID to your editor, should you find a relevant answer.\n
                    In case you find the research to be irrelevant, you can just let your editor know that there is no such query or solution solved 
                    previously to the said developer. There is no need to solve it yourself, only solve if your have the relevant research.
            """,
            allow_delegation = False,
            verbose = True
        )
        
    def write(self) -> Task:
        return Task(
             description="To write content providing the solution to the query : {query}, given the research done by researcher",
            expected_output="""A object consisting of all the content written by the writer, where it follows the structure : 
                id : The thread ID of that conversation on discord, only if the writer is able to find relevant content (This is an OPTIONAL key)
                content : The content piece written by the writer, if they are supported by the research team
            """,
            agent=self.writer(),
            output_pydantic=WriterOutput
        )
        
    def editor(self) -> Agent: 
        return Agent(
            role = "editor",
            goal = "To edit the writer's recommendation to answer the query : {query} and interact with new student queries",
            backstory = """
                    You are the senior editor at an edTech startup 100xDevs, where your job is to handle and give recommendation messages to the
                    new queries created by students on our discord channel. You work is dependent on the writer's content piece, as that would have information
                    on the most relevant answer and reference they could find to the query : {query}. In case the writer is unable to produce any results or 
                    denies any relevant findings to base their content on, you do not need to pass anything to the user as handled in your task.\n
            """,
            allow_delegation = False,
            verbose = True
        )
        
    def edit(self) -> Task:
        return Task(
            description="To edit and give the status of work and final output as a recommendation to the student, if any content given by writer",
            expected_output="""A object consisting of all the final output given by the editor, with the structure of it as follows : 
                status : The status code of the team's findings. If any content given by writer, then 200 else 404.
                relevance : A boolean value indicating whether the team was able to complete the task or not
                solution : The final edited solution from the editor, if none then give the string "NA"
                source : The exact thread ID on discord from which this solution is quoted, if none then give the string "NA"
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