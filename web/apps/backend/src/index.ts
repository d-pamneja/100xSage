import express from 'express'
import { configDotenv } from 'dotenv'
import appRouter from './api/routes'

configDotenv()
const port = process.env.PORT

export const configApp = () => {
    try {
        const app = express()
        app.use(express.json())
        app.use("/backend/v1/",appRouter)
        
        return app
    } catch (error) {
        console.error(`Error in mounting the application : ${error}`)
    }
}


const app = configApp()

app!.listen(port,()=>{
    console.log(`App live at port : ${port}`)
})