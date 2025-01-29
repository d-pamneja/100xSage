import { Request,Response,NextFunction } from "express";
import { S3Client,GetObjectCommand, HeadObjectCommand, PutObjectCommand, DeleteObjectCommand } from "@aws-sdk/client-s3"
import { SQSClient, SendMessageCommand } from "@aws-sdk/client-sqs";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import dotenv from 'dotenv'; 
dotenv.config()

const s3Client = new S3Client({
    region : 'ap-south-1',
    credentials : {
        accessKeyId : process.env.AWS_ACCESSABLE_KEY!,
        secretAccessKey : process.env.AWS_SECRET_ACCESS_KEY!,
    }
})

const sqsClient = new SQSClient({
    region : 'ap-south-1',
    credentials : {
        accessKeyId : process.env.AWS_ACCESSABLE_KEY!,
        secretAccessKey : process.env.AWS_SECRET_ACCESS_KEY!,
    }
})

const BUCKET_NAME = process.env.KNOWLEDGE_BASE_BUCKET_NAME!
const SQS_QUEUE_URL = process.env.KNOWLEDGE_BASE_SQS_QUEUE_URL!


const checkObjectExistence = async (key: string): Promise<boolean> => {
    try {
        const checkCommand = new HeadObjectCommand({
            Bucket: BUCKET_NAME,
            Key: key
        });

        await s3Client.send(checkCommand);
        return true;
    } catch (error: any) {
        if (error.name === "NotFound") {
            return false;
        }
        throw new Error(`Error checking object existence: ${error.message}`);
    }
};

export const getObject = async (req : Request, res: Response) : Promise<any> => {
    try {
        const key = req.query.key as string
        if(await checkObjectExistence(key)){
            const command = new GetObjectCommand({
                Bucket : BUCKET_NAME,
                Key : key
            })
            
            const url = await getSignedUrl(s3Client,command,{expiresIn : 3600})
    
            if(!url){
                return res.status(400).json({message : "Error in generating the signed URL for requested data"})
            }
    
            return res.status(200).json({message : "Successfully generated the signed URL for requested data",url})
        }
        else{
            return res.status(404).json({message : "Object does not exist in given location"})
        }
    } catch (error : any) {
        res.status(500).json({message : `Error in getting object : ${error.message}`})
    }
}

const ensureFolderExists = async (folderPath: string): Promise<void> => {
    const normalizedPath = folderPath.endsWith('/') ? folderPath : `${folderPath}/`;
    
    const createFolderCommand = new PutObjectCommand({
        Bucket: BUCKET_NAME,
        Key: normalizedPath,
    });

    try {
        await s3Client.send(createFolderCommand);
    } catch (error: any) {
        throw new Error(`Error creating folder: ${error.message}`);
    }
};

export const setObject = async (req: Request, res: Response): Promise<any> => {
    try {
        const { userID, courseID, topicID, type, filename,contentType } = req.body;
        
        const fullPath = `${userID}/${courseID}/${type}/${filename}`;

        const userFolder = `${userID}/`;
        const courseFolder = `${userID}/${courseID}`
        const topicFolder = `${userID}/${courseID}/${topicID}`
        const typeFolder = `${userID}/${courseID}/${type}/`;

        if (!await checkObjectExistence(userFolder)) {
            await ensureFolderExists(userFolder);
        }

        if (!await checkObjectExistence(courseFolder)) {
            await ensureFolderExists(courseFolder);
        }

        if (!await checkObjectExistence(topicFolder)) {
            await ensureFolderExists(topicFolder);
        }

        if (!await checkObjectExistence(typeFolder)) {
            await ensureFolderExists(typeFolder);
        }

        const createObjectCommand = new PutObjectCommand({
            Bucket: BUCKET_NAME,
            Key: fullPath,
            ContentType: contentType
        });

        await s3Client.send(createObjectCommand)
        const url = await getSignedUrl(s3Client,createObjectCommand,{expiresIn : 3600})

        if (!url) {
            return res.status(400).json({ 
                message: "Error in generating signed URL for upload" 
            });
        }


        return res.status(200).json({ 
            message: "File uploaded to AWS and signedURL generated",
            url,
            fullPath,
        });

    } catch (error: any) {
        res.status(500).json({ 
            message: `Internal server error in setting object: ${error.message}` 
        });
    }
};

export const send_POST_SQS = async (req: Request, res: Response): Promise<any> => {
    try {
        const { userID, type, filename,fullPath,url } = req.body; 

        const input = { 
            QueueUrl: SQS_QUEUE_URL, 
            MessageBody: 'POST', 
            DelaySeconds: 5, 
            MessageAttributes: { 
              link: { 
                DataType: "String", 
                StringValue: url, 
              },
              key: { 
                DataType: "String", 
                StringValue: fullPath, 
              },
              properties: { 
                DataType: "String", 
                StringValue: JSON.stringify({ 
                    user_id : userID ,
                    name : filename,
                    doc_type: type, 
                }) 
              },
            }
        };
          

        const command = new SendMessageCommand(input);
        const message = await sqsClient.send(command);

        if(!message){
            return res.status(400).json({ 
                message: "Error in sending information to SQS" 
            });
        }

        return res.status(200).json({ 
            message: "Document upload information sent to SQS", 
            SQSInput : input
        });

    } catch (error: any) {
        console.error(error);
        res.status(500).json({ 
            message: `Error in sending SQS message: ${error.message}` 
        });
    }
};

export const removeObject = async (req : Request, res: Response) : Promise<any> => {
    try {
        const key = req.query.key as string
        if(await checkObjectExistence(key)){
            const command = new DeleteObjectCommand({
                Bucket : BUCKET_NAME,
                Key : key
            })

            await s3Client.send(command);

            return res.status(200).json({message : "Successfully deleted the requested data",key})
        }
        else{
            return res.status(404).json({message : "Object does not exist in given location"})
        }
    } catch (error : any) {
        res.status(500).json({message : `Error in deleting object : ${error.message}`})
    }
}

export const send_DELETE_SQS = async (req: Request, res: Response): Promise<any> => {
    try {
        const { key } = req.body; 

        const input = { 
            QueueUrl: SQS_QUEUE_URL, 
            MessageBody: 'DELETE', 
            DelaySeconds: 5, 
            MessageAttributes: { 
              key: { 
                DataType: "String", 
                StringValue: key, 
              },
            }
        };
          

        const command = new SendMessageCommand(input);
        const message = await sqsClient.send(command);

        if(!message){
            return res.status(400).json({ 
                message: "Error in sending information to SQS" 
            });
        }

        return res.status(200).json({ 
            message: "Document delete information sent to SQS", 
            SQSInput : input
        });

    } catch (error: any) {
        console.error(error);
        res.status(500).json({ 
            message: `Error in sending SQS message: ${error.message}` 
        });
    }
};


export default {getObject,setObject,removeObject,send_POST_SQS,send_DELETE_SQS}