import MyTypes from "@/components/ui/docTypes";

export const Types = async ({ courseID,topicID }: { courseID: number,topicID:number }) => {
    const types = [{
        id: 1,
        title: "PDF",
        description: "Upload your PDFs here"
    }, {
        id: 2,
        title: "Text",
        description: "Upload your Text files here"
    }]

    return <MyTypes courseID={courseID} topicID={topicID} types={types}/>

};